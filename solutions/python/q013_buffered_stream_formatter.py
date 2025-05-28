"""
Solution to Question 13: Buffered Stream Data Formatter

This solution implements a buffered stream processor that:
1. Collects data records in a buffer until it reaches the specified size
2. Processes and formats the buffered data when full
3. Handles remaining data after the main stream is exhausted
4. Gracefully handles missing fields and formatting errors

Key implementation details:
- Uses a simple list as the buffer
- Processes data in batches for efficiency
- Handles edge cases like empty streams and oversized buffers
- Provides error handling for missing template fields

DATA STRUCTURE EXAMPLES:

Input: stream_data (List[Dict])
- Structure: [{'field1': value1, 'field2': value2, ...}, ...]
- Each dictionary represents one data record in the stream

Example stream records:
- User activity: {'user_id': 'u123', 'action': 'like', 'post_id': 'p456', 'timestamp': 1640995200}
- News article: {'title': 'Breaking News', 'author': 'John Doe', 'views': 1500, 'category': 'Politics'}
- Product sale: {'product_name': 'Laptop', 'price': 999.99, 'quantity': 2, 'customer': 'Alice'}

Input: buffer_size (int)
- Maximum number of records to collect before processing/printing
- Example: 3

Input: format_template (str)
- String template for formatting each record
- Uses {field_name} placeholders for dictionary keys
- Example: "User {user_id} performed {action} on post {post_id} at {timestamp}"

PROCESSING FLOW EXAMPLE:

Stream data:
[
    {'user_id': 'u001', 'action': 'like', 'post_id': 'p100'},
    {'user_id': 'u002', 'action': 'comment', 'post_id': 'p101'},
    {'user_id': 'u003', 'action': 'share', 'post_id': 'p102'},
    {'user_id': 'u004', 'action': 'view', 'post_id': 'p103'},
    {'user_id': 'u005', 'action': 'like', 'post_id': 'p104'}
]

Buffer size: 3
Format template: "User {user_id} performed {action} on {post_id}"

Processing steps:
1. Buffer fills with first 3 records
2. Print batch 1:
   - "User u001 performed like on p100"
   - "User u002 performed comment on p101"
   - "User u003 performed share on p102"
3. Buffer fills with next 2 records (remaining data)
4. Print batch 2:
   - "User u004 performed view on p103"
   - "User u005 performed like on p104"
"""

def process_buffered_stream(stream_data, buffer_size, format_template):
    """
    Process a stream of data using a buffer, formatting and printing when buffer is full.
    
    Args:
        stream_data (List[Dict]): List of dictionaries representing stream records
        buffer_size (int): Maximum number of records to buffer before processing
        format_template (str): String template for formatting records with {field} placeholders
        
    Returns:
        None (prints formatted output)
    """
    # Input validation
    if not stream_data:
        print("No data to process.")
        return
    
    if buffer_size <= 0:
        print("Buffer size must be positive.")
        return
    
    # Initialize buffer
    buffer = []
    batch_number = 1
    
    # Process each record in the stream
    for record in stream_data:
        # Add record to buffer
        buffer.append(record)
        
        # Check if buffer is full
        if len(buffer) >= buffer_size:
            # Process and print the buffer
            _process_buffer(buffer, format_template, batch_number)
            batch_number += 1
            # Clear buffer for next batch
            buffer.clear()
    
    # Handle any remaining data in buffer
    if buffer:
        _process_buffer(buffer, format_template, batch_number)

def _process_buffer(buffer, format_template, batch_number):
    """
    Helper function to process and print a buffer of records.
    
    Args:
        buffer (List[Dict]): Buffer containing records to process
        format_template (str): String template for formatting
        batch_number (int): Current batch number for display
    """
    print(f"--- Batch {batch_number} ({len(buffer)} records) ---")
    
    for i, record in enumerate(buffer, 1):
        try:
            # Format the record using the template
            formatted_output = format_template.format(**record)
            print(f"{i}. {formatted_output}")
        except KeyError as e:
            # Handle missing fields gracefully
            print(f"{i}. [ERROR] Missing field {e} in record: {record}")
        except Exception as e:
            # Handle other formatting errors
            print(f"{i}. [ERROR] Formatting error: {e}")
    
    print()  # Add blank line after each batch

# Enhanced version with additional features
def process_buffered_stream_enhanced(stream_data, buffer_size, format_template, 
                                   skip_errors=True, show_batch_headers=True):
    """
    Enhanced version with additional configuration options.
    
    Args:
        stream_data (List[Dict]): List of dictionaries representing stream records
        buffer_size (int): Maximum number of records to buffer before processing
        format_template (str): String template for formatting records
        skip_errors (bool): Whether to skip records with formatting errors
        show_batch_headers (bool): Whether to show batch headers
        
    Returns:
        Dict: Statistics about processing (total_records, successful, errors)
    """
    if not stream_data:
        print("No data to process.")
        return {'total_records': 0, 'successful': 0, 'errors': 0}
    
    if buffer_size <= 0:
        print("Buffer size must be positive.")
        return {'total_records': 0, 'successful': 0, 'errors': 0}
    
    buffer = []
    batch_number = 1
    stats = {'total_records': len(stream_data), 'successful': 0, 'errors': 0}
    
    for record in stream_data:
        buffer.append(record)
        
        if len(buffer) >= buffer_size:
            batch_stats = _process_buffer_enhanced(
                buffer, format_template, batch_number, skip_errors, show_batch_headers
            )
            stats['successful'] += batch_stats['successful']
            stats['errors'] += batch_stats['errors']
            batch_number += 1
            buffer.clear()
    
    # Handle remaining data
    if buffer:
        batch_stats = _process_buffer_enhanced(
            buffer, format_template, batch_number, skip_errors, show_batch_headers
        )
        stats['successful'] += batch_stats['successful']
        stats['errors'] += batch_stats['errors']
    
    return stats

