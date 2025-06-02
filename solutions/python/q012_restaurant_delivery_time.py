"""
Question 12: DoorDash Food Delivery Time Calculation - SOLUTION

This problem requires tracking driver movements and calculating total delivery time
for each order from pickup to dropoff, including all intermediate travel time.

Key insights:
1. Group actions by driver (each driver has independent timeline)
2. Track current location and time for each driver
3. Calculate travel time when location changes
4. For orders being carried, accumulate all travel time until dropoff
5. Sort output by order number

Time Complexity: O(n + m log m) where n is actions, m is unique orders
Space Complexity: O(m + d) where m is orders, d is drivers

DATA STRUCTURE EXAMPLES:

Input: actions (List[Dict])
- Structure: [{'location': str, 'order_no': str (optional), 'action_type': str, 'driver': str}, ...]
- action_type values: 'pick_up', 'travel', 'drop_off'
- order_no: only present for 'pick_up' and 'drop_off' actions

Example action dictionaries:
- Pickup action: {'location': 'A', 'order_no': 'order_1', 'action_type': 'pick_up', 'driver': 'driver_1'}
- Travel action: {'location': 'B', 'action_type': 'travel', 'driver': 'driver_1'}  # No order_no
- Dropoff action: {'location': 'C', 'order_no': 'order_1', 'action_type': 'drop_off', 'driver': 'driver_1'}

Input: travel_matrix (List[List[int]])
- Structure: 2D matrix where travel_matrix[i][j] = travel time from location i to location j
- Indices correspond to location_mapping values
- Diagonal elements are 0 (no travel time to same location)

Example travel_matrix:
travel_matrix = [
    [0, 5, 10, 15],  # From A (index 0) to [A, B, C, D]
    [5, 0, 8, 12],   # From B (index 1) to [A, B, C, D]
    [10, 8, 0, 6],   # From C (index 2) to [A, B, C, D]
    [15, 12, 6, 0]   # From D (index 3) to [A, B, C, D]
]

Input: location_mapping (Dict[str, int])
- Structure: {location_name: matrix_index}
- Maps location strings to travel_matrix indices

Example location_mapping:
location_mapping = {'A': 0, 'B': 1, 'C': 2, 'D': 3}

DETAILED SCENARIO WALKTHROUGH:

Scenario: Single driver picks up two orders and delivers them

Actions sequence:
1. {'location': 'A', 'order_no': 'order_1', 'action_type': 'pick_up', 'driver': 'driver_1'}
2. {'location': 'A', 'action_type': 'travel', 'driver': 'driver_1'}
3. {'location': 'B', 'order_no': 'order_2', 'action_type': 'pick_up', 'driver': 'driver_1'}
4. {'location': 'B', 'action_type': 'travel', 'driver': 'driver_1'}
5. {'location': 'C', 'order_no': 'order_1', 'action_type': 'drop_off', 'driver': 'driver_1'}
6. {'location': 'C', 'action_type': 'travel', 'driver': 'driver_1'}
7. {'location': 'D', 'order_no': 'order_2', 'action_type': 'drop_off', 'driver': 'driver_1'}

Timeline Processing:
Time 0: Pick up order_1 at A
Time 0→5: Travel A to B (5 mins)
Time 5: Pick up order_2 at B
Time 5→13: Travel B to C (8 mins)
Time 13: Drop off order_1 at C (total time for order_1: 13 mins)
Time 13→19: Travel C to D (6 mins)
Time 19: Drop off order_2 at D (total time for order_2: 19 - 5 = 14 mins)

MULTIPLE DRIVERS SCENARIO:

Actions for multiple drivers:
[
    {'location': 'A', 'order_no': 'order_3', 'action_type': 'pick_up', 'driver': 'driver_1'},
    {'location': 'B', 'order_no': 'order_4', 'action_type': 'pick_up', 'driver': 'driver_2'},
    {'location': 'A', 'action_type': 'travel', 'driver': 'driver_1'},
    {'location': 'B', 'action_type': 'travel', 'driver': 'driver_2'},
    {'location': 'C', 'order_no': 'order_3', 'action_type': 'drop_off', 'driver': 'driver_1'},
    {'location': 'A', 'order_no': 'order_4', 'action_type': 'drop_off', 'driver': 'driver_2'}
]

Processing:
- driver_1: picks up order_3 at A, travels to C, drops off order_3
- driver_2: picks up order_4 at B, travels to A, drops off order_4

EDGE CASES TO CONSIDER:

1. Driver stays at same location (no travel time added)
2. Multiple orders carried simultaneously
3. Orders dropped off in different sequence than picked up
4. Multiple drivers working independently
5. Travel actions without corresponding location changes
6. Missing pickup or dropoff actions

OUTPUT FORMAT:
The function should print results in order number sequence:
"order_1 is delivered within 15 mins"
"order_2 is delivered within 20 mins"

ALGORITHM APPROACH:
1. Group actions by driver to create individual timelines
2. For each driver, process actions sequentially:
   - Track current location and time
   - Calculate travel time when location changes
   - Record pickup times for orders
   - Calculate delivery time when orders are dropped off
3. Sort results by order number and print

IMPLEMENTATION NOTES:
- The timeline approach is more robust than trying to process all actions globally
- Each driver operates independently with their own timeline
- Travel time is only added when location actually changes
- Orders can be carried simultaneously and dropped off in any order
"""

