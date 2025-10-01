"""
Main DSA Comparison Script
Demonstrates linear search vs dictionary lookup efficiency
"""

import sys
import os
import json
import time
import random
from xml_parser import SMSDataParser
from search_comparison import SearchComparison


def load_transaction_data():
    """Load transaction data from XML file"""
    print("Loading transaction data...")
    
    # Get the path to the XML file
    xml_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'modified_sms_v2.xml')
    
    # Parse XML data
    parser = SMSDataParser(xml_path)
    transactions = parser.parse_xml_to_json()
    
    if not transactions:
        print("Error: No transactions loaded. Please check the XML file.")
        return None
    
    print(f"Successfully loaded {len(transactions)} transactions")
    return transactions


def run_dsa_comparison(transactions):
    """Run the DSA comparison analysis"""
    print("\n" + "=" * 60)
    print("DATA STRUCTURES & ALGORITHMS COMPARISON")
    print("=" * 60)
    
    # Create comparison instance
    comparison = SearchComparison(transactions)
    
    # Generate test IDs (random selection from available IDs)
    available_ids = [t['id'] for t in transactions]
    test_count = min(10, len(available_ids))  # Test with up to 10 IDs
    test_ids = random.sample(available_ids, test_count)
    
    print(f"Testing with {len(test_ids)} transaction IDs: {test_ids}")
    print(f"Running {1000} iterations per test for accuracy\n")
    
    # Run comparison
    results = comparison.compare_search_methods(test_ids, iterations=1000)
    
    # Analyze complexity
    complexity_analysis = comparison.analyze_complexity()
    
    # Display detailed results
    print("\n" + "=" * 60)
    print("DETAILED RESULTS")
    print("=" * 60)
    
    print(f"Test Configuration:")
    print(f"  - Number of transactions: {len(transactions)}")
    print(f"  - Test IDs: {test_ids}")
    print(f"  - Iterations per test: {results['iterations']}")
    
    print(f"\nPerformance Summary:")
    print(f"  - Average Linear Search Time: {results['average_linear_time']:.8f} seconds")
    print(f"  - Average Dictionary Lookup Time: {results['average_dict_time']:.8f} seconds")
    print(f"  - Overall Speedup: {results['overall_speedup']:.2f}x faster")
    
    # Calculate efficiency metrics
    linear_time_ms = results['average_linear_time'] * 1000
    dict_time_ms = results['average_dict_time'] * 1000
    
    print(f"\nTime Comparison (in milliseconds):")
    print(f"  - Linear Search: {linear_time_ms:.4f} ms")
    print(f"  - Dictionary Lookup: {dict_time_ms:.4f} ms")
    print(f"  - Time Difference: {linear_time_ms - dict_time_ms:.4f} ms")
    
    # Memory usage analysis
    print(f"\nMemory Usage Analysis:")
    print(f"  - Original List Size: {len(transactions)} transactions")
    print(f"  - Dictionary Size: {len(comparison.transaction_dict)} entries")
    print(f"  - Memory Overhead: {len(comparison.transaction_dict) * 8} bytes (estimated)")
    
    return results, complexity_analysis


def demonstrate_search_operations(transactions):
    """Demonstrate actual search operations"""
    print("\n" + "=" * 60)
    print("SEARCH OPERATION DEMONSTRATIONS")
    print("=" * 60)
    
    comparison = SearchComparison(transactions)
    
    # Test with a few specific IDs
    test_cases = [1, 5, 10, 15, 20] if len(transactions) >= 20 else [1, 2, 3]
    
    for test_id in test_cases:
        if test_id <= len(transactions):
            print(f"\nSearching for Transaction ID: {test_id}")
            
            # Linear search
            start_time = time.perf_counter()
            linear_result = comparison.linear_search(test_id)
            linear_time = time.perf_counter() - start_time
            
            # Dictionary lookup
            start_time = time.perf_counter()
            dict_result = comparison.dictionary_lookup(test_id)
            dict_time = time.perf_counter() - start_time
            
            print(f"  Linear Search Result: {linear_result is not None}")
            print(f"  Linear Search Time: {linear_time:.8f} seconds")
            print(f"  Dictionary Lookup Result: {dict_result is not None}")
            print(f"  Dictionary Lookup Time: {dict_time:.8f} seconds")
            
            if linear_result and dict_result:
                print(f"  Results Match: {linear_result['id'] == dict_result['id']}")
                print(f"  Speedup: {linear_time / dict_time:.2f}x faster")


