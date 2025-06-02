# Scenario 9: Food Delivery (DoorDash) - Python Questions

## Python Question 9.4.1: Feasibility of Adding Order to Batch - Conceptual

Imagine a Dasher (food delivery driver) is currently handling a batch of one or more orders, each
with specific pickup restaurant locations and customer delivery locations/time windows. A new order
request comes in.

You need to implement a conceptual function:
`can_add_to_batch(current_batch_details, new_order_details, dasher_current_location, current_time)`

The function should determine if the new order can be feasibly added to the current batch without
causing existing orders to be excessively late.

**Key considerations:**
- All orders have a promised delivery deadline
- Orders must be picked up from restaurants first
- Restaurant preparation time for the new order
- Travel times between locations
- Impact of the added order on the existing delivery route/timeline
- Maximum allowable delay for existing orders

**Example Input (Conceptual):**
```python
current_batch_details = [
    {
        'order_id': 'A1', 
        'restaurant_loc': (37.7749, -122.4194),  # San Francisco
        'customer_loc': (37.7858, -122.4064),    # Near Chinatown
        'promised_delivery_deadline': 1617304800, # Unix timestamp
        'est_pickup_time': 1617303900            # 15 min before deadline
    },
    # ... more orders ...
]

new_order_details = {
    'order_id': 'B1',
    'restaurant_loc': (37.7649, -122.4194), 
    'customer_loc': (37.7948, -122.4864),
    'promised_delivery_deadline': 1617305400,
    'est_pickup_time': 1617304500,
    'est_prep_time_remaining': 10 * 60  # 10 minutes in seconds
}

dasher_current_location = (37.7759, -122.4104)  # Current driver location
current_time = 1617303600  # Unix timestamp
```

Your task is to outline a conceptual approach for determining whether the new order can reasonably be added to the batch. Focus on the key factors to consider rather than implementing a complete routing algorithm.

## Python Question 9.4.2: DoorDash Food Delivery Time Calculation

You are given two inputs to calculate the delivery time for each order:

1. A list of dictionaries representing driver actions, where each dict contains:
   - `location`: string (location identifier)
   - `order_no`: string (order number, only present for 'pick_up' and 'drop_off' actions)
   - `action_type`: string ('pick_up', 'travel', 'drop_off')
   - `driver`: string (driver identifier)

2. A 2D matrix representing travel times between locations

**Key Points:**
- When `action_type` is 'travel', there is NO `order_no` in the record.
- A driver can pick up multiple orders before dropping them off.
- ALL time between picking up an order and dropping it off counts toward that order's delivery time.
- Print results as: "order xx is delivered within xxx mins"
- Print in order number sequence.

**Example Scenario:**
Driver picks up `order_1` at location A, travels to B to pick up `order_2`, 
then travels to C to drop off `order_1`. The travel time from A→B also counts 
toward `order_1`'s delivery time since the driver was carrying it.

**Function Signature:**
```python
def calculate_delivery_times(actions, travel_matrix, location_mapping):
    # ... implementation ...
```

## Question 1: Batch Feasibility Check

**Problem**: Determine if a new order can be added to a current batch without causing excessive delays.

### Solution:
```python
def can_add_to_batch(current_batch_details, new_order_details, dasher_current_location, current_time):
    """
    Determine if a new order can feasibly be added to a Dasher's current batch.
    
    Args:
        current_batch_details (list): Current orders in batch
        new_order_details (dict): New order to potentially add
        dasher_current_location (tuple): (lat, lng) of dasher
        current_time (int): Current Unix timestamp
        
    Returns:
        bool: True if order can be added without excessive delays
    """
    # Check basic constraints
    if len(current_batch_details) >= 4:  # Max batch size
        return False
    
    # Check if new order deadline is too tight
    new_deadline = new_order_details.get('promised_delivery_deadline', float('inf'))
    if new_deadline < current_time + 30*60:  # Need at least 30 min
        return False
    
    # Estimate total route time with new order
    estimated_total_time = estimate_route_time(
        current_batch_details + [new_order_details], 
        dasher_current_location
    )
    
    # Check if any existing orders would be late
    for order in current_batch_details:
        order_deadline = order.get('promised_delivery_deadline', float('inf'))
        if current_time + estimated_total_time > order_deadline:
            return False
    
    return True

def estimate_route_time(orders, start_location):
    """Estimate total time for batch route"""
    # Simplified calculation - in reality would use routing algorithms
    total_time = 0
    current_pos = start_location
    
    # Pickup phase
    for order in orders:
        restaurant_loc = order['restaurant_loc']
        travel_time = calculate_travel_time(current_pos, restaurant_loc)
        pickup_time = 5  # 5 minutes pickup time
        total_time += travel_time + pickup_time
        current_pos = restaurant_loc
    
    # Delivery phase  
    for order in orders:
        customer_loc = order['customer_loc']
        travel_time = calculate_travel_time(current_pos, customer_loc)
        delivery_time = 2  # 2 minutes delivery time
        total_time += travel_time + delivery_time
        current_pos = customer_loc
    
    return total_time * 60  # Convert to seconds

def calculate_travel_time(loc1, loc2):
    """Calculate travel time between two locations"""
    # Simplified distance calculation
    import math
    lat1, lng1 = loc1
    lat2, lng2 = loc2
    
    # Haversine distance (simplified)
    distance = math.sqrt((lat2-lat1)**2 + (lng2-lng1)**2) * 69  # Rough miles
    speed_mph = 25  # Average speed including traffic
    time_hours = distance / speed_mph
    return time_hours * 60  # Return minutes
```

## Question 2: Route Optimization

**Problem**: Optimize pickup and delivery sequence for a batch to minimize total time.

