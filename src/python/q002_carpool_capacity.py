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

Example Input:
ride_segments = [(0, 5, 2), (1, 3, 3), (6, 8, 1)]
max_capacity = 4
Expected Output: False
Explanation:
- Time 0: Pickup 2 (Capacity: 2/4)
- Time 1: Pickup 3 (Capacity: 2+3=5/4) -> Exceeds capacity

Example Input:
ride_segments = [(0, 5, 2), (0, 2, 1), (3, 6, 1)]
max_capacity = 3
Expected Output: True
Explanation:
- Time 0: Pickup 2 (Capacity: 2/3)
- Time 0: Pickup 1 (Capacity: 2+1=3/3)
- Time 2: Dropoff 1 (Capacity: 3-1=2/3)
- Time 3: Pickup 1 (Capacity: 2+1=3/3)
- Time 5: Dropoff 2 (Capacity: 3-2=1/3)
- Time 6: Dropoff 1 (Capacity: 1-1=0/3)

Example Input:
ride_segments = [(0, 10, 3), (0, 5, 2)] # Two segments starting at the same time
max_capacity = 4
Expected Output: False (at time 0, capacity becomes 3+2=5)
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
    events = []

    for start_time, end_time, num_passengers in ride_segments:
        events.append((start_time, 'pickup', num_passengers))
        events.append((end_time, 'dropoff', num_passengers))

    # Sort events by time, with dropoffs happening before pickups at the same time
    events.sort(key=lambda x: (x[0], 0 if x[1] == 'dropoff' else 1))

    current_occupancy = 0

    for time, event_type, passengers in events:
        if event_type == 'pickup':
            current_occupancy += passengers
        else:
            current_occupancy -= passengers
        
        if current_occupancy > max_capacity:
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

if __name__ == "__main__":
    test_can_vehicle_complete_rides_with_capacity() 