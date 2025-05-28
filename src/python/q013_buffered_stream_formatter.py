"""
Question 13: Buffered Stream Data Formatter

Write a Python function `process_buffered_stream(stream_data, buffer_size, format_template)` that:

1. Takes a stream of data (list of dictionaries) as input
2. Uses a buffer of specified size to collect data before processing
3. When the buffer is full, formats and prints the buffered data according to a template
4. Continues until all stream data is processed
5. Handles any remaining data in the buffer at the end

The function should process data in batches and format the output using string templates.

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

ADVANCED FORMATTING EXAMPLES:

Example 1 - News articles:
format_template = "📰 '{title}' by {author} ({views} views) - {category}"
Expected output: "📰 'Breaking News' by John Doe (1500 views) - Politics"

Example 2 - Sales data:
format_template = "💰 {quantity}x {product_name} sold for ${price:.2f} to {customer}"
Expected output: "💰 2x Laptop sold for $999.99 to Alice"

Example 3 - System logs:
format_template = "[{level}] {timestamp}: {message} (module: {module})"
Expected output: "[ERROR] 1640995200: Database connection failed (module: auth)"

EDGE CASES TO HANDLE:

1. Stream data smaller than buffer size
2. Empty stream data
3. Missing fields in some records (use default values or skip)
4. Buffer size of 1 (immediate processing)
5. Invalid format template (missing placeholders)

IMPLEMENTATION REQUIREMENTS:

- Process data in batches when buffer is full
- Handle remaining data after main stream is processed
- Format each record according to the template
- Print formatted output for each batch
- Handle missing fields gracefully (skip record or use defaults)
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
    
    if not stream_data or buffer_size<=0:
        return

    buffer = []

    for data in stream_data: 
        buffer.append(data)

        if len(buffer)>=3:
            buffer_copy = buffer
            for d in buffer_copy: 
                formatted_output = format_template.format(**d)

                print(formatted_output)

            buffer.clear()
    
    if len(buffer)>0:
        buffer_copy = buffer
        for d in buffer_copy: 
            formatted_output = format_template.format(**d)

            print(formatted_output)

        buffer.clear()

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
    
    print("\nTest Case 2: News Articles (buffer size 2)")
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
    
    print("\nTest Case 3: Sales Data (buffer size 2)")
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
    
    print("\nTest Case 4: Small Stream (buffer size 5)")
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
    
    print("\nTest Case 5: Immediate Processing (buffer size 1)")
    print("=" * 50)
    process_buffered_stream(
        immediate_stream,
        1,
        "Event: {event} by {user}"
    )

if __name__ == "__main__":
    test_process_buffered_stream() 