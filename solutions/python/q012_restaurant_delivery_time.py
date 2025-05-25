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
    print("🚀 Starting delivery time calculation...")
    print(f"📋 Processing {len(actions)} actions")
    print(f"🗺️  Location mapping: {location_mapping}")
    print("="*60)
    
    # Track order pickup and delivery times
    order_times = {}  # order_no -> {'pickup_time': time, 'delivery_time': time}
    
    # Track driver state: current location and orders being carried
    driver_state = {}  # driver -> {'location': loc, 'carrying_orders': set(), 'current_time': time}
    
    # Process each action in sequence
    current_time = 0
    
    for i, action in enumerate(actions):
        print(f"\n📍 Action {i+1}: {action}")
        
        driver = action['driver']
        location = action['location']
        action_type = action['action_type']
        
        # Initialize driver state if not exists
        if driver not in driver_state:
            print(f"🆕 Initializing new driver: {driver}")
            driver_state[driver] = {
                'location': location,
                'carrying_orders': set(),
                'current_time': 0
            }
            print(f"   Initial state: {driver_state[driver]}")
        
        print(f"🚗 Driver {driver} current state before action:")
        print(f"   Location: {driver_state[driver]['location']}")
        print(f"   Carrying orders: {driver_state[driver]['carrying_orders']}")
        print(f"   Current time: {driver_state[driver]['current_time']} mins")
        
        # Calculate travel time if driver moved to a different location
        if driver_state[driver]['location'] != location:
            from_location = driver_state[driver]['location']
            from_idx = location_mapping[from_location]
            to_idx = location_mapping[location]
            travel_time = travel_matrix[from_idx][to_idx]
            
            print(f"🛣️  TRAVEL DETECTED:")
            print(f"   From: {from_location} (index {from_idx}) → To: {location} (index {to_idx})")
            print(f"   Travel time: {travel_time} mins")
            print(f"   Orders affected: {driver_state[driver]['carrying_orders']}")
            
            # Add travel time to all orders currently being carried by this driver
            for order_no in driver_state[driver]['carrying_orders']:
                if order_no in order_times:
                    old_time = order_times[order_no]['total_time']
                    order_times[order_no]['total_time'] += travel_time
                    print(f"   📦 {order_no}: {old_time} + {travel_time} = {order_times[order_no]['total_time']} mins")
            
            # Update driver's current time and location
            driver_state[driver]['current_time'] += travel_time
            driver_state[driver]['location'] = location
            print(f"   Updated driver time: {driver_state[driver]['current_time']} mins")
        else:
            print(f"🏠 No travel needed - driver already at {location}")
        
        # Handle different action types
        if action_type == 'pick_up':
            order_no = action['order_no']
            print(f"📦 PICKUP: {order_no}")
            # Start tracking this order
            order_times[order_no] = {
                'pickup_time': driver_state[driver]['current_time'],
                'total_time': 0
            }
            driver_state[driver]['carrying_orders'].add(order_no)
            print(f"   Order {order_no} picked up at time {driver_state[driver]['current_time']}")
            print(f"   Driver now carrying: {driver_state[driver]['carrying_orders']}")
            
        elif action_type == 'drop_off':
            order_no = action['order_no']
            print(f"🎯 DROPOFF: {order_no}")
            # Complete this order
            if order_no in order_times:
                order_times[order_no]['delivery_time'] = driver_state[driver]['current_time']
                print(f"   Order {order_no} delivered at time {driver_state[driver]['current_time']}")
                print(f"   Total delivery time: {order_times[order_no]['total_time']} mins")
            driver_state[driver]['carrying_orders'].discard(order_no)
            print(f"   Driver now carrying: {driver_state[driver]['carrying_orders']}")
            
        elif action_type == 'travel':
            print(f"🚗 TRAVEL action (handled by location change logic above)")
        
        print(f"📊 Current order status:")
        for order_no, times in order_times.items():
            status = "✅ Delivered" if 'delivery_time' in times else "🚚 In transit"
            print(f"   {order_no}: {status}, Total time so far: {times['total_time']} mins")
        
        print("-" * 40)
    
    print(f"\n🏁 FINAL RESULTS:")
    print("="*60)
    
    # Sort orders by order number and print results
    sorted_orders = sorted(order_times.keys())
    
    for order_no in sorted_orders:
        total_time = order_times[order_no]['total_time']
        print(f"📦 {order_no} is delivered within {total_time} mins")
    
    print("\n📈 DETAILED ORDER BREAKDOWN:")
    for order_no in sorted_orders:
        times = order_times[order_no]
        pickup_time = times.get('pickup_time', 'N/A')
        delivery_time = times.get('delivery_time', 'N/A')
        total_time = times['total_time']
        print(f"   {order_no}:")
        print(f"     Pickup time: {pickup_time} mins")
        print(f"     Delivery time: {delivery_time} mins")
        print(f"     Total delivery duration: {total_time} mins")


