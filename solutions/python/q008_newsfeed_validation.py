"""
Scenario 6: News Feed
Question 6.4.1: News Feed View Validation

Description:
Process newsfeed logs to determine valid post views per session.
Implement two functions:

1. `process_newsfeed_log(log, session_buffer)`:
   - Process a single log event ('start', 'end', or visibility update)
   - Update the session_buffer data structure with view information
   - Track start time, end time, and maximum visibility percentage

2. `calculate_session_valid_reads(session_id, session_buffer)`:
   - Count and return the number of posts in a session that meet the valid read criteria
     (duration >= 5s OR max_perc >= 80%)


Data Structures:
- `log`: A dictionary representing a log event. Examples:
    - {'event_type': 'start', 'session_id': 's1', 'post_id': 'p1', 'timestamp': 100}
    - {'event_type': 'visibility', 'session_id': 's1', 'post_id': 'p1', 'percentage': 50, 'timestamp': 102}
    - {'event_type': 'end', 'session_id': 's1', 'post_id': 'p1', 'timestamp': 108}

- `session_buffer`: A dictionary to store session data. Structure example:
    {
        's1': {
            'p1': {'start_time': 100, 'end_time': 108, 'max_visibility_perc': 50, 'events': [...]},
            'p2': { ... }
        },
        's2': { ... }
    }

Valid Read Criteria:
- A post view is considered a "valid read" if:
    - The view duration (end_time - start_time) is >= 5 seconds, OR
    - The maximum visibility percentage reached for that post in the session is >= 80%.

Edge cases to consider:
- Logs might be out of order for a given post (e.g., visibility event before start).
  The buffer should handle this by storing events and processing post details once an 'end' event arrives or when calculating valid reads.
- A post might have multiple 'start' or 'end' events. Use the earliest start and latest end.
- A post might not have an 'end' event. Such posts are not considered for duration but can be valid if max_visibility hits 80%.
  For simplicity in this initial version, assume 'end' events are crucial for defining a complete view duration. If a post has no 'end_time' recorded in the buffer, its duration is considered 0 or undefined.
"""

# Initialize session_buffer as a global or passed-in mutable dictionary
# For this example, we'll assume it's passed to functions.

def process_newsfeed_log(log: dict, session_buffer: dict):
    """
    Processes a single newsfeed log event and updates the session buffer.

    Args:
        log: A dictionary representing a log event.
        session_buffer: A dictionary to store and update session data.
                        Example: {'s1': {'p1': {'start_time': ..., 'end_time': ..., 'max_visibility_perc': ...}}}
    """
    event_type = log.get('event_type')
    session_id = log.get('session_id')
    post_id = log.get('post_id')
    timestamp = log.get('timestamp')

    if not all([event_type, session_id, post_id, isinstance(timestamp, (int, float))]):
        # Invalid log structure, skip
        return

    if session_id not in session_buffer:
        session_buffer[session_id] = {} # Initialize as a regular dictionary

    if post_id not in session_buffer[session_id]:
        session_buffer[session_id][post_id] = {
            'start_time': float('inf'),
            'end_time': float('-inf'),
            'max_visibility_perc': 0,
            'has_start': False,
            'has_end': False
        }

    post_data = session_buffer[session_id][post_id]

    if event_type == 'start':
        post_data['start_time'] = min(post_data['start_time'], timestamp)
        post_data['has_start'] = True
    elif event_type == 'end':
        post_data['end_time'] = max(post_data['end_time'], timestamp)
        post_data['has_end'] = True
    elif event_type == 'visibility':
        percentage = log.get('percentage')
        if isinstance(percentage, (int, float)):
            post_data['max_visibility_perc'] = max(post_data['max_visibility_perc'], percentage)
    
    # No need to explicitly store post_data back if it's a mutable dictionary
    # and changes were made in place. However, if post_data was reassigned, it would be.
    # session_buffer[session_id][post_id] = post_data # This line is actually redundant if post_data is not reassigned.


def calculate_session_valid_reads(session_id: str, session_buffer: dict) -> int:
    """
    Calculates the number of valid post reads for a given session_id based on the buffer.

    Args:
        session_id: The ID of the session to analyze.
        session_buffer: The dictionary containing all processed session data.

    Returns:
        The number of posts in the session that meet the valid read criteria.
    """
    if session_id not in session_buffer:
        return 0

    valid_reads_count = 0
    session_posts = session_buffer[session_id]

    for post_id, data in session_posts.items():
        is_valid_read = False
        
        # Ensure both start and end times are present to calculate duration
        # and that they are not the initial float('inf') or float('-inf') values.
        has_defined_start = data['has_start'] and data['start_time'] != float('inf')
        has_defined_end = data['has_end'] and data['end_time'] != float('-inf')

        duration = 0
        if has_defined_start and has_defined_end and data['end_time'] >= data['start_time']:
            duration = data['end_time'] - data['start_time']
        
        # Criteria 1: Duration >= 5 seconds
        if duration >= 5:
            is_valid_read = True
        
        # Criteria 2: Max visibility >= 80%
        if data['max_visibility_perc'] >= 80:
            is_valid_read = True
            
        if is_valid_read:
            valid_reads_count += 1
            
    return valid_reads_count


