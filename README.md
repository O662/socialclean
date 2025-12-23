# socialclean

A simple JSON file comparison tool that helps you identify differences between two JSON files.

## Features

- Compare two JSON files and identify differences
- Detailed difference reporting showing:
  - Keys that exist in one file but not the other
  - Value differences with before/after values
  - Type mismatches
  - Nested object and array comparisons
  - List length differences
- Easy-to-read output format
- Command-line interface

## Installation

No installation required! Just ensure you have Python 3.6 or higher installed.

```bash
# Check Python version
python3 --version
```

## Usage

### Basic Usage

```bash
python3 compare_json.py <file1.json> <file2.json>
```

### Examples

Compare two different JSON files:
```bash
python3 compare_json.py examples/file1.json examples/file2.json
```

Compare identical JSON files:
```bash
python3 compare_json.py examples/file1.json examples/identical.json
```

### Making the script executable (optional)

On Linux/macOS, you can make the script executable:
```bash
chmod +x compare_json.py
./compare_json.py examples/file1.json examples/file2.json
```

## Example Output

When comparing two different files:
```
Comparing JSON files:
  File 1: examples/file1.json
  File 2: examples/file2.json

✗ Found differences:

  age: Value differs
    File 1: 30
    File 2: 31
  address.city: Value differs
    File 1: "Springfield"
    File 2: "Chicago"
  address.country: Only in File 2
    Value: "USA"
  address.zip: Value differs
    File 1: "62701"
    File 2: "60601"
  hobbies[1]: Value differs
    File 1: "gaming"
    File 2: "cooking"
```

When files are identical:
```
Comparing JSON files:
  File 1: examples/file1.json
  File 2: examples/identical.json

✓ The JSON files are identical!
```

## Sample Files

The `examples/` directory contains sample JSON files for testing:
- `file1.json` - Sample JSON file 1
- `file2.json` - Sample JSON file 2 (with differences)
- `identical.json` - Identical copy of file1.json

## How It Works

The tool performs a deep comparison of JSON structures:
1. Loads and validates both JSON files
2. Recursively compares all keys, values, and nested structures
3. Identifies differences at any level of nesting
4. Reports differences in an easy-to-understand format

## Error Handling

The tool handles common errors gracefully:
- File not found errors
- Invalid JSON syntax
- Type mismatches
- Encoding issues

## Requirements

- Python 3.6 or higher (uses standard library only, no external dependencies)

## License

This project is open source and available under the MIT License.