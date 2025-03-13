# <a id="readme-top"></a>
# <h1> MCP Email Summarizer</h1>

<div align="left">
  <p>
  A Model Context Protocol (MCP) server that connects Claude Desktop to Gmail, allowing you to summarize and analyze your emails directly through conversational AI.
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#features">Features</a> </li>
    <li><a href="#built-with">Built With</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## Features
*Email Access: Fetch emails from specific senders or time periods
*Smart Summaries: Ask Claude to summarize email content in various ways

<br />
<br />

## Built With
*Python 3.11 - Core language
*MCP - Model Context Protocol for AI tool integration
*Google Gmail API - Email access
*Claude Desktop - AI assistant with MCP support
  
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites
- Python 3.10 or higher
- Claude Desktop
- Google account with Gmail

###Installation

Clone the repository:
```
clone https://github.com/yourusername/mcp-email-summarizer.git
cd mcp-email-summarizer
```

Create a virtual environment using uv:
```
uv init .
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

Install dependencies:
```
uv add "mcp[cli]" httpx google-api-python-client google-auth-oauthlib
```

###Set Up Gmail API Access

Enable Gmail API:
1. Go to Google Cloud Console.
2. Create a new project (e.g., "MCP Email Summarizer").
3. Navigate to "APIs & Services" > "Library," search for "Gmail API," and enable it.


Create OAuth Credentials:
4. Go to "APIs & Services" > "Credentials."
5. Click "CONFIGURE CONSENT SCREEN"
6. Select "External" in User Type
7. Fill in App Information and add your email address
8. Go to "Scopes" and add "https://www.googleapis.com/auth/gmail.readonly"
9. Go to "Test users" and add your email address
10. Go to "Credentials" and create an OAuth client ID (Desktop application)
11. Download the credentials JSON file and save it as credentials.json in your project folder


Authenticate with Gmail:
12. Create and run the following script to generate your authentication token:
```
from google_auth_oauthlib.flow import InstalledAppFlow
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=0)
with open('token.json', 'w') as token:
    token.write(creds.to_json())
```
Run it:
```
uv credentials.py
```


###Configure Claude Desktop

Create or edit the Claude Desktop configuration file:
```
macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
Windows: %APPDATA%\Claude\claude_desktop_config.json
```

Add your MCP server configuration:
```
{
    "mcpServers": {
        "mcp_email_summarizer": {
            "command": "/Users/username/.local/bin/uv",
            "args": [
                "--directory",
                "/Users/username/mcp_email_summarizer",
                "run",
                "mcp_email_server.py"
            ]
        }
    }
}
```
You need to:

Replace /Users/username/.local/bin/uv with the full path to your uv executable (find using which uv on macOS/Linux or where uv on Windows).
Replace /Users/username/projects/mcp_email_summarizer with the absolute path to your project directory.

###Usage
Open Claude Desktop
Ask questions like:

"Summarize my emails from newsletter@example.com in the past week"
"What are the main topics in my emails from the last month?"
"Find action items in my recent emails"
"Analyze the sentiment of emails from my team"



Claude will:

Request permission to access your emails
Execute the appropriate MCP tools
Present the analyzed information in a conversational format
   

<!-- CONTRIBUTING -->
## Contributing

If you have an idea to improve this, kindly fork the repository and open a pull request. We also welcome enhancement suggestions filed as issues. 
Stars ⭐ from you will brighten our day! Thanks for checking out our project.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/NewFeature`)
3. Commit your Changes (`git commit -m 'Add some NewFeature'`)
4. Push to the Branch (`git push origin feature/NewFeature`)
5. Open a Pull Request


<!-- CONTACT -->
## Contact

Asako Hayase- [LinkedIn](https://www.linkedin.com/in/asako-hayase-924508ba/)
