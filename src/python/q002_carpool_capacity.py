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


    if not ride_segments or max_capacity<=0:
        return False
    
    event = []

    for ride in ride_segments:

        event.append((ride[0],"pickup",ride[2]))
        event.append((ride[1],"dropoff",ride[2]))

    sortedride = sorted(event, key = lambda x:(x[0],0 if x[1]=="dropoff" else 1))

    current_capacity = 0
    for ride in sortedride:
        if ride[1] == "pickup":
            current_capacity+=ride[2]
            if current_capacity>max_capacity:
                return False
        elif ride[1]=="dropoff":
            current_capacity-=ride[2]
        
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

if __name__ == "__main__":
    test_can_vehicle_complete_rides_with_capacity() 