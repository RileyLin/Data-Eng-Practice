"""
Scenario 8: FB Messenger
Question 8.4.1: SQL Generation

Description:
Write a Python function `generate_insert_sql(log_entry, target_table)`
that generates a SQL INSERT statement string based on conditions within the `log_entry` dictionary.
The function should properly escape string values and handle different table structures
based on the source table indicated in the log or by the target_table name itself.

`log_entry` example:
log_entry = {
    'source_table': 'user_messages',
    'timestamp': 1678886400,
    'user_id': 123,
    'message_id': 'msg_abc123',
    'text_content': "Hello there! How are you? I said \'Hi!\'",
    'platform': 'ios'
}

`target_table` could be, for example, 'messages_archive' or 'user_activity'.

Function Logic:
- Determine the columns for the `target_table`.
  (For simplicity, assume fixed schemas for a few known target tables, or infer from `log_entry` keys if generic).
- Extract corresponding values from `log_entry`.
- Properly format values for SQL (e.g., strings quoted, numbers as is).
- Handle SQL string escaping (e.g., single quotes within strings become double single quotes).
- Construct the `INSERT INTO target_table (col1, col2, ...) VALUES (val1, val2, ...);` string.

Example (simplified, actual column mapping would be more robust):
If `target_table` is 'simple_message_log', expected columns might be ('msg_id', 'user', 'content', 'log_time').

`generate_insert_sql(log_entry, 'simple_message_log')` might produce:
`INSERT INTO simple_message_log (msg_id, user_id, text_content, timestamp) VALUES ('msg_abc123', 123, 'Hello there! How are you? I said \'\'Hi!\'\'', 1678886400);`
 (Note: double single quotes for escaping internal single quote in the text).

Considerations:
- Different target tables might require different subsets of fields from `log_entry` or renaming of fields.
- Basic type checking/conversion (e.g., ensuring numbers are not quoted as strings if the DB column is numeric).
- Robust error handling for missing fields or type mismatches is important in a real system.
"""

def escape_sql_string(value: str) -> str:
    """Escapes single quotes in a string for SQL insertion."""
    if value is None:
        return "NULL"
    return "'" + str(value).replace("'", "''") + "'"

def generate_insert_sql(log_entry: dict, target_table: str) -> str:
    """
    Generates a SQL INSERT statement string from a log entry for a target table.

    Args:
        log_entry: A dictionary containing the data to be inserted.
        target_table: The name of the SQL table to insert into.

    Returns:
        A SQL INSERT statement string.
    """
    
    # Define schemas or column mappings for known target tables
    # This is a simplified approach. A more robust system might use a schema registry.
    table_schemas = {
        "user_messages_archive": ["message_id", "user_id", "text_content", "platform", "timestamp"],
        "user_activity_log": ["activity_type", "user_id", "details", "event_timestamp"],
        "generic_event_log": list(log_entry.keys()) # Fallback: use all keys from log_entry
    }

    # Determine columns based on target_table
    if target_table in table_schemas:
        columns = table_schemas[target_table]
        # Remap fields if necessary for specific tables (example for user_activity_log)
        if target_table == "user_activity_log":
            # This requires a more complex mapping logic depending on log_entry structure
            # For this example, let's assume a simple mapping for a hypothetical log_entry for activity
            # This part is highly dependent on the actual structure of log_entry for activity events
            # We will use a simplified direct mapping for now based on hypothetical keys.
            # This example assumes log_entry might have keys like 'action', 'actor_id', 'context', 'time'
            # and we map them to 'activity_type', 'user_id', 'details', 'event_timestamp'
            
            # For the provided log_entry example which is for 'user_messages',
            # inserting into 'user_activity_log' would likely result in missing fields or type errors
            # without a clear transformation rule.
            # Let's make a simple assumption that if source_table is in log_entry, it can be activity_type
            mapped_log_entry = {}
            mapped_log_entry['activity_type'] = log_entry.get('source_table', 'unknown_activity')
            mapped_log_entry['user_id'] = log_entry.get('user_id')
            mapped_log_entry['details'] = log_entry.get('text_content') # Example mapping text to details
            mapped_log_entry['event_timestamp'] = log_entry.get('timestamp')
            current_log_data = mapped_log_entry
        else:
            current_log_data = log_entry
    else:
        # If target_table is not predefined, use all keys from log_entry as columns
        # This might not always be desired but serves as a generic fallback.
        columns = list(log_entry.keys())
        current_log_data = log_entry

    values = []
    valid_columns = []
    for col in columns:
        if col in current_log_data and current_log_data[col] is not None: # Only include columns present in the log
            valid_columns.append(col)
            value = current_log_data[col]
            if isinstance(value, str):
                values.append(escape_sql_string(value))
            elif isinstance(value, (int, float)):
                values.append(str(value))
            elif isinstance(value, bool):
                values.append('TRUE' if value else 'FALSE') # SQL boolean
            else:
                values.append("NULL") # Default for other types or if value was None initially
        elif col in current_log_data and current_log_data[col] is None: # Explicit NULL
             valid_columns.append(col)
             values.append("NULL")
        # If a column from schema is not in current_log_data, it's omitted. 
        # This means the DB table must allow NULLs for such columns or have defaults.

    if not valid_columns:
        # Or raise an error: raise ValueError("No valid columns found for insertion.")
        return f"-- No valid data to insert into {target_table} from log: {log_entry}"

    cols_str = ", ".join([f'`{c}`' for c in valid_columns]) # Use backticks for column names for safety
    vals_str = ", ".join(values)

    return f"INSERT INTO `{target_table}` ({cols_str}) VALUES ({vals_str});"

