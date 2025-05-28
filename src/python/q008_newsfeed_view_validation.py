"""
Question: Process newsfeed logs to determine valid post views per session.

In a newsfeed application, we need to determine which posts were validly "read" by users.
A post is considered a valid read if EITHER:
- It was visible on screen for at least 5 seconds
- OR it reached at least 80% visibility on the screen at some point

Implement two functions:

1. `process_newsfeed_log(log, session_buffer)`:
   - Process a single log event ('start', 'end', or visibility update)
   - Update the session_buffer data structure with view information
   - Track start time, end time, and maximum visibility percentage

2. `calculate_session_valid_reads(session_id, session_buffer)`:
   - Count and return the number of posts in a session that meet the valid read criteria

Log events have this structure:
{
    'session_id': 's1',           # The session identifier
    'post_id': 'p1',              # The post being viewed
    'time_stamp': 100,            # Time in seconds (integer)
    'event_type': 'start',        # 'start' or 'end' or other event
    'percentage': 10              # Visibility percentage (0-100)
}

The session_buffer should track for each (session_id, post_id) pair:
- start: The earliest timestamp the post started being visible
- end: The latest timestamp the post stopped being visible
- max_perc: The maximum visibility percentage the post achieved

Example:
    session_buffer = {}
    
    # Process logs
    process_newsfeed_log({
        'session_id': 's1', 'post_id': 'p1', 
        'time_stamp': 100, 'event_type': 'start', 'percentage': 10
    }, session_buffer)
    
    process_newsfeed_log({
        'session_id': 's1', 'post_id': 'p1',
        'time_stamp': 106, 'event_type': 'end', 'percentage': 90
    }, session_buffer)
    
    process_newsfeed_log({
        'session_id': 's1', 'post_id': 'p2',
        'time_stamp': 110, 'event_type': 'start', 'percentage': 50
    }, session_buffer)
    
    process_newsfeed_log({
        'session_id': 's1', 'post_id': 'p2',
        'time_stamp': 112, 'event_type': 'end', 'percentage': 50
    }, session_buffer)
    
    # Calculate valid reads
    valid_reads = calculate_session_valid_reads('s1', session_buffer)
    # Expected: 1 (post 'p1' is valid, 'p2' is not)
    # - p1: duration = 6s (≥ 5s) and max_perc = 90% (≥ 80%)
    # - p2: duration = 2s (< 5s) and max_perc = 50% (< 80%)
"""

def process_newsfeed_log(log, session_buffer):
    """
    Process a single newsfeed log event, updating session_buffer with view information.
    
    Args:
        log (dict): A newsfeed log event with keys:
                    'session_id', 'post_id', 'time_stamp', 'event_type', 'percentage'
        session_buffer (dict): Data structure tracking view metrics by session/post
        
    Returns:
        None (updates session_buffer in-place)
    """
    
    if not log: 
        return

    session_id = log['session_id']
    post_id = log['post_id']
    time_stamp = log['time_stamp']
    event_type = log['event_type']
    percentage = log['percentage']

    if not all(key in log for key in ['session_id','post_id','time_stamp','event_type','percentage']):
        return

    if session_id not in session_buffer:
        session_buffer[session_id] = {}

    if post_id not in session_buffer[session_id]:
        session_buffer[session_id][post_id]={
            'start_time' : None,
            'end_time': None,
            'max_perc': 0
        }

    
    current_session = session_buffer[session_id][post_id]
    current_start_time = current_session['start_time']
    current_end_time = current_session['end_time']

    if event_type =='start':
        if current_session['start_time'] is not None and 'start_time' in current_session: 
            current_session['start_time'] = min(current_session['start_time'],time_stamp)

        else: 
            current_session['start_time'] = int(time_stamp)

    elif event_type =='end':
        if current_session['end_time'] is not None and 'end_time' in current_session: 
            current_session['end_time'] = max(current_session['end_time'],time_stamp)
        else: 
            current_session['end_time'] = int(time_stamp)


    current_session['max_perc'] = max(current_session['max_perc'],percentage)
    
        

