# Python Questions

This document contains Python questions from the study guide, organized by scenario.

## Scenario 1: Ride Sharing (Uber/Lyft) - Carpooling Feature

### Question 1.4.1: Overlapping User Rides

**Description:**  
A user wants to book multiple rides for themselves. Given a list of requested rides, where each ride is a tuple `(start_time, end_time)` with integer times, write a Python function `can_user_complete_rides(requested_rides)` that returns `True` if the user can theoretically complete all their requested rides (i.e., none of their own rides overlap), and `False` otherwise.

**Example Inputs and Outputs:**
```python
# Example 1
requested_rides = [(0, 30), (30, 60), (70, 90)]
# Expected Output: True

# Example 2
requested_rides = [(0, 60), (30, 90)]
# Expected Output: False

# Example 3
requested_rides = [(10, 20)]
# Expected Output: True

# Example 4
requested_rides = []
# Expected Output: True
```

**Follow-up consideration:** How would this problem change if we were considering a single carpool vehicle with a limited passenger capacity (e.g., 6 passengers), and the input was a list of ride segments for *different* users wanting to share that vehicle?

### Question 1.4.2: Carpool Vehicle Capacity Check

**Description:**  
You are given a list of ride segments for a single carpool vehicle. Each segment is represented by a tuple `(start_time, end_time, num_passengers)`. The vehicle has a maximum passenger capacity. Write a Python function `can_vehicle_complete_rides_with_capacity(ride_segments, max_capacity)` that returns `True` if all ride segments can be completed without exceeding the vehicle's `max_capacity` at any point in time, and `False` otherwise.

Assume `start_time` is when passengers are picked up and `end_time` is when they are dropped off. If a dropoff and a pickup happen at the exact same time, assume the dropoff occurs first.

**Example Inputs and Outputs:**
```python
# Example 1
ride_segments = [(0, 5, 2), (1, 3, 3), (6, 8, 1)]
max_capacity = 4
# Expected Output: False
# Explanation:
# - Time 0: Pickup 2 (Capacity: 2/4)
# - Time 1: Pickup 3 (Capacity: 2+3=5/4) -> Exceeds capacity

# Example 2
ride_segments = [(0, 5, 2), (0, 2, 1), (3, 6, 1)]
max_capacity = 3
# Expected Output: True
# Explanation:
# - Time 0: Pickup 2 (Capacity: 2/3)
# - Time 0: Pickup 1 (Capacity: 2+1=3/3)
# - Time 2: Dropoff 1 (Capacity: 3-1=2/3)
# - Time 3: Pickup 1 (Capacity: 2+1=3/3)
# - Time 5: Dropoff 2 (Capacity: 3-2=1/3)
# - Time 6: Dropoff 1 (Capacity: 1-1=0/3)

# Example 3
ride_segments = [(0, 10, 3), (0, 5, 2)]
max_capacity = 4
# Expected Output: False (at time 0, capacity becomes 3+2=5)
```

## Scenario 2: Short Video (TikTok/Reels) - Sharing Focus

### Question 2.4.1: Session-based Engagement Stream

**Description:**  
Implement the Python function `process_event(event, buffer, totals, test_users)` that:
1. Processes a single engagement event (like, comment, view)
2. Buffers events by session_id in a buffer dictionary
3. Updates aggregate counts for non-internal sessions when a session_end event is received
4. Does not count events from internal test users in the aggregate counts

### Question 2.4.2: Fixed-Size Buffer Stream Processing

**Description:**  
Implement a fixed-size buffer for processing a stream of events. You need to implement two functions:

1. `process_fixed_buffer_stream(event_item, buffer, buffer_size, totals_engagement, totals_view_seconds, test_users)`:
   - Takes an event item (dictionary) and processes it through a fixed-size buffer
   - When the buffer is full (reaches buffer_size), processes the oldest item
   - Tracks engagement counts and view durations, excluding test users
   - Adds new event to the buffer

2. `flush_fixed_buffer(buffer, totals_engagement, totals_view_seconds, test_users)`:
   - Processes all remaining items in the buffer
   - Updates the totals for engagement and view durations

## Scenario 3: Streaming Platform (Netflix/Hulu)

### Question 3.4.1: Average Rating per Category

**Description:**  
Given a list of movies and categories, calculate the average rating per category. Implement the function `calculate_average_ratings(movie_data)` that takes a list of movie dictionaries and returns a dictionary mapping each category to its average rating.

### Question 3.4.2: Top N Movies per Category

**Description:**  
Given a list of movies and their categories, find the top N movies by rating for each category. Implement the function `get_top_n_movies_per_category(movie_data, n)` that returns a dictionary where keys are category names and values are lists of (movie_title, rating) tuples, sorted by rating in descending order.

### Question 3.4.3: Average Rating per Movie

**Description:**  
Given a list of movie rating instances (each with title and rating), calculate the average rating for each unique movie title. Implement the function `calculate_average_movie_ratings(movie_data)` that returns a dictionary mapping each movie title to its average rating.

## Scenario 6: News Feed

### Question 6.4.1: News Feed View Validation

**Description:**  
Process newsfeed logs to determine valid post views per session. Implement two functions:

1. `process_newsfeed_log(log, session_buffer)`:
   - Process a single log event ('start', 'end', or visibility update)
   - Update the session_buffer data structure with view information
   - Track start time, end time, and maximum visibility percentage

2. `calculate_session_valid_reads(session_id, session_buffer)`:
   - Count and return the number of posts in a session that meet the valid read criteria (duration >= 5s OR max_perc >= 80%)

## Scenario 7: Photo Upload (Instagram-like)

### Question 7.4.1: Photo Upload Processing

**Description:**  
Process a stream of photo upload logs ('upload_start', 'upload_end') to calculate the running average upload time for successful uploads. Implement the function `process_upload_log(log, pending_buffer, stats_aggregator)` that processes each event from a stream of upload logs and updates the statistics for successful uploads.

## Scenario 8: FB Messenger

### Question 8.4.1: SQL Generation

**Description:**  
Write a Python function `generate_insert_sql(log_entry, target_table)` that generates a SQL INSERT statement string based on conditions within the log_entry dictionary. The function should properly escape string values and handle different table structures based on the source table.

## Scenario 9: Food Delivery (DoorDash) - Order Batching

### Question 9.4.1: Order Batching Feasibility

**Description:**  
Determine if a new order can feasibly be added to a Dasher's current batch. Implement a conceptual function `can_add_to_batch(current_batch_details, new_order_details, dasher_current_location, current_time)` that considers factors like deadlines, travel times, and the impact on existing orders. 