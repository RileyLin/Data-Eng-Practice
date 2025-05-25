"""
Question 12: Restaurant Delivery Time Calculation

You are given two inputs to calculate the delivery time for each order:

1. A list of dictionaries representing driver actions, where each dict contains:
   - location: string (location identifier)
   - order_no: string (order number, only present for 'pick_up' and 'drop_off' actions)
   - action_type: string ('pick_up', 'travel', 'drop_off')
   - driver: string (driver identifier)

2. A 2D matrix representing travel times between locations (location A to location B)

Important notes:
- When action_type is 'travel', there is no order_no in the record
- A driver can pick up multiple orders before dropping them off
- All time between picking up an order and dropping it off counts toward that order's delivery time
- Orders should be printed in order number sequence

Example Input:
actions = [
    {'location': 'A', 'order_no': 'order_1', 'action_type': 'pick_up', 'driver': 'driver_1'},
    {'location': 'A', 'action_type': 'travel', 'driver': 'driver_1'},
    {'location': 'B', 'order_no': 'order_2', 'action_type': 'pick_up', 'driver': 'driver_1'},
    {'location': 'B', 'action_type': 'travel', 'driver': 'driver_1'},
    {'location': 'C', 'order_no': 'order_1', 'action_type': 'drop_off', 'driver': 'driver_1'},
    {'location': 'C', 'action_type': 'travel', 'driver': 'driver_1'},
    {'location': 'D', 'order_no': 'order_2', 'action_type': 'drop_off', 'driver': 'driver_1'}
]

travel_matrix = [
    [0, 5, 10, 15],  # From A to [A, B, C, D]
    [5, 0, 8, 12],   # From B to [A, B, C, D]
    [10, 8, 0, 6],   # From C to [A, B, C, D]
    [15, 12, 6, 0]   # From D to [A, B, C, D]
]

location_mapping = {'A': 0, 'B': 1, 'C': 2, 'D': 3}

Expected Output:
order_1 is delivered within 15 mins
order_2 is delivered within 20 mins

Write a function calculate_delivery_times(actions, travel_matrix, location_mapping) 
that prints the delivery time for each order.
"""

def calculate_delivery_times(actions, travel_matrix, location_mapping):
    """
    Calculate and print delivery times for each order based on driver actions.
    
    Args:
        actions: List of dictionaries with driver action records
        travel_matrix: 2D list representing travel times between locations
        location_mapping: Dictionary mapping location names to matrix indices
    
    Returns:
        None (prints results)
    """
    """
    order_times = {}

    driver_state={}

    current_time=0

    for action in actions: 

        driver = action.get('driver')
        location = action.get('location')
        action_type = action['action_type']

        if driver not in driver_state:
            driver_state[driver] = {
                'location':location,
                'carrying_orders':set(),
                'current_time':0
            }
        
        if driver_state[driver]['location'] !=location:
            from_idx = location_mapping[driver_state[driver]['location']]
            to_idx = location_mapping[location]
            travel_time = travel_matrix[from_idx][to_idx]

            for order_no in driver_state[driver]['carrying_orders']:
                if order_no in order_times:
                    order_times[order_no]['total_time']+=travel_time

            driver_state[driver]['current_time']+=travel_time
            driver_state[driver]['location']=location

        if action_type == 'pick_up':
            order_no = action['order_no']

            order_times[order_no] = {
                'pickup_time': driver_state[driver]['current_time'],
                'total_time':0
            }

            driver_state[driver]['carrying_orders'].add(order_no)

        elif action_type == 'drop_off':
            order_no = action['order_no']

            if order_no in order_times:
                order_times[order_no]['delivery_time'] = driver_state[driver]['current_time']

                driver_state[driver]['carrying_orders'].discard(order_no)
            

    sorted_orders = sorted(order_times.keys())

    for order_no in sorted_orders:
        total_time = order_times[order_no]['total_time']

    for order_no in sorted_orders:
        times = order_times[order_no]

        pickup_time = times.get('pickup_time','N/A')
        delivery_time = times.get('delivery_time','N/A')
        total_time = times['total_time']

        print(f"{order_no}:")
        print(f" total delivery duration: {total_time} mins")

"""
    print("🚀 TIMELINE APPROACH - DETAILED DEBUGGING")
    print("="*60)
    
    # PHASE 1: Group actions by driver
    print("\n📋 PHASE 1: Grouping actions by driver...")
    driver_timelines = {}

    for i, action in enumerate(actions): 
        driver = action['driver']
        print(f"  Action {i+1}: {action}")

        if driver not in driver_timelines:
            driver_timelines[driver] = []
            print(f"    🆕 Creating new timeline for {driver}")

        driver_timelines[driver].append(action)
        print(f"    ➕ Added to {driver}'s timeline (now has {len(driver_timelines[driver])} actions)")

    print(f"\n📊 TIMELINE SUMMARY:")
    for driver, timeline in driver_timelines.items():
        print(f"  {driver}: {len(timeline)} actions")
        for j, action in enumerate(timeline):
            print(f"    {j+1}. {action}")

    # PHASE 2: Process each driver's timeline
    print(f"\n🔄 PHASE 2: Processing individual driver timelines...")
    all_delivery_times = {}

    for driver_num, (driver, timeline) in enumerate(driver_timelines.items(), 1):
        print(f"\n🚗 DRIVER {driver_num}: Processing {driver}")
        print(f"   Timeline: {len(timeline)} actions to process")
        print("-" * 40)

        current_location = None
        current_time = 0
        carrying_order = {}

        print(f"   Initial state:")
        print(f"     Location: {current_location}")
        print(f"     Time: {current_time} mins")
        print(f"     Carrying: {carrying_order}")

        for step, action in enumerate(timeline, 1): 
            print(f"\n   📍 Step {step}: {action}")
            
            location = action['location']
            action_type = action['action_type']

            # Check for travel
            if current_location is not None and current_location != location: 
                from_idx = location_mapping[current_location]
                to_idx = location_mapping[location]
                travel_time = travel_matrix[from_idx][to_idx]
                
                print(f"     🛣️  TRAVEL DETECTED:")
                print(f"       From: {current_location} (index {from_idx})")
                print(f"       To: {location} (index {to_idx})")
                print(f"       Travel time: {travel_time} mins")
                print(f"       Time before: {current_time} mins")
                
                current_time += travel_time
                print(f"       Time after: {current_time} mins")
            else:
                if current_location is None:
                    print(f"     🏁 Starting location: {location}")
                else:
                    print(f"     🏠 No travel needed - already at {location}")

            current_location = location

            if action_type == 'pick_up':
                order_no = action['order_no']
                carrying_order[order_no] = current_time
                print(f"     📦 PICKUP: {order_no}")
                print(f"       Pickup time recorded: {current_time} mins")
                print(f"       Now carrying: {list(carrying_order.keys())}")

            elif action_type == 'drop_off':
                order_no = action['order_no']
                print(f"     🎯 DROPOFF: {order_no}")
                if order_no in carrying_order:
                    pickup_time = carrying_order[order_no]
                    delivery_time = current_time - pickup_time
                    all_delivery_times[order_no] = delivery_time
                    
                    print(f"       Pickup time was: {pickup_time} mins")
                    print(f"       Dropoff time is: {current_time} mins")
                    print(f"       Total delivery time: {delivery_time} mins")
                    
                    del carrying_order[order_no]
                    print(f"       Removed from carrying list")
                    print(f"       Still carrying: {list(carrying_order.keys())}")
                else:
                    print(f"       ⚠️  Warning: {order_no} not found in carrying orders!")
            
            elif action_type == 'travel':
                print(f"     🚗 TRAVEL action (handled by location change logic)")

            print(f"     Current state:")
            print(f"       Location: {current_location}")
            print(f"       Time: {current_time} mins")
            print(f"       Carrying: {list(carrying_order.keys())}")

        print(f"\n   ✅ {driver} timeline complete!")
        if carrying_order:
            print(f"   ⚠️  Still carrying orders: {list(carrying_order.keys())}")

    # PHASE 3: Display results
    print(f"\n🏁 PHASE 3: Final Results")
    print("="*60)
    print(f"📊 All delivery times calculated: {all_delivery_times}")
    
    sorted_orders = sorted(all_delivery_times.keys())
    print(f"📋 Sorted order list: {sorted_orders}")
    
    print(f"\n🎯 FINAL OUTPUT:")
    for order_no in sorted_orders:
        delivery_time = all_delivery_times[order_no]
        print(f"📦 {order_no} is delivered within {delivery_time} mins")






