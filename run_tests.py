#!/usr/bin/env python3
"""
Run all Python tests in the repository.

This script discovers and runs all tests in the tests/ directory.
"""

import unittest
import os
import sys

def run_all_tests():
    """Discover and run all tests in the tests/ directory."""
    # Add the src directory to the Python path
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
    
    # Discover and run all tests
    test_loader = unittest.TestLoader()
    start_dir = 'tests'
    test_suite = test_loader.discover(start_dir, pattern='test_*.py')
    
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # Return number of failures and errors as exit code
    return len(result.failures) + len(result.errors)

def run_specific_test(test_file):
    """Run a specific test file."""
    # Add the src directory to the Python path
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
    
    # Build the module name
    if test_file.endswith('.py'):
        test_file = test_file[:-3]
    
    if test_file.startswith('tests/'):
        module_name = test_file.replace('/', '.')
    elif test_file.startswith('tests\\'):
        module_name = test_file.replace('\\', '.')
    else:
        module_name = 'tests.' + test_file
    
    # Import the module and run the tests
    test_suite = unittest.defaultTestLoader.loadTestsFromName(module_name)
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # Return number of failures and errors as exit code
    return len(result.failures) + len(result.errors)

def print_usage():
    """Print usage information."""
    print("Usage:")
    print("  python run_tests.py            # Run all tests")
    print("  python run_tests.py <test_file> # Run a specific test file")
    print("Examples:")
    print("  python run_tests.py                          # Run all tests")
    print("  python run_tests.py tests/python/test_ride_overlapping.py  # Run specific test")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help']:
            print_usage()
            sys.exit(0)
        
        # Run specific test file
        exit_code = run_specific_test(sys.argv[1])
    else:
        # Run all tests
        exit_code = run_all_tests()
    
    sys.exit(exit_code) 