def generate_performance_report(results, complexity_analysis):
    """Generate a performance report"""
    print("\n" + "=" * 60)
    print("PERFORMANCE REPORT")
    print("=" * 60)
    
    print("1. ALGORITHM COMPLEXITY ANALYSIS")
    print("-" * 40)
    
    for method, analysis in complexity_analysis.items():
        if isinstance(analysis, dict) and method != 'explanation':
            print(f"\n{method.upper().replace('_', ' ')}:")
            for key, value in analysis.items():
                print(f"  {key.replace('_', ' ').title()}: {value}")
    
    print("\n2. WHY DICTIONARY LOOKUP IS FASTER")
    print("-" * 40)
    explanation = complexity_analysis.get('explanation', {})
    for key, value in explanation.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
    
    print("\n3. RECOMMENDATIONS")
    print("-" * 40)
    print("  - Use Dictionary Lookup when:")
    print("    * Frequent searches by ID are required")
    print("    * Memory is not a constraint")
    print("    * O(1) lookup time is critical")
    print("  - Use Linear Search when:")
    print("    * Memory is limited")
    print("    * Searches are infrequent")
    print("    * Need to search by multiple criteria")
    
    print("\n4. ALTERNATIVE DATA STRUCTURES")
    print("-" * 40)
    print("  - Binary Search Tree (BST):")
    print("    * Time Complexity: O(log n) average case")
    print("    * Space Complexity: O(n)")
    print("    * Good for range queries and sorted data")
    print("  - Hash Table with Chaining:")
    print("    * Time Complexity: O(1) average, O(n) worst case")
    print("    * Space Complexity: O(n)")
    print("    * Better collision handling than simple dict")
    print("  - B-Tree:")
    print("    * Time Complexity: O(log n)")
    print("    * Space Complexity: O(n)")
    print("    * Excellent for large datasets and disk storage")


def save_results_to_file(results, complexity_analysis):
    """Save results to JSON file for further analysis"""
    output_data = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'results': results,
        'complexity_analysis': complexity_analysis,
        'summary': {
            'total_transactions': len(results.get('test_ids', [])),
            'iterations_per_test': results.get('iterations', 0),
            'average_linear_time': results.get('average_linear_time', 0),
            'average_dict_time': results.get('average_dict_time', 0),
            'overall_speedup': results.get('overall_speedup', 0)
        }
    }
    
    output_file = 'dsa_comparison_results.json'
    try:
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        print(f"\nResults saved to: {output_file}")
    except Exception as e:
        print(f"Error saving results: {e}")


def main():
    """Main function to run DSA comparison"""
    print("SMS TRANSACTION DATA STRUCTURES & ALGORITHMS ANALYSIS")
    print("=" * 60)
    
    # Load transaction data
    transactions = load_transaction_data()
    if not transactions:
        return
    
    # Run DSA comparison
    results, complexity_analysis = run_dsa_comparison(transactions)
    
    # Demonstrate search operations
    demonstrate_search_operations(transactions)
    
    # Generate performance report
    generate_performance_report(results, complexity_analysis)
    
    # Save results
    save_results_to_file(results, complexity_analysis)
    
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    print("This analysis demonstrates the efficiency difference between")
    print("linear search (O(n)) and dictionary lookup (O(1)) algorithms")
    print("for searching transaction data by ID.")


if __name__ == "__main__":
    main()