# Test cases
def test_calculate_delivery_times():
    actions = [
        {'location': 'A', 'order_no': 'order_1', 'action_type': 'pick_up', 'driver': 'driver_1'},
        {'location': 'A', 'action_type': 'travel', 'driver': 'driver_1'},
        {'location': 'B', 'order_no': 'order_2', 'action_type': 'pick_up', 'driver': 'driver_1'},
        {'location': 'B', 'action_type': 'travel', 'driver': 'driver_1'},
        {'location': 'C', 'order_no': 'order_1', 'action_type': 'drop_off', 'driver': 'driver_1'},
        {'location': 'C', 'action_type': 'travel', 'driver': 'driver_1'},
        {'location': 'D', 'order_no': 'order_2', 'action_type': 'drop_off', 'driver': 'driver_1'}
    ]
    
    travel_matrix = [
        [0, 5, 10, 15],  # From A to [A, B, C, D]
        [5, 0, 8, 12],   # From B to [A, B, C, D]
        [10, 8, 0, 6],   # From C to [A, B, C, D]
        [15, 12, 6, 0]   # From D to [A, B, C, D]
    ]
    
    location_mapping = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    
    print("Test case 1:")
    calculate_delivery_times(actions, travel_matrix, location_mapping)
    
    # Additional test case with multiple drivers
    actions2 = [
        {'location': 'A', 'order_no': 'order_3', 'action_type': 'pick_up', 'driver': 'driver_1'},
        {'location': 'B', 'order_no': 'order_4', 'action_type': 'pick_up', 'driver': 'driver_2'},
        {'location': 'A', 'action_type': 'travel', 'driver': 'driver_1'},
        {'location': 'B', 'action_type': 'travel', 'driver': 'driver_2'},
        {'location': 'C', 'order_no': 'order_3', 'action_type': 'drop_off', 'driver': 'driver_1'},
        {'location': 'A', 'order_no': 'order_4', 'action_type': 'drop_off', 'driver': 'driver_2'}
    ]
    
    print("\nTest case 2:")
    calculate_delivery_times(actions2, travel_matrix, location_mapping)


if __name__ == "__main__":
    test_calculate_delivery_times() 