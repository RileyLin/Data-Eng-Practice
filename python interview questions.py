# -*- coding: utf-8 -*-
"""
Python Interview Preparation File

This file contains Python functions based on common
data science and product analysis interview scenarios, focusing on
logic and algorithms without relying heavily on external libraries.

The textual content for Product Sense, Data Modeling, and SQL questions
is embedded as comments and multi-line strings for reference within each scenario.
SQL DDL/DML statements are provided as strings for testing with SQLite.

This script includes:
1. Placeholder functions (e.g., `can_user_complete_rides`) for you to implement your answers.
2. Solution functions (e.g., `can_user_complete_rides_solution`) with detailed
   line-by-line explanations for reference.
3. A main block (`if __name__ == '__main__':`) that calls the placeholder functions
   for testing your implementations.
"""

# ============================================================================
# General Interview Notes (Reference)
# ============================================================================
"""
- Speed is Critical: Questions might be straightforward, but you need to work
  through them efficiently. Don't get stuck. Aim for max 8 minutes per SQL/Python
  question in initial screens.
- Explain Your Thought Process: Clearly articulate your reasoning, assumptions,
  and trade-offs, especially in data modeling and product sense questions.
- Hints are Okay: Interviewers often provide hints if you're stuck. Listen
  carefully and show you can incorporate feedback – this demonstrates learning
  ability, a key hiring signal.
- Data Scale: Assume datasets are large (billions of records). Mentioning data
  partitioning (e.g., by date on fact tables) and optimizing dashboards by
  reading from pre-aggregated daily/hourly tables instead of raw fact tables
  can earn bonus points.
- Follow-up Questions: Expect "why" and "how" follow-ups. Interviewers probe
  for depth and specific signals (ownership, impact, technical depth,
  collaboration). Be prepared to elaborate.
- Bonus Questions: If you finish early, you might get an additional question,
  potentially including ML concepts depending on the role/interviewer.
- SQL Fundamentals: Be solid on GROUP BY, HAVING, sub-queries, window functions
  (SUM() OVER, ROW_NUMBER(), etc.), CASE statements (e.g., SUM(CASE WHEN ...)),
  and self-joins.
- Python Fundamentals: Master lists, strings, tuples, dictionaries, and common
  operations/methods.
"""

# ============================================================================
# Behavioral Questions (Example Themes & Signals - Reference)
# ============================================================================
"""
- Motivation & Role Understanding:
    * "What does data engineering / data science mean to you?"
    * "Tell me about a project where you used data to make an impact or convince others."
    * "How do you plan to succeed at Meta?"
- Execution & Prioritization:
    * "How do you handle prioritizing competing tasks or projects? Describe your framework."
    * "Tell me about a time you led a project. What was the impact?"
- Self-Awareness & Learning:
    * "Tell me about a time you were wrong or made a mistake. How did you handle it?"

(See Solutions section in the accompanying Markdown document for example approaches)
"""

# ============================================================================
# --- Scenario 1: Ride Sharing - Carpooling Focus ---
# ============================================================================

# ----------------------------------------------------------------------------
# 1.1 Product Sense (Questions - Reference)
# ----------------------------------------------------------------------------
"""
Question 1.1.1 (Value Proposition & Mission Alignment): ...
Question 1.1.2 (Tracking Performance): ...
"""

# ----------------------------------------------------------------------------
# 1.2 Data Modeling (Question - Reference)
# ----------------------------------------------------------------------------
"""
Question 1.2.1 (Supporting Multiple Riders): ...
"""

# ----------------------------------------------------------------------------
# 1.3 SQL (Questions - Reference)
# ----------------------------------------------------------------------------
"""
Question 1.3.1 (Carpool Segment Percentage): ...
Question 1.3.2 (Drivers Preferring Carpool): ...
"""

# ----------------------------------------------------------------------------
# 1.4 Python (Question & Solution with Line-by-Line Explanation)
# ----------------------------------------------------------------------------
"""
Question 1.4.1 (Overlapping User Rides):
A user wants to book multiple rides for themselves. Given a list of
requested rides, where each ride is a tuple `(start_time, end_time)`
with integer times, write a Python function
`can_user_complete_rides(requested_rides)` that returns `True` if the user
can theoretically complete all their requested rides (i.e., none of their
own rides overlap), and `False` otherwise.

Example Input:
requested_rides = [(0, 30), (30, 60), (70, 90)]
Expected Output: True

Example Input:
requested_rides = [(0, 60), (30, 90)]
Expected Output: False

Example Input:
requested_rides = [(10, 20)]
Expected Output: True

Example Input:
requested_rides = []
Expected Output: True

  * (Follow-up consideration for discussion): How would this problem change
    if we were considering a single carpool vehicle with a limited passenger
    capacity (e.g., 6 passengers), and the input was a list of ride segments
    for *different* users wanting to share that vehicle? (Conceptual discussion,
    no full code needed for follow-up).
"""
# Placeholder for your answer to Question 1.4.1
def can_user_complete_rides(requested_rides):
    # TODO: Implement your logic here
    if len(requested_rides)<=1:
      return True
   
    sorted_rides = list(requested_rides)
    #to avoid changing the original list 

    sorted_rides.sort()

    for i in range(len(requested_rides)-1):
      current_end_time = requested_rides[i][1]

      current_start_time = requested_rides[i+1][0]

      if current_end_time>current_start_time:
        return False
    

    return True















# Solution for Question 1.4.1
def can_user_complete_rides_solution(requested_rides):
    """
    Solution for: Checks if a list of ride requests (start_time, end_time) for a single user overlap.
    This version focuses on a single user's schedule.

    Args:
        requested_rides: A list of tuples, where each tuple is (start_time, end_time).
                         Times are integers. Assumes end_time > start_time.

    Returns:
        True if no rides overlap, False otherwise.

    Explanation (Overall):
    - Handles base cases (0 or 1 ride).
    - Sorts rides by start time to enable linear comparison.
    - Iterates through sorted rides, checking if the current ride's end time
      is after the next ride's start time.
    - Returns False immediately if an overlap is found.
    - Returns True if the loop completes without finding overlaps.

    Further Considerations (Potential Follow-ups or More Complex Versions):
    - Capacity Constraint: If the question implied a single carpool vehicle's capacity
      (e.g., max 6 passengers), the problem changes. Each `requested_ride` tuple might
      need to include `num_passengers`. Then, you'd need to track the number of
      concurrent passengers in the vehicle over time. This involves processing events
      (pickups and drop-offs) sorted by time and maintaining a current passenger count,
      returning False if the count ever exceeds capacity. This is more complex than
      the current implementation, which assumes it's about one user's schedule.
    - Multiple Dashers/Vehicles: If it's about assigning a list of bookings to a fleet,
      it becomes a variation of the bin packing or interval scheduling problem with
      multiple machines, which is significantly more complex.

    Line-by-Line Explanation:
    -------------------------
    """
    # Line 1: `if len(requested_rides) <= 1:`
    #   - Checks if the input list `requested_rides` contains 0 or 1 ride.
    #   - If so, there's no possibility of an overlap.
    if len(requested_rides) <= 1:
        # Line 2: `return True`
        #   - Immediately returns `True` as 0 or 1 ride cannot overlap.
        return True

    # Line 3: `sorted_rides = list(requested_rides)`
    #   - Creates a shallow copy of the `requested_rides` list. This is important
    #     to avoid modifying the original list passed to the function if `sort()`
    #     is called on it directly (though `list.sort()` sorts in-place,
    #     creating a copy first is safer if the original list is needed elsewhere
    #     unchanged, or if `sorted()` built-in function was used instead).
    sorted_rides = list(requested_rides)

    # Line 4: `sorted_rides.sort(key=lambda x: x[0])`
    #   - Sorts the `sorted_rides` list in-place.
    #   - `key=lambda x: x[0]` specifies that the sort should be based on the
    #     first element (index 0) of each tuple `x` in the list. In this context,
    #     `x[0]` is the `start_time` of a ride.
    #   - Sorting by start time is crucial for the subsequent overlap check logic.
    sorted_rides.sort(key=lambda x: x[0])

    # Line 5: `for i in range(len(sorted_rides) - 1):`
    #   - Initiates a loop that iterates from the first ride up to the
    #     second-to-last ride in the `sorted_rides` list.
    #   - `len(sorted_rides) - 1` is used because each iteration compares ride `i`
    #     with ride `i+1`.
    for i in range(len(sorted_rides) - 1):
        # Line 6: `current_ride_end_time = sorted_rides[i][1]`
        #   - Retrieves the end time of the current ride (`sorted_rides[i]`).
        #   - The end time is the second element (index 1) of the ride tuple.
        current_ride_end_time = sorted_rides[i][1]

        # Line 7: `next_ride_start_time = sorted_rides[i+1][0]`
        #   - Retrieves the start time of the next ride in the sequence (`sorted_rides[i+1]`).
        #   - The start time is the first element (index 0) of the ride tuple.
        next_ride_start_time = sorted_rides[i+1][0]

        # Line 8: `if current_ride_end_time > next_ride_start_time:`
        #   - This is the core logic for detecting an overlap.
        #   - If the end time of the current ride is greater than the start time
        #     of the next ride, it means the current ride has not finished before
        #     the next ride begins, hence an overlap exists.
        #   - Note: If `current_ride_end_time == next_ride_start_time`, it's typically
        #     considered non-overlapping (one ends exactly when the other starts).
        if current_ride_end_time > next_ride_start_time:
            # Line 9: `return False`
            #   - If an overlap is detected, the function immediately returns `False`
            #     as not all rides can be completed.
            return False

    # Line 10: `return True`
    #   - If the loop completes without executing `return False` (i.e., no overlaps
    #     were found between any adjacent rides in the sorted list), this line is reached.
    #   - It means all rides can be completed without overlap, so `True` is returned.
    return True


