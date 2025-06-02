# Scenario 1: Ridesharing Python Questions (Uber/Lyft) - Carpooling Feature

## Question 1: Carpool Vehicle Capacity Check

**Problem**: You are given a list of ride segments for a single carpool vehicle. Each segment is represented by a tuple `(start_time, end_time, num_passengers)`. The vehicle has a maximum passenger capacity. Write a Python function `can_vehicle_complete_rides_with_capacity(ride_segments, max_capacity)` that returns `True` if all ride segments can be completed without exceeding the vehicle's `max_capacity` at any point in time, and `False` otherwise.

**Key Rules**:
- `start_time` is when passengers are picked up
- `end_time` is when passengers are dropped off
- If dropoff and pickup happen at same time, dropoff occurs first
- Return `False` for empty input (no rides to complete)

**Examples**:
```python
# Example 1 - Capacity exceeded
ride_segments = [(0, 5, 2), (1, 3, 3), (6, 8, 1)]
max_capacity = 4
# At time 1: 2 + 3 = 5 passengers > 4 capacity
# Expected: False

# Example 2 - Capacity respected
ride_segments = [(0, 5, 2), (0, 2, 1), (3, 6, 1)]
max_capacity = 3
# Max concurrent: 3 passengers at time 0-2
# Expected: True
```

### Solution:
```python
def can_vehicle_complete_rides_with_capacity(ride_segments, max_capacity):
    """
    Checks if ride segments can be completed without exceeding capacity.
    
    Args:
        ride_segments: List of tuples (start_time, end_time, num_passengers)
        max_capacity: Maximum passenger capacity of vehicle
        
    Returns:
        True if all segments can be completed, False otherwise
    """
    if not ride_segments:
        return False
    
    # Create events for pickups (+passengers) and dropoffs (-passengers)
    events = []
    
    for start_time, end_time, num_passengers in ride_segments:
        events.append((start_time, num_passengers))      # pickup
        events.append((end_time, -num_passengers))       # dropoff
    
    # Sort by time, with dropoffs before pickups at same time
    events.sort(key=lambda x: (x[0], x[1]))
    
    current_capacity = 0
    
    for time, passenger_change in events:
        current_capacity += passenger_change
        if current_capacity > max_capacity:
            return False
    
    return True
```

---

## Question 2: Optimize Carpool Route

**Problem**: Given a list of pickup and dropoff locations with their coordinates, determine the optimal route order to minimize total driving distance. Each passenger must be picked up before being dropped off.

**Input**:
- `passengers`: List of tuples `(pickup_lat, pickup_lng, dropoff_lat, dropoff_lng, passenger_id)`
- `driver_location`: Tuple `(driver_lat, driver_lng)`

**Output**: Optimal sequence of locations to visit

