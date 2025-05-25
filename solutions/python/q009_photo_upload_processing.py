\"\"\"
Scenario 7: Photo Upload (Instagram-like)
Question 7.4.1: Photo Upload Processing

Description:
Process a stream of photo upload logs ('upload_start', 'upload_end')
to calculate the running average upload time for successful uploads.
Implement the function `process_upload_log(log, pending_buffer, stats_aggregator)`
that processes each event from a stream of upload logs and updates the statistics for successful uploads.

Data Structures:
- `log`: A dictionary representing an upload log event. Examples:
    - {'event_type': 'upload_start', 'photo_id': 'photo123', 'user_id': 'userA', 'timestamp': 1000}
    - {'event_type': 'upload_end', 'photo_id': 'photo123', 'user_id': 'userA', 'timestamp': 1005, 'status': 'success'}
    - {'event_type': 'upload_end', 'photo_id': 'photo456', 'user_id': 'userB', 'timestamp': 1010, 'status': 'failure'}

- `pending_buffer`: A dictionary to store 'upload_start' events for photos currently being uploaded.
    - Key: `photo_id`
    - Value: Dictionary with `start_time` and other relevant info like `user_id`.
    - Example: {'photo123': {'start_time': 1000, 'user_id': 'userA'}}

- `stats_aggregator`: A dictionary to store aggregated statistics.
    - Example: {'total_successful_uploads': 0, 'total_upload_time_ms': 0, 'average_upload_time_ms': 0.0}

Function Logic:
- If `event_type` is 'upload_start':
    - Store the photo_id and start_time in `pending_buffer`.
- If `event_type` is 'upload_end':
    - Check if the `photo_id` exists in `pending_buffer`.
    - If it exists:
        - Calculate upload_duration = end_timestamp - start_timestamp.
        - If `status` is 'success':
            - Increment `stats_aggregator['total_successful_uploads']`.
            - Add `upload_duration` to `stats_aggregator['total_upload_time_ms']`.
            - Recalculate `stats_aggregator['average_upload_time_ms']`.
        - Remove the `photo_id` from `pending_buffer`.

Edge Cases:
- 'upload_end' event arrives for a `photo_id` not in `pending_buffer` (ignore or log error).
- Multiple 'upload_start' events for the same `photo_id` (use the latest start time, or the first, depending on product logic - assume overwrite with latest for this problem).
- Timestamps are in milliseconds.
\"\"\"


