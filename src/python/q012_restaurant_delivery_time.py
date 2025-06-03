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

    '''
    {driver1: [action,action],}
    '''

    if not actions: 
        return 
    
    driver_timeline = {}

    for action in actions: 

        driver = action['driver']

        if driver not in driver_timeline:
            driver_timeline[driver] = []

        driver_timeline[driver].append(action)

    
    all_deliveries_time ={}
    
    for driver, all_actions in driver_timeline.items():

        current_location = None
        current_time = 0
        carrying_orders = {}
        for action in all_actions:
            order_no = action.get('order_no')
            location = action.get('location')
            action_type = action.get('action_type')

            if current_location is not None and current_location!=location:

                from_idx = location_mapping[current_location]
                to_idx = location_mapping[location]

                time_spent = travel_matrix[from_idx][to_idx]

                current_time +=time_spent

            current_location = location

            if action_type =='pick_up':
                carrying_orders[order_no]=current_time

            elif action_type =='drop_off':
                total_time = current_time -carrying_orders[order_no]
                all_deliveries_time[order_no]= total_time
                del carrying_orders[order_no]


    ordered_deliveries = sorted(all_deliveries_time.keys())
    
    for order_no in ordered_deliveries:

        print(f"{order_no} is delivered within {all_deliveries_time[order_no]}")



        








    



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

def calculate_delivery_statistics_tuple_input(action_tuples, location_distances):
    """
    Variation 1: Calculate delivery statistics using tuple input format and return detailed stats.
    
    Args:
        action_tuples: List[Tuple] - each tuple is (driver, location, action_type, order_no_or_none)
        location_distances: Dict[Tuple[str, str], int] - maps (from_loc, to_loc) to travel time
    
    Returns:
        Dict with keys: 'delivery_times', 'average_time', 'max_time', 'total_orders'
    """
    if not action_tuples:
        return {'delivery_times': {}, 'average_time': 0, 'max_time': 0, 'total_orders': 0}
    
    # Group by driver
    driver_timelines = {}
    for driver, location, action_type, order_no in action_tuples:
        if driver not in driver_timelines:
            driver_timelines[driver] = []
        driver_timelines[driver].append((location, action_type, order_no))
    
    all_delivery_times = {}
    
    for driver, timeline in driver_timelines.items():
        current_location = None
        current_time = 0
        carrying_orders = {}
        
        for location, action_type, order_no in timeline:
            # Calculate travel time if location changed
            if current_location and current_location != location:
                travel_key = (current_location, location)
                if travel_key in location_distances:
                    current_time += location_distances[travel_key]
            
            current_location = location
            
            if action_type == 'pick_up' and order_no:
                carrying_orders[order_no] = current_time
            elif action_type == 'drop_off' and order_no:
                if order_no in carrying_orders:
                    delivery_time = current_time - carrying_orders[order_no]
                    all_delivery_times[order_no] = delivery_time
                    del carrying_orders[order_no]
    
    # Calculate statistics
    if all_delivery_times:
        times = list(all_delivery_times.values())
        avg_time = sum(times) / len(times)
        max_time = max(times)
    else:
        avg_time = max_time = 0
    
    return {
        'delivery_times': all_delivery_times,
        'average_time': round(avg_time, 2),
        'max_time': max_time,
        'total_orders': len(all_delivery_times)
    }

def calculate_driver_performance_metrics(driver_schedules, distance_graph):
    """
    Variation 2: Calculate comprehensive driver performance using graph input.
    
    Args:
        driver_schedules: Dict[str, List[Dict]] - maps driver_id to list of events
                         Each event: {'time': int, 'location': str, 'event': str, 'order': str}
        distance_graph: Dict[str, Dict[str, int]] - adjacency list with distances
    
    Returns:
        Dict[str, Dict] - performance metrics per driver
    """
    driver_metrics = {}
    
    for driver_id, schedule in driver_schedules.items():
        # Sort events by time
        sorted_schedule = sorted(schedule, key=lambda x: x['time'])
        
        total_distance = 0
        total_time = 0
        orders_delivered = 0
        current_location = None
        active_orders = set()
        order_pickup_times = {}
        delivery_times = []
        
        for event in sorted_schedule:
            location = event['location']
            event_type = event['event']
            order_id = event.get('order')
            event_time = event['time']
            
            # Calculate travel distance if location changed
            if current_location and current_location != location:
                if current_location in distance_graph and location in distance_graph[current_location]:
                    travel_distance = distance_graph[current_location][location]
                    total_distance += travel_distance
            
            current_location = location
            total_time = max(total_time, event_time)
            
            if event_type == 'pickup' and order_id:
                active_orders.add(order_id)
                order_pickup_times[order_id] = event_time
            elif event_type == 'delivery' and order_id:
                if order_id in active_orders:
                    delivery_time = event_time - order_pickup_times[order_id]
                    delivery_times.append(delivery_time)
                    active_orders.remove(order_id)
                    orders_delivered += 1
        
        # Calculate efficiency metrics
        avg_delivery_time = sum(delivery_times) / len(delivery_times) if delivery_times else 0
        orders_per_hour = (orders_delivered / total_time * 60) if total_time > 0 else 0
        
        driver_metrics[driver_id] = {
            'total_distance': total_distance,
            'total_time': total_time,
            'orders_delivered': orders_delivered,
            'average_delivery_time': round(avg_delivery_time, 2),
            'orders_per_hour': round(orders_per_hour, 2),
            'distance_per_order': round(total_distance / orders_delivered, 2) if orders_delivered > 0 else 0
        }
    
    return driver_metrics