### Solution:
```python
import math
from itertools import permutations

def calculate_distance(lat1, lng1, lat2, lng2):
    """Calculate Euclidean distance between two points"""
    return math.sqrt((lat2 - lat1)**2 + (lng2 - lng1)**2)

def optimize_carpool_route(passengers, driver_location):
    """
    Find optimal route order for carpool pickups and dropoffs.
    
    Args:
        passengers: List of (pickup_lat, pickup_lng, dropoff_lat, dropoff_lng, passenger_id)
        driver_location: (driver_lat, driver_lng)
        
    Returns:
        List of (lat, lng, action, passenger_id) representing optimal route
    """
    if not passengers:
        return []
    
    # Create all locations with actions
    locations = []
    for pickup_lat, pickup_lng, dropoff_lat, dropoff_lng, passenger_id in passengers:
        locations.append((pickup_lat, pickup_lng, 'pickup', passenger_id))
        locations.append((dropoff_lat, dropoff_lng, 'dropoff', passenger_id))
    
    def is_valid_route(route):
        """Check if route picks up before dropping off each passenger"""
        picked_up = set()
        for _, _, action, passenger_id in route:
            if action == 'pickup':
                picked_up.add(passenger_id)
            elif action == 'dropoff' and passenger_id not in picked_up:
                return False
        return True
    
    def calculate_route_distance(route):
        """Calculate total distance for a route"""
        if not route:
            return 0
        
        total_distance = calculate_distance(
            driver_location[0], driver_location[1],
            route[0][0], route[0][1]
        )
        
        for i in range(len(route) - 1):
            total_distance += calculate_distance(
                route[i][0], route[i][1],
                route[i+1][0], route[i+1][1]
            )
        
        return total_distance
    
    # For small inputs, try all valid permutations
    if len(locations) <= 8:  # Factorial complexity limit
        best_route = None
        best_distance = float('inf')
        
        for perm in permutations(locations):
            if is_valid_route(perm):
                distance = calculate_route_distance(perm)
                if distance < best_distance:
                    best_distance = distance
                    best_route = perm
        
        return list(best_route) if best_route else []
    
    # For larger inputs, use greedy heuristic
    return greedy_carpool_route(passengers, driver_location)

def greedy_carpool_route(passengers, driver_location):
    """Greedy heuristic for larger route optimization"""
    route = []
    current_location = driver_location
    remaining_pickups = {p[4]: (p[0], p[1]) for p in passengers}
    remaining_dropoffs = {p[4]: (p[2], p[3]) for p in passengers}
    picked_up = set()
    
    while remaining_pickups or remaining_dropoffs:
        best_location = None
        best_distance = float('inf')
        best_action = None
        best_passenger = None
        
        # Consider pickups
        for passenger_id, (lat, lng) in remaining_pickups.items():
            distance = calculate_distance(current_location[0], current_location[1], lat, lng)
            if distance < best_distance:
                best_distance = distance
                best_location = (lat, lng)
                best_action = 'pickup'
                best_passenger = passenger_id
        
        # Consider dropoffs for picked up passengers
        for passenger_id in picked_up:
            if passenger_id in remaining_dropoffs:
                lat, lng = remaining_dropoffs[passenger_id]
                distance = calculate_distance(current_location[0], current_location[1], lat, lng)
                if distance < best_distance:
                    best_distance = distance
                    best_location = (lat, lng)
                    best_action = 'dropoff'
                    best_passenger = passenger_id
        
        # Execute best action
        route.append((best_location[0], best_location[1], best_action, best_passenger))
        current_location = best_location
        
        if best_action == 'pickup':
            picked_up.add(best_passenger)
            del remaining_pickups[best_passenger]
        else:
            picked_up.remove(best_passenger)
            del remaining_dropoffs[best_passenger]
    
    return route
```

---

## Question 3: Carpool Matching Algorithm

**Problem**: Given a set of ride requests and available drivers, implement a matching algorithm that maximizes the number of successful carpool matches while respecting constraints.

**Constraints**:
- Maximum 4 passengers per vehicle
- Pickup locations must be within 0.5 miles of each other
- Destination locations must be within 1 mile of each other
- Maximum 15 minutes detour per passenger