"""
Question 1.4.2 (Carpool Vehicle Capacity Check):
You are given a list of ride segments for a single carpool vehicle. Each segment is
represented by a tuple `(start_time, end_time, num_passengers)`. The vehicle has a
maximum passenger capacity. Write a Python function
`can_vehicle_complete_rides_with_capacity(ride_segments, max_capacity)`
that returns `True` if all ride segments can be completed without exceeding the
vehicle's `max_capacity` at any point in time, and `False` otherwise.

Assume `start_time` is when passengers are picked up and `end_time` is when they are dropped off.
If a dropoff and a pickup happen at the exact same time, assume the dropoff occurs first.

Example Input:
ride_segments = [(0, 5, 2), (1, 3, 3), (6, 8, 1)]
max_capacity = 4
Expected Output: False
Explanation:
- Time 0: Pickup 2 (Capacity: 2/4)
- Time 1: Pickup 3 (Capacity: 2+3=5/4) -> Exceeds capacity

Example Input:
ride_segments = [(0, 5, 2), (0, 2, 1), (3, 6, 1)]
max_capacity = 3
Expected Output: True
Explanation:
- Time 0: Pickup 2 (Capacity: 2/3)
- Time 0: Pickup 1 (Capacity: 2+1=3/3)
- Time 2: Dropoff 1 (Capacity: 3-1=2/3)
- Time 3: Pickup 1 (Capacity: 2+1=3/3)
- Time 5: Dropoff 2 (Capacity: 3-2=1/3)
- Time 6: Dropoff 1 (Capacity: 1-1=0/3)

Example Input:
ride_segments = [(0, 10, 3), (0, 5, 2)] # Two segments starting at the same time
max_capacity = 4
Expected Output: False (at time 0, capacity becomes 3+2=5)
"""
# Placeholder for your answer to Question 1.4.2
def can_vehicle_complete_rides_with_capacity(ride_segments, max_capacity):
    # TODO: Implement your logic here
    pass










# Solution for Question 1.4.2
def can_vehicle_complete_rides_with_capacity_solution(ride_segments, max_capacity):
    """
    Solution for: Checks if a list of ride segments can be completed by a single
    vehicle without exceeding its maximum passenger capacity.

    Args:
        ride_segments: A list of tuples, where each tuple is
                       (start_time, end_time, num_passengers).
        max_capacity: An integer representing the maximum passenger capacity
                      of the vehicle.

    Returns:
        True if all segments can be completed without exceeding capacity,
        False otherwise.

    Line-by-Line Explanation:
    -------------------------
    """
    # Line 1: `events = []`
    #   - Initializes an empty list called `events`. This list will store all
    #     pickup and dropoff actions as individual event points in time.
    events = []

    # Line 2: `for start_time, end_time, num_passengers in ride_segments:`
    #   - Iterates through each `ride_segment` tuple in the input list.
    #   - Unpacks each tuple into `start_time`, `end_time`, and `num_passengers`.
    for start_time, end_time, num_passengers in ride_segments:
        # Line 3: `events.append((start_time, 'pickup', num_passengers))`
        #   - For each ride segment, a 'pickup' event is created.
        #   - It's a tuple containing the time of the event (`start_time`),
        #     the type of event ('pickup'), and the number of passengers involved.
        #   - This event is added to the `events` list.
        events.append((start_time, 'pickup', num_passengers))
        # Line 4: `events.append((end_time, 'dropoff', num_passengers))`
        #   - Similarly, a 'dropoff' event is created for the `end_time` of the segment.
        #   - This event is also added to the `events` list.
        events.append((end_time, 'dropoff', num_passengers))

    # Line 5: `events.sort(key=lambda x: (x[0], x[1] == 'dropoff'))`
    #   - Sorts the `events` list. This is a crucial step.
    #   - `key=lambda x: (x[0], x[1] == 'dropoff')`: This defines the sorting criteria.
    #     - It sorts primarily by the event time (`x[0]`).
    #     - For events occurring at the exact same time, it uses a secondary sort criterion:
    #       `x[1] == 'dropoff'`. This expression evaluates to `True` (which Python treats
    #       as 1 in sorting context) for 'dropoff' events and `False` (treated as 0)
    #       for 'pickup' events (or any other type).
    #     - Since `False` (0) comes before `True` (1) in default ascending sort order,
    #       if a 'pickup' and 'dropoff' happen at the same time, the 'dropoff' event
    #       will effectively be processed *before* the 'pickup' if we sort ascending
    #       and then iterate. To ensure dropoffs are processed first at the same time,
    #       we want 'dropoff' (True, 1) to come before 'pickup' (False, 0) if we are using
    #       a standard ascending sort.
    #       A common way to sort dropoffs first at the same time point is to make 'dropoff'
    #       map to a smaller value. `x[1] == 'pickup'` would sort pickups first.
    #       Let's refine the sort key to ensure dropoffs come first at the same time:
    #       A 'dropoff' type should have a lower sort order value than 'pickup' at the same time.
    #       `lambda x: (x[0], 0 if x[1] == 'dropoff' else 1)`
    #       This means if x[0] (time) is the same, dropoffs (key part = 0) will come before pickups (key part = 1).
    events.sort(key=lambda x: (x[0], 0 if x[1] == 'dropoff' else 1))


    # Line 6: `current_occupancy = 0`
    #   - Initializes a variable to keep track of the number of passengers currently
    #     in the vehicle.
    current_occupancy = 0
    # Line 7: `for time, event_type, passengers in events:`
    #   - Iterates through the sorted list of `events`.
    for time, event_type, passengers in events:
        # Line 8: `if event_type == 'pickup':`
        #   - Checks if the current event is a 'pickup'.
        if event_type == 'pickup':
            # Line 9: `current_occupancy += passengers`
            #   - If it's a pickup, add the number of `passengers` to `current_occupancy`.
            current_occupancy += passengers
        # Line 10: `elif event_type == 'dropoff':`
        #   - Else, if the current event is a 'dropoff'.
        elif event_type == 'dropoff':
            # Line 11: `current_occupancy -= passengers`
            #   - If it's a dropoff, subtract the number of `passengers` from `current_occupancy`.
            current_occupancy -= passengers
        
        # Line 12: `if current_occupancy > max_capacity:`
        #   - After each event (pickup or dropoff), check if the `current_occupancy`
        #     has exceeded the `max_capacity` of the vehicle.
        if current_occupancy > max_capacity:
            # Line 13: `return False`
            #   - If capacity is exceeded at any point, immediately return `False`.
            return False
            
    # Line 14: `return True`
    #   - If the loop completes and capacity was never exceeded, it means all
    #     segments can be completed. Return `True`.
    return True

# ============================================================================
# --- Scenario 2: Short Video / Reels ---
# ============================================================================

# ----------------------------------------------------------------------------
# 2.1 Product Sense (Questions - Reference)
# ----------------------------------------------------------------------------
"""
Question 2a (Original): Measuring Success, Visualizing DAU ...
New PS Question 1: Tracking significant user location changes ...
New PS Question 2: Comparing engagement of original vs. shared content ...
Product Analytics/Dashboarding Idea: Visualizing Reels' impact on other features ...
"""

# ----------------------------------------------------------------------------
# 2.2 Data Modeling (Question - Reference)
# ----------------------------------------------------------------------------
"""
Question 2b: Handling high volume & multi-layer sharing ...
"""

