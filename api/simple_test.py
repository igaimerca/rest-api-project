"""
Simple test script for SMS Transaction REST API using urllib
Demonstrates all CRUD operations and authentication
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
        # Prepare request
        if data:
            data = json.dumps(data).encode('utf-8')
        
        # Create request
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header('Content-Type', 'application/json')
        
        if auth_header:
            req.add_header('Authorization', auth_header)
        
        # Make request
        with urllib.request.urlopen(req) as response:
            response_data = response.read().decode('utf-8')
            return response.getcode(), response_data
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8')
    except Exception as e:
        return 500, str(e)


def test_api():
    """Test the SMS Transaction API"""
    base_url = "http://localhost:8000"
    auth_header = "Basic YWRtaW46cGFzc3dvcmQxMjM="  # admin:password123
    
    print("SMS TRANSACTION API TEST SUITE")
    print("=" * 60)
    print("Make sure the API server is running on http://localhost:8000")
    print("Starting tests in 3 seconds...")
    time.sleep(3)
    
    # Test 1: Authentication with valid credentials
    print("\n1. Testing authentication with valid credentials...")
    status, response = make_request(f"{base_url}/transactions", auth_header=auth_header)
    print(f"   Status Code: {status}")
    if status == 200:
        data = json.loads(response)
        print(f"   ✓ Successfully authenticated and retrieved {len(data.get('transactions', []))} transactions")
    else:
        print(f"   ✗ Authentication failed: {response}")
        return
    
    # Test 2: Authentication with invalid credentials
    print("\n2. Testing authentication with invalid credentials...")
    status, response = make_request(f"{base_url}/transactions", auth_header="Basic invalid_credentials")
    print(f"   Status Code: {status}")
    if status == 401:
        print("   ✓ Correctly rejected invalid credentials")
    else:
        print(f"   ✗ Unexpected response: {response}")
    
    # Test 3: Get specific transaction
    print("\n3. Testing GET specific transaction...")
    status, response = make_request(f"{base_url}/transactions/1", auth_header=auth_header)
    print(f"   Status Code: {status}")
    if status == 200:
        transaction = json.loads(response)
        print(f"   ✓ Retrieved transaction ID {transaction.get('id')}: {transaction.get('type')} - {transaction.get('amount')}")
    else:
        print(f"   ✗ Error: {response}")
    
    # Test 4: Create new transaction
    print("\n4. Testing CREATE transaction...")
    new_transaction = {
        "type": "deposit",
        "amount": 100000,
        "sender": "+250788999999",
        "receiver": "+250789000000",
        "timestamp": "2024-01-16T20:00:00Z",
        "status": "completed",
        "description": "Test transaction created via API"
    }
    
    status, response = make_request(f"{base_url}/transactions", method='POST', data=new_transaction, auth_header=auth_header)
    print(f"   Status Code: {status}")
    if status == 201:
        created_transaction = json.loads(response)
        created_id = created_transaction.get('id')
        print(f"   ✓ Created transaction ID {created_id}")
        
        # Verify the transaction was created by getting all transactions
        print("\n   Verifying transaction was created...")
        status, response = make_request(f"{base_url}/transactions", auth_header=auth_header)
        if status == 200:
            data = json.loads(response)
            total_count = len(data.get('transactions', []))
            print(f"   Total transactions now: {total_count}")
            
            # Check if our transaction exists
            found = False
            for t in data.get('transactions', []):
                if t.get('id') == created_id:
                    found = True
                    print(f"   ✓ Transaction {created_id} found in list")
                    break
            if not found:
                print(f"   ✗ Transaction {created_id} not found in list")
        
        # Test 5: Update transaction
        print("\n5. Testing UPDATE transaction...")
        update_data = {
            "amount": 150000,
            "status": "pending",
            "description": "Updated test transaction"
        }
        
        status, response = make_request(f"{base_url}/transactions/{created_id}", method='PUT', data=update_data, auth_header=auth_header)
        print(f"   Status Code: {status}")
        if status == 200:
            updated_transaction = json.loads(response)
            print(f"   ✓ Updated transaction ID {created_id}: Amount = {updated_transaction.get('amount')}")
        else:
            print(f"   ✗ Update failed: {response}")
        
        # Test 6: Delete transaction
        print("\n6. Testing DELETE transaction...")
        status, response = make_request(f"{base_url}/transactions/{created_id}", method='DELETE', auth_header=auth_header)
        print(f"   Status Code: {status}")
        if status == 200:
            print(f"   ✓ Deleted transaction ID {created_id}")
        else:
            print(f"   ✗ Delete failed: {response}")
    
    else:
        print(f"   ✗ Create failed: {response}")
    
    # Test 7: Error handling - non-existent transaction
    print("\n7. Testing error handling - non-existent transaction...")
    status, response = make_request(f"{base_url}/transactions/999", auth_header=auth_header)
    print(f"   Status Code: {status}")
    if status == 404:
        print("   ✓ Correctly returned 404 for non-existent transaction")
    else:
        print(f"   ✗ Unexpected response: {response}")
    
    # Test 8: Error handling - invalid ID format
    print("\n8. Testing error handling - invalid ID format...")
    status, response = make_request(f"{base_url}/transactions/abc", auth_header=auth_header)
    print(f"   Status Code: {status}")
    if status == 400:
        print("   ✓ Correctly returned 400 for invalid ID format")
    else:
        print(f"   ✗ Unexpected response: {response}")
    
    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    test_api()
