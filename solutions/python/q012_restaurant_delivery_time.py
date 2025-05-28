"""
Question 12: Restaurant Delivery Time Calculation - SOLUTION

This problem requires tracking driver movements and calculating total delivery time
for each order from pickup to dropoff, including all intermediate travel time.

Key insights:
1. Track each order's pickup and dropoff times
2. Calculate travel time between consecutive locations for each driver
3. For orders being carried, accumulate all travel time until dropoff
4. Handle multiple drivers independently
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
    
    This implementation uses a timeline-based approach where each driver's actions
    are processed sequentially to track their movement and order handling.
    
    Args:
        actions: List of dictionaries with driver action records
        travel_matrix: 2D list representing travel times between locations
        location_mapping: Dictionary mapping location names to matrix indices
    
    Returns:
        None (prints results)
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

def component_explanation():
    """
    Explains the key components of the delivery time calculation problem.
    """
    print("🔍 COMPONENT BREAKDOWN:")
    print("="*50)
    
    print("\n1. 📋 ACTIONS LIST:")
    print("   - Sequence of driver activities")
    print("   - Each action has: location, action_type, driver")
    print("   - pickup/dropoff actions also have: order_no")
    print("   - Actions are processed in chronological order")
    
    print("\n2. 🗺️  TRAVEL MATRIX:")
    print("   - 2D grid of travel times between locations")
    print("   - Matrix[i][j] = time from location i to location j")
    print("   - Symmetric matrix (usually)")
    print("   - Diagonal is 0 (no time to travel to same location)")
    
    print("\n3. 🏷️  LOCATION MAPPING:")
    print("   - Converts location names to matrix indices")
    print("   - Example: {'A': 0, 'B': 1, 'C': 2}")
    print("   - Enables lookup of travel times")
    
    print("\n4. ⏱️  TIME CALCULATION:")
    print("   - Track each driver's current time and location")
    print("   - Add travel time when location changes")
    print("   - Record pickup time for each order")
    print("   - Calculate delivery time = dropoff_time - pickup_time")

def interview_explanation():
    """
    Provides talking points for explaining the solution in an interview.
    """
    print("\n🎯 INTERVIEW TALKING POINTS:")
    print("="*50)
    
    print("\n💭 PROBLEM UNDERSTANDING:")
    print("   'This is a logistics simulation problem where we need to track")
    print("    multiple drivers handling multiple orders with realistic travel times.'")
    
    print("\n🧠 APPROACH REASONING:")
    print("   'I'll use a timeline-based approach because:'")
    print("   - Each driver operates independently")
    print("   - Actions must be processed in sequence")
    print("   - Need to track state (location, time, carried orders)")
    print("   - Travel time only applies when location actually changes'")
    
    print("\n⚡ ALGORITHM STEPS:")
    print("   1. Group actions by driver (separate timelines)")
    print("   2. For each driver, process actions sequentially:")
    print("      - Track current location and time")
    print("      - Add travel time when location changes")
    print("      - Record pickup times")
    print("      - Calculate delivery times at dropoff")
    print("   3. Sort and output results")
    
    print("\n🔧 EDGE CASES:")
    print("   - Multiple orders carried simultaneously")
    print("   - Orders dropped in different sequence than picked up")
    print("   - Multiple drivers working independently")
    print("   - Travel actions that don't change location")

def demonstrate_timeline_benefits():
    """
    Shows why the timeline approach is better than alternatives.
    """
    print("\n🏆 WHY TIMELINE APPROACH WINS:")
    print("="*50)
    
    print("\n❌ NAIVE APPROACH PROBLEMS:")
    print("   - Processing all actions globally loses driver context")
    print("   - Hard to track which driver is where at what time")
    print("   - Difficult to handle multiple orders per driver")
    print("   - Complex state management across drivers")
    
    print("\n✅ TIMELINE APPROACH BENEFITS:")
    print("   - Each driver has independent timeline")
    print("   - Clear state tracking (location, time, orders)")
    print("   - Natural handling of multiple orders")
    print("   - Easy to debug and verify")
    print("   - Scales well with more drivers")
    
    print("\n🎯 REAL-WORLD APPLICABILITY:")
    print("   - Models actual delivery logistics")
    print("   - Can extend to handle driver breaks, traffic, etc.")
    print("   - Supports optimization algorithms")
    print("   - Easy to add features like order priorities")

def interview_cheat_sheet():
    """
    Quick reference for interview discussion.
    """
    print("\n📝 INTERVIEW CHEAT SHEET:")
    print("="*50)
    
    print("\n🔑 KEY INSIGHTS:")
    print("   • Timeline per driver = independent state tracking")
    print("   • Travel time only when location changes")
    print("   • Delivery time = dropoff_time - pickup_time")
    print("   • Sort output by order number")
    
    print("\n⚠️  GOTCHAS:")
    print("   • Travel actions don't always mean location change")
    print("   • Multiple orders can be carried simultaneously")
    print("   • Order dropoff sequence may differ from pickup sequence")
    
    print("\n🚀 FOLLOW-UP QUESTIONS TO EXPECT:")
    print("   • How would you optimize driver routes?")
    print("   • What if drivers have different speeds?")
    print("   • How to handle real-time traffic updates?")
    print("   • What about order priorities or time windows?")
    
    print("\n💡 OPTIMIZATION IDEAS:")
    print("   • Precompute shortest paths (Floyd-Warshall)")
    print("   • Use priority queues for order scheduling")
    print("   • Implement route optimization algorithms")
    print("   • Add caching for repeated calculations")

# Test functions for demonstration
def test_simple_example():
    """Simple test case for basic understanding."""
    print("\n🧪 SIMPLE TEST CASE:")
    print("="*30)
    
    actions = [
        {'location': 'A', 'order_no': 'order_1', 'action_type': 'pick_up', 'driver': 'driver_1'},
        {'location': 'A', 'action_type': 'travel', 'driver': 'driver_1'},
        {'location': 'B', 'order_no': 'order_1', 'action_type': 'drop_off', 'driver': 'driver_1'}
    ]
    
    travel_matrix = [
        [0, 10],  # A to [A, B]
        [10, 0]   # B to [A, B]
    ]
    
    location_mapping = {'A': 0, 'B': 1}
    
    print("Actions:", actions)
    print("Travel matrix:", travel_matrix)
    print("Expected: order_1 delivered in 10 mins")
    print("\nResult:")
    calculate_delivery_times(actions, travel_matrix, location_mapping)

def explain_complex_scenario():
    """Explains the complex multi-order scenario step by step."""
    print("\n🎭 COMPLEX SCENARIO EXPLANATION:")
    print("="*50)
    
    print("📋 Scenario: Driver picks up 2 orders, delivers them")
    print("🗺️  Route: A → B → C → D")
    print("📦 Orders: order_1 (A→C), order_2 (B→D)")
    
    print("\n⏰ Timeline:")
    print("Time 0:  At A, pickup order_1")
    print("Time 5:  Travel A→B, at B, pickup order_2")
    print("Time 13: Travel B→C, at C, dropoff order_1 (13-0=13 mins)")
    print("Time 19: Travel C→D, at D, dropoff order_2 (19-5=14 mins)")
    
    print("\n🎯 Key Insights:")
    print("• order_1 carried for 13 minutes total")
    print("• order_2 carried for 14 minutes total")
    print("• Driver can carry multiple orders simultaneously")
    print("• Each order's time = dropoff_time - pickup_time")

# Example usage and test cases
if __name__ == "__main__":
    # Run component explanations
    component_explanation()
    interview_explanation()
    demonstrate_timeline_benefits()
    interview_cheat_sheet()
    
    # Run simple test
    test_simple_example()
    
    # Explain complex scenario
    explain_complex_scenario()
    
    print("\n" + "="*60)
    print("🚀 MAIN TEST CASES:")
    print("="*60)
    
    # Original test case
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
    
    print("\n📋 Test case 1 - Single driver, multiple orders:")
    calculate_delivery_times(actions, travel_matrix, location_mapping)
    
    # Multiple drivers test case
    actions2 = [
        {'location': 'A', 'order_no': 'order_3', 'action_type': 'pick_up', 'driver': 'driver_1'},
        {'location': 'B', 'order_no': 'order_4', 'action_type': 'pick_up', 'driver': 'driver_2'},
        {'location': 'A', 'action_type': 'travel', 'driver': 'driver_1'},
        {'location': 'B', 'action_type': 'travel', 'driver': 'driver_2'},
        {'location': 'C', 'order_no': 'order_3', 'action_type': 'drop_off', 'driver': 'driver_1'},
        {'location': 'A', 'order_no': 'order_4', 'action_type': 'drop_off', 'driver': 'driver_2'}
    ]
    
    print("\n📋 Test case 2 - Multiple drivers:")
    calculate_delivery_times(actions2, travel_matrix, location_mapping) 