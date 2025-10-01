"""
Test script for SMS Transaction REST API
Demonstrates all CRUD operations and authentication
"""

import urllib.request
import urllib.parse
import urllib.error
import json
import base64
import time
from typing import Dict, Any


class APITester:
    """Test class for the SMS Transaction API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.auth_header = self._get_auth_header("admin", "password123")
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Authorization': self.auth_header
        })
    
    def _get_auth_header(self, username: str, password: str) -> str:
        """Generate Basic Auth header"""
        credentials = f"{username}:{password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded_credentials}"
    
    def test_authentication(self):
        """Test authentication with valid and invalid credentials"""
        print("=" * 60)
        print("TESTING AUTHENTICATION")
        print("=" * 60)
        
        # Test with valid credentials
        print("1. Testing with valid credentials...")
        response = self.session.get(f"{self.base_url}/transactions")
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {len(data.get('transactions', []))} transactions found")
        else:
            print(f"   Error: {response.text}")
        
        # Test with invalid credentials
        print("\n2. Testing with invalid credentials...")
        invalid_session = requests.Session()
        invalid_session.headers.update({
            'Content-Type': 'application/json',
            'Authorization': 'Basic invalid_credentials'
        })
        response = invalid_session.get(f"{self.base_url}/transactions")
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 401:
            print("   ✓ Correctly rejected invalid credentials")
        else:
            print(f"   ✗ Unexpected response: {response.text}")
    
    def test_get_all_transactions(self):
        """Test GET /transactions endpoint"""
        print("\n" + "=" * 60)
        print("TESTING GET ALL TRANSACTIONS")
        print("=" * 60)
        
        response = self.session.get(f"{self.base_url}/transactions")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            transactions = data.get('transactions', [])
            print(f"Total Transactions: {len(transactions)}")
            print(f"Count Field: {data.get('count')}")
            
            if transactions:
                print("\nFirst transaction:")
                print(json.dumps(transactions[0], indent=2))
        else:
            print(f"Error: {response.text}")
    
    def test_get_specific_transaction(self):
        """Test GET /transactions/{id} endpoint"""
        print("\n" + "=" * 60)
        print("TESTING GET SPECIFIC TRANSACTION")
        print("=" * 60)
        
        # Test with existing ID
        print("1. Testing with existing transaction ID (1)...")
        response = self.session.get(f"{self.base_url}/transactions/1")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            transaction = response.json()
            print(f"   Transaction ID: {transaction.get('id')}")
            print(f"   Type: {transaction.get('type')}")
            print(f"   Amount: {transaction.get('amount')}")
        else:
            print(f"   Error: {response.text}")
        
        # Test with non-existing ID
        print("\n2. Testing with non-existing transaction ID (999)...")
        response = self.session.get(f"{self.base_url}/transactions/999")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 404:
            print("   ✓ Correctly returned 404 for non-existing transaction")
        else:
            print(f"   ✗ Unexpected response: {response.text}")
        
        # Test with invalid ID format
        print("\n3. Testing with invalid ID format (abc)...")
        response = self.session.get(f"{self.base_url}/transactions/abc")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 400:
            print("   ✓ Correctly returned 400 for invalid ID format")
        else:
            print(f"   ✗ Unexpected response: {response.text}")
    
    def test_create_transaction(self):
        """Test POST /transactions endpoint"""
        print("\n" + "=" * 60)
        print("TESTING CREATE TRANSACTION")
        print("=" * 60)
        
        new_transaction = {
            "type": "deposit",
            "amount": 100000,
            "sender": "+250788999999",
            "receiver": "+250789000000",
            "timestamp": "2024-01-16T20:00:00Z",
            "status": "completed",
            "description": "Test transaction created via API"
        }
        
        print("Creating new transaction...")
        print(f"Transaction data: {json.dumps(new_transaction, indent=2)}")
        
        response = self.session.post(f"{self.base_url}/transactions", json=new_transaction)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            created_transaction = response.json()
            print("✓ Transaction created successfully!")
            print(f"Created Transaction ID: {created_transaction.get('id')}")
            print(f"Response: {json.dumps(created_transaction, indent=2)}")
            return created_transaction.get('id')
        else:
            print(f"✗ Error creating transaction: {response.text}")
            return None
    
    def test_update_transaction(self, transaction_id: int):
        """Test PUT /transactions/{id} endpoint"""
        print("\n" + "=" * 60)
        print("TESTING UPDATE TRANSACTION")
        print("=" * 60)
        
        if not transaction_id:
            print("No transaction ID provided for update test")
            return
        
        update_data = {
            "amount": 150000,
            "status": "pending",
            "description": "Updated test transaction"
        }
        
        print(f"Updating transaction ID {transaction_id}...")
        print(f"Update data: {json.dumps(update_data, indent=2)}")
        
        response = self.session.put(f"{self.base_url}/transactions/{transaction_id}", json=update_data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            updated_transaction = response.json()
            print("✓ Transaction updated successfully!")
            print(f"Updated Transaction: {json.dumps(updated_transaction, indent=2)}")
        else:
            print(f"✗ Error updating transaction: {response.text}")
    
    def test_delete_transaction(self, transaction_id: int):
        """Test DELETE /transactions/{id} endpoint"""
        print("\n" + "=" * 60)
        print("TESTING DELETE TRANSACTION")
        print("=" * 60)
        
        if not transaction_id:
            print("No transaction ID provided for delete test")
            return
        
        print(f"Deleting transaction ID {transaction_id}...")
        
        response = self.session.delete(f"{self.base_url}/transactions/{transaction_id}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✓ Transaction deleted successfully!")
            print(f"Response: {response.text}")
        else:
            print(f"✗ Error deleting transaction: {response.text}")
    
    def test_error_handling(self):
        """Test various error scenarios"""
        print("\n" + "=" * 60)
        print("TESTING ERROR HANDLING")
        print("=" * 60)
        
        # Test missing required fields in POST
        print("1. Testing POST with missing required fields...")
        incomplete_data = {
            "type": "deposit",
            "amount": 50000
            # Missing other required fields
        }
        
        response = self.session.post(f"{self.base_url}/transactions", json=incomplete_data)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 400:
            print("   ✓ Correctly returned 400 for missing required fields")
        else:
            print(f"   ✗ Unexpected response: {response.text}")
        
        # Test invalid JSON
        print("\n2. Testing POST with invalid JSON...")
        invalid_session = requests.Session()
        invalid_session.headers.update({
            'Content-Type': 'application/json',
            'Authorization': self.auth_header
        })
        
        response = invalid_session.post(
            f"{self.base_url}/transactions",
            data="invalid json data"
        )
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 400:
            print("   ✓ Correctly returned 400 for invalid JSON")
        else:
            print(f"   ✗ Unexpected response: {response.text}")
    
    def run_all_tests(self):
        """Run all API tests"""
        print("SMS TRANSACTION API TEST SUITE")
        print("=" * 60)
        print("Make sure the API server is running on http://localhost:8000")
        print("Starting tests in 3 seconds...")
        time.sleep(3)
        
        try:
            # Test authentication
            self.test_authentication()
            
            # Test GET operations
            self.test_get_all_transactions()
            self.test_get_specific_transaction()
            
            # Test POST operation
            created_id = self.test_create_transaction()
            
            # Test PUT operation
            if created_id:
                self.test_update_transaction(created_id)
            
            # Test error handling
            self.test_error_handling()
            
            # Test DELETE operation
            if created_id:
                self.test_delete_transaction(created_id)
            
            print("\n" + "=" * 60)
            print("ALL TESTS COMPLETED")
            print("=" * 60)
            
        except requests.exceptions.ConnectionError:
            print("\n✗ ERROR: Could not connect to the API server")
            print("Make sure the server is running on http://localhost:8000")
        except Exception as e:
            print(f"\n✗ ERROR: {e}")


def main():
    """Main function to run API tests"""
    tester = APITester()
    tester.run_all_tests()


if __name__ == "__main__":
    main()
