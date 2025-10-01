"""
XML Parser for SMS Transaction Data
Converts XML data to JSON objects for API consumption
"""

import xml.etree.ElementTree as ET
import json
from typing import List, Dict, Any


class SMSDataParser:
    """Parser for SMS transaction XML data"""
    
    def __init__(self, xml_file_path: str):
        self.xml_file_path = xml_file_path
        self.transactions = []
    
    def parse_xml_to_json(self) -> List[Dict[str, Any]]:
        """
        Parse XML file and convert to list of JSON objects
        
        Returns:
            List[Dict[str, Any]]: List of transaction dictionaries
        """
        try:
            # Parse the XML file
            tree = ET.parse(self.xml_file_path)
            root = tree.getroot()
            
            # Extract transaction data
            for transaction in root.findall('transaction'):
                transaction_data = {
                    'id': int(transaction.get('id')),
                    'type': transaction.find('type').text,
                    'amount': int(transaction.find('amount').text),
                    'sender': transaction.find('sender').text,
                    'receiver': transaction.find('receiver').text,
                    'timestamp': transaction.find('timestamp').text,
                    'status': transaction.find('status').text,
                    'description': transaction.find('description').text
                }
                self.transactions.append(transaction_data)
            
            return self.transactions
            
        except ET.ParseError as e:
            print(f"XML parsing error: {e}")
            return []
        except FileNotFoundError:
            print(f"XML file not found: {self.xml_file_path}")
            return []
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []
    
    def save_to_json(self, output_file: str) -> bool:
        """
        Save parsed data to JSON file
        
        Args:
            output_file (str): Path to output JSON file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.transactions, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving to JSON: {e}")
            return False
    
    def get_transaction_by_id(self, transaction_id: int) -> Dict[str, Any] | None:
        """
        Get a specific transaction by ID
        
        Args:
            transaction_id (int): ID of the transaction to retrieve
            
        Returns:
            Dict[str, Any] | None: Transaction data or None if not found
        """
        for transaction in self.transactions:
            if transaction['id'] == transaction_id:
                return transaction
        return None
    
    def get_transactions_by_type(self, transaction_type: str) -> List[Dict[str, Any]]:
        """
        Get all transactions of a specific type
        
        Args:
            transaction_type (str): Type of transactions to retrieve
            
        Returns:
            List[Dict[str, Any]]: List of matching transactions
        """
        return [t for t in self.transactions if t['type'] == transaction_type]
    
    def get_transactions_by_status(self, status: str) -> List[Dict[str, Any]]:
        """
        Get all transactions with a specific status
        
        Args:
            status (str): Status of transactions to retrieve
            
        Returns:
            List[Dict[str, Any]]: List of matching transactions
        """
        return [t for t in self.transactions if t['status'] == status]


def main():
    """Main function to demonstrate XML parsing"""
    parser = SMSDataParser('modified_sms_v2.xml')
    
    # Parse XML to JSON
    transactions = parser.parse_xml_to_json()
    
    if transactions:
        print(f"Successfully parsed {len(transactions)} transactions")
        
        # Save to JSON file
        parser.save_to_json('transactions.json')
        print("Data saved to transactions.json")
        
        # Display first transaction as example
        if transactions:
            print("\nFirst transaction:")
            print(json.dumps(transactions[0], indent=2))
    else:
        print("No transactions found or parsing failed")


if __name__ == "__main__":
    main()
