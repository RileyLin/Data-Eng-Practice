"""
Solution to Question 1.4.1 (Overlapping User Rides)
"""

def can_user_complete_rides(requested_rides):
    """
    Checks if a list of ride requests (start_time, end_time) for a single user overlap.
    
    Args:
        requested_rides: A list of tuples, where each tuple is (start_time, end_time).
                         Times are integers. Assumes end_time > start_time.
    
    Returns:
        True if no rides overlap, False otherwise.
    """
    # Edge case: if no rides, they can all be completed
    if not requested_rides:
        return True
    
    # Sort rides by start time to process in chronological order
    sorted_rides = sorted(requested_rides)
    
    # Keep track of the end time of the previous ride
    prev_end_time = sorted_rides[0][1]
    
    # Iterate through the remaining rides
    for i in range(1, len(sorted_rides)):
        current_start = sorted_rides[i][0]
        current_end = sorted_rides[i][1]
        
        # If current ride starts before previous ride ends, there's an overlap
        if current_start < prev_end_time:
            return False
        
        # Update previous end time
        prev_end_time = current_end
    
    # All rides can be completed
    return True

# Test cases
def test_can_user_complete_rides():
    assert can_user_complete_rides([(0, 30), (30, 60), (70, 90)]) == True
    assert can_user_complete_rides([(0, 60), (30, 90)]) == False
    assert can_user_complete_rides([(10, 20)]) == True
    assert can_user_complete_rides([]) == True
    print("All test cases passed!")

if __name__ == "__main__":
    test_can_user_complete_rides() 