def calculate_delivery_times(actions, travel_matrix, location_mapping):
    """
    Calculate and print delivery times for each order based on driver actions.
    
    Args:
        actions: List[Dict] - driver action records
        travel_matrix: List[List[int]] - travel times between locations  
        location_mapping: Dict[str, int] - maps location names to matrix indices
    
    Prints:
        "order xx is delivered within xxx mins" for each order, sorted by order number
    """
    # Group actions by driver to create individual timelines
    driver_timelines = {}
    for action in actions:
        driver = action['driver']
        if driver not in driver_timelines:
            driver_timelines[driver] = []
        driver_timelines[driver].append(action)
    
    # Process each driver's timeline independently
    all_delivery_times = {}
    
    for driver, timeline in driver_timelines.items():
        current_location = None
        current_time = 0
        carrying_orders = {}  # order_no -> pickup_time
        
        for action in timeline:
            location = action['location']
            action_type = action['action_type']
            
            # Calculate travel time if location changed
            if current_location is not None and current_location != location:
                from_idx = location_mapping[current_location]
                to_idx = location_mapping[location]
                travel_time = travel_matrix[from_idx][to_idx]
                current_time += travel_time
            
            current_location = location
            
            if action_type == 'pick_up':
                order_no = action['order_no']
                carrying_orders[order_no] = current_time
                
            elif action_type == 'drop_off':
                order_no = action['order_no']
                if order_no in carrying_orders:
                    pickup_time = carrying_orders[order_no]
                    delivery_time = current_time - pickup_time
                    all_delivery_times[order_no] = delivery_time
                    del carrying_orders[order_no]
    
    # Print results in order number sequence
    sorted_orders = sorted(all_delivery_times.keys())
    for order_no in sorted_orders:
        delivery_time = all_delivery_times[order_no]
        print(f"{order_no} is delivered within {delivery_time} mins")

def test_calculate_delivery_times():
    """Test the delivery time calculation with various scenarios"""
    
    # Test Case 1: Single driver with two orders
    print("Test Case 1: Single driver, multiple orders")
    actions1 = [
        {'location': 'A', 'order_no': 'order_1', 'action_type': 'pick_up', 'driver': 'driver_1'},
        {'location': 'B', 'action_type': 'travel', 'driver': 'driver_1'},
        {'location': 'B', 'order_no': 'order_2', 'action_type': 'pick_up', 'driver': 'driver_1'},
        {'location': 'C', 'action_type': 'travel', 'driver': 'driver_1'},
        {'location': 'C', 'order_no': 'order_1', 'action_type': 'drop_off', 'driver': 'driver_1'},
        {'location': 'D', 'action_type': 'travel', 'driver': 'driver_1'},
        {'location': 'D', 'order_no': 'order_2', 'action_type': 'drop_off', 'driver': 'driver_1'}
    ]
    
    travel_matrix1 = [
        [0, 5, 10, 15],  # From A to [A, B, C, D]
        [5, 0, 8, 12],   # From B to [A, B, C, D]  
        [10, 8, 0, 6],   # From C to [A, B, C, D]
        [15, 12, 6, 0]   # From D to [A, B, C, D]
    ]
    
    location_mapping1 = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    
    calculate_delivery_times(actions1, travel_matrix1, location_mapping1)
    print()
    
    # Test Case 2: Multiple drivers
    print("Test Case 2: Multiple drivers")
    actions2 = [
        {'location': 'A', 'order_no': 'order_3', 'action_type': 'pick_up', 'driver': 'driver_1'},
        {'location': 'B', 'order_no': 'order_4', 'action_type': 'pick_up', 'driver': 'driver_2'},
        {'location': 'C', 'action_type': 'travel', 'driver': 'driver_1'},
        {'location': 'A', 'action_type': 'travel', 'driver': 'driver_2'},
        {'location': 'C', 'order_no': 'order_3', 'action_type': 'drop_off', 'driver': 'driver_1'},
        {'location': 'A', 'order_no': 'order_4', 'action_type': 'drop_off', 'driver': 'driver_2'}
    ]
    
    calculate_delivery_times(actions2, travel_matrix1, location_mapping1)
    print()

def algorithm_walkthrough():
    """
    Demonstrates the algorithm step-by-step for interview understanding.
    """
    print("🚀 ALGORITHM WALKTHROUGH")
    print("="*50)
    
    print("\nKey Insight: Process each driver independently")
    print("Each driver has their own timeline and carries multiple orders")
    
    print("\nStep-by-step for single driver scenario:")
    print("1. Driver starts at A, picks up order_1 (time: 0)")
    print("2. Travel A→B (5 mins), now at time 5")
    print("3. Pick up order_2 at B (still time 5)")
    print("4. Travel B→C (8 mins), now at time 13") 
    print("5. Drop off order_1 at C (delivery time: 13-0 = 13 mins)")
    print("6. Travel C→D (6 mins), now at time 19")
    print("7. Drop off order_2 at D (delivery time: 19-5 = 14 mins)")
    
    print("\nOutput:")
    print("order_1 is delivered within 13 mins")
    print("order_2 is delivered within 14 mins")

if __name__ == "__main__":
    test_calculate_delivery_times()
    print()
    algorithm_walkthrough() 