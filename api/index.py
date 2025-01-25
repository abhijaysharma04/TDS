import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Enable CORS
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # Load the marks.json file
            with open('./api/marks.json', 'r') as file:
                data = json.load(file)

            # Parse query parameters
            query = parse_qs(urlparse(self.path).query)
            names = query.get("name", [])

            # Fetch marks for the provided names
            marks = [entry["marks"] for entry in data if entry["name"] in names]

            # Send JSON response
            response = {"marks": marks}
            self.wfile.write(json.dumps(response).encode('utf-8'))

        except FileNotFoundError:
            self.send_response(500)
            self.end_headers()
            error_response = {"error": "marks.json file not found"}
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            error_response = {"error": str(e)}
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
