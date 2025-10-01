"""
REST API for SMS Transaction Data
Implements CRUD operations with Basic Authentication
"""

import json
import base64
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any, Optional
import sys
import os

# Add the parent directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dsa.xml_parser import SMSDataParser

# Global data store to persist across requests
_transactions = []
_transaction_dict = {}
_data_loaded = False

def load_transaction_data():
    """Load transaction data from XML file"""
    global _transactions, _transaction_dict, _data_loaded
    
    if _data_loaded:
        return
    
    try:
        xml_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'modified_sms_v2.xml')
        parser = SMSDataParser(xml_path)
        _transactions = parser.parse_xml_to_json()
        _transaction_dict = {t['id']: t for t in _transactions}
        _data_loaded = True
        print(f"Loaded {len(_transactions)} transactions")
    except Exception as e:
        print(f"Error loading transactions: {e}")
        _transactions = []
        _transaction_dict = {}
        _data_loaded = True


class TransactionAPIHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler for Transaction API"""
    
    def __init__(self, *args, **kwargs):
        # Load data only once
        load_transaction_data()
        super().__init__(*args, **kwargs)
    
    def authenticate(self) -> bool:
        """
        Authenticate using Basic Authentication
        
        Returns:
            bool: True if authenticated, False otherwise
        """
        auth_header = self.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Basic '):
            return False
        
        try:
            # Decode the base64 encoded credentials
            encoded_credentials = auth_header[6:]  # Remove 'Basic ' prefix
            decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
            username, password = decoded_credentials.split(':', 1)
            
            # Simple hardcoded credentials (in production, use proper user management)
            return username == 'admin' and password == 'password123'
            
        except Exception as e:
            print(f"Authentication error: {e}")
            return False
    
    def send_unauthorized_response(self):
        """Send 401 Unauthorized response"""
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="Transaction API"')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        error_response = {
            'error': 'Unauthorized',
            'message': 'Authentication required',
            'status_code': 401
        }
        self.wfile.write(json.dumps(error_response).encode('utf-8'))
    
    def send_json_response(self, data: Any, status_code: int = 200):
        """Send JSON response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        
        response = json.dumps(data, indent=2, ensure_ascii=False)
        self.wfile.write(response.encode('utf-8'))
    
    def send_error_response(self, message: str, status_code: int = 400):
        """Send error response"""
        error_data = {
            'error': message,
            'status_code': status_code
        }
        self.send_json_response(error_data, status_code)
    
    def parse_json_body(self) -> Optional[Dict[str, Any]]:
        """Parse JSON from request body"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                return None
            
            body = self.rfile.read(content_length)
            return json.loads(body.decode('utf-8'))
        except Exception as e:
            print(f"Error parsing JSON body: {e}")
            return None
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        if not self.authenticate():
            self.send_unauthorized_response()
            return
        
        path = self.path.split('?')[0]  # Remove query parameters
        
        if path == '/transactions':
            # GET /transactions - List all transactions
            self.send_json_response({
                'transactions': _transactions,
                'count': len(_transactions)
            })
        
        elif path.startswith('/transactions/'):
            # GET /transactions/{id} - Get specific transaction
            try:
                transaction_id = int(path.split('/')[-1])
                transaction = _transaction_dict.get(transaction_id)
                
                if transaction:
                    self.send_json_response(transaction)
                else:
                    self.send_error_response(f'Transaction with ID {transaction_id} not found', 404)
            except ValueError:
                self.send_error_response('Invalid transaction ID format', 400)
        
        else:
            self.send_error_response('Endpoint not found', 404)
    
    def do_POST(self):
        """Handle POST requests"""
        if not self.authenticate():
            self.send_unauthorized_response()
            return
        
        if self.path == '/transactions':
            # POST /transactions - Create new transaction
            data = self.parse_json_body()
            
            if not data:
                self.send_error_response('Invalid JSON data', 400)
                return
            
            # Validate required fields
            required_fields = ['type', 'amount', 'sender', 'receiver', 'timestamp', 'status', 'description']
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                self.send_error_response(f'Missing required fields: {", ".join(missing_fields)}', 400)
                return
            
            # Generate new ID
            new_id = max([t['id'] for t in _transactions], default=0) + 1
            
            # Create new transaction
            new_transaction = {
                'id': new_id,
                'type': data['type'],
                'amount': int(data['amount']),
                'sender': data['sender'],
                'receiver': data['receiver'],
                'timestamp': data['timestamp'],
                'status': data['status'],
                'description': data['description']
            }
            
            # Add to data structures
            _transactions.append(new_transaction)
            _transaction_dict[new_id] = new_transaction
            
            self.send_json_response(new_transaction, 201)
        
        else:
            self.send_error_response('Endpoint not found', 404)
    
    def do_PUT(self):
        """Handle PUT requests"""
        if not self.authenticate():
            self.send_unauthorized_response()
            return
        
        if self.path.startswith('/transactions/'):
            # PUT /transactions/{id} - Update existing transaction
            try:
                transaction_id = int(self.path.split('/')[-1])
                data = self.parse_json_body()
                
                if not data:
                    self.send_error_response('Invalid JSON data', 400)
                    return
                
                # Check if transaction exists
                if transaction_id not in _transaction_dict:
                    self.send_error_response(f'Transaction with ID {transaction_id} not found', 404)
                    return
                
                # Update transaction
                updated_transaction = _transaction_dict[transaction_id].copy()
                for key, value in data.items():
                    if key != 'id':  # Don't allow ID changes
                        updated_transaction[key] = value
                
                # Update in both data structures
                _transaction_dict[transaction_id] = updated_transaction
                for i, transaction in enumerate(_transactions):
                    if transaction['id'] == transaction_id:
                        _transactions[i] = updated_transaction
                        break
                
                self.send_json_response(updated_transaction)
                
            except ValueError:
                self.send_error_response('Invalid transaction ID format', 400)
        
        else:
            self.send_error_response('Endpoint not found', 404)
    
    def do_DELETE(self):
        """Handle DELETE requests"""
        if not self.authenticate():
            self.send_unauthorized_response()
            return
        
        if self.path.startswith('/transactions/'):
            # DELETE /transactions/{id} - Delete transaction
            try:
                transaction_id = int(self.path.split('/')[-1])
                
                if transaction_id not in _transaction_dict:
                    self.send_error_response(f'Transaction with ID {transaction_id} not found', 404)
                    return
                
                # Remove from both data structures
                del _transaction_dict[transaction_id]
                _transactions[:] = [t for t in _transactions if t['id'] != transaction_id]
                
                self.send_json_response({
                    'message': f'Transaction {transaction_id} deleted successfully',
                    'status_code': 200
                })
                
            except ValueError:
                self.send_error_response('Invalid transaction ID format', 400)
        
        else:
            self.send_error_response('Endpoint not found', 404)


def run_server(port: int = 8000):
    """Run the REST API server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, TransactionAPIHandler)
    
    print(f"Starting REST API server on port {port}")
    print("Available endpoints:")
    print("  GET    /transactions          - List all transactions")
    print("  GET    /transactions/{id}     - Get specific transaction")
    print("  POST   /transactions          - Create new transaction")
    print("  PUT    /transactions/{id}     - Update transaction")
    print("  DELETE /transactions/{id}     - Delete transaction")
    print("\nAuthentication: Basic Auth (admin:password123)")
    print(f"Server running at http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.shutdown()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='REST API for SMS Transaction Data')
    parser.add_argument('--port', type=int, default=8000, help='Port to run the server on')
    args = parser.parse_args()
    
    run_server(args.port)
