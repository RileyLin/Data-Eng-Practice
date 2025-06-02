# Scenario 11: Food Delivery (DoorDash) - Restaurant Focus - Python Questions

## Python Question 11.4.1: DoorDash Food Delivery Time Calculation (Restaurant Perspective)

This question is similar to the general delivery time calculation but can be adapted to focus on metrics important to restaurants, such as "time from order acceptance by restaurant to pickup by Dasher" or "total time from order placement to customer delivery for orders from a specific restaurant."

You are given two inputs to calculate the delivery time for each order:

1. A list of dictionaries representing driver/order events, where each dict contains:
   - `location`: string (location identifier, could be restaurant or customer)
   - `order_no`: string (order number, present for 'pick_up', 'drop_off', and potentially restaurant-specific events like 'order_ready_for_pickup')
   - `action_type`: string (e.g., 'pick_up', 'travel', 'drop_off', 'order_accepted_by_restaurant', 'order_ready_for_pickup')
   - `driver`: string (driver identifier, if applicable)
   - `timestamp`: int (Unix timestamp for the event)

2. A 2D matrix representing travel times between locations (if needed for broader calculations).

**Key Points (Restaurant Focus):**
- Need to track key timestamps: order placed, order accepted by restaurant, food ready for pickup, Dasher picked up, order delivered.
- Calculate metrics like: average food preparation time, average Dasher wait time at restaurant, average delivery time per restaurant.
- The core logic involves processing a sequence of events for each order and calculating time differences between relevant event pairs.

**Example Scenario (Restaurant Metrics Focus):**
- **Order Placed:** `timestamp_placed`
- **Restaurant Accepts Order:** `timestamp_accepted` (Prep starts)
- **Food Ready for Pickup:** `timestamp_ready` (Prep ends)
- **Dasher Picks Up Order:** `timestamp_picked_up`
- **Order Delivered to Customer:** `timestamp_delivered`

Calculate:
- `prep_time = timestamp_ready - timestamp_accepted`
- `dasher_wait_time = timestamp_picked_up - timestamp_ready`
- `delivery_time_after_pickup = timestamp_delivered - timestamp_picked_up`
- `total_fulfillment_time = timestamp_delivered - timestamp_placed`

**Function Signature Idea:**
```python
def analyze_restaurant_order_timings(order_events_log):
    # Group events by order_no
    # For each order, extract key timestamps
    # Calculate desired time differences (prep time, wait time, etc.)
    # Aggregate metrics per restaurant (e.g., average prep time for Restaurant X)
    pass
```

*(This reuses the theme of `q012_restaurant_delivery_time.py` but frames it towards restaurant-specific analytics based on a more detailed event log that would include restaurant-side events.)*

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