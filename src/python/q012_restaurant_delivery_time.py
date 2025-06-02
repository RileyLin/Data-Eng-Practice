"""
Question 12: DoorDash Food Delivery Time Calculation

You are given two inputs to calculate the delivery time for each order:

1. A list of dictionaries representing driver actions, where each dict contains:
   - location: string (location identifier)
   - order_no: string (order number, only present for 'pick_up' and 'drop_off' actions)
   - action_type: string ('pick_up', 'travel', 'drop_off')
   - driver: string (driver identifier)

2. A 2D matrix representing travel times between locations

Key Points:
- When action_type is 'travel', there is NO order_no in the record
- A driver can pick up multiple orders before dropping them off
- ALL time between picking up an order and dropping it off counts toward that order's delivery time
- Print results as: "order xx is delivered within xxx mins"
- Print in order number sequence

Example:
Driver picks up order_1 at location A, travels to B to pick up order_2, 
then travels to C to drop off order_1. The travel time from A→B also counts 
toward order_1's delivery time since the driver was carrying it.
"""

def calculate_delivery_times(actions, travel_matrix, location_mapping):
    """
    Calculate delivery times for each order based on driver actions.
    
    Args:
        actions: List[Dict] - driver action records
        travel_matrix: List[List[int]] - travel times between locations  
        location_mapping: Dict[str, int] - maps location names to matrix indices
    
    Prints:
        "order xx is delivered within xxx mins" for each order, sorted by order number
    """
    # TODO: Implement the delivery time calculation
    # 
    # Algorithm:
    # 1. Group actions by driver to process each driver's timeline separately
    # 2. For each driver, track:
    #    - Current location and time
    #    - Orders currently being carried
    #    - Pickup time for each order
    # 3. Process actions sequentially:
    #    - For 'travel': calculate travel time and update all carried orders
    #    - For 'pick_up': record order pickup time and add to carried orders
    #    - For 'drop_off': calculate total delivery time and remove from carried orders
    # 4. Sort results by order number and print


    if not actions: 
        return 
    
    driver_timeline = {}

    for action in actions:
        driver = action['driver']

        if driver not in driver_timeline:
            driver_timeline[driver]=[]

        driver_timeline[driver].append(action)

    all_delivery ={}

    for d, driver_actions in driver_timeline.items():

        carrying_orders = {}

        current_time = 0
        current_location = None

        for action in driver_actions:
            order_no = action.get('order_no')

            action_type = action.get('action_type')

            location = action.get('location')

            if current_location is not None and current_location!=location: 
                from_idx = location_mapping[current_location]
                to_idx = location_mapping[location]

                time_spent = travel_matrix[from_idx][to_idx]

                current_time+=time_spent
            
            current_location = location

            if action_type == 'pick_up':
                carrying_orders[order_no] = current_time

            if action_type == 'drop_off':
                total_time = current_time - carrying_orders[order_no]

                all_delivery[order_no]= total_time

                del carrying_orders[order_no]

        
    sorted_order_no = sorted(all_delivery.keys())

    for order in sorted_order_no:
        print(f"{order} is delivered with in {all_delivery[order]}")



def test_calculate_delivery_times():
    """Test the delivery time calculation with various scenarios"""
    
    # Test Case 1: Single driver with two orders
    actions1 = [
        {'location': 'A', 'order_no': 'order_1', 'action_type': 'pick_up', 'driver': 'driver_1'},
        {'location': 'B', 'action_type': 'travel', 'driver': 'driver_1'},  # No order_no
        {'location': 'B', 'order_no': 'order_2', 'action_type': 'pick_up', 'driver': 'driver_1'},
        {'location': 'C', 'action_type': 'travel', 'driver': 'driver_1'},  # No order_no
        {'location': 'C', 'order_no': 'order_1', 'action_type': 'drop_off', 'driver': 'driver_1'},
        {'location': 'D', 'action_type': 'travel', 'driver': 'driver_1'},  # No order_no
        {'location': 'D', 'order_no': 'order_2', 'action_type': 'drop_off', 'driver': 'driver_1'}
    ]
    
    travel_matrix1 = [
        [0, 5, 10, 15],  # From A to [A, B, C, D]
        [5, 0, 8, 12],   # From B to [A, B, C, D]  
        [10, 8, 0, 6],   # From C to [A, B, C, D]
        [15, 12, 6, 0]   # From D to [A, B, C, D]
    ]
    
    location_mapping1 = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    
    print("Test Case 1: Single driver, multiple orders")
    calculate_delivery_times(actions1, travel_matrix1, location_mapping1)
    print()
    
    # Test Case 2: Multiple drivers
    actions2 = [
        {'location': 'A', 'order_no': 'order_3', 'action_type': 'pick_up', 'driver': 'driver_1'},
        {'location': 'B', 'order_no': 'order_4', 'action_type': 'pick_up', 'driver': 'driver_2'},
        {'location': 'C', 'action_type': 'travel', 'driver': 'driver_1'},  # No order_no
        {'location': 'A', 'action_type': 'travel', 'driver': 'driver_2'},  # No order_no
        {'location': 'C', 'order_no': 'order_3', 'action_type': 'drop_off', 'driver': 'driver_1'},
        {'location': 'A', 'order_no': 'order_4', 'action_type': 'drop_off', 'driver': 'driver_2'}
    ]
    
    print("Test Case 2: Multiple drivers")
    calculate_delivery_times(actions2, travel_matrix1, location_mapping1)
    print()

if __name__ == "__main__":
    test_calculate_delivery_times() 