#!/usr/bin/env python3
"""
Debug script to test the API data persistence issue
"""

import urllib.request
import urllib.parse
import urllib.error
import json
import base64
import time

def make_request(url, method='GET', data=None, auth_header=None):
    """Make HTTP request using urllib"""
    try:
        if data:
            data = json.dumps(data).encode('utf-8')
        
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header('Content-Type', 'application/json')
        
        if auth_header:
            req.add_header('Authorization', auth_header)
        
        with urllib.request.urlopen(req) as response:
            response_data = response.read().decode('utf-8')
            return response.getcode(), response_data
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8')
    except Exception as e:
        return 500, str(e)

def test_data_persistence():
    """Test if data persists between requests"""
    base_url = "http://localhost:8000"
    auth_header = "Basic YWRtaW46cGFzc3dvcmQxMjM="
    
    print("Testing data persistence...")
    
    # 1. Get initial count
    print("\n1. Getting initial transaction count...")
    status, response = make_request(f"{base_url}/transactions", auth_header=auth_header)
    if status == 200:
        data = json.loads(response)
        initial_count = data.get('count', 0)
        print(f"   Initial count: {initial_count}")
    else:
        print(f"   Error: {response}")
        return
    
    # 2. Create a new transaction
    print("\n2. Creating new transaction...")
    new_transaction = {
        "type": "deposit",
        "amount": 50000,
        "sender": "+250788111111",
        "receiver": "+250788222222",
        "timestamp": "2024-01-16T21:00:00Z",
        "status": "completed",
        "description": "Debug test transaction"
    }
    
    status, response = make_request(f"{base_url}/transactions", method='POST', data=new_transaction, auth_header=auth_header)
    if status == 201:
        created_data = json.loads(response)
        created_id = created_data.get('id')
        print(f"   Created transaction ID: {created_id}")
    else:
        print(f"   Error creating transaction: {response}")
        return
    
    # 3. Get count again immediately
    print("\n3. Getting count after creation...")
    status, response = make_request(f"{base_url}/transactions", auth_header=auth_header)
    if status == 200:
        data = json.loads(response)
        after_count = data.get('count', 0)
        print(f"   Count after creation: {after_count}")
        
        if after_count > initial_count:
            print("   ✓ Data persisted!")
        else:
            print("   ✗ Data did not persist!")
            
        # Check if our transaction is in the list
        transactions = data.get('transactions', [])
        found = any(t.get('id') == created_id for t in transactions)
        if found:
            print(f"   ✓ Transaction {created_id} found in list")
        else:
            print(f"   ✗ Transaction {created_id} not found in list")
    else:
        print(f"   Error: {response}")

if __name__ == "__main__":
    test_data_persistence()
