#!/usr/bin/env python3
"""
JSON File Comparison Tool

This script compares two JSON files and displays the differences between them.
"""

import json
import sys
import argparse
from typing import Any, Dict, List, Set, Tuple


def load_json_file(filepath: str) -> Any:
    """Load and parse a JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{filepath}': {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading '{filepath}': {e}", file=sys.stderr)
        sys.exit(1)


def compare_values(val1: Any, val2: Any, path: str = "") -> List[str]:
    """
    Recursively compare two values and return a list of differences.
    
    Args:
        val1: First value to compare
        val2: Second value to compare
        path: Current path in the JSON structure (for reporting)
    
    Returns:
        List of difference descriptions
    """
    differences = []
    
    # If types are different
    if type(val1) != type(val2):
        differences.append(f"  {path}: Type mismatch - {type(val1).__name__} vs {type(val2).__name__}")
        differences.append(f"    File 1: {json.dumps(val1)}")
        differences.append(f"    File 2: {json.dumps(val2)}")
        return differences
    
    # Compare dictionaries
    if isinstance(val1, dict):
        keys1 = set(val1.keys())
        keys2 = set(val2.keys())
        
        # Keys only in first dict
        only_in_1 = keys1 - keys2
        for key in sorted(only_in_1):
            differences.append(f"  {path}.{key}: Only in File 1")
            differences.append(f"    Value: {json.dumps(val1[key])}")
        
        # Keys only in second dict
        only_in_2 = keys2 - keys1
        for key in sorted(only_in_2):
            differences.append(f"  {path}.{key}: Only in File 2")
            differences.append(f"    Value: {json.dumps(val2[key])}")
        
        # Compare common keys
        common_keys = keys1 & keys2
        for key in sorted(common_keys):
            new_path = f"{path}.{key}" if path else key
            differences.extend(compare_values(val1[key], val2[key], new_path))
    
    # Compare lists
    elif isinstance(val1, list):
        if len(val1) != len(val2):
            differences.append(f"  {path}: List length differs - {len(val1)} vs {len(val2)}")
        
        # Compare elements at same indices
        for i in range(min(len(val1), len(val2))):
            new_path = f"{path}[{i}]"
            differences.extend(compare_values(val1[i], val2[i], new_path))
        
        # Show extra elements
        if len(val1) > len(val2):
            for i in range(len(val2), len(val1)):
                differences.append(f"  {path}[{i}]: Extra element in File 1")
                differences.append(f"    Value: {json.dumps(val1[i])}")
        elif len(val2) > len(val1):
            for i in range(len(val1), len(val2)):
                differences.append(f"  {path}[{i}]: Extra element in File 2")
                differences.append(f"    Value: {json.dumps(val2[i])}")
    
    # Compare primitive values
    else:
        if val1 != val2:
            differences.append(f"  {path}: Value differs")
            differences.append(f"    File 1: {json.dumps(val1)}")
            differences.append(f"    File 2: {json.dumps(val2)}")
    
    return differences


def compare_json_files(file1: str, file2: str) -> None:
    """
    Compare two JSON files and print the differences.
    
    Args:
        file1: Path to the first JSON file
        file2: Path to the second JSON file
    """
    print(f"Comparing JSON files:")
    print(f"  File 1: {file1}")
    print(f"  File 2: {file2}")
    print()
    
    # Load both JSON files
    data1 = load_json_file(file1)
    data2 = load_json_file(file2)
    
    # Compare the data
    differences = compare_values(data1, data2)
    
    # Display results
    if not differences:
        print("✓ The JSON files are identical!")
    else:
        print(f"✗ Found {len(differences)} difference(s):")
        print()
        for diff in differences:
            print(diff)
    
    print()


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Compare two JSON files and display their differences.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s file1.json file2.json
  %(prog)s data/old.json data/new.json
        '''
    )
    
    parser.add_argument('file1', help='First JSON file to compare')
    parser.add_argument('file2', help='Second JSON file to compare')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    
    args = parser.parse_args()
    
    compare_json_files(args.file1, args.file2)


if __name__ == '__main__':
    main()
