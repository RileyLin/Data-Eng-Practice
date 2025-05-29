"""
Question: Write a Python function `generate_insert_sql(log_entry, target_table)` that takes:
1. A log entry (dictionary)
2. A target table name (string)

The function should generate and return a SQL INSERT statement string based on conditions 
within the log_entry dictionary. Specifically:

- If log_entry['table'] == 'A', create an INSERT statement for columns 'col1_from_A' and 'col2_from_A'
  with values from log_entry['col1'] and log_entry['col2']
  
- If log_entry['table'] == 'B', create an INSERT statement for columns 'col3_from_B' and 'col4_from_B'
  with values from log_entry['col3'] and log_entry['col4']

- If source table is unknown or required column values are missing, return None

- String values should be properly escaped (replace single quotes with two single quotes)
- Assume numeric values don't need special handling

WARNING: This is for demonstration purposes only - in production code, you should
use parameterized queries to prevent SQL injection vulnerabilities.

Example Input:
log_entry_A = {'col1': "value'1", 'col2': 123, 'table': 'A'}
target_table = "MyTargetTable"

Expected Output: 
"INSERT INTO MyTargetTable (col1_from_A, col2_from_A) VALUES ('value''1', 123);"

Example Input:
log_entry_B = {'col3': 'value3', 'col4': 456.7, 'table': 'B'}
target_table = "MyTargetTable"

Expected Output:
"INSERT INTO MyTargetTable (col3_from_B, col4_from_B) VALUES ('value3', 456.7);"
"""

def generate_insert_sql(log_entry, target_table):
    """
    Generate a SQL INSERT statement string based on the source table in log_entry.
    
    Args:
        log_entry (dict): A dictionary containing the log data with a 'table' field
                         and corresponding column values.
        target_table (str): The name of the target table for the INSERT statement.
        
    Returns:
        str or None: A SQL INSERT statement string if valid input,
                    None if source table is unknown or required values are missing.
    """
    #
    if not log_entry or not target_table: 
        return None 
    
    if 'table' not in log_entry or 'col1' not in log_entry:
        return None
    
    log_copy = log_entry.copy()
    table_name = log_entry['table']
    del log_copy['table']

    for col in log_copy:
        

# Test cases
def test_generate_insert_sql():
    # Test case 1: Table A with normal values
    log_entry_A = {'col1': 'value1', 'col2': 123, 'table': 'A'}
    result_A = generate_insert_sql(log_entry_A, 'MyTargetTable')
    expected_A = "INSERT INTO MyTargetTable (col1_from_A, col2_from_A) VALUES ('value1', 123);"
    assert result_A == expected_A, f"Expected: {expected_A}, Got: {result_A}"
    
    # Test case 2: Table A with string containing a single quote
    log_entry_A2 = {'col1': "value'1", 'col2': 123, 'table': 'A'}
    result_A2 = generate_insert_sql(log_entry_A2, 'MyTargetTable')
    expected_A2 = "INSERT INTO MyTargetTable (col1_from_A, col2_from_A) VALUES ('value''1', 123);"
    assert result_A2 == expected_A2, f"Expected: {expected_A2}, Got: {result_A2}"
    
    # Test case 3: Table B
    log_entry_B = {'col3': 'value3', 'col4': 456.7, 'table': 'B'}
    result_B = generate_insert_sql(log_entry_B, 'MyTargetTable')
    expected_B = "INSERT INTO MyTargetTable (col3_from_B, col4_from_B) VALUES ('value3', 456.7);"
    assert result_B == expected_B, f"Expected: {expected_B}, Got: {result_B}"
    
    # Test case 4: Unknown table
    log_entry_unknown = {'col1': 'value1', 'col2': 123, 'table': 'C'}
    result_unknown = generate_insert_sql(log_entry_unknown, 'MyTargetTable')
    assert result_unknown is None, f"Expected None, Got: {result_unknown}"
    
    # Test case 5: Missing required values
    log_entry_missing = {'col1': 'value1', 'table': 'A'}  # Missing col2
    result_missing = generate_insert_sql(log_entry_missing, 'MyTargetTable')
    assert result_missing is None, f"Expected None, Got: {result_missing}"
    
    print("All test cases passed!")

if __name__ == "__main__":
    test_generate_insert_sql() 