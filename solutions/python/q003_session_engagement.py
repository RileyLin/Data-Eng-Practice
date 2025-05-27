"""
Solution to Session Engagement Processing

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
    buffer = {}
    totals = {'view': 0, 'click': 0}
    test_users = {'user_test_A', 'user_test_B'}
    
    # Test case 1: Regular user session
    process_event({'session_id': 's1', 'user_id': 'user1', 'event_type': 'view'}, 
                 buffer, totals, test_users)
    process_event({'session_id': 's1', 'user_id': 'user1', 'event_type': 'click'}, 
                 buffer, totals, test_users)
    process_event({'session_id': 's1', 'user_id': 'user1', 'event_type': 'session_end'}, 
                 buffer, totals, test_users)
    
    assert totals['view'] == 1
    assert totals['click'] == 1
    assert 's1' not in buffer
    
    # Test case 2: Test user session (should not affect totals)
    process_event({'session_id': 's2', 'user_id': 'user_test_A', 'event_type': 'view'}, 
                 buffer, totals, test_users)
    process_event({'session_id': 's2', 'user_id': 'user_test_A', 'event_type': 'session_end'}, 
                 buffer, totals, test_users)
    
    assert totals['view'] == 1  # Should not increase
    
    print("All test cases passed!")

if __name__ == "__main__":
    test_process_event() 