# ----------------------------------------------------------------------------
# 2.3 SQL (Questions - Reference)
# ----------------------------------------------------------------------------
"""
Question 2c (Original): Posts with zero likes/reacts on posting day ...
Question 2e (New): Content created today with reactions but no comments ...
"""

# ----------------------------------------------------------------------------
# 2.4 Python - Session-based Engagement Stream (Question & Solution)
# ----------------------------------------------------------------------------
"""
Question: Implement the Python function `process_event(event)` and related logic...
(Full question description and I/O examples in earlier part of this file)
"""
# Global state for session-based engagement stream processing
engagement_buffer_user = {}
total_engagement_counts_user = {'likes': 0, 'comments': 0, 'views': 0}
internal_test_users_config = {'user_test_A', 'user_test_B'}

# Placeholder for your answer
def process_event(event, buffer, totals, test_users):
    
    session_id = event.get('session_id')

    user_id = event.get('user_id')

    event_type = event.get('event_type')


    if not session_id:
        return 
    
    if session_id not in engagement_buffer_user:

        engagement_buffer_user[session_id] = {'events':[],'is_internal':False}
    
    is_event_internal = user_id in internal_test_users_config = user_id in internal_test_users

    engagement_buffer_user[session_id]['events'].append(event)

    if is_event_internal:
        engagement_buffer_user[session_id]['is_internal'] = True
    
    if event_type == 'session_end':
        session_data = engagement_buffer_user.pop(session_id,None)
    
    if session_data:
        if not session_data['is_internal']:
            for buffered_event in session_data['events']:
                b_event_type = buffered_event.get('event_type')

                if b_event_type =='like':
                    total_engagement_counts_user['likes']+=1

                elif b_event_type =='comment':
                    total_engagement_counts_user['comment']+=1
                
                elif b_event_type =='view':
                    total_engagement_counts_user['views']+=1

# Solution
_solution_engagement_buffer = {}
_solution_total_engagement_counts = {'likes': 0, 'comments': 0, 'views': 0}
_solution_internal_test_users = {'user_test_A', 'user_test_B'}
def reset_engagement_state_solution():
    """Solution for: Resets the global state for engagement processing."""
    global _solution_engagement_buffer, _solution_total_engagement_counts
    _solution_engagement_buffer = {}
    _solution_total_engagement_counts = {'likes': 0, 'comments': 0, 'views': 0}

def process_event_solution(event):
    """
    Solution for: Processes a single engagement event, buffers it by session_id,
    and updates aggregate counts for non-internal sessions upon session_end.

    Args:
        event (dict): An engagement event dictionary with keys like
                      'session_id', 'user_id', 'event_type'.

    Line-by-Line Explanation:
    -------------------------
    """
    global _solution_engagement_buffer, _solution_total_engagement_counts, _solution_internal_test_users

    # Line 1: `session_id = event.get('session_id')`
    #   - Purpose: Safely extract the session identifier from the event.
    #   - Why `get()`: To avoid a `KeyError` if 'session_id' is missing, returning `None` instead.
    session_id = event.get('session_id')
    # Line 2: `user_id = event.get('user_id')`
    #   - Purpose: Safely extract the user identifier.
    user_id = event.get('user_id')
    # Line 3: `event_type = event.get('event_type')`
    #   - Purpose: Safely extract the type of event.
    event_type = event.get('event_type')

    # Line 4: `if not session_id:`
    #   - Purpose: Validate essential data. Events without a session ID cannot be
    #     correctly buffered or processed in a session-based manner.
    if not session_id:
        # Line 6: `return`
        #   - Action: Exit the function if no session ID is present.
        return

    # Line 7: `if session_id not in _solution_engagement_buffer:`
    #   - Purpose: Check if this is the first event seen for this particular session.
    if session_id not in _solution_engagement_buffer:
        # Line 8: `_solution_engagement_buffer[session_id] = {'events': [], 'is_internal': False}`
        #   - Action: If it's a new session, initialize its entry in the
        #     `_solution_engagement_buffer` dictionary.
        #   - Why this structure: Each session will store a list of its `events` and
        #     a boolean flag `is_internal` to track if any event within it is from a test user.
        _solution_engagement_buffer[session_id] = {'events': [], 'is_internal': False}

    # Line 9: `is_event_internal = user_id in _solution_internal_test_users`
    #   - Purpose: Determine if the current specific event is from an internal test user.
    #   - Action: Checks if the `user_id` exists in the predefined set of internal test users.
    is_event_internal = user_id in _solution_internal_test_users

    # Line 10: `_solution_engagement_buffer[session_id]['events'].append(event)`
    #   - Purpose: Store the current event as part of its session.
    #   - Action: Appends the entire `event` dictionary to the list of events
    #     associated with its `session_id`.
    _solution_engagement_buffer[session_id]['events'].append(event)

    # Line 11: `if is_event_internal:`
    #   - Purpose: If the current event is from an internal user, the entire session
    #     should be treated as internal.
    if is_event_internal:
        # Line 12: `_solution_engagement_buffer[session_id]['is_internal'] = True`
        #   - Action: Sets the `is_internal` flag for the session to `True`.
        #   - Why: This is a "sticky" flag; once any event marks the session as internal,
        #     the entire session is considered internal for aggregation purposes.
         _solution_engagement_buffer[session_id]['is_internal'] = True

    # Line 13: `if event_type == 'session_end':`
    #   - Purpose: Detect the end of a session to trigger processing of its buffered events.
    if event_type == 'session_end':
        # Line 14: `session_data = _solution_engagement_buffer.pop(session_id, None)`
        #   - Purpose: Retrieve all data for the ended session and remove it from the active buffer.
        #   - Action: `pop()` removes the entry for `session_id` from the buffer and returns its value.
        #   - Why `None` default: Provides robustness if a `session_end` event is received for
        #     a session not in the buffer (e.g., duplicate end event).
        session_data = _solution_engagement_buffer.pop(session_id, None)

        # Line 15: `if session_data:`
        #   - Purpose: Ensure that data was actually retrieved for the session (it wasn't an orphaned `session_end`).
        if session_data:
            # Line 16: `if not session_data['is_internal']:`
            #   - Purpose: The core logic to exclude test sessions from aggregation.
            #   - Action: Proceeds to aggregate events only if the session's `is_internal` flag is `False`.
            if not session_data['is_internal']:
                # Line 17: `for buffered_event in session_data['events']:`
                #   - Purpose: Process each event that was collected for this non-internal session.
                for buffered_event in session_data['events']:
                    # Line 18: `b_event_type = buffered_event.get('event_type')`
                    #   - Purpose: Get the type of the individual buffered event.
                    b_event_type = buffered_event.get('event_type')
                    # Line 19-24: Conditional aggregation
                    #   - Purpose: Increment the appropriate global engagement counters based on the event type.
                    if b_event_type == 'like':
                        _solution_total_engagement_counts['likes'] += 1
                    elif b_event_type == 'comment':
                         _solution_total_engagement_counts['comments'] += 1
                    elif b_event_type == 'view': # Assumes a 'view' event directly counts as one view
                         _solution_total_engagement_counts['views'] += 1
            # Line 25: `else:` (corresponds to `if not session_data['is_internal']`)
            #   - Purpose: Handle sessions that were marked as internal.
            # else:
                # Action: No aggregation is performed for internal sessions.
                pass

# ----------------------------------------------------------------------------
# 2.6 Python - Fixed-Size Buffer Stream Processing (Question & Solution)
# ----------------------------------------------------------------------------
"""
Question: Write a python function to take an input of stream data (list of dictionaries)
and then print it out following some string format... (aggregates total_engagement, total_view_seconds)
(Full question description and I/O examples in earlier part of this file)
"""
# Global state for fixed buffer stream processing
fixed_buffer_stream_data_user = []
FIXED_BUFFER_SIZE_CONFIG = 3
fixed_buffer_total_engagement_user = 0
fixed_buffer_total_view_seconds_user = 0.0
fixed_buffer_test_user_ids_config = {'test_user_reel'}

# Placeholder for your answer
def process_fixed_buffer_stream(event_item, buffer, buffer_size, totals_engagement_ref, totals_view_seconds_ref, test_users):
    # TODO: Implement
    pass
def flush_fixed_buffer(buffer, totals_engagement_ref, totals_view_seconds_ref, test_users):
    # TODO: Implement
    pass

