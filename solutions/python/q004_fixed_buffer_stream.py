"""
Solution to Question: Implement a fixed-size buffer for processing a stream of events.
"""

def process_fixed_buffer_stream(event_item, buffer, buffer_size, totals_engagement, totals_view_seconds, test_users):
    """
    Process a stream item through a fixed-size buffer, updating totals when items are displaced.
    
    Args:
        event_item (dict): The event to process
        buffer (list): The fixed-size buffer (list of dicts)
        buffer_size (int): Maximum size of the buffer
        totals_engagement (list): Running count of engagement events (passed by reference)
        totals_view_seconds (list): Running total of view duration in seconds (passed by reference)
        test_users (set): Set of test user IDs to exclude from aggregation
    """
    # Check if buffer is full and needs to process the oldest item
    if len(buffer) >= buffer_size:
        oldest_item = buffer.pop(0)  # Remove and get the oldest item
        
        # Process the oldest item if not from test user
        if oldest_item['user_id'] not in test_users:
            if oldest_item['event_type'] == 'view' and 'view_duration_ms' in oldest_item:
                # Convert milliseconds to seconds
                view_seconds = oldest_item['view_duration_ms'] / 1000.0
                totals_view_seconds[0] += view_seconds
            elif oldest_item['event_type'] in ['like', 'comment', 'share']:
                totals_engagement[0] += 1
    
    # Add the new event to the buffer
    buffer.append(event_item)

def flush_fixed_buffer(buffer, totals_engagement, totals_view_seconds, test_users):
    """
    Process all remaining items in the buffer and update totals.
    
    Args:
        buffer (list): The fixed-size buffer to flush
        totals_engagement (list): Running count of engagement events (passed by reference)
        totals_view_seconds (list): Running total of view duration in seconds (passed by reference)
        test_users (set): Set of test user IDs to exclude from aggregation
    """
    # Make a copy of the buffer to iterate through while modifying the original
    buffer_copy = buffer.copy()
    
    # Process all items in the buffer
    for item in buffer_copy:
        # Remove item from buffer
        buffer.remove(item)
        
        # Skip items from test users
        if item['user_id'] in test_users:
            continue
            
        if item['event_type'] == 'view' and 'view_duration_ms' in item:
            # Convert milliseconds to seconds
            view_seconds = item['view_duration_ms'] / 1000.0
            totals_view_seconds[0] += view_seconds
        elif item['event_type'] in ['like', 'comment', 'share']:
            totals_engagement[0] += 1

# Test cases
def test_fixed_buffer_processing():
    # Using lists with single elements to simulate pass-by-reference
    buffer = []
    buffer_size = 3
    totals_engagement = [0]
    totals_view_seconds = [0.0]
    test_users = {'test_user_reel'}
    
    # Test Case 1: Process events until buffer fills and displacement occurs
    process_fixed_buffer_stream(
        {'user_id': 'user1', 'event_type': 'like', 'post_id': ['p1']},
        buffer, buffer_size, totals_engagement, totals_view_seconds, test_users)
    
    process_fixed_buffer_stream(
        {'user_id': 'user2', 'event_type': 'view', 'post_id': 'p2', 'view_duration_ms': 10000},
        buffer, buffer_size, totals_engagement, totals_view_seconds, test_users)
    
    process_fixed_buffer_stream(
        {'user_id': 'user3', 'event_type': 'comment', 'post_id': 'p3'},
        buffer, buffer_size, totals_engagement, totals_view_seconds, test_users)
    
    assert len(buffer) == 3, f"Expected buffer size 3, got {len(buffer)}"
    assert totals_engagement[0] == 0, "No items should be processed yet"
    
    # This should process the oldest item (like from user1)
    process_fixed_buffer_stream(
        {'user_id': 'user4', 'event_type': 'share', 'post_id': 'p4'},
        buffer, buffer_size, totals_engagement, totals_view_seconds, test_users)
    
    assert len(buffer) == 3, f"Expected buffer size 3, got {len(buffer)}"
    assert totals_engagement[0] == 1, f"Expected engagement count 1, got {totals_engagement[0]}"
    
    # Test Case 2: Test user events should not be counted
    process_fixed_buffer_stream(
        {'user_id': 'test_user_reel', 'event_type': 'like', 'post_id': 'p5'},
        buffer, buffer_size, totals_engagement, totals_view_seconds, test_users)
    
    # This should process a view event (from user2)
    process_fixed_buffer_stream(
        {'user_id': 'user6', 'event_type': 'comment', 'post_id': 'p6'},
        buffer, buffer_size, totals_engagement, totals_view_seconds, test_users)
    
    assert totals_view_seconds[0] == 10.0, f"Expected 10.0 view seconds, got {totals_view_seconds[0]}"
    assert totals_engagement[0] == 2, f"Expected engagement count 2, got {totals_engagement[0]}"
    
    # Test Case 3: Flush buffer
    flush_fixed_buffer(buffer, totals_engagement, totals_view_seconds, test_users)
    
    assert len(buffer) == 0, "Buffer should be empty after flush"
    assert totals_engagement[0] == 4, f"Expected final engagement count 4, got {totals_engagement[0]}"
    
    print("All test cases passed!")

if __name__ == "__main__":
    test_fixed_buffer_processing() 