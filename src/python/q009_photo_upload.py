"""
Question: Process a stream of photo upload logs ('upload_start', 'upload_end')
to calculate the running average upload time for successful uploads.

Implement the function `process_upload_log(log, pending_buffer, stats_aggregator)` that:
1. Processes each event from a stream of upload logs
2. Keeps track of 'upload_start' events in the pending_buffer
3. When an 'upload_end' event arrives and is successful:
   - Calculate the upload duration
   - Update the aggregate statistics

DATA STRUCTURE EXAMPLES:

Input: log (dict)
- Structure: {'timestamp': int, 'event_type': str, 'upload_id': str, 'is_success': bool (optional)}
- event_type values: 'upload_start' or 'upload_end'
- is_success: only present in 'upload_end' events

Example log events:
- Start event: {'timestamp': 1000, 'event_type': 'upload_start', 'upload_id': 'up1'}
- Successful end: {'timestamp': 1150, 'event_type': 'upload_end', 'upload_id': 'up1', 'is_success': True}
- Failed end: {'timestamp': 1200, 'event_type': 'upload_end', 'upload_id': 'up2', 'is_success': False}

Input/Output: pending_buffer (dict)
- Structure: {upload_id: start_timestamp}
- Tracks uploads currently in progress
- Example: {'up1': 1000, 'up2': 1050}

Input/Output: stats_aggregator (dict)
- Structure: {'total_duration_ms': int, 'successful_uploads': int}
- Accumulates statistics for successful uploads only
- Example: {'total_duration_ms': 350, 'successful_uploads': 2}

PROCESSING FLOW EXAMPLE:

Initial state:
pending_buffer = {}
stats_aggregator = {'total_duration_ms': 0, 'successful_uploads': 0}

Step 1: Process upload_start
log = {'timestamp': 1000, 'event_type': 'upload_start', 'upload_id': 'up1'}
→ pending_buffer = {'up1': 1000}
→ stats_aggregator unchanged

Step 2: Process another upload_start
log = {'timestamp': 1050, 'event_type': 'upload_start', 'upload_id': 'up2'}
→ pending_buffer = {'up1': 1000, 'up2': 1050}
→ stats_aggregator unchanged

Step 3: Process successful upload_end
log = {'timestamp': 1150, 'event_type': 'upload_end', 'upload_id': 'up1', 'is_success': True}
→ Duration = 1150 - 1000 = 150ms
→ pending_buffer = {'up2': 1050} (up1 removed)
→ stats_aggregator = {'total_duration_ms': 150, 'successful_uploads': 1}

Step 4: Process failed upload_end
log = {'timestamp': 1250, 'event_type': 'upload_end', 'upload_id': 'up2', 'is_success': False}
→ pending_buffer = {} (up2 removed)
→ stats_aggregator unchanged (failed uploads not counted)

Step 5: Process upload_end without matching start (edge case)
log = {'timestamp': 1300, 'event_type': 'upload_end', 'upload_id': 'up3', 'is_success': True}
→ No matching start found, ignore
→ pending_buffer = {}
→ stats_aggregator unchanged

Final state:
pending_buffer = {}
stats_aggregator = {'total_duration_ms': 150, 'successful_uploads': 1}
Average upload time = 150 / 1 = 150ms

Edge Cases:
- upload_end without matching upload_start: Ignore
- Failed uploads (is_success=False): Remove from pending but don't update stats
- Duplicate upload_start for same upload_id: Overwrite previous start time
- Missing is_success field in upload_end: Treat as failed
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
    event_type = log['event_type']
    upload_id = log['upload_id']
    timestamp = log['timestamp']
    
    if event_type == 'upload_start':
        # Record the start time for this upload
        pending_buffer[upload_id] = timestamp
        
    elif event_type == 'upload_end':
        # Check if we have a matching start event
        if upload_id in pending_buffer:
            start_timestamp = pending_buffer[upload_id]
            
            # Remove from pending buffer regardless of success
            del pending_buffer[upload_id]
            
            # Only update stats if upload was successful
            is_success = log.get('is_success', False)
            if is_success:
                duration_ms = timestamp - start_timestamp
                stats_aggregator['total_duration_ms'] += duration_ms
                stats_aggregator['successful_uploads'] += 1

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