# Solution
_solution_fixed_buffer_stream_data = []
_solution_FIXED_BUFFER_SIZE = 3
_solution_fixed_buffer_total_engagement = 0
_solution_fixed_buffer_total_view_seconds = 0.0
_solution_fixed_buffer_test_user_ids = {'test_user_reel'}
def reset_fixed_buffer_state_solution():
    """Solution for: Resets the global state for fixed buffer stream processing."""
    global _solution_fixed_buffer_stream_data, _solution_fixed_buffer_total_engagement, _solution_fixed_buffer_total_view_seconds
    _solution_fixed_buffer_stream_data = []
    _solution_fixed_buffer_total_engagement = 0
    _solution_fixed_buffer_total_view_seconds = 0.0

def process_fixed_buffer_stream_solution(event_item):
    """
    Solution for: Processes a stream of input data (dictionaries) using a fixed-size buffer.

    Args:
        event_item (dict): A dictionary representing an event.

    Line-by-Line Explanation:
    -------------------------
    """
    global _solution_fixed_buffer_stream_data, _solution_FIXED_BUFFER_SIZE
    global _solution_fixed_buffer_total_engagement, _solution_fixed_buffer_total_view_seconds, _solution_fixed_buffer_test_user_ids

    # Line 1-3: Extract event properties and determine if it's a test event.
    user_id = event_item.get('user_id')
    event_type = event_item.get('event_type')
    is_test_event = user_id in _solution_fixed_buffer_test_user_ids

    # Line 4-7: `current_event_data = { ... }`
    #   - Purpose: Create a container for the event and its test status.
    #   - Why: The 'is_test' status needs to be associated with the event when it's
    #     later popped from the buffer, not just when it's initially processed.
    current_event_data = {
        'data': event_item,
        'is_test': is_test_event
    }

    # Line 8: `if len(_solution_fixed_buffer_stream_data) >= _solution_FIXED_BUFFER_SIZE:`
    #   - Purpose: Check if the buffer is full. If so, the oldest item needs to be
    #     processed and removed to make space for the new item.
    if len(_solution_fixed_buffer_stream_data) >= _solution_FIXED_BUFFER_SIZE:
        # Line 9: `oldest_event_container = _solution_fixed_buffer_stream_data.pop(0)`
        #   - Action: Removes and returns the item at the beginning of the list (oldest item, FIFO).
        oldest_event_container = _solution_fixed_buffer_stream_data.pop(0)
        # Line 10: `old_event = oldest_event_container['data']`
        #   - Action: Extracts the actual event dictionary from the container.
        old_event = oldest_event_container['data']
        # Line 11: `was_old_event_test = oldest_event_container['is_test']`
        #   - Action: Retrieves the test status of this oldest event.
        was_old_event_test = oldest_event_container['is_test']

        # Line 12: `if not was_old_event_test:`
        #   - Purpose: Aggregate data only if the event being removed was NOT a test event.
        if not was_old_event_test:
            # Line 13-14: Aggregate view duration.
            #   - Why `get()`: Handles cases where 'view_duration_ms' might be missing.
            #   - Why `/ 1000.0`: Converts milliseconds to seconds.
            if old_event.get('event_type') == 'view' and old_event.get('view_duration_ms') is not None:
                _solution_fixed_buffer_total_view_seconds += old_event['view_duration_ms'] / 1000.0
            # Line 15-17: Aggregate other types of engagements.
            #   - Why `!= 'view'`: A simple way to count non-view events as general engagement.
            #     This could be more specific (e.g., `in ['like', 'comment', 'share']`).
            if old_event.get('event_type') != 'view':
                 _solution_fixed_buffer_total_engagement += 1
        
        # Line 18-23: Formatting `post_ids_str` for printing (optional, for debugging/output).
        #   - Purpose: Create a human-readable string of post IDs.
        #   - Why `isinstance`: Handles cases where `post_id` could be a single value or a list.
        post_ids_str = ""
        if isinstance(old_event.get('post_id'), list):
            post_ids_str = ", ".join(map(str, old_event['post_id']))
        elif old_event.get('post_id') is not None:
            post_ids_str = str(old_event.get('post_id'))
        
        # Line 24-25: Printing details of the processed (removed) item. (Commented out for production)
        # print(f"Output (processed oldest): User: {old_event.get('user_id')}, Event: {old_event.get('event_type')}, Posts: [{post_ids_str}], WasTest: {was_old_event_test}")
        # print(f"  Current Aggregates -> Total Engagement: {_solution_fixed_buffer_total_engagement}, Total View Seconds: {_solution_fixed_buffer_total_view_seconds:.2f}")

    # Line 26: `_solution_fixed_buffer_stream_data.append(current_event_data)`
    #   - Purpose: Add the new incoming event (and its test status) to the buffer.
    #   - Action: Appends to the end of the list.
    _solution_fixed_buffer_stream_data.append(current_event_data)

    # Line 27: `if is_test_event:`
    #   - Purpose: As per requirement, print test events when they are added to the buffer.
    if is_test_event:
        # Line 28-32: Formatting `post_ids_str_new` for the newly added test item.
        post_ids_str_new = ""
        if isinstance(event_item.get('post_id'), list):
            post_ids_str_new = ", ".join(map(str, event_item['post_id']))
        elif event_item.get('post_id') is not None:
            post_ids_str_new = str(event_item.get('post_id'))
        # Line 33: Printing details of the buffered test event. (Commented out for production)
        # print(f"Buffered (Test Event): User: {user_id}, Event: {event_type}, Posts: [{post_ids_str_new}] - Not aggregated yet.")
    
def flush_fixed_buffer_solution():
    """
    Solution for: Processes and prints any remaining items in the fixed_buffer_stream_data.
    Called typically at the end of the stream to ensure all buffered items are handled.

    Line-by-Line Explanation:
    -------------------------
    """
    global _solution_fixed_buffer_stream_data, _solution_fixed_buffer_total_engagement, _solution_fixed_buffer_total_view_seconds
    # Line 1: `while _solution_fixed_buffer_stream_data:`
    #   - Purpose: Loop as long as there are items remaining in the buffer.
    while _solution_fixed_buffer_stream_data:
        # Line 2-5: Same logic as when the buffer is full: remove the oldest item,
        #   extract its data and original test status.
        oldest_event_container = _solution_fixed_buffer_stream_data.pop(0)
        old_event = oldest_event_container['data']
        was_old_event_test = oldest_event_container['is_test']

        # Line 6-10: Aggregate data if the flushed item was not a test event.
        #   - This is identical to the aggregation logic in `process_fixed_buffer_stream_solution`.
        if not was_old_event_test:
            if old_event.get('event_type') == 'view' and old_event.get('view_duration_ms') is not None:
                _solution_fixed_buffer_total_view_seconds += old_event['view_duration_ms'] / 1000.0
            if old_event.get('event_type') != 'view':
                 _solution_fixed_buffer_total_engagement += 1
        
        # Line 11-15: Format post_ids for printing the flushed item.
        post_ids_str = ""
        if isinstance(old_event.get('post_id'), list):
            post_ids_str = ", ".join(map(str, old_event['post_id']))
        elif old_event.get('post_id') is not None:
            post_ids_str = str(old_event.get('post_id'))
        # Line 16: Print details of the flushed item. (Commented out for production)
        # print(f"Output (flushed): User: {old_event.get('user_id')}, Event: {old_event.get('event_type')}, Posts: [{post_ids_str}], WasTest: {was_old_event_test}")
    # Line 17: Print final aggregates after the buffer is empty. (Commented out for production)
    # print(f"Final Aggregates -> Total Engagement: {_solution_fixed_buffer_total_engagement}, Total View Seconds: {_solution_fixed_buffer_total_view_seconds:.2f}")

# ============================================================================
# --- Scenario 3: Streaming Platform ---
# ============================================================================
# ----------------------------------------------------------------------------
# 3.1 Product Sense (Questions - Reference)
# ----------------------------------------------------------------------------
""" Question: User engagement types and metrics for Platform, User, Video levels ... """

# ----------------------------------------------------------------------------
# 3.2 Data Modeling (Question - Reference)
# ----------------------------------------------------------------------------
""" Question: Design `fact_viewing_sessions`, measures, FKs, handling duration/pauses/completion ... """

# ----------------------------------------------------------------------------
# 3.3 SQL (Questions - Reference)
# ----------------------------------------------------------------------------
"""
Question (Snapshot Update): Update `user_cumulative_snapshot` from `fact_viewing_sessions` ...
Question (New Content Aggregation): Distinct user count and sum of watch time per content_id ...
"""

