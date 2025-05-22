"""
Question: Implement the Python function `process_event(event, buffer, totals, test_users)` that:

1. Processes a single engagement event (like, comment, view)
2. Buffers events by session_id in a buffer dictionary
3. Updates aggregate counts for non-internal sessions when a session_end event is received
4. Does not count events from internal test users in the aggregate counts

Args:
    event (dict): An engagement event dictionary with keys:
        - 'session_id': Unique identifier for the user session
        - 'user_id': ID of the user who performed the action
        - 'event_type': Type of event ('like', 'comment', 'view', 'session_end', etc.)
    buffer (dict): Session buffer to store events by session_id
    totals (dict): Running counts of engagement types {'likes': 0, 'comments': 0, 'views': 0}
    test_users (set): Set of internal test user IDs to exclude from aggregation

Example:
    buffer = {}
    totals = {'likes': 0, 'comments': 0, 'views': 0}
    test_users = {'user_test_A', 'user_test_B'}
    
    # Process regular user events
    process_event({'session_id': 's1', 'user_id': 'user1', 'event_type': 'like'}, 
                 buffer, totals, test_users)
    process_event({'session_id': 's1', 'user_id': 'user1', 'event_type': 'view'}, 
                 buffer, totals, test_users)
    process_event({'session_id': 's1', 'user_id': 'user1', 'event_type': 'session_end'}, 
                 buffer, totals, test_users)
    # After processing, totals should be {'likes': 1, 'comments': 0, 'views': 1}
    
    # Process test user events (should not affect totals)
    process_event({'session_id': 's2', 'user_id': 'user_test_A', 'event_type': 'like'}, 
                 buffer, totals, test_users)
    process_event({'session_id': 's2', 'user_id': 'user_test_A', 'event_type': 'session_end'}, 
                 buffer, totals, test_users)
    # Totals should still be {'likes': 1, 'comments': 0, 'views': 1}
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
    
    session_id = event.get('session_id')
    user_id = event.get('user_id')
    event_type = event.get('event_type')


    if session_id not in buffer:
        buffer[session_id]= {'events':[],'users':set()}
    
    buffer[session_id]['events'].append(event)
    buffer[session_id]['users'].add(user_id)

    if event_type == 'session_end':
        is_test_session = any(user in test_users for user in buffer[session_id]['users'])

        if not is_test_session:

            for e in buffer[session_id]['events']:
                e_type = e['event_type']

                if e_type =='like':
                    totals['likes']+=1
                elif e_type =='view':
                    totals['views']+=1
                elif e_type == 'comment':
                    totals['comments']+=1
        del buffer[session_id]



# Test cases
def test_process_event():
    # Setup test data
    buffer = {}
    totals = {'likes': 0, 'comments': 0, 'views': 0}
    test_users = {'user_test_A', 'user_test_B'}
    
    # Test case 1: Regular user session
    process_event({'session_id': 's1', 'user_id': 'user1', 'event_type': 'like'}, 
                 buffer, totals, test_users)
    process_event({'session_id': 's1', 'user_id': 'user1', 'event_type': 'view'}, 
                 buffer, totals, test_users)
    process_event({'session_id': 's1', 'user_id': 'user1', 'event_type': 'session_end'}, 
                 buffer, totals, test_users)
    
    assert totals['likes'] == 1, f"Expected 1 like, but got {totals['likes']}"
    assert totals['views'] == 1, f"Expected 1 view, but got {totals['views']}"
    assert totals['comments'] == 0, f"Expected 0 comments, but got {totals['comments']}"
    assert 's1' not in buffer, "Session should be removed from buffer after session_end"
    
    # Test case 2: Internal test user session (should not affect totals)
    process_event({'session_id': 's2', 'user_id': 'user_test_A', 'event_type': 'like'}, 
                 buffer, totals, test_users)
    process_event({'session_id': 's2', 'user_id': 'user_test_A', 'event_type': 'session_end'}, 
                 buffer, totals, test_users)
    
    assert totals['likes'] == 1, "Test user likes should not affect totals"
    
    # Test case 3: Mixed session (regular user event + test user event = internal session)
    process_event({'session_id': 's3', 'user_id': 'user2', 'event_type': 'comment'}, 
                 buffer, totals, test_users)
    process_event({'session_id': 's3', 'user_id': 'user_test_B', 'event_type': 'like'}, 
                 buffer, totals, test_users)
    process_event({'session_id': 's3', 'user_id': 'user2', 'event_type': 'session_end'}, 
                 buffer, totals, test_users)
    
    assert totals['comments'] == 0, "Comments from mixed sessions should not be counted"
    
    print("All test cases passed!")

if __name__ == "__main__":
    test_process_event() 