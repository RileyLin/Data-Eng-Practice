"""
Solution to Question 1.4.2 (Carpool Vehicle Capacity Check)

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
    
    Uses a sweep line algorithm to process pickup and dropoff events in chronological order.
    """
    if not ride_segments or max_capacity <= 0:
        return False
    
    # Create events for pickups and dropoffs
    events = []
    for start_time, end_time, num_passengers in ride_segments:
        events.append((start_time, 'pickup', num_passengers))
        events.append((end_time, 'dropoff', num_passengers))
    
    # Sort events by time, with dropoffs before pickups at the same time
    events.sort(key=lambda x: (x[0], 0 if x[1] == 'dropoff' else 1))
    
    current_capacity = 0
    for time, event_type, num_passengers in events:
        if event_type == 'pickup':
            current_capacity += num_passengers
            if current_capacity > max_capacity:
                return False
        else:  # dropoff
            current_capacity -= num_passengers
    
    return True

# Test cases
def test_can_vehicle_complete_rides_with_capacity():
    assert can_vehicle_complete_rides_with_capacity([(0, 5, 2), (1, 3, 3), (6, 8, 1)], 4) == False
    assert can_vehicle_complete_rides_with_capacity([(0, 5, 2), (0, 2, 1), (3, 6, 1)], 3) == True
    assert can_vehicle_complete_rides_with_capacity([(0, 10, 3), (0, 5, 2)], 4) == False
    print("All test cases passed!")

if __name__ == "__main__":
    test_can_vehicle_complete_rides_with_capacity() 