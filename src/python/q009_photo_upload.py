"""
Question: Process a stream of photo upload logs ('upload_start', 'upload_end')
to calculate the running average upload time for successful uploads.

Implement the function `process_upload_log(log, pending_buffer, stats_aggregator)` that:
1. Processes each event from a stream of upload logs
2. Keeps track of 'upload_start' events in the pending_buffer
3. When an 'upload_end' event arrives and is successful:
   - Calculate the upload duration
   - Update the aggregate statistics

The function should handle two types of events:
- 'upload_start': Log the start time for a specific upload_id
- 'upload_end': Calculate duration and update stats if successful

Log events have this structure:
{
    'timestamp': 1000,            # Time in milliseconds (integer)
    'event_type': 'upload_start', # 'upload_start' or 'upload_end'
    'upload_id': 'up1',           # Unique identifier for the upload
    'is_success': True            # Only present in 'upload_end' events
}

The pending_buffer keeps track of uploads in progress: { 'upload_id': start_timestamp }
The stats_aggregator tracks overall statistics: { 'total_duration_ms': 0, 'successful_uploads': 0 }

Example:
    pending_buffer = {}
    stats_aggregator = {'total_duration_ms': 0, 'successful_uploads': 0}
    
    # Process logs
    process_upload_log(
        {'timestamp': 1000, 'event_type': 'upload_start', 'upload_id': 'up1'},
        pending_buffer, stats_aggregator)
    
    process_upload_log(
        {'timestamp': 1050, 'event_type': 'upload_start', 'upload_id': 'up2'},
        pending_buffer, stats_aggregator)
    
    process_upload_log(
        {'timestamp': 1150, 'event_type': 'upload_end', 'upload_id': 'up1', 'is_success': True},
        pending_buffer, stats_aggregator)
    # Duration for up1: 1150 - 1000 = 150ms
    # After processing: stats_aggregator = {'total_duration_ms': 150, 'successful_uploads': 1}
    
    process_upload_log(
        {'timestamp': 1250, 'event_type': 'upload_end', 'upload_id': 'up2', 'is_success': True},
        pending_buffer, stats_aggregator)
    # Duration for up2: 1250 - 1050 = 200ms
    # After processing: stats_aggregator = {'total_duration_ms': 350, 'successful_uploads': 2}
    # Average upload time: 350 / 2 = 175ms
"""

def process_upload_log(log, pending_buffer, stats_aggregator):
    """
    Process a single upload log event and update the upload statistics.
    
    Args:
        log (dict): An upload log event with keys including:
                    'timestamp', 'event_type', 'upload_id', and possibly 'is_success'
        pending_buffer (dict): Dictionary tracking in-progress uploads: { 'upload_id': start_timestamp }
        stats_aggregator (dict): Dictionary with aggregate statistics:
                                { 'total_duration_ms': int, 'successful_uploads': int }
        
    Returns:
        None (updates pending_buffer and stats_aggregator in-place)
    """
    # TODO: Implement your solution here
    pass

# Test cases
def test_photo_upload_processing():
    # Test case 1: Basic upload start/end successful processing
    pending_buffer = {}
    stats_aggregator = {'total_duration_ms': 0, 'successful_uploads': 0}
    
    # Process logs
    process_upload_log(
        {'timestamp': 1000, 'event_type': 'upload_start', 'upload_id': 'up1'},
        pending_buffer, stats_aggregator)
    
    # After start event, pending_buffer should have the upload
    assert 'up1' in pending_buffer, "Upload should be tracked in pending_buffer after start event"
    assert pending_buffer['up1'] == 1000, "Start timestamp should be correctly recorded"
    
    process_upload_log(
        {'timestamp': 1150, 'event_type': 'upload_end', 'upload_id': 'up1', 'is_success': True},
        pending_buffer, stats_aggregator)
    
    # After end event, pending_buffer should not have the upload anymore
    assert 'up1' not in pending_buffer, "Upload should be removed from pending_buffer after end event"
    
    # Stats should be updated
    assert stats_aggregator['total_duration_ms'] == 150, f"Expected duration 150ms, got {stats_aggregator['total_duration_ms']}ms"
    assert stats_aggregator['successful_uploads'] == 1, f"Expected 1 successful upload, got {stats_aggregator['successful_uploads']}"
    
    # Test case 2: Multiple uploads with different durations
    process_upload_log(
        {'timestamp': 2000, 'event_type': 'upload_start', 'upload_id': 'up2'},
        pending_buffer, stats_aggregator)
    
    process_upload_log(
        {'timestamp': 2300, 'event_type': 'upload_end', 'upload_id': 'up2', 'is_success': True},
        pending_buffer, stats_aggregator)
    
    # Stats should accumulate
    assert stats_aggregator['total_duration_ms'] == 450, f"Expected total duration 450ms, got {stats_aggregator['total_duration_ms']}ms"
    assert stats_aggregator['successful_uploads'] == 2, f"Expected 2 successful uploads, got {stats_aggregator['successful_uploads']}"
    
    # Test case 3: Failed upload should not affect statistics
    process_upload_log(
        {'timestamp': 3000, 'event_type': 'upload_start', 'upload_id': 'up3'},
        pending_buffer, stats_aggregator)
    
    process_upload_log(
        {'timestamp': 3200, 'event_type': 'upload_end', 'upload_id': 'up3', 'is_success': False},
        pending_buffer, stats_aggregator)
    
    # Stats should remain unchanged
    assert stats_aggregator['total_duration_ms'] == 450, "Failed upload should not affect total duration"
    assert stats_aggregator['successful_uploads'] == 2, "Failed upload should not affect successful upload count"
    
    # Test case 4: Out-of-order events (end without start) should be handled gracefully
    process_upload_log(
        {'timestamp': 4000, 'event_type': 'upload_end', 'upload_id': 'up4', 'is_success': True},
        pending_buffer, stats_aggregator)
    
    # Stats should remain unchanged
    assert stats_aggregator['total_duration_ms'] == 450, "End without start should not affect statistics"
    assert stats_aggregator['successful_uploads'] == 2, "End without start should not affect successful upload count"
    
    print("All test cases passed!")

if __name__ == "__main__":
    test_photo_upload_processing() 