def calculate_session_valid_reads(session_id: str, session_buffer: dict) -> int:
    """
    Calculates the number of valid post reads for a given session_id based on the buffer.

    Args:
        session_id: The ID of the session to analyze.
        session_buffer: The dictionary containing all processed session data.

    Returns:
        The number of posts in the session that meet the valid read criteria.


- It was visible on screen for at least 5 seconds
- OR it reached at least 80% visibility on the screen at some point

    """

    session = session_buffer[session_id]


    count = 0

    for post in session: 
        start = session[post]['start_time']
        end = session[post]['end_time']

        perc = session[post]['max_perc']
        if (end-start)>=5:
            count+=1
        elif perc>=80:
            count+=1
        else:
            continue
    return count

# Test cases
def test_newsfeed_view_validation():
    # Test case 1: Basic valid/invalid read detection
    session_buffer = {}
    
    # Process log events for session 's1'
    process_newsfeed_log({
        'session_id': 's1', 'post_id': 'p1', 
        'time_stamp': 100, 'event_type': 'start', 'percentage': 10
    }, session_buffer)
    
    process_newsfeed_log({
        'session_id': 's1', 'post_id': 'p1',
        'time_stamp': 106, 'event_type': 'end', 'percentage': 90
    }, session_buffer)
    
    process_newsfeed_log({
        'session_id': 's1', 'post_id': 'p2',
        'time_stamp': 110, 'event_type': 'start', 'percentage': 50
    }, session_buffer)
    
    process_newsfeed_log({
        'session_id': 's1', 'post_id': 'p2',
        'time_stamp': 112, 'event_type': 'end', 'percentage': 50
    }, session_buffer)
    
    valid_reads = calculate_session_valid_reads('s1', session_buffer)
    assert valid_reads == 1, f"Expected 1 valid read in session 's1', got {valid_reads}"
    
    # Test case 2: High visibility but short duration
    process_newsfeed_log({
        'session_id': 's2', 'post_id': 'p3', 
        'time_stamp': 200, 'event_type': 'start', 'percentage': 85
    }, session_buffer)
    
    process_newsfeed_log({
        'session_id': 's2', 'post_id': 'p3',
        'time_stamp': 202, 'event_type': 'end', 'percentage': 85
    }, session_buffer)
    
    valid_reads = calculate_session_valid_reads('s2', session_buffer)
    assert valid_reads == 1, f"Expected 1 valid read in session 's2' (high visibility), got {valid_reads}"
    
    # Test case 3: Long duration but low visibility
    process_newsfeed_log({
        'session_id': 's3', 'post_id': 'p4', 
        'time_stamp': 300, 'event_type': 'start', 'percentage': 40
    }, session_buffer)
    
    process_newsfeed_log({
        'session_id': 's3', 'post_id': 'p4',
        'time_stamp': 306, 'event_type': 'end', 'percentage': 40
    }, session_buffer)
    
    valid_reads = calculate_session_valid_reads('s3', session_buffer)
    assert valid_reads == 1, f"Expected 1 valid read in session 's3' (long duration), got {valid_reads}"
    
    # Test case 4: Session with no valid reads
    process_newsfeed_log({
        'session_id': 's4', 'post_id': 'p5', 
        'time_stamp': 400, 'event_type': 'start', 'percentage': 40
    }, session_buffer)
    
    process_newsfeed_log({
        'session_id': 's4', 'post_id': 'p5',
        'time_stamp': 402, 'event_type': 'end', 'percentage': 40
    }, session_buffer)
    
    valid_reads = calculate_session_valid_reads('s4', session_buffer)
    assert valid_reads == 0, f"Expected 0 valid reads in session 's4', got {valid_reads}"
    
    print("All test cases passed!")

if __name__ == "__main__":
    test_newsfeed_view_validation() 