### Solution:
```python
from collections import defaultdict
import heapq

def match_carpool_requests(ride_requests, available_drivers):
    """
    Match ride requests to drivers for optimal carpooling.
    
    Args:
        ride_requests: List of dicts with keys: id, pickup_lat, pickup_lng, 
                      dest_lat, dest_lng, requested_time
        available_drivers: List of dicts with keys: id, current_lat, current_lng,
                          max_capacity, available_time
    
    Returns:
        List of matches: [{driver_id, passenger_ids, estimated_time, total_distance}]
    """
    MAX_PICKUP_DISTANCE = 0.5
    MAX_DEST_DISTANCE = 1.0
    MAX_DETOUR_MINUTES = 15
    
    def can_group_requests(requests):
        """Check if requests can be grouped together"""
        if len(requests) > 4:
            return False
        
        # Check pickup proximity
        pickup_coords = [(r['pickup_lat'], r['pickup_lng']) for r in requests]
        for i, (lat1, lng1) in enumerate(pickup_coords):
            for j, (lat2, lng2) in enumerate(pickup_coords[i+1:], i+1):
                if calculate_distance(lat1, lng1, lat2, lng2) > MAX_PICKUP_DISTANCE:
                    return False
        
        # Check destination proximity
        dest_coords = [(r['dest_lat'], r['dest_lng']) for r in requests]
        for i, (lat1, lng1) in enumerate(dest_coords):
            for j, (lat2, lng2) in enumerate(dest_coords[i+1:], i+1):
                if calculate_distance(lat1, lng1, lat2, lng2) > MAX_DEST_DISTANCE:
                    return False
        
        return True
    
    # Group compatible requests
    request_groups = []
    remaining_requests = ride_requests.copy()
    
    # Try to form groups of 2-4 passengers
    for group_size in range(4, 1, -1):  # Start with larger groups
        groups_formed = []
        
        for i, req1 in enumerate(remaining_requests):
            if req1 is None:
                continue
            
            current_group = [req1]
            
            for j, req2 in enumerate(remaining_requests[i+1:], i+1):
                if req2 is None or len(current_group) >= group_size:
                    continue
                
                test_group = current_group + [req2]
                if can_group_requests(test_group):
                    current_group.append(req2)
            
            if len(current_group) >= 2:  # Only form groups of 2+
                groups_formed.append(current_group)
                for req in current_group:
                    idx = remaining_requests.index(req)
                    remaining_requests[idx] = None
        
        request_groups.extend(groups_formed)
    
    # Add individual requests as single-passenger groups
    for req in remaining_requests:
        if req is not None:
            request_groups.append([req])
    
    # Match groups to drivers
    matches = []
    used_drivers = set()
    
    # Sort drivers by availability time
    available_drivers.sort(key=lambda d: d['available_time'])
    
    for group in sorted(request_groups, key=len, reverse=True):  # Prioritize larger groups
        best_driver = None
        best_score = float('inf')
        
        for driver in available_drivers:
            if driver['id'] in used_drivers:
                continue
            
            if len(group) > driver['max_capacity']:
                continue
            
            # Calculate driver distance to pickup area
            group_center_lat = sum(r['pickup_lat'] for r in group) / len(group)
            group_center_lng = sum(r['pickup_lng'] for r in group) / len(group)
            
            driver_distance = calculate_distance(
                driver['current_lat'], driver['current_lng'],
                group_center_lat, group_center_lng
            )
            
            # Simple scoring: prioritize closer drivers
            score = driver_distance
            
            if score < best_score:
                best_score = score
                best_driver = driver
        
        if best_driver:
            # Create route for this match
            passengers = [(r['pickup_lat'], r['pickup_lng'], 
                          r['dest_lat'], r['dest_lng'], r['id']) for r in group]
            
            route = optimize_carpool_route(passengers, 
                                         (best_driver['current_lat'], best_driver['current_lng']))
            
            total_distance = calculate_route_distance_from_driver(route, 
                                                                (best_driver['current_lat'], best_driver['current_lng']))
            
            matches.append({
                'driver_id': best_driver['id'],
                'passenger_ids': [r['id'] for r in group],
                'estimated_time': len(route) * 3,  # Rough estimate: 3 min per stop
                'total_distance': total_distance,
                'route': route
            })
            
            used_drivers.add(best_driver['id'])
    
    return matches

def calculate_route_distance_from_driver(route, driver_location):
    """Calculate total route distance starting from driver location"""
    if not route:
        return 0
    
    total = calculate_distance(driver_location[0], driver_location[1], 
                             route[0][0], route[0][1])
    
    for i in range(len(route) - 1):
        total += calculate_distance(route[i][0], route[i][1], 
                                  route[i+1][0], route[i+1][1])
    
    return total
```

## Test Cases and Usage Examples

```python
# Test capacity checking
def test_carpool_capacity():
    assert can_vehicle_complete_rides_with_capacity([(0, 5, 2), (1, 3, 3)], 4) == False
    assert can_vehicle_complete_rides_with_capacity([(0, 5, 2), (0, 2, 1), (3, 6, 1)], 3) == True
    assert can_vehicle_complete_rides_with_capacity([], 4) == False
    print("Capacity tests passed!")

# Test route optimization
def test_route_optimization():
    passengers = [
        (0, 0, 5, 5, 'P1'),
        (1, 1, 6, 6, 'P2')
    ]
    driver_location = (0, 0)
    
    route = optimize_carpool_route(passengers, driver_location)
    print(f"Optimal route: {route}")

# Test matching algorithm
def test_matching():
    requests = [
        {'id': 'R1', 'pickup_lat': 0, 'pickup_lng': 0, 'dest_lat': 5, 'dest_lng': 5, 'requested_time': 0},
        {'id': 'R2', 'pickup_lat': 0.2, 'pickup_lng': 0.1, 'dest_lat': 5.2, 'dest_lng': 5.1, 'requested_time': 0}
    ]
    
    drivers = [
        {'id': 'D1', 'current_lat': 0, 'current_lng': 0, 'max_capacity': 4, 'available_time': 0}
    ]
    
    matches = match_carpool_requests(requests, drivers)
    print(f"Matches: {matches}")

if __name__ == "__main__":
    test_carpool_capacity()
    test_route_optimization()
    test_matching()
```

## Key Concepts Tested

1. **Algorithm Design**: Event-based processing, greedy algorithms, optimization
2. **Data Structures**: Lists, tuples, sets, heaps for efficient processing
3. **Constraint Satisfaction**: Capacity limits, distance constraints, time windows
4. **Geometric Calculations**: Distance calculations, proximity checks
5. **Optimization**: Route planning, matching algorithms, trade-off analysis 

# Scenario 1: Ride Sharing - Python Questions

## Python Question 1.4.1: Overlapping User Rides

