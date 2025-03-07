#!/usr/bin/env python3
import os
import json
import datetime
import argparse
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger('file-finder-mcp')

class MCPRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200, content_type='application/json'):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()
        
    def do_GET(self):
        self._set_headers()
        self.wfile.write(json.dumps({"status": "running"}).encode())
        
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            logger.info(f"Received request: {data}")
            
            if 'query' in data:
                query = data['query']
                results = self.find_files(query)
                response = {
                    "results": results
                }
                self._set_headers()
                self.wfile.write(json.dumps(response).encode())
            else:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Missing 'query' parameter"}).encode())
                
        except json.JSONDecodeError:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode())
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def find_files(self, query):
        """Find files in the file system matching the query fragment."""
        results = []
        
        # Get the root directory to start the search from
        # Default to the current working directory if not specified
        root_dir = os.path.abspath(os.getcwd())
        
        for root, _, files in os.walk(root_dir):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, root_dir)
                
                # Check if the query is in the file path
                if query.lower() in rel_path.lower():
                    try:
                        # Get file stats
                        stats = os.stat(file_path)
                        creation_time = datetime.datetime.fromtimestamp(stats.st_ctime)
                        
                        results.append({
                            "name": file,
                            "path": rel_path,
                            "size": stats.st_size,
                            "created": creation_time.isoformat()
                        })
                    except Exception as e:
                        logger.error(f"Error getting file stats for {file_path}: {str(e)}")
        
        return results

def run_server(host='localhost', port=8000):
    server_address = (host, port)
    httpd = HTTPServer(server_address, MCPRequestHandler)
    logger.info(f"Starting MCP server on {host}:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='File Finder MCP Server')
    parser.add_argument('--host', default='localhost', help='Host to bind the server to')
    parser.add_argument('--port', type=int, default=8000, help='Port to bind the server to')
    
    args = parser.parse_args()
    run_server(args.host, args.port) 