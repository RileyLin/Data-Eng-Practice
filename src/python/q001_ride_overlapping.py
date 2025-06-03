"""
Question 1.4.1 (Overlapping User Rides):
A user wants to book multiple rides for themselves. Given a list of
requested rides, where each ride is a tuple `(start_time, end_time)`
with integer times, write a Python function
`can_user_complete_rides(requested_rides)` that returns `True` if the user
can theoretically complete all their requested rides (i.e., none of their
own rides overlap), and `False` otherwise.

DATA STRUCTURE EXAMPLES:

Input: requested_rides (List[Tuple[int, int]])
- Each tuple represents (start_time, end_time) for a single ride
- Times are integers (could represent minutes, hours, etc.)
- end_time > start_time for valid rides

Example 1 - Non-overlapping rides:
requested_rides = [(0, 30), (30, 60), (70, 90)]
Visualization:
Time:  0    30   60   70   90
       |----| |----| |----| 
       Ride1  Ride2  Ride3
Expected Output: True

Example 2 - Overlapping rides:
requested_rides = [(0, 60), (30, 90)]
Visualization:
Time:  0    30   60   90
       |---------|
            |---------|
           Ride1  Ride2 (overlap from 30-60)
Expected Output: False

Example 3 - Single ride:
requested_rides = [(10, 20)]
Expected Output: True

Example 4 - Empty list:
requested_rides = []
Expected Output: True

Example 5 - Edge case (rides touching but not overlapping):
requested_rides = [(0, 30), (30, 60)]
Visualization:
Time:  0    30   60
       |----||----| 
       Ride1 Ride2 (touching at time 30, but not overlapping)
Expected Output: True

Follow-up consideration: How would this problem change if we were considering 
a single carpool vehicle with a limited passenger capacity (e.g., 6 passengers), 
and the input was a list of ride segments for *different* users wanting to share 
that vehicle?
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
    if not requested_rides:
        return True 
    
    sorted_rides = sorted(requested_rides, key = lambda x:x[0])

    previous_end_time = 0

    for ride in sorted_rides:

        if ride[0]<previous_end_time: 
            return False
        
        previous_end_time = ride[1]

    return True


def can_user_complete_rides_with_conflicts(requested_rides):
    """
    Variation: Accepts ride requests as list of dicts and returns (bool, conflicting_ride_ids).
    Each dict: {'id': int, 'start': int, 'end': int, 'type': str}
    Returns (True/False, list_of_conflicting_ride_ids)
    """
    if not requested_rides:
        return (True, [])
    
    conflict_ids = set()
    sorted_rides = sorted(requested_rides, key=lambda x: x['start'])
    
    previous_end_time = 0
    previous_ride = None
    
    for ride in sorted_rides:
        if ride['start'] < previous_end_time:
            # Current ride conflicts with previous ride
            conflict_ids.add(ride['id'])
            if previous_ride:
                conflict_ids.add(previous_ride['id'])
        
        # Update previous_end_time to the maximum end time seen so far
        if ride['end'] > previous_end_time:
            previous_end_time = ride['end']
            previous_ride = ride
    
    # Return (can_complete, conflicting_ids)
    return (len(conflict_ids) == 0, sorted(list(conflict_ids)))

def get_ride_schedule_summary(requested_rides):
    """
    Bonus variation: Returns detailed scheduling information.
    Input: List of dicts with {'id', 'start', 'end', 'type'}
    Returns: Dict with scheduling analysis
    """
    if not requested_rides:
        return {'can_complete': True, 'total_time': 0, 'conflicts': [], 'ride_count': 0}
    
    can_complete, conflicts = can_user_complete_rides_with_conflicts(requested_rides)
    
    total_time = sum(ride['end'] - ride['start'] for ride in requested_rides)
    ride_types = {}
    
    for ride in requested_rides:
        ride_type = ride.get('type', 'unknown')
        ride_types[ride_type] = ride_types.get(ride_type, 0) + 1
    
    return {
        'can_complete': can_complete,
        'total_time': total_time,
        'conflicts': conflicts,
        'ride_count': len(requested_rides),
        'ride_types': ride_types
    }

# Test cases
def test_can_user_complete_rides():
    assert can_user_complete_rides([(0, 30), (30, 60), (70, 90)]) == True
    assert can_user_complete_rides([(0, 60), (30, 90)]) == False
    assert can_user_complete_rides([(10, 20)]) == True
    assert can_user_complete_rides([]) == True
    print("All test cases passed!")

# Test cases for variations

def test_can_user_complete_rides_with_conflicts():
    # Test 1: No conflicts
    rides = [
        {'id': 1, 'start': 0, 'end': 30, 'type': 'regular'},
        {'id': 2, 'start': 30, 'end': 60, 'type': 'regular'},
        {'id': 3, 'start': 70, 'end': 90, 'type': 'premium'}
    ]
    assert can_user_complete_rides_with_conflicts(rides) == (True, [])
    
    # Test 2: Two rides overlap
    rides = [
        {'id': 1, 'start': 0, 'end': 60, 'type': 'regular'},
        {'id': 2, 'start': 30, 'end': 90, 'type': 'premium'}
    ]
    assert can_user_complete_rides_with_conflicts(rides) == (False, [1, 2])
    
    # Test 3: Multiple conflicts
    rides = [
        {'id': 1, 'start': 0, 'end': 50, 'type': 'regular'},
        {'id': 2, 'start': 25, 'end': 75, 'type': 'premium'},
        {'id': 3, 'start': 60, 'end': 100, 'type': 'regular'},
        {'id': 4, 'start': 80, 'end': 120, 'type': 'premium'}
    ]
    assert can_user_complete_rides_with_conflicts(rides) == (False, [2, 3, 4])
    
    # Test 4: Empty input
    rides = []
    assert can_user_complete_rides_with_conflicts(rides) == (True, [])
    
    # Test 5: Single ride
    rides = [{'id': 1, 'start': 10, 'end': 20, 'type': 'regular'}]
    assert can_user_complete_rides_with_conflicts(rides) == (True, [])
    
    print("All conflict detection test cases passed!")

def test_get_ride_schedule_summary():
    # Test 1: Normal case with no conflicts
    rides = [
        {'id': 1, 'start': 0, 'end': 30, 'type': 'regular'},
        {'id': 2, 'start': 30, 'end': 60, 'type': 'premium'},
        {'id': 3, 'start': 70, 'end': 90, 'type': 'regular'}
    ]
    result = get_ride_schedule_summary(rides)
    expected = {
        'can_complete': True,
        'total_time': 80,  # 30 + 30 + 20
        'conflicts': [],
        'ride_count': 3,
        'ride_types': {'regular': 2, 'premium': 1}
    }
    assert result == expected
    
    # Test 2: With conflicts
    rides = [
        {'id': 1, 'start': 0, 'end': 60, 'type': 'regular'},
        {'id': 2, 'start': 30, 'end': 90, 'type': 'premium'}
    ]
    result = get_ride_schedule_summary(rides)
    expected = {
        'can_complete': False,
        'total_time': 120,  # 60 + 60
        'conflicts': [1, 2],
        'ride_count': 2,
        'ride_types': {'regular': 1, 'premium': 1}
    }
    assert result == expected
    
    # Test 3: Empty input
    result = get_ride_schedule_summary([])
    expected = {
        'can_complete': True,
        'total_time': 0,
        'conflicts': [],
        'ride_count': 0,
        'ride_types': {}
    }
    assert result == expected
    
    print("All schedule summary test cases passed!")

if __name__ == "__main__":
    test_can_user_complete_rides()
    test_can_user_complete_rides_with_conflicts()
    test_get_ride_schedule_summary() 