def calculate_delivery_times_alternative(actions, travel_matrix, location_mapping):
    """
    Alternative implementation using a more explicit timeline approach.
    This version builds a complete timeline and then calculates delivery times.
    """
    # Build timeline of events for each driver
    driver_timelines = {}
    
    for action in actions:
        driver = action['driver']
        if driver not in driver_timelines:
            driver_timelines[driver] = []
        driver_timelines[driver].append(action)
    
    # Calculate delivery times for each driver's timeline
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
    
    # Sort and print results
    sorted_orders = sorted(all_delivery_times.keys())
    for order_no in sorted_orders:
        delivery_time = all_delivery_times[order_no]
        print(f"{order_no} is delivered within {delivery_time} mins")


# Test cases
def test_simple_example():
    """Simple test to understand the core mechanics step by step."""
    
    print("🔍 SIMPLE EXAMPLE TO UNDERSTAND THE MECHANICS")
    print("="*70)
    
    # Very simple scenario: One driver, one order
    simple_actions = [
        {'location': 'A', 'order_no': 'order_1', 'action_type': 'pick_up', 'driver': 'driver_1'},
        {'location': 'A', 'action_type': 'travel', 'driver': 'driver_1'},
        {'location': 'B', 'order_no': 'order_1', 'action_type': 'drop_off', 'driver': 'driver_1'}
    ]
    
    travel_matrix = [
        [0, 10],  # From A to [A, B] 
        [10, 0]   # From B to [A, B]
    ]
    
    location_mapping = {'A': 0, 'B': 1}
    
    print("📝 Scenario: Driver picks up order_1 at A, travels to B, drops off order_1")
    print("🗺️  Travel time A→B: 10 mins")
    print()
    
    calculate_delivery_times(simple_actions, travel_matrix, location_mapping)
    
    print("\n" + "="*70)
    print("💡 KEY INSIGHT: The order accumulates travel time while being carried!")
    print("   - Order picked up at A (time 0)")
    print("   - Driver travels A→B (10 mins) while carrying order")
    print("   - Order delivered at B (total delivery time: 10 mins)")


def test_calculate_delivery_times():
    """Test the delivery time calculation with provided examples."""
    
    print("=== Testing Main Implementation ===")
    
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
    
    print("Test case 1 - Single driver with multiple orders:")
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
    
    print("\nTest case 2 - Multiple drivers:")
    calculate_delivery_times(actions2, travel_matrix, location_mapping)
    
    print("\n=== Testing Alternative Implementation ===")
    print("Test case 1 - Alternative approach:")
    calculate_delivery_times_alternative(actions, travel_matrix, location_mapping)


def analyze_solution():
    """
    Analysis of the solution approach:
    
    1. **State Tracking**: We maintain driver state including current location,
       orders being carried, and accumulated time.
    
    2. **Travel Time Calculation**: When a driver moves between locations,
       we calculate travel time using the matrix and add it to all orders
       currently being carried.
    
    3. **Order Lifecycle**: Track pickup and dropoff events, calculating
       total delivery time as the difference.
    
    4. **Multiple Drivers**: Handle each driver independently with their
       own state and timeline.
    
    5. **Edge Cases**: Handle drivers starting at different locations,
       orders picked up and dropped off by the same driver, and travel
       actions without order numbers.
    
    **Time Complexity**: O(n + m log m) where n = number of actions, 
    m = number of unique orders (for sorting output)
    
    **Space Complexity**: O(m + d) where m = number of orders, 
    d = number of drivers
    
    **Key Insights**:
    - Travel time accumulates for ALL orders currently being carried
    - Order delivery time = total accumulated travel time from pickup to dropoff
    - Driver state must be maintained independently for concurrent operations
    """
    pass


