# Placeholder for q003_session_engagement_user_level_filter.py

def process_event_user_level_filter(event, buffer, totals, test_users):
    \"\"\"
    Process a single engagement event, buffer it by session_id, and update 
    aggregate counts upon session_end. Events from test_users are excluded,
    even if they are in a session with non-test_users.
    
    Args:
        event (dict): An engagement event dictionary with 'session_id', 
                      'user_id', and 'event_type'.
        buffer (dict): Session buffer to store events by session_id. 
                       Each session_id maps to {'events': [], 'users': set()}.
        totals (dict): Running counts of engagement types (e.g., {'view': 0, 'click': 0}).
        test_users (set): Set of internal test user IDs to exclude.
        
    Returns:
        None (updates buffer and totals in-place)
    \"\"\"
    session_id = event['session_id']
    user_id = event['user_id']
    event_type = event['event_type']
    
    # Initialize session in buffer if not already present
    if session_id not in buffer:
        buffer[session_id] = {
            'events': [],
            'users': set() # Still useful to track all users in session for other analytics if needed
        }
    
    # Add event to session buffer
    # Crucially, the event itself (containing its specific user_id) is stored.
    buffer[session_id]['events'].append(event)
    buffer[session_id]['users'].add(user_id)
    
    # If session_end event received, process the session
    if event_type == 'session_end':
        # Iterate through each event in the ended session
        for e in buffer[session_id]['events']:
            event_user_id = e['user_id']
            
            # Only count the event if the user who generated THIS event is NOT a test user
            if event_user_id not in test_users:
                e_type = e['event_type']
                # Only count event types that are in the totals dictionary (e.g., 'view', 'click')
                # 'session_start', 'session_end' are typically not counted themselves as engagement metrics here.
                if e_type in totals:
                    totals[e_type] += 1
        
        # Remove session from buffer after processing
        del buffer[session_id]

# Example Usage (adapted from the original q003_session_engagement.py)
if __name__ == '__main__':
    events_stream = [
        {'session_id': 's1', 'user_id': 'u1', 'event_type': 'session_start'},
        {'session_id': 's1', 'user_id': 'u1', 'event_type': 'view'},
        {'session_id': 's1', 'user_id': 'u2_test', 'event_type': 'click'}, # u2_test is a test user
        {'session_id': 's1', 'user_id': 'u1', 'event_type': 'view'},
        {'session_id': 's1', 'user_id': 'u2_test', 'event_type': 'view'}, # Event by test user
        {'session_id': 's1', 'user_id': 'u1', 'event_type': 'session_end'},

        {'session_id': 's2', 'user_id': 'u3', 'event_type': 'session_start'},
        {'session_id': 's2', 'user_id': 'u3', 'event_type': 'click'},
        {'session_id': 's2', 'user_id': 'u3', 'event_type': 'session_end'},

        {'session_id': 's3', 'user_id': 'u4_test', 'event_type': 'session_start'}, # Whole session is test
        {'session_id': 's3', 'user_id': 'u4_test', 'event_type': 'view'},
        {'session_id': 's3', 'user_id': 'u4_test', 'event_type': 'session_end'},
    ]

    session_buffer = {}
    engagement_totals = {'view': 0, 'click': 0} 
    internal_test_users = {'u2_test', 'u4_test'}

    print(f"Initial totals: {engagement_totals}")
    print(f"Test users: {internal_test_users}\n")

    for event_data in events_stream:
        print(f"Processing event: {event_data}")
        process_event_user_level_filter(event_data, session_buffer, engagement_totals, internal_test_users)
        if event_data['event_type'] == 'session_end':
            print(f"  Session {event_data['session_id']} ended. Current totals: {engagement_totals}")
            print(f"  Buffer state: {session_buffer}\n")
        else:
            print(f"  Buffer state: {session_buffer}")
            print(f"  Totals (mid-session): {engagement_totals}\n")

    print("\nFinal Engagement Totals (User-Level Filtering):")
    print(engagement_totals)

    # Expected Output for User-Level Filtering:
    # Session s1:
    #   u1 (real user): view, view (2 views)
    #   u2_test (test user): click, view (ignored)
    # Session s2:
    #   u3 (real user): click (1 click)
    # Session s3:
    #   u4_test (test user): view (ignored)
    #
    # Final Totals: {'view': 2, 'click': 1} 