# Test functions for variations

def test_calculate_delivery_statistics_tuple_input():
    """Test the tuple-based delivery statistics calculation"""
    
    print("Variation 1 Test: Tuple input format")
    
    # Test data as tuples: (driver, location, action_type, order_no_or_none)
    action_tuples = [
        ('driver_1', 'A', 'pick_up', 'order_1'),
        ('driver_1', 'B', 'travel', None),
        ('driver_1', 'B', 'pick_up', 'order_2'),
        ('driver_1', 'C', 'travel', None),
        ('driver_1', 'C', 'drop_off', 'order_1'),
        ('driver_1', 'D', 'travel', None),
        ('driver_1', 'D', 'drop_off', 'order_2')
    ]
    
    # Distance mapping as dict of tuples
    location_distances = {
        ('A', 'B'): 5,
        ('B', 'C'): 8,
        ('C', 'D'): 6,
        ('A', 'C'): 10,
        ('B', 'D'): 12
    }
    
    result = calculate_delivery_statistics_tuple_input(action_tuples, location_distances)
    print(f"Result: {result}")
    
    # Print individual delivery times
    for order, time in sorted(result['delivery_times'].items()):
        print(f"{order} delivered in {time} minutes")
    
    print(f"Average delivery time: {result['average_time']} minutes")
    print(f"Maximum delivery time: {result['max_time']} minutes")
    print()

def test_calculate_driver_performance_metrics():
    """Test the driver performance metrics calculation"""
    
    print("Variation 2 Test: Driver performance metrics")
    
    # Driver schedules with explicit timestamps
    driver_schedules = {
        'driver_1': [
            {'time': 0, 'location': 'A', 'event': 'pickup', 'order': 'order_1'},
            {'time': 5, 'location': 'B', 'event': 'pickup', 'order': 'order_2'},
            {'time': 13, 'location': 'C', 'event': 'delivery', 'order': 'order_1'},
            {'time': 19, 'location': 'D', 'event': 'delivery', 'order': 'order_2'}
        ],
        'driver_2': [
            {'time': 0, 'location': 'B', 'event': 'pickup', 'order': 'order_3'},
            {'time': 12, 'location': 'A', 'event': 'delivery', 'order': 'order_3'}
        ]
    }
    
    # Distance graph (adjacency list format)
    distance_graph = {
        'A': {'B': 5, 'C': 10, 'D': 15},
        'B': {'A': 5, 'C': 8, 'D': 12},
        'C': {'A': 10, 'B': 8, 'D': 6},
        'D': {'A': 15, 'B': 12, 'C': 6}
    }
    
    metrics = calculate_driver_performance_metrics(driver_schedules, distance_graph)
    
    for driver_id, stats in metrics.items():
        print(f"{driver_id} Performance:")
        print(f"  Total distance: {stats['total_distance']} units")
        print(f"  Total time: {stats['total_time']} minutes")
        print(f"  Orders delivered: {stats['orders_delivered']}")
        print(f"  Average delivery time: {stats['average_delivery_time']} minutes")
        print(f"  Orders per hour: {stats['orders_per_hour']}")
        print(f"  Distance per order: {stats['distance_per_order']} units")
        print()

if __name__ == "__main__":
    test_calculate_delivery_times()
    test_calculate_delivery_statistics_tuple_input()
    test_calculate_driver_performance_metrics() 