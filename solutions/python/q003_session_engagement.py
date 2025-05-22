"""
Solution to Question about session engagement processing
"""

def process_event(event, buffer, totals, test_users):
    """
    Process a single engagement event, buffer it by session_id, and update 
    aggregate counts for non-internal sessions upon session_end.
    
    Args:
        event (dict): An engagement event dictionary
        buffer (dict): Session buffer to store events by session_id 
        totals (dict): Running counts of engagement types
        test_users (set): Set of internal test user IDs to exclude
        
    Returns:
        None (updates buffer and totals in-place)
    """
    session_id = event['session_id']
    user_id = event['user_id']
    event_type = event['event_type']
    
    # Initialize session in buffer if not already present
    if session_id not in buffer:
        buffer[session_id] = {
            'events': [],
            'users': set()
        }
    
    # Add event to session buffer
    buffer[session_id]['events'].append(event)
    buffer[session_id]['users'].add(user_id)
    
    # If session_end event received, process the session
    if event_type == 'session_end':
        # Check if any user in this session is a test user
        is_test_session = any(user in test_users for user in buffer[session_id]['users'])
        
        # Only update totals if not a test session
        if not is_test_session:
            # Count events by type
            for e in buffer[session_id]['events']:
                e_type = e['event_type']
                # Only count event types that are in the totals dictionary
                if e_type in totals:
                    totals[e_type] += 1
        
        # Remove session from buffer after processing
        del buffer[session_id]

# Test cases
def test_process_event():
    # Setup test data
    buffer = {}
    totals = {'like': 0, 'comment': 0, 'view': 0}  # Note: the keys match event_type exactly
    test_users = {'user_test_A', 'user_test_B'}
    
    # Test case 1: Regular user session
    process_event({'session_id': 's1', 'user_id': 'user1', 'event_type': 'like'}, 
                 buffer, totals, test_users)
    process_event({'session_id': 's1', 'user_id': 'user1', 'event_type': 'view'}, 
                 buffer, totals, test_users)
    process_event({'session_id': 's1', 'user_id': 'user1', 'event_type': 'session_end'}, 
                 buffer, totals, test_users)
    
    assert totals['like'] == 1, f"Expected 1 like, but got {totals['like']}"
    assert totals['view'] == 1, f"Expected 1 view, but got {totals['view']}"
    assert totals['comment'] == 0, f"Expected 0 comments, but got {totals['comment']}"
    assert 's1' not in buffer, "Session should be removed from buffer after session_end"
    
    # Test case 2: Internal test user session (should not affect totals)
    process_event({'session_id': 's2', 'user_id': 'user_test_A', 'event_type': 'like'}, 
                 buffer, totals, test_users)
    process_event({'session_id': 's2', 'user_id': 'user_test_A', 'event_type': 'session_end'}, 
                 buffer, totals, test_users)
    
    assert totals['like'] == 1, "Test user likes should not affect totals"
    
    # Test case 3: Mixed session (regular user event + test user event = internal session)
    process_event({'session_id': 's3', 'user_id': 'user2', 'event_type': 'comment'}, 
                 buffer, totals, test_users)
    process_event({'session_id': 's3', 'user_id': 'user_test_B', 'event_type': 'like'}, 
                 buffer, totals, test_users)
    process_event({'session_id': 's3', 'user_id': 'user2', 'event_type': 'session_end'}, 
                 buffer, totals, test_users)
    
    assert totals['comment'] == 0, "Comments from mixed sessions should not be counted"
    
    print("All test cases passed!")

if __name__ == "__main__":
    test_process_event() 