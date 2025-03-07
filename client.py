#!/usr/bin/env python3
import json
import argparse
import requests

def search_files(query, host='localhost', port=8000):
    """
    Send a search request to the MCP server.
    
    Args:
        query (str): The file path fragment to search for
        host (str): The host where the MCP server is running
        port (int): The port where the MCP server is running
        
    Returns:
        dict: The server response
    """
    url = f"http://{host}:{port}"
    headers = {'Content-Type': 'application/json'}
    data = {'query': query}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to MCP server: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='File Finder MCP Client')
    parser.add_argument('query', help='File path fragment to search for')
    parser.add_argument('--host', default='localhost', help='Host where the MCP server is running')
    parser.add_argument('--port', type=int, default=8000, help='Port where the MCP server is running')
    
    args = parser.parse_args()
    
    results = search_files(args.query, args.host, args.port)
    if results:
        print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main() 