def component_explanation():
    """
    DETAILED COMPONENT EXPLANATION based on the debug output:
    
    🔧 **CORE COMPONENTS BREAKDOWN**:
    
    1. **Driver State Tracking** (`driver_state` dictionary):
       - `location`: Current driver location
       - `carrying_orders`: Set of orders currently being carried
       - `current_time`: Driver's accumulated time (for timeline tracking)
    
    2. **Order Time Tracking** (`order_times` dictionary):
       - `pickup_time`: When order was picked up
       - `delivery_time`: When order was delivered  
       - `total_time`: Accumulated travel time while being carried
    
    3. **Travel Time Calculation**:
       - Detects when driver moves between locations
       - Uses travel_matrix[from_idx][to_idx] to get travel time
       - Adds travel time to ALL orders currently being carried
    
    4. **Action Processing**:
       - `pick_up`: Start tracking order, add to carrying_orders set
       - `drop_off`: Stop tracking order, remove from carrying_orders set
       - `travel`: Handled implicitly by location change detection
    
    🎯 **KEY INSIGHT FROM DEBUG OUTPUT**:
    
    In the complex scenario, we see:
    - Action 3: order_1 accumulates 5 mins (A→B travel)
    - Action 5: BOTH order_1 and order_2 accumulate 8 mins (B→C travel)
    - Action 7: order_2 accumulates 6 mins (C→D travel)
    
    Final results:
    - order_1: 5 + 8 = 13 mins total
    - order_2: 8 + 6 = 14 mins total
    
    This shows how orders accumulate travel time ONLY while being carried!
    
    🚀 **ALGORITHM FLOW**:
    
    For each action:
    1. Check if driver moved → Calculate travel time
    2. Add travel time to all carried orders
    3. Update driver location and time
    4. Handle pickup/dropoff action
    5. Update order and driver state
    
    The beauty is in the simplicity: orders accumulate time naturally
    as drivers move while carrying them!
    """
    print(component_explanation.__doc__)


def explain_complex_scenario():
    """Explain the complex scenario with multiple orders step by step."""
    
    print("\n🧠 UNDERSTANDING THE COMPLEX MULTI-ORDER SCENARIO")
    print("="*70)
    
    actions = [
        {'location': 'A', 'order_no': 'order_1', 'action_type': 'pick_up', 'driver': 'driver_1'},
        {'location': 'A', 'action_type': 'travel', 'driver': 'driver_1'},
        {'location': 'B', 'order_no': 'order_2', 'action_type': 'pick_up', 'driver': 'driver_1'},
        {'location': 'B', 'action_type': 'travel', 'driver': 'driver_1'},
        {'location': 'C', 'order_no': 'order_1', 'action_type': 'drop_off', 'driver': 'driver_1'},
        {'location': 'C', 'action_type': 'travel', 'driver': 'driver_1'},
        {'location': 'D', 'order_no': 'order_2', 'action_type': 'drop_off', 'driver': 'driver_1'}
    ]
    
    print("📋 SCENARIO BREAKDOWN:")
    print("1. Pick up order_1 at A")
    print("2. Travel A→B (order_1 accumulates 5 mins)")
    print("3. Pick up order_2 at B (now carrying both orders)")
    print("4. Travel B→C (both order_1 and order_2 accumulate 8 mins)")
    print("5. Drop off order_1 at C (total: 5+8=13 mins)")
    print("6. Travel C→D (order_2 accumulates 6 mins)")
    print("7. Drop off order_2 at D (total: 8+6=14 mins)")
    print()
    
    print("🔑 KEY CONCEPT: When multiple orders are carried simultaneously,")
    print("   ALL carried orders accumulate the same travel time!")
    print()