# Example Usage
if __name__ == "__main__":
    log1 = {
        'source_table': 'user_messages',
        'timestamp': 1678886400,
        'user_id': 123,
        'message_id': 'msg_abc123',
        'text_content': "Hello there! It's a great day, isn't it?",
        'platform': 'ios',
        'is_premium_user': True,
        'message_length': None # Testing None value
    }

    # Test Case 1: Target table 'user_messages_archive'
    sql1 = generate_insert_sql(log1, "user_messages_archive")
    print(f"Log Entry 1: {log1}")
    print(f"Generated SQL 1 (user_messages_archive): {sql1}")
    expected_sql1 = "INSERT INTO `user_messages_archive` (`message_id`, `user_id`, `text_content`, `platform`, `timestamp`) VALUES ('msg_abc123', 123, 'Hello there! It''s a great day, isn''t it?', 'ios', 1678886400);"
    # Note: The schema for user_messages_archive doesn't include is_premium_user or message_length
    # The function correctly omits them if not in the defined schema for that table.
    # To be very precise, let's refine the expected based on strict schema columns:
    cols_for_exp1 = ['message_id', 'user_id', 'text_content', 'platform', 'timestamp']
    vals_for_exp1 = [escape_sql_string(log1['message_id']), str(log1['user_id']), escape_sql_string(log1['text_content']), escape_sql_string(log1['platform']), str(log1['timestamp'])]
    expected_sql1_precise = f"INSERT INTO `user_messages_archive` (`message_id`, `user_id`, `text_content`, `platform`, `timestamp`) VALUES ({', '.join(vals_for_exp1)});"
    assert sql1 == expected_sql1_precise, f"SQL1 Mismatch: \nExpected: {expected_sql1_precise}\nGot:      {sql1}"
    print("Test Case 1 Passed.\\n")

    # Test Case 2: Target table 'user_activity_log' (uses mapping)
    # This test is a bit conceptual as the mapping in the function is simple.
    # A real log for activity might look different.
    log2_activity_source = {
        'source_table': 'login_event', # This will be mapped to 'activity_type'
        'timestamp': 1678887000,
        'user_id': 456,
        'details_field': 'Successful login from web.', # Mapped to 'details' if we adjust mapping logic
        'text_content': 'Login successful for user 456' # current simple mapping will take this for details
    }
    sql2 = generate_insert_sql(log2_activity_source, "user_activity_log")
    print(f"Log Entry 2: {log2_activity_source}")
    print(f"Generated SQL 2 (user_activity_log): {sql2}")
    # Expected based on current simple mapping in generate_insert_sql:
    # activity_type = 'login_event', user_id = 456, details = 'Login successful for user 456', event_timestamp = 1678887000
    expected_sql2 = "INSERT INTO `user_activity_log` (`activity_type`, `user_id`, `details`, `event_timestamp`) VALUES ('login_event', 456, 'Login successful for user 456', 1678887000);"
    assert sql2 == expected_sql2, f"SQL2 Mismatch: \nExpected: {expected_sql2}\nGot:      {sql2}"
    print("Test Case 2 Passed.\\n")

    # Test Case 3: Generic target table (uses all log entry keys)
    log3 = {
        'event_name': 'photo_uploaded',
        'user': 789,
        'file_size_kb': 2048,
        'source_ip': '192.168.1.100',
        'active': False,
        'description': "A 'nice' photo."
    }
    sql3 = generate_insert_sql(log3, "new_generic_events") # "new_generic_events" is not in predefined schemas
    print(f"Log Entry 3: {log3}")
    print(f"Generated SQL 3 (new_generic_events): {sql3}")
    # Order of columns might vary if relying on dict.keys(), so we check for content
    # For a precise test, we should sort keys if the schema is truly dynamic.
    # The function now uses list(log_entry.keys()) so order is preserved from Python 3.7+
    expected_sql3_cols = "`event_name`, `user`, `file_size_kb`, `source_ip`, `active`, `description`"
    expected_sql3_vals = "'photo_uploaded', 789, 2048, '192.168.1.100', FALSE, 'A ''nice'' photo.'"
    expected_sql3 = f"INSERT INTO `new_generic_events` ({expected_sql3_cols}) VALUES ({expected_sql3_vals});"
    assert sql3 == expected_sql3, f"SQL3 Mismatch: \nExpected: {expected_sql3}\nGot:      {sql3}"
    print("Test Case 3 Passed.\\n")
    
    # Test Case 4: Log entry with only a few fields for a table with more columns (expecting NULLs implicitly)
    # The current function only includes fields *present* in the log_entry that are also in the schema (or all if generic)
    # So if schema has `col_c` but log does not, `col_c` is omitted from INSERT.
    # This is different from inserting explicit NULL for schema columns not in log.
    # Let's test with a log that has fewer keys than `user_messages_archive` schema.
    log4_partial = {
        'message_id': 'msg_short1',
        'user_id': 1001,
        'text_content': 'Short.'
        # platform and timestamp are missing
    }
    sql4 = generate_insert_sql(log4_partial, "user_messages_archive")
    print(f"Log Entry 4: {log4_partial}")
    print(f"Generated SQL 4 (user_messages_archive with partial data): {sql4}")
    expected_sql4 = "INSERT INTO `user_messages_archive` (`message_id`, `user_id`, `text_content`) VALUES ('msg_short1', 1001, 'Short.');"
    assert sql4 == expected_sql4, f"SQL4 Mismatch: \nExpected: {expected_sql4}\nGot:      {sql4}"
    print("Test Case 4 Passed.\\n")

    # Test Case 5: Log entry with all values being None or missing for a specific schema
    log5_nones = {
        'message_id': None,
        'user_id': None,
        'text_content': None,
        'platform': None,
        'timestamp': None
    }
    sql5 = generate_insert_sql(log5_nones, "user_messages_archive")
    print(f"Log Entry 5: {log5_nones}")
    print(f"Generated SQL 5 (all NULLs): {sql5}")
    expected_sql5 = "INSERT INTO `user_messages_archive` (`message_id`, `user_id`, `text_content`, `platform`, `timestamp`) VALUES (NULL, NULL, NULL, NULL, NULL);"
    assert sql5 == expected_sql5, f"SQL5 Mismatch: \nExpected: {expected_sql5}\nGot:      {sql5}"
    print("Test Case 5 Passed.\\n")

    print("All q010 tests passed!") 