### Solution:
```python
def optimize_batch_route(orders, dasher_location):
    """
    Optimize the route for a batch of orders.
    
    Args:
        orders (list): List of order dictionaries
        dasher_location (tuple): Starting location (lat, lng)
        
    Returns:
        dict: Optimized route with pickup and delivery sequences
    """
    from itertools import permutations
    
    if len(orders) <= 1:
        return {'pickup_sequence': orders, 'delivery_sequence': orders, 'total_time': 0}
    
    best_route = None
    best_time = float('inf')
    
    # Try different pickup sequences (limited to avoid exponential complexity)
    for pickup_seq in permutations(orders):
        # For each pickup sequence, try different delivery sequences
        for delivery_seq in permutations(pickup_seq):
            route_time = calculate_route_time(pickup_seq, delivery_seq, dasher_location)
            
            if route_time < best_time:
                best_time = route_time
                best_route = {
                    'pickup_sequence': list(pickup_seq),
                    'delivery_sequence': list(delivery_seq),
                    'total_time': route_time
                }
    
    return best_route

def calculate_route_time(pickup_seq, delivery_seq, start_location):
    """Calculate total time for a specific route sequence"""
    total_time = 0
    current_location = start_location
    
    # Pickup phase
    for order in pickup_seq:
        restaurant_loc = order['restaurant_loc']
        travel_time = calculate_travel_time(current_location, restaurant_loc)
        total_time += travel_time + 5  # 5 min pickup
        current_location = restaurant_loc
    
    # Delivery phase
    for order in delivery_seq:
        customer_loc = order['customer_loc']
        travel_time = calculate_travel_time(current_location, customer_loc)
        total_time += travel_time + 2  # 2 min delivery
        current_location = customer_loc
    
    return total_time
```

## Question 3: Batch Performance Analytics

**Problem**: Analyze batch performance metrics and identify optimization opportunities.

### Solution:
```python
class BatchAnalyzer:
    """Analyze batch performance and identify optimization opportunities"""
    
    def __init__(self):
        self.batch_data = []
    
    def add_batch_data(self, batch_info):
        """Add completed batch data for analysis"""
        self.batch_data.append(batch_info)
    
    def analyze_batch_size_performance(self):
        """Analyze performance by batch size"""
        from collections import defaultdict
        
        size_metrics = defaultdict(list)
        
        for batch in self.batch_data:
            size = len(batch['orders'])
            
            # Calculate metrics
            avg_delivery_time = sum(order['delivery_time'] for order in batch['orders']) / size
            on_time_rate = sum(1 for order in batch['orders'] if order['on_time']) / size
            efficiency = size / (batch['total_duration'] / 60)  # orders per hour
            
            size_metrics[size].append({
                'avg_delivery_time': avg_delivery_time,
                'on_time_rate': on_time_rate,
                'efficiency': efficiency
            })
        
        # Aggregate by size
        results = {}
        for size, metrics in size_metrics.items():
            results[size] = {
                'avg_delivery_time': sum(m['avg_delivery_time'] for m in metrics) / len(metrics),
                'avg_on_time_rate': sum(m['on_time_rate'] for m in metrics) / len(metrics),
                'avg_efficiency': sum(m['efficiency'] for m in metrics) / len(metrics),
                'batch_count': len(metrics)
            }
        
        return results
    
    def identify_optimization_opportunities(self):
        """Identify areas for route optimization"""
        opportunities = []
        
        for batch in self.batch_data:
            if len(batch['orders']) < 2:
                continue
            
            # Check for suboptimal sequencing
            delivery_times = [order['delivery_time'] for order in batch['orders']]
            time_variance = max(delivery_times) - min(delivery_times)
            
            if time_variance > 20:  # High variance indicates poor sequencing
                opportunities.append({
                    'batch_id': batch['batch_id'],
                    'issue': 'High delivery time variance',
                    'variance': time_variance,
                    'recommendation': 'Optimize delivery sequence'
                })
            
            # Check for geographic inefficiency
            if batch['total_distance'] / len(batch['orders']) > 8:  # > 8 miles per order
                opportunities.append({
                    'batch_id': batch['batch_id'],
                    'issue': 'High distance per order',
                    'distance_per_order': batch['total_distance'] / len(batch['orders']),
                    'recommendation': 'Tighter geographic clustering'
                })
        
        return opportunities

# Test the analyzer
def test_batch_analyzer():
    analyzer = BatchAnalyzer()
    
    # Add sample batch data
    sample_batches = [
        {
            'batch_id': 'B1',
            'total_duration': 45,  # minutes
            'total_distance': 12,  # miles
            'orders': [
                {'delivery_time': 25, 'on_time': True},
                {'delivery_time': 35, 'on_time': True}
            ]
        },
        {
            'batch_id': 'B2',
            'total_duration': 60,
            'total_distance': 25,
            'orders': [
                {'delivery_time': 20, 'on_time': True},
                {'delivery_time': 45, 'on_time': False},
                {'delivery_time': 50, 'on_time': False}
            ]
        }
    ]
    
    for batch in sample_batches:
        analyzer.add_batch_data(batch)
    
    # Analyze performance
    size_performance = analyzer.analyze_batch_size_performance()
    opportunities = analyzer.identify_optimization_opportunities()
    
    print("Performance by batch size:", size_performance)
    print("Optimization opportunities:", opportunities)

if __name__ == "__main__":
    test_batch_analyzer()
```

## Key Concepts

1. **Constraint Satisfaction**: Balancing delivery deadlines with route efficiency
2. **Combinatorial Optimization**: Finding optimal pickup/delivery sequences
3. **Geospatial Analysis**: Distance and travel time calculations
4. **Performance Analytics**: Measuring and optimizing batch effectiveness 