def interview_explanation():
    """
    🎯 **INTERVIEW TALKING POINTS: Comparing Two Approaches**
    
    ==========================================
    📊 **APPROACH 1: Real-time State Tracking**
    ==========================================
    
    **How it works:**
    - Processes actions sequentially in a single pass
    - Maintains global driver state across all actions
    - Updates order times immediately as travel happens
    - Accumulates time for all carried orders on each move
    
    **Pros:**
    ✅ Memory efficient - O(d + m) space
    ✅ Single pass through data - O(n) time
    ✅ Real-time processing capability
    ✅ Handles streaming data well
    
    **Cons:**
    ❌ Complex state management across drivers
    ❌ Harder to debug intermediate states
    ❌ Tightly coupled logic (travel + order tracking)
    ❌ Less intuitive mental model
    
    ==========================================
    📈 **APPROACH 2: Timeline-based Processing**
    ==========================================
    
    **How it works:**
    - Groups actions by driver first
    - Processes each driver's timeline independently
    - Calculates delivery times per driver, then aggregates
    - Clear separation of concerns
    
    **Pros:**
    ✅ **Clearer mental model** - matches real-world driver behavior
    ✅ **Easier to debug** - can inspect each driver's timeline
    ✅ **Better separation of concerns** - driver logic isolated
    ✅ **More maintainable** - easier to modify driver-specific logic
    ✅ **Parallel processing potential** - drivers are independent
    ✅ **Easier testing** - can test individual driver scenarios
    
    **Cons:**
    ❌ Slightly higher memory usage - O(n + d + m)
    ❌ Two-pass algorithm (group + process)
    
    ==========================================
    🗣️ **HOW TO JUSTIFY TIMELINE APPROACH**
    ==========================================
    
    **Opening Statement:**
    "I prefer the timeline approach because it better models the real-world 
    problem and provides clearer separation of concerns."
    
    **Key Justification Points:**
    
    1. **Mental Model Clarity:**
       "In reality, each driver operates independently. The timeline approach 
       mirrors this by processing each driver's actions as a separate sequence,
       making the code more intuitive to understand and maintain."
    
    2. **Debugging & Maintenance:**
       "When debugging delivery time issues, you can isolate and examine 
       individual driver timelines. This makes it much easier to trace 
       problems and validate logic."
    
    3. **Scalability Considerations:**
       "The timeline approach naturally supports parallel processing - each 
       driver's timeline can be processed independently, which is valuable 
       for large-scale systems."
    
    4. **Code Organization:**
       "The separation allows for driver-specific optimizations or business 
       rules without affecting the core algorithm structure."
    
    ==========================================
    🤔 **HANDLING FOLLOW-UP QUESTIONS**
    ==========================================
    
    **Q: "But isn't the real-time approach more efficient?"**
    A: "While it uses slightly less memory, the difference is minimal in practice.
       The timeline approach's benefits in maintainability and debuggability 
       often outweigh the small memory overhead, especially in production systems
       where code clarity is crucial."
    
    **Q: "What if we need real-time processing?"**
    A: "Great question! For real-time scenarios, we could adapt the timeline 
       approach by processing driver timelines incrementally as new actions 
       arrive, maintaining the same clear structure while supporting streaming."
    
    **Q: "How would you handle very large datasets?"**
    A: "The timeline approach actually scales better because:
       1. We can process drivers in parallel
       2. We can implement driver-specific optimizations
       3. Memory usage per driver is bounded
       4. We can even persist/cache individual driver timelines"
    
    **Q: "What about memory usage with many drivers?"**
    A: "The memory overhead is O(n) for storing actions per driver, which is 
       the same data we're processing anyway. The benefit of clearer code 
       structure typically justifies this small overhead."
    
    ==========================================
    💡 **TECHNICAL DEPTH DEMONSTRATION**
    ==========================================
    
    **Show Understanding of Trade-offs:**
    "I chose the timeline approach understanding there's a memory trade-off, 
    but I believe the benefits in code maintainability, debuggability, and 
    scalability make it the better choice for a production system."
    
    **Demonstrate Systems Thinking:**
    "In a real delivery system, you'd likely want to:
    - Audit individual driver performance
    - Handle driver-specific business rules
    - Support parallel processing for scale
    The timeline approach naturally supports all of these requirements."
    
    **Show Flexibility:**
    "That said, if memory constraints were critical or we needed true 
    streaming processing, I could implement the real-time approach. The 
    choice depends on the specific system requirements."
    """
    print(interview_explanation.__doc__)


