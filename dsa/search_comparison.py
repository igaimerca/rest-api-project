"""
Data Structures and Algorithms Comparison
Compares linear search vs dictionary lookup efficiency
"""

import time
import random
from typing import List, Dict, Any, Optional


class SearchComparison:
    """Compare different search algorithms for transaction data"""
    
    def __init__(self, transactions: List[Dict[str, Any]]):
        self.transactions = transactions
        self.transaction_dict = {t['id']: t for t in transactions}
    
    def linear_search(self, target_id: int) -> Optional[Dict[str, Any]]:
        """
        Linear search through list of transactions
        
        Args:
            target_id (int): ID to search for
            
        Returns:
            Optional[Dict[str, Any]]: Found transaction or None
        """
        for transaction in self.transactions:
            if transaction['id'] == target_id:
                return transaction
        return None
    
    def dictionary_lookup(self, target_id: int) -> Optional[Dict[str, Any]]:
        """
        Dictionary lookup for transaction
        
        Args:
            target_id (int): ID to search for
            
        Returns:
            Optional[Dict[str, Any]]: Found transaction or None
        """
        return self.transaction_dict.get(target_id)
    
    def measure_search_time(self, search_func, target_id: int, iterations: int = 1000) -> float:
        """
        Measure average search time for a given function
        
        Args:
            search_func: Function to measure
            target_id (int): ID to search for
            iterations (int): Number of iterations to average
            
        Returns:
            float: Average time in seconds
        """
        times = []
        
        for _ in range(iterations):
            start_time = time.perf_counter()
            search_func(target_id)
            end_time = time.perf_counter()
            times.append(end_time - start_time)
        
        return sum(times) / len(times)
    
    def compare_search_methods(self, test_ids: List[int], iterations: int = 1000) -> Dict[str, Any]:
        """
        Compare linear search vs dictionary lookup
        
        Args:
            test_ids (List[int]): List of IDs to test
            iterations (int): Number of iterations per test
            
        Returns:
            Dict[str, Any]: Comparison results
        """
        results = {
            'linear_search_times': [],
            'dictionary_lookup_times': [],
            'test_ids': test_ids,
            'iterations': iterations
        }
        
        print(f"Comparing search methods with {iterations} iterations each...")
        print(f"Testing with {len(test_ids)} different IDs\n")
        
        for i, test_id in enumerate(test_ids, 1):
            print(f"Test {i}/{len(test_ids)}: Searching for ID {test_id}")
            
            # Measure linear search
            linear_time = self.measure_search_time(self.linear_search, test_id, iterations)
            results['linear_search_times'].append(linear_time)
            
            # Measure dictionary lookup
            dict_time = self.measure_search_time(self.dictionary_lookup, test_id, iterations)
            results['dictionary_lookup_times'].append(dict_time)
            
            print(f"  Linear Search: {linear_time:.8f} seconds")
            print(f"  Dictionary Lookup: {dict_time:.8f} seconds")
            print(f"  Speedup: {linear_time / dict_time:.2f}x faster\n")
        
        # Calculate averages
        avg_linear = sum(results['linear_search_times']) / len(results['linear_search_times'])
        avg_dict = sum(results['dictionary_lookup_times']) / len(results['dictionary_lookup_times'])
        
        results['average_linear_time'] = avg_linear
        results['average_dict_time'] = avg_dict
        results['overall_speedup'] = avg_linear / avg_dict
        
        print("=" * 50)
        print("SUMMARY RESULTS")
        print("=" * 50)
        print(f"Average Linear Search Time: {avg_linear:.8f} seconds")
        print(f"Average Dictionary Lookup Time: {avg_dict:.8f} seconds")
        print(f"Overall Speedup: {results['overall_speedup']:.2f}x faster")
        print("=" * 50)
        
        return results
    
    def analyze_complexity(self) -> Dict[str, str]:
        """
        Analyze time complexity of both methods
        
        Returns:
            Dict[str, str]: Complexity analysis
        """
        return {
            'linear_search': {
                'time_complexity': 'O(n)',
                'space_complexity': 'O(1)',
                'description': 'Must check each element in the list until found'
            },
            'dictionary_lookup': {
                'time_complexity': 'O(1) average case',
                'space_complexity': 'O(n)',
                'description': 'Direct key access using hash table'
            },
            'explanation': {
                'why_dict_faster': 'Dictionary uses hash table for O(1) average lookup time',
                'trade_off': 'Dictionary requires O(n) extra space to store the mapping',
                'when_to_use_linear': 'When memory is limited and searches are infrequent',
                'when_to_use_dict': 'When frequent lookups are needed and memory is available'
            }
        }


def generate_test_data(num_transactions: int = 25) -> List[Dict[str, Any]]:
    """
    Generate test transaction data
    
    Args:
        num_transactions (int): Number of transactions to generate
        
    Returns:
        List[Dict[str, Any]]: List of transaction dictionaries
    """
    transactions = []
    types = ['deposit', 'withdrawal', 'transfer', 'payment']
    statuses = ['completed', 'pending', 'failed']
    
    for i in range(1, num_transactions + 1):
        transaction = {
            'id': i,
            'type': random.choice(types),
            'amount': random.randint(1000, 500000),
            'sender': f"+250788{random.randint(100000, 999999)}",
            'receiver': f"+250788{random.randint(100000, 999999)}",
            'timestamp': f"2024-01-{random.randint(15, 20)}T{random.randint(8, 23):02d}:{random.randint(0, 59):02d}:00Z",
            'status': random.choice(statuses),
            'description': f"Transaction {i} description"
        }
        transactions.append(transaction)
    
    return transactions


def main():
    """Main function to demonstrate search comparison"""
    print("Data Structures and Algorithms Comparison")
    print("=" * 50)
    
    # Generate test data
    transactions = generate_test_data(25)
    print(f"Generated {len(transactions)} test transactions")
    
    # Create comparison instance
    comparison = SearchComparison(transactions)
    
    # Test with random IDs
    test_ids = random.sample(range(1, len(transactions) + 1), min(10, len(transactions)))
    
    # Run comparison
    results = comparison.compare_search_methods(test_ids, iterations=1000)
    
    # Analyze complexity
    complexity = comparison.analyze_complexity()
    
    print("\nCOMPLEXITY ANALYSIS")
    print("=" * 50)
    for method, analysis in complexity.items():
        if isinstance(analysis, dict):
            print(f"\n{method.upper()}:")
            for key, value in analysis.items():
                print(f"  {key}: {value}")
    
    return results, complexity


if __name__ == "__main__":
    main()