# Example Usage
if __name__ == "__main__":
    session_buffer_main = {}

    logs1 = [
        {'event_type': 'start', 'session_id': 's1', 'post_id': 'p1', 'timestamp': 100},
        {'event_type': 'visibility', 'session_id': 's1', 'post_id': 'p1', 'percentage': 50, 'timestamp': 102},
        {'event_type': 'end', 'session_id': 's1', 'post_id': 'p1', 'timestamp': 108}, # duration 8s, max_vis 50% -> VALID (duration)
        
        {'event_type': 'start', 'session_id': 's1', 'post_id': 'p2', 'timestamp': 110},
        {'event_type': 'visibility', 'session_id': 's1', 'post_id': 'p2', 'percentage': 85, 'timestamp': 112},
        {'event_type': 'end', 'session_id': 's1', 'post_id': 'p2', 'timestamp': 113}, # duration 3s, max_vis 85% -> VALID (visibility)

        {'event_type': 'start', 'session_id': 's1', 'post_id': 'p3', 'timestamp': 120},
        {'event_type': 'visibility', 'session_id': 's1', 'post_id': 'p3', 'percentage': 10, 'timestamp': 121},
        {'event_type': 'end', 'session_id': 's1', 'post_id': 'p3', 'timestamp': 122}, # duration 2s, max_vis 10% -> INVALID
    ]

    for log_entry in logs1:
        process_newsfeed_log(log_entry, session_buffer_main)
    
    print("Session Buffer after logs1:")
    import json
    print(json.dumps(session_buffer_main, indent=4))

    valid_reads_s1 = calculate_session_valid_reads('s1', session_buffer_main)
    print(f"Valid reads for session s1: {valid_reads_s1}") # Expected: 2
    assert valid_reads_s1 == 2, f"Test Case 1 Failed for s1: Expected 2, got {valid_reads_s1}"
    print("Test Case 1 for s1 Passed.\n")

    # Test with a session that doesn't exist
    valid_reads_s_nonexistent = calculate_session_valid_reads('s_nonexistent', session_buffer_main)
    print(f"Valid reads for session s_nonexistent: {valid_reads_s_nonexistent}") # Expected: 0
    assert valid_reads_s_nonexistent == 0, "Test Case for non-existent session failed."
    print("Test Case for non-existent session Passed.\n")

    session_buffer_main_2 = {}
    logs2 = [
        # Post with only high visibility, no end event (duration 0, max_vis 90%) -> VALID
        {'event_type': 'start', 'session_id': 's2', 'post_id': 'pA', 'timestamp': 200},
        {'event_type': 'visibility', 'session_id': 's2', 'post_id': 'pA', 'percentage': 90, 'timestamp': 201},
        # This post will not have a duration calculated as 'end_time' remains -inf.
        # However, max_visibility_perc is 90, so it should be valid.

        # Post with long duration, but low visibility (duration 10s, max_vis 10%) -> VALID
        {'event_type': 'start', 'session_id': 's2', 'post_id': 'pB', 'timestamp': 210},
        {'event_type': 'visibility', 'session_id': 's2', 'post_id': 'pB', 'percentage': 10, 'timestamp': 212},
        {'event_type': 'end', 'session_id': 's2', 'post_id': 'pB', 'timestamp': 220},

        # Post with short duration and low visibility (duration 1s, max_vis 5%) -> INVALID
        {'event_type': 'start', 'session_id': 's2', 'post_id': 'pC', 'timestamp': 230},
        {'event_type': 'visibility', 'session_id': 's2', 'post_id': 'pC', 'percentage': 5, 'timestamp': 230.5},
        {'event_type': 'end', 'session_id': 's2', 'post_id': 'pC', 'timestamp': 231},
        
        # Post with multiple visibility events, latest end time should be used
        {'event_type': 'start', 'session_id': 's2', 'post_id': 'pD', 'timestamp': 240},
        {'event_type': 'visibility', 'session_id': 's2', 'post_id': 'pD', 'percentage': 30, 'timestamp': 241},
        {'event_type': 'end', 'session_id': 's2', 'post_id': 'pD', 'timestamp': 243}, # duration 3s
        {'event_type': 'visibility', 'session_id': 's2', 'post_id': 'pD', 'percentage': 85, 'timestamp': 244}, # max_vis 85%
        {'event_type': 'end', 'session_id': 's2', 'post_id': 'pD', 'timestamp': 245}, # duration becomes 5s -> VALID (duration or visibility)
    ]
    for log_entry in logs2:
        process_newsfeed_log(log_entry, session_buffer_main_2)

    print("Session Buffer after logs2:")
    print(json.dumps(session_buffer_main_2, indent=4))

    valid_reads_s2 = calculate_session_valid_reads('s2', session_buffer_main_2)
    print(f"Valid reads for session s2: {valid_reads_s2}") # Expected: 3 (pA, pB, pD)
    assert valid_reads_s2 == 3, f"Test Case 2 Failed for s2: Expected 3, got {valid_reads_s2}"
    print("Test Case 2 for s2 Passed.\n")
    
    # Test for out-of-order events (visibility before start)
    session_buffer_main_3 = {}
    logs3 = [
        {'event_type': 'visibility', 'session_id': 's3', 'post_id': 'pX', 'percentage': 90, 'timestamp': 300},
        {'event_type': 'start', 'session_id': 's3', 'post_id': 'pX', 'timestamp': 301},
        {'event_type': 'end', 'session_id': 's3', 'post_id': 'pX', 'timestamp': 303}, # duration 2s, max_vis 90% -> VALID
    ]
    for log_entry in logs3:
        process_newsfeed_log(log_entry, session_buffer_main_3)
    
    print("Session Buffer after logs3 (out-of-order):")
    print(json.dumps(session_buffer_main_3, indent=4))
    valid_reads_s3 = calculate_session_valid_reads('s3', session_buffer_main_3)
    print(f"Valid reads for session s3: {valid_reads_s3}") # Expected: 1
    assert valid_reads_s3 == 1, f"Test Case 3 Failed for s3: Expected 1, got {valid_reads_s3}"
    print("Test Case 3 for s3 Passed.\n")


    print("All q008 tests passed!") 