# ----------------------------------------------------------------------------
# 3.4 Python - Average Rating per Category (Question & Solution)
# ----------------------------------------------------------------------------
"""
Question: Given a list of movies and categories, map movies to categories
and return the average rating per category.
(This is `calculate_average_ratings` from the original guide)

Example Input:
movie_data = [
    {'title': 'Movie A', 'category': 'Action', 'rating': 8.5},
    {'title': 'Movie B', 'category': 'Comedy', 'rating': 7.0},
    {'title': 'Movie C', 'category': 'Action', 'rating': 9.0},
    {'title': 'Movie D', 'category': 'Drama', 'rating': 8.0},
    {'title': 'Movie E', 'category': 'Comedy', 'rating': 6.5},
    {'title': 'Movie F', 'category': 'Action', 'rating': '7.5'}, # Rating as string
    {'title': 'Movie G', 'category': 'Action'}, # Missing rating
    {'title': 'Movie H', 'rating': 5.0} # Missing category
]
Expected Output:
{
    'Action': (8.5 + 9.0 + 7.5) / 3 = 8.333...,
    'Comedy': (7.0 + 6.5) / 2 = 6.75,
    'Drama': 8.0 / 1 = 8.0
}
"""
# Placeholder for your answer to Average Rating per Category
def calculate_average_ratings(movie_data):
    # TODO: Implement your logic here
    return {}

# Solution for Average Rating per Category
def calculate_average_ratings_solution(movie_data):
    """
    Solution for: Calculates the average rating per category from a list of movie dicts.

    Args:
        movie_data: A list of dictionaries, where each dict represents a movie
                    and should have 'category' and 'rating' keys.

    Returns:
        A dictionary mapping category (str) to average rating (float).

    Line-by-Line Explanation:
    -------------------------
    """
    # Line 1: `if not movie_data:`
    if not movie_data:
        # Line 2: `return {}`
        return {}

    # Line 3: `category_stats = {}`
    category_stats = {}

    # Line 4: `for movie in movie_data:`
    for movie in movie_data:
        # Line 5: `category = movie.get('category')`
        category = movie.get('category')
        # Line 6: `rating = movie.get('rating')`
        rating = movie.get('rating')

        # Line 7: `if category and rating is not None:`
        if category and rating is not None:
            # Line 8: `try: numeric_rating = float(rating)`
            try:
                numeric_rating = float(rating)
            # Line 9-11: `except (ValueError, TypeError): continue`
            except (ValueError, TypeError):
                continue

            # Line 12: `if category not in category_stats:`
            if category not in category_stats:
                # Line 13: Initialize category stats
                category_stats[category] = {'total_rating': 0.0, 'count': 0}
            
            # Line 14: `category_stats[category]['total_rating'] += numeric_rating`
            category_stats[category]['total_rating'] += numeric_rating
            # Line 15: `category_stats[category]['count'] += 1`
            category_stats[category]['count'] += 1

    # Line 16: `average_ratings = {}`
    average_ratings = {}
    # Line 17: `for category, stats in category_stats.items():`
    for category, stats in category_stats.items():
        # Line 18: `if stats['count'] > 0:`
        if stats['count'] > 0:
            # Line 19: Calculate and store average rating
            average_ratings[category] = stats['total_rating'] / stats['count']

    # Line 20: `return average_ratings`
    return average_ratings

# ----------------------------------------------------------------------------
# 3.5 Python - Top N Movies per Category (Question & Solution)
# ----------------------------------------------------------------------------
"""
Question: Given a list of movies and categories, map movies to categories
and return top N movies per category based on rating.
(This is `get_top_n_movies_per_category` from the original guide)

Example Input:
movie_data = [
    {'title': 'Movie A', 'category': 'Action', 'rating': 8.5},
    {'title': 'Movie B', 'category': 'Comedy', 'rating': 7.0},
    {'title': 'Movie C', 'category': 'Action', 'rating': 9.0},
    {'title': 'Movie G', 'category': 'Action', 'rating': 8.8},
    {'title': 'Movie H', 'category': 'Comedy', 'rating': 9.5}
]
n = 1
Expected Output:
{
    'Action': [('Movie C', 9.0)],
    'Comedy': [('Movie H', 9.5)]
}

Example Input:
movie_data = (same as above)
n = 2
Expected Output:
{
    'Action': [('Movie C', 9.0), ('Movie G', 8.8)],
    'Comedy': [('Movie H', 9.5), ('Movie B', 7.0)]
}
"""
# Placeholder for your answer to Top N Movies per Category
def get_top_n_movies_per_category(movie_data, n):
    
    if not movie_data and n<1:
        return None
    movies_by_category = {}
    for movie in movie_data:
        title = movie.get('title')
        category = movie.get('category')
        rating = movie.get('rating')

        
    return {}

# Solution for Top N Movies per Category
def get_top_n_movies_per_category_solution(movie_data, n):
    """
    Solution for: Given a list of movie dictionaries, finds the top N movies by rating
    for each category.

    Args:
        movie_data: A list of dictionaries, where each dict represents a movie
                    and has at least 'title', 'category', and 'rating' keys.
        n (int): The number of top movies to return per category.

    Returns:
        A dictionary where keys are category names (str) and values are lists
        of tuples, each tuple being (movie_title, rating), sorted in
        descending order of rating. Each list contains at most N movies.

    Line-by-Line Explanation:
    -------------------------
    """
    # Line 1: `if not movie_data or n <= 0:`
    if not movie_data or n <= 0:
        # Line 2: `return {}`
        return {}

    # Line 3: `movies_by_category = {}`
    movies_by_category = {}
    # Line 4: `for movie in movie_data:`
    for movie in movie_data:
        # Line 5-7: Retrieve movie details
        title = movie.get('title')
        category = movie.get('category')
        rating = movie.get('rating')

        # Line 8: `if title and category and rating is not None:`
        if title and category and rating is not None:
            # Line 9-13: Convert rating to float
            try:
                numeric_rating = float(rating)
            except (ValueError, TypeError):
                continue

            # Line 14: `if category not in movies_by_category:`
            if category not in movies_by_category:
                # Line 15: Initialize list for new category
                movies_by_category[category] = []
            # Line 16: `movies_by_category[category].append((numeric_rating, title))`
            #   - Note: Storing rating first in the tuple `(numeric_rating, title)`
            #     makes default tuple sorting (which `list.sort` uses if no key or a
            #     simple key is provided) work directly on ratings.
            movies_by_category[category].append((numeric_rating, title))

    # Line 17: `top_n_by_category = {}`
    top_n_by_category = {}
    # Line 18: `for category, movies in movies_by_category.items():`
    for category, movies in movies_by_category.items():
        # Line 19: `movies.sort(key=lambda x: x[0], reverse=True)`
        #   - Sorts the list of `(rating, title)` tuples for the current category.
        #   - `key=lambda x: x[0]` sorts based on the rating (the first element).
        #   - `reverse=True` ensures descending order (highest rating first).
        movies.sort(key=lambda x: x[0], reverse=True)

        # Line 20: `top_n_list = [(title, rating) for rating, title in movies[:n]]`
        #   - `movies[:n]` takes the top N (or fewer) movies from the sorted list.
        #   - The list comprehension then iterates through these top `(rating, title)` tuples
        #     and creates new tuples in the `(title, rating)` format for the final output.
        top_n_list = [(title, rating) for rating, title in movies[:n]]
        # Line 21: `top_n_by_category[category] = top_n_list`
        top_n_by_category[category] = top_n_list

    # Line 22: `return top_n_by_category`
    return top_n_by_category

# ----------------------------------------------------------------------------
# 3.6 Python - Average Rating per Movie (Question & Solution)
# ----------------------------------------------------------------------------
"""
Question: Given a list of movie rating instances (each with title and rating),
calculate the average rating for each unique movie title.
(This is `calculate_average_movie_ratings` from the original guide)

Example Input:
movie_ratings_list = [
    {'title': 'Movie Alpha', 'rating': 8.0},
    {'title': 'Movie Beta', 'rating': 7.0},
    {'title': 'Movie Alpha', 'rating': 9.0},
    {'title': 'Movie Alpha', 'rating': 8.5},
    {'title': 'Movie Beta', 'rating': 7.5},
]
Expected Output:
{
    'Movie Alpha': 8.5,  # (8.0 + 9.0 + 8.5) / 3
    'Movie Beta': 7.25   # (7.0 + 7.5) / 2
}
"""
# Placeholder for your answer to Average Rating per Movie
def calculate_average_movie_ratings(movie_data):
    # TODO: Implement your logic here
    return {}

