"""
Question 1.4.2 (Carpool Vehicle Capacity Check):
You are given a list of ride segments for a single carpool vehicle. Each segment is
represented by a tuple `(start_time, end_time, num_passengers)`. The vehicle has a
maximum passenger capacity. Write a Python function
`can_vehicle_complete_rides_with_capacity(ride_segments, max_capacity)`
that returns `True` if all ride segments can be completed without exceeding the
vehicle's `max_capacity` at any point in time, and `False` otherwise.

Assume `start_time` is when passengers are picked up and `end_time` is when they are dropped off.
If a dropoff and a pickup happen at the exact same time, assume the dropoff occurs first.

DATA STRUCTURE EXAMPLES:

Input: ride_segments (List[Tuple[int, int, int]])
- Each tuple represents (start_time, end_time, num_passengers)
- start_time: when passengers are picked up (integer)
- end_time: when passengers are dropped off (integer)
- num_passengers: number of passengers for this segment (positive integer)

Input: max_capacity (int)
- Maximum number of passengers the vehicle can hold at any time

Example 1 - Capacity exceeded:
ride_segments = [(0, 5, 2), (1, 3, 3), (6, 8, 1)]
max_capacity = 4
Timeline:
Time 0: +2 passengers (total: 2/4) ✓
Time 1: +3 passengers (total: 5/4) ✗ EXCEEDS CAPACITY
Expected Output: False

Example 2 - Capacity respected:
ride_segments = [(0, 5, 2), (0, 2, 1), (3, 6, 1)]
max_capacity = 3
Timeline:
Time 0: +2 passengers (total: 2/3) ✓
Time 0: +1 passenger (total: 3/3) ✓
Time 2: -1 passenger (total: 2/3) ✓
Time 3: +1 passenger (total: 3/3) ✓
Time 5: -2 passengers (total: 1/3) ✓
Time 6: -1 passenger (total: 0/3) ✓
Expected Output: True

Example 3 - Simultaneous pickups exceeding capacity:
ride_segments = [(0, 10, 3), (0, 5, 2)]
max_capacity = 4
Timeline:
Time 0: +3 passengers (total: 3/4) ✓
Time 0: +2 passengers (total: 5/4) ✗ EXCEEDS CAPACITY
Expected Output: False

Example 4 - Simultaneous pickup/dropoff (dropoff first):
ride_segments = [(0, 5, 3), (5, 10, 2)]
max_capacity = 3
Timeline:
Time 5: -3 passengers (total: 0/3) ✓ (dropoff first)
Time 5: +2 passengers (total: 2/3) ✓
Expected Output: True

Example 5 - Empty input:
ride_segments = []
max_capacity = 4
Expected Output: False (edge case - no rides to complete)
"""

def can_vehicle_complete_rides_with_capacity(ride_segments, max_capacity):
    """
    Checks if a list of ride segments can be completed by a single vehicle 
    without exceeding its maximum passenger capacity.
    
    Args:
        ride_segments: A list of tuples, where each tuple is 
                      (start_time, end_time, num_passengers).
        max_capacity: An integer representing the maximum passenger capacity
                      of the vehicle.
                      
    Returns:
        True if all segments can be completed without exceeding capacity,
        False otherwise.
    """

    # put the list of tuples in to list of actions that I can clissfy and track current capacity


    if not ride_segments: 
        return False
    
    current_capacity = 0
    timeline = []

    for ride in ride_segments:

        timeline.append((ride[0],ride[2],'pickup'))
        timeline.append((ride[1],ride[2],'dropoff'))

    
    # Sort timeline by time, prioritizing dropoffs before pickups at same timestamp
    # This is more explicit using a separate function rather than a lambda
    def sort_key(event):
        time = event[0]
        event_type = event[2]
        # Standard pattern: return tuple with primary and secondary sort keys
        # Use -1 for dropoff so it comes before 1 for pickup
        return (time, -1 if event_type == 'dropoff' else 1)
        
    sorted_timeline = sorted(timeline, key=sort_key)

    for event in sorted_timeline: 

        if event[2]=='dropoff':

            current_capacity-=event[1]
        elif event[2]=='pickup':
            current_capacity+=event[1]
        
        if current_capacity>max_capacity:
            return False
        
    return True
    


                             
                        




