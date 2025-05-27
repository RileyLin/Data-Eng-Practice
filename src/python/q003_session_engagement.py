"""
Question: Implement the Python function `process_event(event, buffer, totals, test_users)` that:

1. Processes a single engagement event (like, comment, view)
2. Buffers events by session_id in a buffer dictionary
3. Updates aggregate counts for non-internal sessions when a session_end event is received
4. Does not count events from internal test users in the aggregate counts

DATA STRUCTURE EXAMPLES:

Input: event (dict)
- Keys: 'session_id', 'user_id', 'event_type'
- Example: {'session_id': 's1', 'user_id': 'user1', 'event_type': 'like'}

Input: buffer (dict)
- Structure: {session_id: {'events': [event1, event2, ...], 'users': {user1, user2, ...}}}
- Example: {'s1': {'events': [{'session_id': 's1', 'user_id': 'user1', 'event_type': 'like'}], 'users': {'user1'}}}

Input: totals (dict)
- Structure: {event_type: count}
- Example: {'likes': 5, 'comments': 3, 'views': 10}

Input: test_users (set)
- Structure: {user_id1, user_id2, ...}
- Example: {'user_test_A', 'user_test_B', 'internal_user_123'}

Example Scenario 1 - Regular user session:
Events: [
    {'session_id': 's1', 'user_id': 'user1', 'event_type': 'like'},
    {'session_id': 's1', 'user_id': 'user1', 'event_type': 'view'},
    {'session_id': 's1', 'user_id': 'user1', 'event_type': 'session_end'}
]
Result: totals updated with +1 like, +1 view

Example Scenario 2 - Test user session (ignored):
Events: [
    {'session_id': 's2', 'user_id': 'user_test_A', 'event_type': 'like'},
    {'session_id': 's2', 'user_id': 'user_test_A', 'event_type': 'session_end'}
]
Result: totals unchanged (test user session ignored)

Example Scenario 3 - Mixed session (has test user, so entire session ignored):
Events: [
    {'session_id': 's3', 'user_id': 'user2', 'event_type': 'comment'},
    {'session_id': 's3', 'user_id': 'user_test_B', 'event_type': 'like'},
    {'session_id': 's3', 'user_id': 'user2', 'event_type': 'session_end'}
]
Result: totals unchanged (session contains test user, so entire session ignored)

Buffer Evolution Example:
Initial: buffer = {}
After event 1: buffer = {'s1': {'events': [event1], 'users': {'user1'}}}
After event 2: buffer = {'s1': {'events': [event1, event2], 'users': {'user1'}}}
After session_end: buffer = {} (session processed and removed)
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
        buffer[session_id]={'event':[],'user': set()}

    buffer[session_id]['event'].append(event)
    buffer[session_id]['user'].add(user_id)
    if event_type == 'session_end':
        is_test_session = any(user in test_users for user in buffer[session_id]['user'])
        if not is_test_session:
            for e in buffer[session_id]['event']:
                e_user_id = e['user_id']
                e_event_type = e['event_type']

                if e_event_type in totals:
                    totals[e_event_type]+=1
            
        
        del buffer[session_id]
            

# Test cases
def test_process_event():
    # Setup test data
    buffer = {}
    totals = {'likes': 0, 'comments': 0, 'views': 0}
    test_users = {'user_test_A', 'user_test_B'}
    
    # Test case 1: Regular user session
    process_event({'session_id': 's1', 'user_id': 'user1', 'event_type': 'likes'}, 
                 buffer, totals, test_users)
    process_event({'session_id': 's1', 'user_id': 'user1', 'event_type': 'views'}, 
                 buffer, totals, test_users)
    process_event({'session_id': 's1', 'user_id': 'user1', 'event_type': 'session_end'}, 
                 buffer, totals, test_users)
    
    assert totals['likes'] == 1, f"Expected 1 like, but got {totals['likes']}"
    assert totals['views'] == 1, f"Expected 1 view, but got {totals['views']}"
    assert totals['comments'] == 0, f"Expected 0 comments, but got {totals['comments']}"
    assert 's1' not in buffer, "Session should be removed from buffer after session_end"
    
    # Test case 2: Internal test user session (should not affect totals)
    process_event({'session_id': 's2', 'user_id': 'user_test_A', 'event_type': 'likes'}, 
                 buffer, totals, test_users)
    process_event({'session_id': 's2', 'user_id': 'user_test_A', 'event_type': 'session_end'}, 
                 buffer, totals, test_users)
    
    assert totals['likes'] == 1, "Test user likes should not affect totals"
    
    # Test case 3: Mixed session (regular user event + test user event = internal session)
    # process_event({'session_id': 's3', 'user_id': 'user2', 'event_type': 'comments'}, 
    #              buffer, totals, test_users)
    # process_event({'session_id': 's3', 'user_id': 'user_test_B', 'event_type': 'likes'}, 
    #              buffer, totals, test_users)
    # process_event({'session_id': 's3', 'user_id': 'user2', 'event_type': 'session_end'}, 
    #              buffer, totals, test_users)
    
    # assert totals['comments'] == 0, "Comments from mixed sessions should not be counted"
    
    print("All test cases passed!")

if __name__ == "__main__":
    test_process_event() 