def demonstrate_timeline_benefits():
    """
    🔬 **PRACTICAL DEMONSTRATION: Why Timeline Approach is Better**
    
    Let me show you specific scenarios where timeline approach shines:
    """
    
    print("🔬 PRACTICAL DEMONSTRATION: Timeline Approach Benefits")
    print("="*60)
    
    print("\n1. 🐛 **DEBUGGING SCENARIO:**")
    print("   Problem: 'Driver_1's order_5 has wrong delivery time'")
    print("   Timeline approach: Extract driver_1's timeline, trace step-by-step")
    print("   Real-time approach: Must replay entire action sequence")
    
    print("\n2. 🔧 **MAINTENANCE SCENARIO:**")
    print("   Requirement: 'Add driver break time handling'")
    print("   Timeline approach: Modify individual driver processing logic")
    print("   Real-time approach: Modify global state management (more complex)")
    
    print("\n3. 📊 **ANALYTICS SCENARIO:**")
    print("   Need: 'Generate per-driver performance reports'")
    print("   Timeline approach: Driver data already grouped and accessible")
    print("   Real-time approach: Must re-process or maintain separate tracking")
    
    print("\n4. ⚡ **SCALABILITY SCENARIO:**")
    print("   Challenge: 'Process 10,000 drivers with 1M actions'")
    print("   Timeline approach: Process drivers in parallel, natural partitioning")
    print("   Real-time approach: Sequential processing, harder to parallelize")
    
    print("\n5. 🧪 **TESTING SCENARIO:**")
    print("   Need: 'Unit test driver behavior with complex pickup/dropoff patterns'")
    print("   Timeline approach: Create isolated driver timeline, test independently")
    print("   Real-time approach: Must create full action sequence with other drivers")


def interview_cheat_sheet():
    """
    📋 **INTERVIEW CHEAT SHEET: Timeline Approach Defense**
    
    🎯 **OPENING STATEMENT:**
    "I implemented both approaches, but I prefer the timeline method because 
    it better models real-world driver behavior and provides clearer code organization."
    
    🔑 **KEY TALKING POINTS:**
    
    1. **MENTAL MODEL** 📚
       "Each driver operates independently in reality → code should reflect this"
    
    2. **DEBUGGING** 🐛  
       "Can isolate individual driver issues without replaying entire sequence"
    
    3. **MAINTAINABILITY** 🔧
       "Driver-specific features (breaks, routes) easier to add"
    
    4. **SCALABILITY** ⚡
       "Natural parallel processing - each driver timeline independent"
    
    5. **TESTING** 🧪
       "Can unit test individual driver scenarios in isolation"
    
    ⚖️ **TRADE-OFF ACKNOWLEDGMENT:**
    "Yes, it uses slightly more memory (O(n) vs O(d+m)), but the benefits 
    in code clarity and maintainability justify this in production systems."
    
    🛡️ **COUNTER-ARGUMENTS:**
    
    Memory concerns? → "Overhead is minimal, same data we're processing anyway"
    Real-time needs? → "Can adapt timeline approach for incremental processing"
    Efficiency? → "Timeline approach enables parallel processing for better throughput"
    
    💪 **CONFIDENCE CLOSER:**
    "Both approaches work, but timeline approach sets us up better for 
    real-world requirements like debugging, analytics, and scaling."
    """
    print(interview_cheat_sheet.__doc__)


if __name__ == "__main__":
    test_simple_example()
    explain_complex_scenario()
    test_calculate_delivery_times()
    print("\n" + "="*50)
    print("Solution Analysis:")
    analyze_solution()
    print("\n" + "="*50)
    print("Component Explanation:")
    component_explanation()
    print("\n" + "="*50)
    print("Interview Explanation:")
    interview_explanation()
    print("\n" + "="*50)
    demonstrate_timeline_benefits()
    print("\n" + "="*50)
    print("INTERVIEW CHEAT SHEET:")
    interview_cheat_sheet() 