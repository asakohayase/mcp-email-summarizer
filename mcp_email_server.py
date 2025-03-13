from typing import List, Dict, Any
import os
import base64
from datetime import datetime, timedelta
import json
import sys
from mcp.server.fastmcp import FastMCP
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# Initialize FastMCP server
mcp = FastMCP("mcp_email_summarizer")

def get_gmail_service() -> Any:
    """Build and return a Gmail service object from token.json."""
    # Load credentials from token.json
    token_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'token.json')
    if not os.path.exists(token_path):
        print(f"Error: token.json not found at {token_path}", file=sys.stderr)
        raise FileNotFoundError(f"token.json not found at {token_path}")
    
    with open(token_path, 'r') as token_file:
        token_data = json.load(token_file)
    
    credentials = Credentials.from_authorized_user_info(token_data)
    return build('gmail', 'v1', credentials=credentials)

def parse_email_content(message: Dict[str, Any]) -> Dict[str, Any]:
    """Extract and decode email content from a Gmail API message."""
    parsed_email = {
        "id": message["id"],
        "threadId": message["threadId"],
        "date": None,
        "subject": None,
        "sender": None,
        "body": None
    }
    
    # Parse headers
    for header in message["payload"]["headers"]:
        if header["name"] == "Date":
            parsed_email["date"] = header["value"]
        elif header["name"] == "Subject":
            parsed_email["subject"] = header["value"]
        elif header["name"] == "From":
            parsed_email["sender"] = header["value"]
    
    # Extract body content
    if "parts" in message["payload"]:
        for part in message["payload"]["parts"]:
            if part["mimeType"] == "text/plain":
                data = part["body"].get("data", "")
                if data:
                    decoded_bytes = base64.urlsafe_b64decode(data)
                    parsed_email["body"] = decoded_bytes.decode("utf-8")
    else:
        # Handle single-part emails
        data = message["payload"]["body"].get("data", "")
        if data:
            decoded_bytes = base64.urlsafe_b64decode(data)
            parsed_email["body"] = decoded_bytes.decode("utf-8")
            
    return parsed_email

@mcp.tool()
async def fetch_emails(sender_email: str = "", days: int = 30) -> List[Dict[str, Any]]:
    """
    Fetch emails from a specific sender within a given timeframe.
    
    Args:
        sender_email: Email address to filter by (leave empty to fetch all emails)
        days: Number of days to look back (default: 30)
        
    Returns:
        List of emails with their content
    """
    try:
        print(f"Fetching emails from {sender_email if sender_email else 'any sender'} for the past {days} days", file=sys.stderr)
        # Create Gmail API service
        service = get_gmail_service()
        
        # Calculate date for query
        date_from = (datetime.now() - timedelta(days=days)).strftime('%Y/%m/%d')
        
        # Build query - only filter by sender if one is provided
        if sender_email:
            query = f"from:{sender_email} after:{date_from}"
        else:
            query = f"after:{date_from}"
            
        print(f"Query: {query}", file=sys.stderr)
        
        # Get message IDs
        results = service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])
        
        if not messages:
            print("No messages found", file=sys.stderr)
            return []
        
        print(f"Found {len(messages)} messages", file=sys.stderr)
        
        # Fetch full content for each message
        emails = []
        for message_info in messages:
            message = service.users().messages().get(userId='me', id=message_info['id'], format='full').execute()
            parsed_email = parse_email_content(message)
            emails.append(parsed_email)
        
        return emails
    
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return [{"error": str(e)}]

@mcp.tool()
async def summarize_emails(emails: List[Dict[str, Any]]) -> str:
    """
    Format emails for summarization by Claude.
    
    Args:
        emails: List of email objects
        
    Returns:
        Formatted email content for Claude to summarize
    """
    if not emails:
        return "No emails found from the specified sender in the given timeframe."
    
    if isinstance(emails, list) and emails and "error" in emails[0]:
        return f"Error fetching emails: {emails[0]['error']}"
    
    formatted_emails = []
    for i, email in enumerate(emails):
        formatted_email = f"""
Email #{i+1}
Date: {email.get('date', 'Unknown')}
Subject: {email.get('subject', 'No subject')}
---
{email.get('body', 'No content')}
"""
        formatted_emails.append(formatted_email)
    
    return "\n\n".join(formatted_emails)

if __name__ == "__main__":
    # Initialize and run the server
    print("Starting MCP Email Summarizer server...", file=sys.stderr)
    mcp.run(transport='stdio')