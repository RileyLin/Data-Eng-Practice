"""
Question: Implement a fixed-size buffer for processing a stream of events.

You need to implement two functions:

1. `process_fixed_buffer_stream(event_item, buffer, buffer_size, totals_engagement, totals_view_seconds, test_users)`:
   - Takes an event item (dictionary) and processes it through a fixed-size buffer
   - When the buffer is full (reaches buffer_size), processes the oldest item
   - Tracks engagement counts and view durations, excluding test users
   - Adds new event to the buffer

2. `flush_fixed_buffer(buffer, totals_engagement, totals_view_seconds, test_users)`:
   - Processes all remaining items in the buffer
   - Updates the totals for engagement and view durations

The buffer processes events that can be:
- Regular engagement events (likes, comments, shares) - count as +1 to engagement total
- View events with a 'view_duration_ms' field - converted to seconds and added to view_seconds total
- Events from test users (user_id in test_users set) should NOT be included in the totals

Event items have this structure:
{
    'user_id': 'user123',
    'event_type': 'like' OR 'view' OR 'comment' OR 'share', 
    'post_id': ['p1'] OR 'p1',
    'view_duration_ms': 5000  # Only present for 'view' events
}

Examples:
    buffer = []
    buffer_size = 3
    totals_engagement = 0
    totals_view_seconds = 0.0
    test_users = {'test_user_reel'}
    
    # Process events
    process_fixed_buffer_stream(
        {'user_id': 'user1', 'event_type': 'like', 'post_id': ['p1']},
        buffer, buffer_size, totals_engagement, totals_view_seconds, test_users)
    # Buffer now has 1 item, no totals change yet
    
    process_fixed_buffer_stream(
        {'user_id': 'user2', 'event_type': 'view', 'post_id': 'p2', 'view_duration_ms': 10000},
        buffer, buffer_size, totals_engagement, totals_view_seconds, test_users)
    # Buffer now has 2 items, no totals change yet
    
    process_fixed_buffer_stream(
        {'user_id': 'user3', 'event_type': 'comment', 'post_id': 'p3'},
        buffer, buffer_size, totals_engagement, totals_view_seconds, test_users)
    # Buffer now has 3 items, no totals change yet
    
    process_fixed_buffer_stream(
        {'user_id': 'user4', 'event_type': 'share', 'post_id': 'p4'},
        buffer, buffer_size, totals_engagement, totals_view_seconds, test_users)
    # Buffer full! Oldest item (like) is processed: totals_engagement = 1
    # Buffer now has 3 items again, with the new item added
    
    # Flush the buffer
    flush_fixed_buffer(buffer, totals_engagement, totals_view_seconds, test_users)
    # All items processed: view (10s), comment (+1), share (+1)
    # Final totals: totals_engagement = 3, totals_view_seconds = 10.0
"""

def process_fixed_buffer_stream(event_item, buffer, buffer_size, totals_engagement, totals_view_seconds, test_users):
    """
    Process a stream item through a fixed-size buffer, updating totals when items are displaced.
    
    Args:
        event_item (dict): The event to process
        buffer (list): The fixed-size buffer (list of dicts, with each dict containing 'data' and 'is_test')
        buffer_size (int): Maximum size of the buffer
        totals_engagement (int): Running count of engagement events (passed by reference)
        totals_view_seconds (float): Running total of view duration in seconds (passed by reference)
        test_users (set): Set of test user IDs to exclude from aggregation
        
    Note: totals_engagement and totals_view_seconds are expected to be mutable objects
    that will be updated in-place (e.g., a list with a single element: [0], [0.0])
    """
    
    if len(buffer)>=buffer_size:
        oldest_item = buffer.pop(0)

        if oldest_item['user_id'] not in test_users:
            if oldest_item['event_type']=='view' and 'view_duration_ms' in oldest_item:

                view_seconds = oldest_item['view_duration_ms']/1000.0
                totals_view_seconds[0]+=view_seconds
            elif oldest_item['event_type'] in ['like','comment','share']:
                totals_engagement[0]+=1
    
    print(f"Engagement count: {totals_engagement}")
    buffer.append(event_item)

def flush_fixed_buffer(buffer, totals_engagement, totals_view_seconds, test_users):
    """
    Process all remaining items in the buffer and update totals.
    
    Args:
        buffer (list): The fixed-size buffer to flush
        totals_engagement (int): Running count of engagement events (passed by reference)
        totals_view_seconds (float): Running total of view duration in seconds (passed by reference)
        test_users (set): Set of test user IDs to exclude from aggregation
    """
    
    buffer_copy = buffer.copy()

    for item in buffer_copy:
        buffer.remove(item)

        if item['user_id'] in test_users:
            continue
        
        if item['event_type']=='view' and 'view_duration_ms' in item:

            view_seconds = item['view_duration_ms']/1000.0

            totals_view_seconds[0] +=view_seconds
        
        elif item['event_type'] in ['like','comment','share']:
            totals_engagement[0] +=1
        



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