# Test cases
def test_can_vehicle_complete_rides_with_capacity():
    # Test case 1: Should exceed capacity at time 1
    assert can_vehicle_complete_rides_with_capacity([(0, 5, 2), (1, 3, 3), (6, 8, 1)], 4) == False
    
    # Test case 2: Should be exactly at capacity but never exceed it
    assert can_vehicle_complete_rides_with_capacity([(0, 5, 2), (0, 2, 1), (3, 6, 1)], 3) == True
    
    # Test case 3: Should exceed capacity at time 0
    assert can_vehicle_complete_rides_with_capacity([(0, 10, 3), (0, 5, 2)], 4) == False
    
    print("All test cases passed!")

def can_vehicle_complete_rides_with_capacity_dict(ride_segments, max_capacity):
    """
    Variation: Accepts ride_segments as a list of dicts and returns (bool, max_passengers).
    Each dict: {'start': int, 'end': int, 'passengers': int}
    Returns (True/False, max_passengers_seen)
    """

    if not ride_segments or max_capacity<=0:
        return (False,0)
    
    all_segments = []
    
    for segment in ride_segments: 

        all_segments.append((segment['start'],'pickup',segment['passengers']))
        all_segments.append((segment['end'],'dropoff',segment['passengers']))

    current_capacity = 0
    max_num = 0

    sorted_segments = sorted(all_segments,key = lambda x:(x[0],0 if x[1]=='dropoff' else 1))
    
    for segment in sorted_segments:
        
        if segment[1]=='pickup':
            current_capacity+=segment[2]
        elif segment[1]=='dropoff':
            current_capacity-=segment[2]
        max_num= max(max_num,current_capacity)

        if current_capacity>max_capacity:
            print((False,max_num))
            return (False,max_num)

    print(max_num)
    return (True,max_num)




# New test cases for the variation

def test_can_vehicle_complete_rides_with_capacity_dict():
    # Test 1: Exceeds capacity
    rides = [
        {'start': 0, 'end': 5, 'passengers': 2},
        {'start': 1, 'end': 3, 'passengers': 3},
        {'start': 6, 'end': 8, 'passengers': 1}
    ]
    assert can_vehicle_complete_rides_with_capacity_dict(rides, 4) == (False, 5)

    # Test 2: Exactly at capacity
    rides = [
        {'start': 0, 'end': 5, 'passengers': 2},
        {'start': 0, 'end': 2, 'passengers': 1},
        {'start': 3, 'end': 6, 'passengers': 1}
    ]
    assert can_vehicle_complete_rides_with_capacity_dict(rides, 3) == (True, 3)

    # Test 3: Simultaneous pickup/dropoff
    rides = [
        {'start': 0, 'end': 5, 'passengers': 3},
        {'start': 5, 'end': 10, 'passengers': 2}
    ]
    assert can_vehicle_complete_rides_with_capacity_dict(rides, 3) == (True, 3)

    # Test 4: Empty input
    rides = []
    assert can_vehicle_complete_rides_with_capacity_dict(rides, 4) == (False, 0)

    # Test 5: Negative/zero capacity
    rides = [
        {'start': 0, 'end': 1, 'passengers': 1}
    ]
    assert can_vehicle_complete_rides_with_capacity_dict(rides, 0) == (False, 0)

    print("All dict-based test cases passed!")

if __name__ == "__main__":
    test_can_vehicle_complete_rides_with_capacity()
    #test_can_vehicle_complete_rides_with_capacity_dict() 