A user wants to book multiple rides for themselves. Given a list of
requested rides, where each ride is a tuple `(start_time, end_time)`
with integer times, write a Python function
`can_user_complete_rides(requested_rides)` that returns `True` if the user
can theoretically complete all their requested rides (i.e., none of their
own rides overlap), and `False` otherwise.

**DATA STRUCTURE EXAMPLES:**

Input: `requested_rides` (List[Tuple[int, int]])
- Each tuple represents (start_time, end_time) for a single ride
- Times are integers (could represent minutes, hours, etc.)
- `end_time > start_time` for valid rides

**Example 1 - Non-overlapping rides:**
```
requested_rides = [(0, 30), (30, 60), (70, 90)]
```
Visualization:
```
Time:  0    30   60   70   90
       |----| |----| |----| 
       Ride1  Ride2  Ride3
```
Expected Output: `True`

**Example 2 - Overlapping rides:**
```
requested_rides = [(0, 60), (30, 90)]
```
Visualization:
```
Time:  0    30   60   90
       |---------|
            |---------|
           Ride1  Ride2 (overlap from 30-60)
```
Expected Output: `False`

**Example 3 - Single ride:**
```
requested_rides = [(10, 20)]
```
Expected Output: `True`

**Example 4 - Empty list:**
```
requested_rides = []
```
Expected Output: `True`

**Example 5 - Edge case (rides touching but not overlapping):**
```
requested_rides = [(0, 30), (30, 60)]
```
Visualization:
```
Time:  0    30   60
       |----||----| 
       Ride1 Ride2 (touching at time 30, but not overlapping)
```
Expected Output: `True`

**Follow-up consideration:** How would this problem change if we were considering 
a single carpool vehicle with a limited passenger capacity (e.g., 6 passengers), 
and the input was a list of ride segments for *different* users wanting to share 
that vehicle?

## Python Question 1.4.2: Carpool Vehicle Capacity Check

You are given a list of ride segments for a single carpool vehicle. Each segment is
represented by a tuple `(start_time, end_time, num_passengers)`. The vehicle has a
maximum passenger capacity. Write a Python function
`can_vehicle_complete_rides_with_capacity(ride_segments, max_capacity)`
that returns `True` if all ride segments can be completed without exceeding the
vehicle's `max_capacity` at any point in time, and `False` otherwise.

Assume `start_time` is when passengers are picked up and `end_time` is when they are dropped off.
If a dropoff and a pickup happen at the exact same time, assume the dropoff occurs first.

**DATA STRUCTURE EXAMPLES:**

Input: `ride_segments` (List[Tuple[int, int, int]])
- Each tuple represents (start_time, end_time, num_passengers)
- `start_time`: when passengers are picked up (integer)
- `end_time`: when passengers are dropped off (integer)
- `num_passengers`: number of passengers for this segment (positive integer)

Input: `max_capacity` (int)
- Maximum number of passengers the vehicle can hold at any time

**Example 1 - Capacity exceeded:**
```
ride_segments = [(0, 5, 2), (1, 3, 3), (6, 8, 1)]
max_capacity = 4
```
Timeline:
```
Time 0: +2 passengers (total: 2/4) ✓
Time 1: +3 passengers (total: 5/4) ✗ EXCEEDS CAPACITY
```
Expected Output: `False`

**Example 2 - Capacity respected:**
```
ride_segments = [(0, 5, 2), (0, 2, 1), (3, 6, 1)]
max_capacity = 3
```
Timeline:
```
Time 0: +2 passengers (total: 2/3) ✓
Time 0: +1 passenger (total: 3/3) ✓
Time 2: -1 passenger (total: 2/3) ✓
Time 3: +1 passenger (total: 3/3) ✓
Time 5: -2 passengers (total: 1/3) ✓
Time 6: -1 passenger (total: 0/3) ✓
```
Expected Output: `True`

**Example 3 - Simultaneous pickups exceeding capacity:**
```
ride_segments = [(0, 10, 3), (0, 5, 2)]
max_capacity = 4
```
Timeline:
```
Time 0: +3 passengers (total: 3/4) ✓
Time 0: +2 passengers (total: 5/4) ✗ EXCEEDS CAPACITY
```
Expected Output: `False`

**Example 4 - Simultaneous pickup/dropoff (dropoff first):**
```
ride_segments = [(0, 5, 3), (5, 10, 2)]
max_capacity = 3
```
Timeline:
```
Time 5: -3 passengers (total: 0/3) ✓ (dropoff first)
Time 5: +2 passengers (total: 2/3) ✓
```
Expected Output: `True`

**Example 5 - Empty input:**
```
ride_segments = []
max_capacity = 4
```
Expected Output: `False` (edge case - no rides to complete) 