def process_upload_log(log: dict, pending_buffer: dict, stats_aggregator: dict):
    \"\"\"
    Processes a single photo upload log event and updates the pending buffer and stats aggregator.

    Args:
        log: A dictionary representing the log event.
        pending_buffer: A dictionary to store pending uploads.
        stats_aggregator: A dictionary to store aggregated statistics.
    \"\"\"
    event_type = log.get(\'event_type\')
    photo_id = log.get(\'photo_id\')
    timestamp = log.get(\'timestamp\')
    user_id = log.get(\'user_id\') # Though not directly used in stats, good to have for context

    if not all([event_type, photo_id, isinstance(timestamp, (int, float))]):
        # Basic validation for required fields
        print(f"Skipping invalid log: {log}")
        return

    if event_type == 'upload_start':
        pending_buffer[photo_id] = {
            'start_time': timestamp,
            'user_id': user_id
        }
    elif event_type == 'upload_end':
        if photo_id in pending_buffer:
            start_info = pending_buffer[photo_id]
            start_time = start_info['start_time']
            
            if timestamp < start_time:
                # End time is before start time, invalid event order for this photo_id
                print(f"Warning: 'upload_end' for {photo_id} has timestamp {timestamp} before start_time {start_time}. Ignoring.")
                # Optionally, remove from pending_buffer if it indicates a data issue
                # del pending_buffer[photo_id]
                return

            upload_duration_ms = timestamp - start_time
            status = log.get(\'status\')

            if status == 'success':
                stats_aggregator['total_successful_uploads'] = stats_aggregator.get('total_successful_uploads', 0) + 1
                stats_aggregator['total_upload_time_ms'] = stats_aggregator.get('total_upload_time_ms', 0) + upload_duration_ms
                
                if stats_aggregator['total_successful_uploads'] > 0:
                    stats_aggregator['average_upload_time_ms'] = \
                        stats_aggregator['total_upload_time_ms'] / stats_aggregator['total_successful_uploads']
                else:
                    stats_aggregator['average_upload_time_ms'] = 0.0
            
            # Remove from buffer regardless of status, as the upload attempt has concluded
            del pending_buffer[photo_id]
        else:
            # 'upload_end' for a photo_id not in buffer, or already processed
            print(f"Warning: 'upload_end' for {photo_id} not found in pending_buffer or already processed. Log: {log}")

# Example Usage
if __name__ == "__main__":
    pending_uploads = {}
    upload_stats = {
        'total_successful_uploads': 0,
        'total_upload_time_ms': 0,
        'average_upload_time_ms': 0.0
    }

    logs = [
        {'event_type': 'upload_start', 'photo_id': 'p1', 'user_id': 'uA', 'timestamp': 1000},
        {'event_type': 'upload_start', 'photo_id': 'p2', 'user_id': 'uB', 'timestamp': 1002},
        {'event_type': 'upload_end', 'photo_id': 'p1', 'user_id': 'uA', 'timestamp': 1005, 'status': 'success'}, # p1: 5ms
        {'event_type': 'upload_end', 'photo_id': 'p2', 'user_id': 'uB', 'timestamp': 1010, 'status': 'failure'},
        {'event_type': 'upload_start', 'photo_id': 'p3', 'user_id': 'uA', 'timestamp': 1012},
        {'event_type': 'upload_end', 'photo_id': 'p3', 'user_id': 'uA', 'timestamp': 1022, 'status': 'success'}, # p3: 10ms
        {'event_type': 'upload_end', 'photo_id': 'p_orphan', 'user_id': 'uC', 'timestamp': 1025, 'status': 'success'}, # Orphan end
        {'event_type': 'upload_start', 'photo_id': 'p4', 'user_id': 'uD', 'timestamp': 1030},
        {'event_type': 'upload_end', 'photo_id': 'p4', 'user_id': 'uD', 'timestamp': 1033, 'status': 'success'}, # p4: 3ms
        # Test: start event after end event for same photo id (should be ignored by current logic)
        {'event_type': 'upload_start', 'photo_id': 'p5', 'user_id': 'uE', 'timestamp': 1040},
        {'event_type': 'upload_end', 'photo_id': 'p5', 'user_id': 'uE', 'timestamp': 1035, 'status': 'success'}, # Invalid: end before start
    ]

    expected_stats_sequence = [
        # After p1 success (duration 5ms)
        {'total_successful_uploads': 1, 'total_upload_time_ms': 5, 'average_upload_time_ms': 5.0},
        # After p2 failure (no change to success stats)
        {'total_successful_uploads': 1, 'total_upload_time_ms': 5, 'average_upload_time_ms': 5.0},
        # After p3 success (duration 10ms, total_time = 5+10=15, count=2, avg=7.5)
        {'total_successful_uploads': 2, 'total_upload_time_ms': 15, 'average_upload_time_ms': 7.5},
        # After p_orphan (no change, as no start)
        {'total_successful_uploads': 2, 'total_upload_time_ms': 15, 'average_upload_time_ms': 7.5},
        # After p4 success (duration 3ms, total_time = 15+3=18, count=3, avg=6.0)
        {'total_successful_uploads': 3, 'total_upload_time_ms': 18, 'average_upload_time_ms': 6.0},
        # After p5 invalid (no change)
        {'total_successful_uploads': 3, 'total_upload_time_ms': 18, 'average_upload_time_ms': 6.0},
    ]
    
    stat_idx = 0
    for i, log_entry in enumerate(logs):
        print(f"Processing log: {log_entry}")
        process_upload_log(log_entry, pending_uploads, upload_stats)
        print(f"Pending Buffer: {pending_uploads}")
        print(f"Upload Stats: {upload_stats}")
        
        # Check stats after events that are supposed to change them
        if log_entry['event_type'] == 'upload_end':
            # p_orphan and p5 (invalid end) don't have a prior start in this sequence for validation
            if log_entry['photo_id'] not in ['p_orphan', 'p5'] or \
               (log_entry['photo_id'] == 'p5' and log_entry['timestamp'] < pending_uploads.get('p5', {}).get('start_time', float('inf'))):
                 # The p5 condition is tricky here because it is removed after processing the invalid log. We are mainly interested in successful and failed valid pairs.
                pass # Covered by stat_idx logic

            # Compare with expected sequence
            if stat_idx < len(expected_stats_sequence):
                 current_expected_stats = expected_stats_sequence[stat_idx]
                 # We only assert if the photo_id from log is one that would lead to a change or defined state in expected_stats_sequence
                 # This is simplified; more robust testing would track specific photo_ids if needed.
                 
                 # This assertion focuses on the state *after* processing an 'upload_end'
                 # Check if this log should have updated stats
                 is_success_end = log_entry.get('status') == 'success' and log_entry['photo_id'] in ['p1', 'p2', 'p3', 'p4']
                 is_failure_end = log_entry.get('status') == 'failure' and log_entry['photo_id'] in ['p1', 'p2', 'p3', 'p4']
                 
                 # The expected_stats_sequence is designed to be checked after each 'upload_end' that *could* modify stats or represents a step.
                 # We advance stat_idx for p1(s), p2(f), p3(s), p_orphan(no_change), p4(s), p5(invalid_no_change)
                 print(f"Comparing with expected_stats_sequence[{stat_idx}]: {current_expected_stats}")
                 assert upload_stats == current_expected_stats, \
                     f"Stats mismatch after log {i+1} ({log_entry[\'photo_id\']}). Expected {current_expected_stats}, got {upload_stats}"
                 print(f"Assertion passed for log {i+1} ({log_entry[\'photo_id\']}).")
            stat_idx +=1
        print("---")

    print("Final Pending Buffer:", pending_uploads) # Should be empty if all starts had ends
    print("Final Upload Stats:", upload_stats)
    
    final_expected_stats = {'total_successful_uploads': 3, 'total_upload_time_ms': 18, 'average_upload_time_ms': 6.0}
    assert upload_stats == final_expected_stats, f"Final stats mismatch. Expected {final_expected_stats}, got {upload_stats}"
    assert not pending_uploads, f"Pending buffer is not empty: {pending_uploads}"

    print("All q009 tests passed!") 