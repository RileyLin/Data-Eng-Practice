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

Step-by-step processing:
Time 0: Driver at A, picks up order_1
Time 0: Travel from A to B (5 mins) → Time becomes 5
Time 5: Driver at B, picks up order_2 (now carrying order_1 and order_2)
Time 5: Travel from B to C (8 mins) → Time becomes 13
Time 13: Driver at C, drops off order_1 (delivery time: 13 - 0 = 13 mins)
Time 13: Travel from C to D (6 mins) → Time becomes 19
Time 19: Driver at D, drops off order_2 (delivery time: 19 - 5 = 14 mins)

Wait, let me recalculate this correctly:
Time 0: Pick up order_1 at A
Time 0→5: Travel A to B (5 mins)
Time 5: Pick up order_2 at B
Time 5→13: Travel B to C (8 mins)
Time 13: Drop off order_1 at C (total time for order_1: 13 mins)
Time 13→19: Travel C to D (6 mins)
Time 19: Drop off order_2 at D (total time for order_2: 19 - 5 = 14 mins)

Actually, let me check the expected output again...
Expected: order_1 = 15 mins, order_2 = 20 mins

Let me trace this more carefully:
- order_1: picked up at time 0, dropped off when driver reaches C
- order_2: picked up when driver reaches B, dropped off when driver reaches D

Timeline:
Start: time 0, location A
Action 1: Pick up order_1 at A (time 0)
Action 2: Travel A→B (5 mins) → time 5
Action 3: Pick up order_2 at B (time 5)
Action 4: Travel B→C (8 mins) → time 13
Action 5: Drop off order_1 at C (time 13) → order_1 delivery time = 13 mins
Action 6: Travel C→D (6 mins) → time 19
Action 7: Drop off order_2 at D (time 19) → order_2 delivery time = 19 - 5 = 14 mins

Hmm, this doesn't match expected output. Let me check if there's a different interpretation...

Actually, looking at the expected output (15 and 20), maybe the travel actions add time even when staying at the same location, or there's a different calculation method.

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