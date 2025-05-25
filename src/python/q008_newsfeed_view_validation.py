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
    
    event_type = log.get('event_type')
    session_id = log.get('session_id')
    post_id = log.get('post_id')
    time_stamp = log.get('time_stamp')
    percentage = log.get('percentage')

    if not all([event_type,session_id,post_id,isinstance(time_stamp,(int,float))]):
        return

    if session_id not in session_buffer:
        session_buffer[session_id]={}
    
    if post_id not in session_buffer[session_id]:
        session_buffer[session_id][post_id]={
            'start_time':None,
            'end_time': None,
            'max_visibility_perc':0,
            'has_start':False,
            'has_end':False
        }

    post_data = session_buffer[session_id][post_id]

    if event_type =='start':
        if post_data['start_time'] is not None:
            post_data['start_time'] = min(post_data['start_time'],time_stamp)
        else: 
            post_data['start_time'] = time_stamp
            post_data['has_start'] = True
    elif event_type == 'end':
        if post_data['end_time'] is not None:
            post_data['end_time'] = max(post_data['end_time'],time_stamp)
        else:
            post_data['end_time'] = time_stamp    
            post_data['has_end']=True
    
    if isinstance(percentage,(int,float)):
        post_data['max_visibility_perc'] = max(post_data['max_visibility_perc'],percentage)

def calculate_session_valid_reads(session_id, session_buffer):
    """
    Count the number of posts in a session that meet valid read criteria.
    
    Args:
        session_id (str): The session to process
        session_buffer (dict): Data structure tracking view metrics by session/post
        
    Returns:
        int: Count of posts meeting valid read criteria (duration >= 5s OR max_perc >= 80%)
    """
    
    if session_id not in session_buffer:
        return 0 
    
    valid_read_counts = 0

    session_posts = session_buffer[session_id]
    print(f'session_id: {session_id}')
    for post_id, data in session_posts.items():
        is_valid_read = False

        has_defined_start = data['has_start'] and data['start_time'] is not None
        has_defined_end = data['has_end'] and data['end_time'] is not None

        duration = 0

        if has_defined_start and has_defined_end and data['end_time']>=data['start_time']:
            duration = data['end_time']-data['start_time']

        if duration >=5:
            is_valid_read = True
        
        if data['max_visibility_perc']>=80:
            is_valid_read = True
        
        if is_valid_read:
            valid_read_counts+=1
        print(f'duration: {duration}')
        print(f'valid_read_counts: {valid_read_counts}')
        
    return valid_read_counts


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