def _process_buffer_enhanced(buffer, format_template, batch_number, 
                           skip_errors, show_batch_headers):
    """
    Enhanced helper function with error handling and statistics.
    """
    stats = {'successful': 0, 'errors': 0}
    
    if show_batch_headers:
        print(f"--- Batch {batch_number} ({len(buffer)} records) ---")
    
    for i, record in enumerate(buffer, 1):
        try:
            formatted_output = format_template.format(**record)
            print(f"{i}. {formatted_output}")
            stats['successful'] += 1
        except KeyError as e:
            stats['errors'] += 1
            if not skip_errors:
                print(f"{i}. [ERROR] Missing field {e} in record: {record}")
        except Exception as e:
            stats['errors'] += 1
            if not skip_errors:
                print(f"{i}. [ERROR] Formatting error: {e}")
    
    if show_batch_headers:
        print()
    
    return stats

# Test cases
def test_process_buffered_stream():
    # Test case 1: Basic user activity stream
    user_stream = [
        {'user_id': 'u001', 'action': 'like', 'post_id': 'p100'},
        {'user_id': 'u002', 'action': 'comment', 'post_id': 'p101'},
        {'user_id': 'u003', 'action': 'share', 'post_id': 'p102'},
        {'user_id': 'u004', 'action': 'view', 'post_id': 'p103'},
        {'user_id': 'u005', 'action': 'like', 'post_id': 'p104'}
    ]
    
    print("Test Case 1: User Activity Stream (buffer size 3)")
    print("=" * 50)
    process_buffered_stream(
        user_stream, 
        3, 
        "User {user_id} performed {action} on {post_id}"
    )
    
    # Test case 2: News articles with different formatting
    news_stream = [
        {'title': 'Breaking News', 'author': 'John Doe', 'views': 1500, 'category': 'Politics'},
        {'title': 'Tech Update', 'author': 'Jane Smith', 'views': 800, 'category': 'Technology'},
        {'title': 'Sports Highlight', 'author': 'Mike Johnson', 'views': 2200, 'category': 'Sports'}
    ]
    
    print("Test Case 2: News Articles (buffer size 2)")
    print("=" * 50)
    process_buffered_stream(
        news_stream,
        2,
        "📰 '{title}' by {author} ({views} views) - {category}"
    )
    
    # Test case 3: Sales data with number formatting
    sales_stream = [
        {'product_name': 'Laptop', 'price': 999.99, 'quantity': 2, 'customer': 'Alice'},
        {'product_name': 'Mouse', 'price': 25.50, 'quantity': 1, 'customer': 'Bob'},
        {'product_name': 'Keyboard', 'price': 75.00, 'quantity': 3, 'customer': 'Charlie'},
        {'product_name': 'Monitor', 'price': 299.99, 'quantity': 1, 'customer': 'Diana'}
    ]
    
    print("Test Case 3: Sales Data (buffer size 2)")
    print("=" * 50)
    process_buffered_stream(
        sales_stream,
        2,
        "💰 {quantity}x {product_name} for ${price} to {customer}"
    )
    
    # Test case 4: Edge case - buffer larger than data
    small_stream = [
        {'name': 'Alice', 'score': 95},
        {'name': 'Bob', 'score': 87}
    ]
    
    print("Test Case 4: Small Stream (buffer size 5)")
    print("=" * 50)
    process_buffered_stream(
        small_stream,
        5,
        "Student {name} scored {score} points"
    )
    
    # Test case 5: Buffer size of 1 (immediate processing)
    immediate_stream = [
        {'event': 'login', 'user': 'admin'},
        {'event': 'logout', 'user': 'admin'}
    ]
    
    print("Test Case 5: Immediate Processing (buffer size 1)")
    print("=" * 50)
    process_buffered_stream(
        immediate_stream,
        1,
        "Event: {event} by {user}"
    )
    
    # Test case 6: Error handling - missing fields
    error_stream = [
        {'user_id': 'u001', 'action': 'like'},  # Missing post_id
        {'user_id': 'u002', 'post_id': 'p101'},  # Missing action
        {'user_id': 'u003', 'action': 'share', 'post_id': 'p102'}  # Complete record
    ]
    
    print("Test Case 6: Error Handling (missing fields)")
    print("=" * 50)
    process_buffered_stream(
        error_stream,
        2,
        "User {user_id} performed {action} on {post_id}"
    )
    
    # Test case 7: Enhanced version with statistics
    print("Test Case 7: Enhanced Version with Statistics")
    print("=" * 50)
    stats = process_buffered_stream_enhanced(
        error_stream,
        2,
        "User {user_id} performed {action} on {post_id}",
        skip_errors=False,
        show_batch_headers=True
    )
    print(f"Processing Statistics: {stats}")

if __name__ == "__main__":
    test_process_buffered_stream() 