# Solution for Average Rating per Movie
def calculate_average_movie_ratings_solution(movie_data):
    """
    Solution for: Calculates the average rating per movie title from a list of movie dicts.
    Each dict represents a single rating instance for a movie.

    Args:
        movie_data: A list of dictionaries, where each dict should have
                    'title' and 'rating' keys.

    Returns:
        A dictionary mapping movie title (str) to its average rating (float).

    Line-by-Line Explanation:
    -------------------------
    """
    # Line 1: `if not movie_data:`
    if not movie_data:
        # Line 2: `return {}`
        return {}

    # Line 3: `movie_stats = {}`
    movie_stats = {}

    # Line 4: `for rating_instance in movie_data:`
    for rating_instance in movie_data:
        # Line 5: `title = rating_instance.get('title')`
        title = rating_instance.get('title')
        # Line 6: `rating = rating_instance.get('rating')`
        rating = rating_instance.get('rating')

        # Line 7: `if title and rating is not None:`
        if title and rating is not None:
            # Line 8-12: Convert rating to float
            try:
                numeric_rating = float(rating)
            except (ValueError, TypeError):
                continue

            # Line 13: `if title not in movie_stats:`
            if title not in movie_stats:
                # Line 14: Initialize stats for new movie title
                movie_stats[title] = {'total_rating': 0.0, 'count': 0}
            
            # Line 15: `movie_stats[title]['total_rating'] += numeric_rating`
            movie_stats[title]['total_rating'] += numeric_rating
            # Line 16: `movie_stats[title]['count'] += 1`
            movie_stats[title]['count'] += 1

    # Line 17: `average_ratings_per_movie = {}`
    average_ratings_per_movie = {}
    # Line 18: `for title, stats in movie_stats.items():`
    for title, stats in movie_stats.items():
        # Line 19: `if stats['count'] > 0:`
        if stats['count'] > 0:
            # Line 20: Calculate and store average rating for the movie
            average_ratings_per_movie[title] = stats['total_rating'] / stats['count']
            
    # Line 21: `return average_ratings_per_movie`
    return average_ratings_per_movie

# ============================================================================
# --- Scenario 4, 5, 6, 7, 8 Python Functions (Implementations & Explanations) ---
# ============================================================================

# ----------------------------------------------------------------------------
# Scenario: News Feed (Python part from original guide, similar to Short Video stream)
# `process_newsfeed_log` and `calculate_session_valid_reads`
# ----------------------------------------------------------------------------
"""
Question: Process newsfeed logs to determine valid post views per session.
A view is valid if a post is on screen for >= 5 seconds OR >= 80% visible.
`process_newsfeed_log(log)` updates impression data (start, end, max_perc).
`calculate_session_valid_reads(session_id)` computes valid views for a session.

Example Input for `process_newsfeed_log` (called multiple times):
log1 = {'session_id': 's1', 'post_id': 'p1', 'time_stamp': 100, 'event_type': 'start', 'percentage': 10}
log2 = {'session_id': 's1', 'post_id': 'p1', 'time_stamp': 106, 'event_type': 'end', 'percentage': 90}
log3 = {'session_id': 's1', 'post_id': 'p2', 'time_stamp': 110, 'event_type': 'start', 'percentage': 50}
log4 = {'session_id': 's1', 'post_id': 'p2', 'time_stamp': 112, 'event_type': 'end', 'percentage': 50}

After processing these logs for session 's1':
Example call: `calculate_session_valid_reads('s1')`
Expected Output: 1 (p1 is valid: duration 6s >= 5s; p2 is not: duration 2s < 5s AND max_perc 50 < 80)
"""
# Global state for newsfeed view validation
# These will be used by your functions if you choose to use globals.
newsfeed_session_data_user = {}

# Placeholder for your answer to process_newsfeed_log
def process_newsfeed_log(log, session_buffer):
    # TODO: Implement your logic here
    # Args:
    #  log (dict): the event log
    #  session_buffer (dict): e.g. newsfeed_session_data_user
    pass

# Placeholder for your answer to calculate_session_valid_reads
def calculate_session_valid_reads(session_id, session_buffer):
    # TODO: Implement your logic here
    # Args:
    #  session_id (str): the session to process
    #  session_buffer (dict): e.g. newsfeed_session_data_user
    return 0


# Solution for News Feed View Validation
_solution_newsfeed_session_data = {}

def reset_newsfeed_state_solution():
    global _solution_newsfeed_session_data
    _solution_newsfeed_session_data = {}

def process_newsfeed_log_solution(log):
    """
    Solution for: Processes a single newsfeed log event ('start' or 'end') and updates
    the global newsfeed_session_data dictionary.

    Args:
        log (dict): A newsfeed log event. Expected keys: 'session_id', 'post_id',
                    'time_stamp', 'event_type', 'percentage'.
    Line-by-Line Explanation:
    -------------------------
    """
    global _solution_newsfeed_session_data

    # Line 1-5: Safely get log details
    session_id = log.get('session_id')
    post_id = log.get('post_id')
    timestamp = log.get('time_stamp')
    event_type = log.get('event_type')
    percentage = log.get('percentage', 0)

    # Line 6-8: Basic validation
    if not all([session_id, post_id, timestamp is not None, event_type]):
        return

    # Line 9: Initialize session if new
    if session_id not in _solution_newsfeed_session_data:
        _solution_newsfeed_session_data[session_id] = {}

    # Line 10: Initialize post within session if new
    if post_id not in _solution_newsfeed_session_data[session_id]:
         _solution_newsfeed_session_data[session_id][post_id] = {'start': None, 'end': None, 'max_perc': 0}

    # Line 11: Get reference to post_info
    post_info = _solution_newsfeed_session_data[session_id][post_id]

    # Line 12: `if event_type == 'start':`
    if event_type == 'start':
        # Line 13-14: Update start time if earlier
        if post_info['start'] is None or timestamp < post_info['start']:
            post_info['start'] = timestamp
    # Line 15: `elif event_type == 'end':`
    elif event_type == 'end':
        # Line 16-17: Update end time if later
         if post_info['end'] is None or timestamp > post_info['end']:
             post_info['end'] = timestamp

    # Line 18-23: Update max_perc
    try:
        numeric_percentage = float(percentage)
        current_max_perc = float(post_info.get('max_perc', 0))
        post_info['max_perc'] = max(current_max_perc, numeric_percentage)
    except (ValueError, TypeError):
        pass

def calculate_session_valid_reads_solution(session_id):
    """
    Solution for: Calculates the number of valid reads for a given session_id based on
    the data stored in the global newsfeed_session_data.

    Args:
        session_id (str): The ID of the session.

    Returns:
        int: Count of posts meeting valid read criteria (duration >= 5s OR max_perc >= 80%).

    Line-by-Line Explanation:
    -------------------------
    """
    global _solution_newsfeed_session_data
    # Line 1: `valid_reads_count = 0`
    valid_reads_count = 0

    # Line 2: `if session_id in _solution_newsfeed_session_data:`
    if session_id in _solution_newsfeed_session_data:
        # Line 3: `session_posts = _solution_newsfeed_session_data.get(session_id, {})`
        session_posts = _solution_newsfeed_session_data.get(session_id, {})
        # Line 4: `for post_id, info in session_posts.items():`
        for post_id, info in session_posts.items():
            # Line 5-7: Retrieve start, end, max_perc
            start_time = info.get('start')
            end_time = info.get('end')
            max_perc = info.get('max_perc', 0)

            # Line 8: Check for valid start and end times
            if start_time is not None and end_time is not None and end_time >= start_time:
                # Line 9: `duration = end_time - start_time`
                duration = end_time - start_time
                # Line 10: Apply valid read criteria
                if duration >= 5 or max_perc >= 80:
                    # Line 11: `valid_reads_count += 1`
                    valid_reads_count += 1
    # Line 12: `else:`
    # else:
        pass

    # Line 13: `return valid_reads_count`
    return valid_reads_count

# ----------------------------------------------------------------------------
# Scenario: Photo Upload (Python part from original guide)
# `process_upload_log`
# ----------------------------------------------------------------------------
"""
Question: Process a stream of photo upload logs ('upload_start', 'upload_end')
to calculate the running average upload time for successful uploads.
`process_upload_log(log)` handles each event.

Example Input Stream (processed one by one):
logs = [
     {'timestamp': 1000, 'event_type': 'upload_start', 'upload_id': 'up1'},
     {'timestamp': 1050, 'event_type': 'upload_start', 'upload_id': 'up2'},
     {'timestamp': 1150, 'event_type': 'upload_end', 'upload_id': 'up1', 'is_success': True},
     {'timestamp': 1250, 'event_type': 'upload_end', 'upload_id': 'up2', 'is_success': True},
]
Expected Behavior (conceptual print output during processing):
- After up1 ends: "Processed successful upload up1. Duration: 150 ms. ... Current Avg Time: 150.00 ms"
- After up2 ends: "Processed successful upload up2. Duration: 200 ms. ... Current Avg Time: 175.00 ms"
Final upload_stats_user: {'total_duration_ms': 350, 'successful_uploads': 2}
"""
# Global state for photo upload processing
# These will be used by your function if you choose to use globals.
pending_uploads_user = {}
upload_stats_user = {'total_duration_ms': 0, 'successful_uploads': 0}

