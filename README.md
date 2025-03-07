# File Finder MCP Server

A Model Context Protocol (MCP) server for finding files in the file system by path fragment. This server integrates with Cline in VSCode to provide file search capabilities.

## Features

- Find files in the file system by path fragment
- Returns file name, path, size, and creation date
- Easy integration with Cline in VSCode

## Installation

### Prerequisites

- Python 3.6 or higher
- VSCode with Cline extension installed

### Steps

1. Clone the repository:

```bash
cd file-finder-mcp
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Install the package (optional):

```bash
pip install -e .
```

## Usage

### Starting the MCP Server

You can start the server directly:

```bash
python server.py
```

Or with custom host and port:

```bash
python server.py --host 127.0.0.1 --port 8080
```

### Testing with the Client

The repository includes a test client that you can use to verify the server is working:

```bash
python client.py "search_term"
```

For example, to search for all Python files:

```bash
python client.py ".py"
```

### Integrating with Cline in VSCode

1. Open VSCode settings (File > Preferences > Settings)
2. Search for "Cline: MCP Servers"
3. Click on "Edit in settings.json"
4. Add the following configuration:

```json
{
  "mcpServers": {
    "file-finder-mcp": {
      "args": [
        "--host", "localhost",
        "--port", "8000"
      ],
      "command": "python",
      "scriptPath": "/path/to/file-finder-mcp/server.py",
      "autoApprove": [],
      "disabled": false
    }
  }
}
```

Replace `/path/to/file-finder-mcp/server.py` with the actual path to the server.py file on your system.

## Example Prompts for Cline

You can use the following prompts in Cline to test the MCP server:

```
Find files with "config" in the path
```

```
Search for Python files in the current project
```

```
Find all JSON files in the system
```

## API Reference

### Endpoint

`POST http://localhost:8000`

### Request Format

```json
{
  "query": "file_path_fragment"
}
```

### Response Format

```json
{
  "results": [
    {
      "name": "filename.ext",
      "path": "relative/path/to/filename.ext",
      "size": 1234,
      "created": "2025-01-01T12:00:00"
    },
    ...
  ]
}
```
