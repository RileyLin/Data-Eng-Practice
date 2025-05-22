"""
Solution to Question 1.4.2 (Carpool Vehicle Capacity Check)
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

    # Create events for pickups and dropoffs
    for start_time, end_time, num_passengers in ride_segments:
        events.append((start_time, 'pickup', num_passengers))
        events.append((end_time, 'dropoff', num_passengers))

    # Sort events by time, with dropoffs happening before pickups at the same time
    events.sort(key=lambda x: (x[0], 0 if x[1] == 'dropoff' else 1))

    current_occupancy = 0

    # Process events in order
    for time, event_type, passengers in events:
        if event_type == 'pickup':
            current_occupancy += passengers
        else:
            current_occupancy -= passengers
        
        # Check if capacity is exceeded after each event
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