# Placeholder for your answer to process_upload_log
def process_upload_log(log, pending_buffer, stats_aggregator):
    # TODO: Implement your logic here
    # Args:
    #  log (dict): the event log
    #  pending_buffer (dict): e.g. pending_uploads_user
    #  stats_aggregator (dict): e.g. upload_stats_user
    pass

# Solution for Photo Upload
_solution_pending_uploads = {}
_solution_upload_stats = {'total_duration_ms': 0, 'successful_uploads': 0}

def reset_upload_state_solution():
    global _solution_pending_uploads, _solution_upload_stats
    _solution_pending_uploads = {}
    _solution_upload_stats = {'total_duration_ms': 0, 'successful_uploads': 0}

def process_upload_log_solution(log):
    """
    Solution for: Processes upload 'start'/'end' logs, calculates duration,
    and updates aggregate statistics for successful uploads.

    Args:
        log (dict): An upload log event.
    Line-by-Line Explanation:
    -------------------------
    """
    global _solution_pending_uploads, _solution_upload_stats

    # Line 1-3: Retrieve log details
    timestamp = log.get('timestamp')
    event_type = log.get('event_type')
    upload_id = log.get('upload_id')

    # Line 4-6: Basic validation
    if not all([timestamp is not None, event_type, upload_id]):
        return

    # Line 7: `if event_type == 'upload_start':`
    if event_type == 'upload_start':
        # Line 8: Check for duplicate start
        if upload_id in _solution_pending_uploads:
            pass
        # Line 9: Store start time
        _solution_pending_uploads[upload_id] = timestamp

    # Line 10: `elif event_type == 'upload_end':`
    elif event_type == 'upload_end':
        # Line 11: Check if start event was recorded
        if upload_id in _solution_pending_uploads:
            # Line 12: Get start_time and remove from pending
            start_time = _solution_pending_uploads.pop(upload_id)
            # Line 13: Calculate duration
            duration_ms = timestamp - start_time

            # Line 14-16: Check for negative duration
            if duration_ms < 0:
                return

            # Line 17: Get success status
            is_success = log.get('is_success', False)

            # Line 18: `if is_success:`
            if is_success:
                # Line 19: Update total duration
                _solution_upload_stats['total_duration_ms'] += duration_ms
                # Line 20: Update successful upload count
                _solution_upload_stats['successful_uploads'] += 1

                # Line 21-23: Optional: print current average
                if _solution_upload_stats['successful_uploads'] > 0:
                    current_avg = _solution_upload_stats['total_duration_ms'] / _solution_upload_stats['successful_uploads']
                    # print(f"Success: {upload_id}, Duration: {duration_ms}ms. Avg: {current_avg:.2f}ms")
            # Line 24: `else:` (failed upload)
            # else:
                pass
        # Line 25: `else:` (end event without start)
        # else:
            pass

# ----------------------------------------------------------------------------
# Scenario: FB Messenger (Python part from original guide)
# `generate_insert_sql`
# ----------------------------------------------------------------------------
"""
Question: Write a Python function `generate_insert_sql(log_entry, target_table)`
that takes a log entry (dictionary) and a target table name (string).
Based on conditions within the `log_entry` (e.g., `log_entry['table'] == 'A'`),
it should generate and return a SQL `INSERT` statement string.
Be mindful of basic string formatting and SQL injection risks (for this exercise,
focus on string construction, mentioning the risk).

Example Input:
log_entry_A = {'col1': "value'1", 'col2': 123, 'table': 'A'}
target_table_C = "MyTargetTable"
Expected Output: "INSERT INTO MyTargetTable (col1_from_A, col2_from_A) VALUES ('value''1', 123);"

Example Input:
log_entry_B = {'col3': 'value3', 'col4': 456.7, 'table': 'B'}
target_table_C = "MyTargetTable"
Expected Output: "INSERT INTO MyTargetTable (col3_from_B, col4_from_B) VALUES ('value3', 456.7);"
"""
# Placeholder for your answer to generate_insert_sql
def generate_insert_sql(log_entry, target_table):
    # TODO: Implement your logic here
    return None

# Solution for FB Messenger SQL Generation
def generate_insert_sql_solution(log_entry, target_table):
    """
    Solution for: Generates a SQL INSERT statement string.
    WARNING: Vulnerable to SQL injection. For demonstration only.

    Args:
        log_entry (dict): Log data.
        target_table (str): Target SQL table name.

    Returns:
        str: SQL INSERT statement or None.
    Line-by-Line Explanation:
    -------------------------
    """
    # Line 1: `source_table = log_entry.get('table')`
    source_table = log_entry.get('table')
    # Line 2: `sql_statement = None`
    sql_statement = None

    # Line 3: `try:`
    try:
        # Line 4: `if source_table == 'A':`
        if source_table == 'A':
            # Line 5-6: Get values for Table A
            col1_val = log_entry.get('col1')
            col2_val = log_entry.get('col2')
            # Line 7: Validate presence
            if col1_val is not None and col2_val is not None:
                # Line 8: Basic escaping (INSECURE)
                escaped_col1 = str(col1_val).replace("'", "''")
                # Line 9: Assume col2 is numeric
                col2_formatted = col2_val
                # Line 10: Construct SQL
                sql_statement = f"INSERT INTO {target_table} (col1_from_A, col2_from_A) VALUES ('{escaped_col1}', {col2_formatted});"
            # Line 11: `else:`
            # else:
                pass
        # Line 12: `elif source_table == 'B':`
        elif source_table == 'B':
            # Line 13-14: Get values for Table B
            col3_val = log_entry.get('col3')
            col4_val = log_entry.get('col4')
            # Line 15-20: Validate, escape, construct SQL for Table B
            if col3_val is not None and col4_val is not None:
                escaped_col3 = str(col3_val).replace("'", "''")
                col4_formatted = col4_val
                sql_statement = f"INSERT INTO {target_table} (col3_from_B, col4_from_B) VALUES ('{escaped_col3}', {col4_formatted});"
            # else:
                pass
        # Line 21: `else:` (unknown source table)
        # else:
            pass
    # Line 22: `except Exception as e:`
    except Exception as e:
        # Line 23: `sql_statement = None`
        sql_statement = None

    # Line 24: `return sql_statement`
    return sql_statement

# ============================================================================
# --- Scenario 9: Food Delivery - Order Batching (Python part) ---
# ============================================================================
# ----------------------------------------------------------------------------
# 2.4 Python (Question & Solution with Line-by-Line Explanation)
# ----------------------------------------------------------------------------
"""
Question 2.4.1 (Feasibility of Adding Order to Batch - Conceptual):
Imagine a Dasher is currently handling a batch of one or more orders, each
with specific pickup restaurant locations and customer delivery locations/time
windows. A new order request comes in.

  * Outline the logic for a Python function
    `can_add_to_batch(current_batch_details, new_order_details, dasher_current_location, current_time)`
    that would determine if this `new_order_details` can be feasibly added
    to the `current_batch_details`.
  * What key pieces of information would you need for `current_batch_details`
    and `new_order_details`?
  * What are the main conditions or constraints your function would need to
    check to ensure all orders (existing and new) can still likely be
    delivered within acceptable timeframes and without excessive detours?
  * (Focus on the logical checks and data points, not a complex routing
    algorithm. Pseudocode or a high-level Python function structure is sufficient).

Example Input (Conceptual):
current_batch_details = [
    {'order_id': 'A1', 'restaurant_loc': (lat1,lon1), 'customer_loc': (lat2,lon2), 'deadline': T1, ...},
    {'order_id': 'A2', 'restaurant_loc': (lat3,lon3), 'customer_loc': (lat4,lon4), 'deadline': T2, ...}
]
new_order_details = {'order_id': 'B1', 'restaurant_loc': (lat5,lon5), 'customer_loc': (lat6,lon6), 'deadline': T3, ...}
dasher_current_location = (lat_current, lon_current)
current_time = T_now

Expected Output: True or False
"""
# Placeholder for your answer to can_add_to_batch_conceptual
def can_add_to_batch_conceptual(current_batch_details, new_order_details, dasher_current_location, current_time):
    # TODO: Implement your conceptual logic outline here
    # This function is more about discussing the factors and constraints.
    # A simple boolean return based on a naive check is fine for the placeholder.
    print(f"Placeholder: Conceptual check for adding order {new_order_details.get('order_id')}")
    return True # Or False based on some simple placeholder logic

# Solution for can_add_to_batch_conceptual
def can_add_to_batch_conceptual_solution(current_batch_details, new_order_details, dasher_current_location, current_time):
    """
    Solution for: Outlines the logic to determine if a new order can be feasibly added
    to a Dasher's current batch. This is conceptual.

    Args: (as described in the question)
        current_batch_details (list): List of dicts for existing orders.
        new_order_details (dict): Dict for the new order.
        dasher_current_location (tuple): (lat, long).
        current_time (timestamp): Current time.

    Returns:
        bool: True if the new order can likely be added, False otherwise.

    Line-by-Line Explanation (of the provided simplified placeholder):
    -----------------------------------------------------------------
    (The code block below is a placeholder as the question asks for conceptual logic.
     The detailed conceptual logic is provided in the multi-line string above this function's docstring
     and also in the main Markdown document.)
    """
    # Line 1: `# Placeholder for detailed logic - see Solutions section in the markdown`
    #   - This is a comment indicating that the actual complex logic (involving route
    #     optimization, time window checks for all orders, etc.) is described textually
    #     in the "Solutions & Explanations" part of the main challenge document,
    #     not fully coded here. The full conceptual logic is also detailed below this code block.
    # print(f"Conceptual check for adding order {new_order_details.get('order_id')} to batch.") # Commented out
    # Line 2: `# Example naive check (actual logic is much more complex)`
    #   - Another comment highlighting that the following `if` condition is a highly
    #     simplified, naive check for demonstration purposes and doesn't represent the
    #     true complexity.
    # Line 3: `if new_order_details.get('promised_delivery_deadline', float('inf')) < current_time + 30*60:`
    #   - This line performs a very basic check.
    #   - `new_order_details.get('promised_delivery_deadline', float('inf'))`: It tries
    #     to get the `promised_delivery_deadline` for the new order. If the key is
    #     missing, it defaults to `float('inf')` (positive infinity).
    #   - `current_time + 30*60`: It calculates a time 30 minutes from the `current_time`
    #     (assuming `current_time` and deadlines are in seconds since epoch or a
    #     comparable unit; 30 minutes * 60 seconds/minute).
    #   - The condition checks if the new order's deadline is less than 30 minutes from
    #     now. This is a simplistic way to see if the order is even remotely feasible
    #     in a short timeframe, but it doesn't consider existing batch commitments,
    #     locations, or travel times.
    if new_order_details.get('promised_delivery_deadline', float('inf')) < current_time + 30*60: # Example: 30 minutes * 60 seconds/minute
        # Line 4: `return True`
        #   - If the naive condition in Line 3 is met, the function returns `True`.
        return True
    # Line 5: `return False`
    #   - If the condition in Line 3 is not met, the function returns `False`.
    return False


# ============================================================================
# SQL Setup and Query Strings (Reference - for SQLite testing)
# ============================================================================
# (SQL_ROUND1_SETUP_STMTS, SQL_QUERY_1_3_1, etc. remain here as before)
# ...

# ============================================================================
# Helper function to execute SQL with SQLite (for testing)
# ============================================================================
# (execute_sql_lite function remains here as before)
# ...

# ============================================================================
# Main execution block for testing (optional)
# ============================================================================
if __name__ == '__main__':
    print("="*40)
    print("Challenge Document - Python Executable Reference")
    print("="*40)

    # --- Test Round 1 Python ---
    print("\n--- Testing Round 1 Python: can_user_complete_rides ---")
    rides1_py = [(0, 30), (30, 60), (60, 90)]
    rides2_py = [(0, 60), (30, 90)]
    # Call your placeholder function here
    print(f"Rides1: {rides1_py} -> Can complete? {can_user_complete_rides(rides1_py)}") # Expected: Your function's output
    print(f"Rides2: {rides2_py} -> Can complete? {can_user_complete_rides(rides2_py)}") # Expected: Your function's output

    # --- Test Round 2 Python - Session-based Engagement Stream ---
    print("\n--- Testing Round 2 Python: process_event (Session-based) ---")
    # To test your process_event, you'd set up the global-like variables
    # or pass them if you refactor the placeholder.
    engagement_buffer_user.clear() # Resetting for your test
    total_engagement_counts_user = {'likes': 0, 'comments': 0, 'views': 0} # Resetting for your test
    sample_event_s2 = {'session_id': 's1', 'user_id': 'user1', 'event_type': 'view'}
    process_event(sample_event_s2, engagement_buffer_user, total_engagement_counts_user, internal_test_users_config)
    print(f"Buffer after event (user): {engagement_buffer_user}")
    print(f"Totals after event (user): {total_engagement_counts_user}")


    # --- Test Round 2 Python - Fixed-Size Buffer Stream ---
    print("\n--- Testing Round 2 Python: process_fixed_buffer_stream ---")
    # Resetting for your test
    fixed_buffer_stream_data_user.clear()
    fixed_buffer_total_engagement_user = 0
    fixed_buffer_total_view_seconds_user = 0.0
    sample_fixed_event = {'user_id': 'userA', 'event_type': 'like', 'post_id': ['p1']}
    # Note: Modifying simple numerics like totals_engagement directly as arguments
    # won't work as expected because ints/floats are immutable.
    # Your placeholder function `process_fixed_buffer_stream` would need to handle this,
    # e.g., by using the global variables directly, or by returning new totals,
    # or by using mutable containers like a list [0] for the totals.
    # For this example, we'll assume it uses the global `_user` suffixed variables.
    process_fixed_buffer_stream(
        sample_fixed_event,
        fixed_buffer_stream_data_user,
        FIXED_BUFFER_SIZE_CONFIG,
        fixed_buffer_total_engagement_user,
        fixed_buffer_total_view_seconds_user,
        fixed_buffer_test_user_ids_config
    )
    # You would then inspect the global `_user` suffixed variables
    print(f"Fixed Buffer (user): {fixed_buffer_stream_data_user}")
    print(f"Fixed Totals E (user): {fixed_buffer_total_engagement_user}, V (user): {fixed_buffer_total_view_seconds_user}")


    # --- Test Round 3 Python ---
    print("\n--- Testing Round 3 Python: Average Rating per Category ---")
    movie_data_cat = [{'category': 'Action', 'rating': 8}, {'category': 'Action', 'rating': 9}]
    print(f"Avg Cat Ratings: {calculate_average_ratings(movie_data_cat)}")

    print("\n--- Testing Round 3 Python: Top N Movies per Category ---")
    movie_data_top_n = [{'title': 'M1', 'category': 'Action', 'rating': 8}, {'title': 'M2', 'category': 'Action', 'rating': 9}]
    print(f"Top N Movies: {get_top_n_movies_per_category(movie_data_top_n, 1)}")

    print("\n--- Testing Round 3 Python: Average Rating per Movie ---")
    movie_data_ratings = [{'title': 'M1', 'rating': 8}, {'title': 'M1', 'rating': 9}]
    print(f"Avg Movie Ratings: {calculate_average_movie_ratings(movie_data_ratings)}")


    # --- Test Round 9 (DoorDash) Python (Conceptual) ---
    print("\n--- Testing Round 9 Python: can_add_to_batch_conceptual (Example Call) ---")
    sample_current_batch_r9 = [{'order_id': 'A1', 'promised_delivery_deadline': 1715824800}]
    sample_new_order_r9 = {'order_id': 'B1', 'restaurant_location': (34.05, -118.25), 'customer_location': (34.06, -118.26), 'estimated_pickup_ready_time': 1715823000, 'promised_delivery_deadline': 1715826600}
    # Call your placeholder function here
    can_add_r9 = can_add_to_batch_conceptual(
        sample_current_batch_r9,
        sample_new_order_r9,
        dasher_current_location=(34.04, -118.24),
        current_time=1715821200
    )
    print(f"Can add new order B1 to batch? {can_add_r9}")


    print("\nChallenge script complete. Review embedded comments for PS/DM/SQL solutions.")
    print("To run SQL tests, uncomment the execute_sql_lite calls in the original script.")
    print("To run Python tests for your implementations, fill in the placeholder functions and uncomment their calls.")

