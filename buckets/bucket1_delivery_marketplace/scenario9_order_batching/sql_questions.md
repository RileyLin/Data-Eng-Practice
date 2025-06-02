# Scenario 9: Order Batching (DoorDash) - SQL Questions

## Database Schema Reference

Based on the order batching data model:

### Dimension Tables
- **dim_orders**: order_key, order_id, customer_key, restaurant_key, order_value, order_placed_time, promised_delivery_time, order_status, priority_level
- **dim_batches**: batch_key, batch_id, driver_key, batch_created_time, batch_started_time, batch_completed_time, total_orders, batch_status, total_distance_miles, total_duration_minutes
- **dim_drivers**: driver_key, driver_id, vehicle_type, max_capacity, avg_rating, status, region
- **dim_restaurants**: restaurant_key, restaurant_id, restaurant_name, latitude, longitude, avg_prep_time_minutes, cuisine_type
- **dim_customers**: customer_key, customer_id, delivery_latitude, delivery_longitude, customer_tier, address_type

### Fact Tables
- **fact_batch_orders**: order_key, batch_key, pickup_sequence, delivery_sequence, pickup_time, delivery_time, pickup_to_delivery_time_minutes, delivery_delay_minutes, on_time_delivery
- **fact_delivery_routes**: route_segment_key, batch_key, order_key, segment_type, start_latitude, start_longitude, end_latitude, end_longitude, segment_start_time, segment_end_time, segment_distance_miles, segment_duration_minutes
- **fact_batch_performance**: batch_key, performance_date_key, avg_delivery_time_minutes, delivery_time_variance, customer_satisfaction_score, driver_earnings, cost_per_delivery, efficiency_score, successful_deliveries, failed_deliveries

---

## Question 1: Batch Size Optimization Analysis

**Problem**: Analyze the relationship between batch size and delivery performance to identify optimal batching strategies.

**Expected Output**: Performance metrics by batch size showing trade-offs between efficiency and customer satisfaction.

### Solution:
```sql
WITH batch_performance_metrics AS (
    SELECT 
        db.batch_id,
        db.total_orders as batch_size,
        db.total_distance_miles,
        db.total_duration_minutes,
        db.driver_key,
        
        -- Customer experience metrics
        AVG(fbo.pickup_to_delivery_time_minutes) as avg_delivery_time,
        STDDEV(fbo.pickup_to_delivery_time_minutes) as delivery_time_variance,
        AVG(fbo.delivery_delay_minutes) as avg_delay,
        COUNT(CASE WHEN fbo.on_time_delivery = TRUE THEN 1 END)::DECIMAL / COUNT(*) as on_time_rate,
        
        -- Efficiency metrics
        SUM(do.order_value) as total_batch_value,
        db.total_orders::DECIMAL / (db.total_duration_minutes / 60.0) as orders_per_hour,
        SUM(do.order_value) / db.total_distance_miles as value_per_mile
        
    FROM dim_batches db
    JOIN fact_batch_orders fbo ON db.batch_key = fbo.batch_key
    JOIN dim_orders do ON fbo.order_key = do.order_key
    WHERE db.batch_completed_time >= CURRENT_DATE - 30
      AND db.batch_status = 'completed'
    GROUP BY db.batch_id, db.total_orders, db.total_distance_miles, 
             db.total_duration_minutes, db.driver_key
)
SELECT 
    batch_size,
    COUNT(*) as total_batches,
    
    -- Customer experience aggregates
    ROUND(AVG(avg_delivery_time), 2) as avg_delivery_time_minutes,
    ROUND(AVG(delivery_time_variance), 2) as delivery_time_std_dev,
    ROUND(AVG(avg_delay), 2) as avg_delay_minutes,
    ROUND(AVG(on_time_rate) * 100, 1) as on_time_delivery_pct,
    
    -- Efficiency aggregates
    ROUND(AVG(orders_per_hour), 2) as avg_orders_per_hour,
    ROUND(AVG(value_per_mile), 2) as avg_value_per_mile,
    ROUND(AVG(total_batch_value), 2) as avg_batch_value,
    
    -- Performance vs single delivery comparison
    ROUND(AVG(avg_delivery_time) / 
          (SELECT AVG(fbo2.pickup_to_delivery_time_minutes) 
           FROM fact_batch_orders fbo2 
           JOIN dim_batches db2 ON fbo2.batch_key = db2.batch_key 
           WHERE db2.total_orders = 1), 2) as delivery_time_vs_single_order_ratio
           
FROM batch_performance_metrics
GROUP BY batch_size
ORDER BY batch_size;
```

---

## Question 2: Driver Productivity Analysis

**Problem**: Compare driver productivity metrics between batched and non-batched deliveries to quantify batching benefits.

**Expected Output**: Driver efficiency comparison showing productivity gains from batching.

### Solution:
```sql
WITH driver_daily_performance AS (
    SELECT 
        dd.driver_id,
        dd.vehicle_type,
        dd.region,
        DATE(db.batch_completed_time) as performance_date,
        
        -- Batch metrics
        COUNT(CASE WHEN db.total_orders > 1 THEN db.batch_id END) as batched_deliveries,
        COUNT(CASE WHEN db.total_orders = 1 THEN db.batch_id END) as single_deliveries,
        
        -- Time and efficiency
        SUM(db.total_duration_minutes) as total_active_minutes,
        SUM(db.total_orders) as total_orders_delivered,
        SUM(db.total_distance_miles) as total_distance_driven,
        
        -- Earnings (assuming from batch performance)
        SUM(fbp.driver_earnings) as total_earnings,
        
        -- Customer satisfaction
        AVG(fbp.customer_satisfaction_score) as avg_customer_satisfaction
        
    FROM dim_drivers dd
    JOIN dim_batches db ON dd.driver_key = db.driver_key
    JOIN fact_batch_performance fbp ON db.batch_key = fbp.batch_key
    WHERE db.batch_completed_time >= CURRENT_DATE - 30
      AND db.batch_status = 'completed'
    GROUP BY dd.driver_id, dd.vehicle_type, dd.region, DATE(db.batch_completed_time)
),
driver_performance_summary AS (
    SELECT 
        driver_id,
        vehicle_type,
        region,
        COUNT(*) as active_days,
        
        -- Productivity metrics
        AVG(total_orders_delivered::DECIMAL / (total_active_minutes / 60.0)) as avg_orders_per_hour,
        AVG(total_earnings::DECIMAL / (total_active_minutes / 60.0)) as avg_earnings_per_hour,
        AVG(total_distance_driven::DECIMAL / total_orders_delivered) as avg_miles_per_order,
        
        -- Batching adoption
        AVG(batched_deliveries::DECIMAL / NULLIF(batched_deliveries + single_deliveries, 0)) as batch_adoption_rate,
        
        -- Quality metrics
        AVG(avg_customer_satisfaction) as overall_customer_satisfaction
        
    FROM driver_daily_performance
    WHERE total_orders_delivered > 0
    GROUP BY driver_id, vehicle_type, region
)
SELECT 
    vehicle_type,
    region,
    COUNT(*) as total_drivers,
    
    -- Performance by batching adoption
    AVG(CASE WHEN batch_adoption_rate >= 0.7 THEN avg_orders_per_hour END) as high_batch_orders_per_hour,
    AVG(CASE WHEN batch_adoption_rate < 0.3 THEN avg_orders_per_hour END) as low_batch_orders_per_hour,
    
    AVG(CASE WHEN batch_adoption_rate >= 0.7 THEN avg_earnings_per_hour END) as high_batch_earnings_per_hour,
    AVG(CASE WHEN batch_adoption_rate < 0.3 THEN avg_earnings_per_hour END) as low_batch_earnings_per_hour,
    
    -- Efficiency comparison
    AVG(avg_miles_per_order) as avg_miles_per_order,
    AVG(batch_adoption_rate) as avg_batch_adoption_rate,
    AVG(overall_customer_satisfaction) as avg_customer_satisfaction,
    
    -- Productivity improvement from batching
    ROUND(
        (AVG(CASE WHEN batch_adoption_rate >= 0.7 THEN avg_orders_per_hour END) - 
         AVG(CASE WHEN batch_adoption_rate < 0.3 THEN avg_orders_per_hour END)) /
        NULLIF(AVG(CASE WHEN batch_adoption_rate < 0.3 THEN avg_orders_per_hour END), 0) * 100, 
        1
    ) as productivity_improvement_pct
    
FROM driver_performance_summary
GROUP BY vehicle_type, region
ORDER BY vehicle_type, region;
```

---

## Question 3: Geographic Batching Effectiveness

**Problem**: Analyze how batching performance varies by geographic density and distance patterns.

**Expected Output**: Geographic analysis showing optimal batching zones and distance patterns.

### Solution:
```sql
WITH location_metrics AS (
    SELECT 
        db.batch_id,
        db.total_orders as batch_size,
        db.total_distance_miles,
        db.total_duration_minutes,
        
        -- Calculate geographic spread of batch
        MAX(SQRT(POW(dc.delivery_latitude - AVG(dc.delivery_latitude) OVER (PARTITION BY db.batch_id), 2) + 
                 POW(dc.delivery_longitude - AVG(dc.delivery_longitude) OVER (PARTITION BY db.batch_id), 2))) as max_delivery_spread,
        
        AVG(dc.delivery_latitude) as avg_delivery_lat,
        AVG(dc.delivery_longitude) as avg_delivery_lng,
        
        -- Restaurant concentration
        COUNT(DISTINCT dr.restaurant_key) as unique_restaurants,
        
        -- Performance metrics
        AVG(fbo.pickup_to_delivery_time_minutes) as avg_delivery_time,
        COUNT(CASE WHEN fbo.on_time_delivery = TRUE THEN 1 END)::DECIMAL / COUNT(*) as on_time_rate
        
    FROM dim_batches db
    JOIN fact_batch_orders fbo ON db.batch_key = fbo.batch_key
    JOIN dim_orders do ON fbo.order_key = do.order_key
    JOIN dim_customers dc ON do.customer_key = dc.customer_key
    JOIN dim_restaurants dr ON do.restaurant_key = dr.restaurant_key
    WHERE db.batch_completed_time >= CURRENT_DATE - 30
      AND db.batch_status = 'completed'
      AND db.total_orders > 1  -- Only analyze actual batches
    GROUP BY db.batch_id, db.total_orders, db.total_distance_miles, db.total_duration_minutes
),
geographic_segments AS (
    SELECT 
        *,
        CASE 
            WHEN max_delivery_spread <= 0.01 THEN 'Very Dense'      -- ~1 mile radius
            WHEN max_delivery_spread <= 0.02 THEN 'Dense'           -- ~2 mile radius  
            WHEN max_delivery_spread <= 0.05 THEN 'Medium Density'   -- ~5 mile radius
            ELSE 'Sparse'
        END as density_segment,
        
        CASE 
            WHEN total_distance_miles / batch_size <= 3 THEN 'Short Distance'
            WHEN total_distance_miles / batch_size <= 7 THEN 'Medium Distance'
            ELSE 'Long Distance'
        END as distance_segment
    FROM location_metrics
)
SELECT 
    density_segment,
    distance_segment,
    COUNT(*) as total_batches,
    AVG(batch_size) as avg_batch_size,
    
    -- Geographic metrics
    AVG(max_delivery_spread) as avg_geographic_spread,
    AVG(unique_restaurants::DECIMAL / batch_size) as avg_restaurants_per_order,
    
    -- Performance metrics
    ROUND(AVG(avg_delivery_time), 2) as avg_delivery_time_minutes,
    ROUND(AVG(on_time_rate) * 100, 1) as on_time_delivery_pct,
    
    -- Efficiency metrics
    ROUND(AVG(total_distance_miles / batch_size), 2) as avg_distance_per_order,
    ROUND(AVG(batch_size::DECIMAL / (total_duration_minutes / 60.0)), 2) as avg_orders_per_hour,
    
    -- Efficiency score (orders per hour / distance per order)
    ROUND(
        AVG(batch_size::DECIMAL / (total_duration_minutes / 60.0)) / 
        NULLIF(AVG(total_distance_miles / batch_size), 0), 
        3
    ) as efficiency_ratio
    
FROM geographic_segments
GROUP BY density_segment, distance_segment
ORDER BY 
    CASE density_segment 
        WHEN 'Very Dense' THEN 1 
        WHEN 'Dense' THEN 2 
        WHEN 'Medium Density' THEN 3 
        WHEN 'Sparse' THEN 4 
    END,
    CASE distance_segment 
        WHEN 'Short Distance' THEN 1 
        WHEN 'Medium Distance' THEN 2 
        WHEN 'Long Distance' THEN 3 
    END;
```

---

## Question 4: Peak Hour Batching Performance

**Problem**: Analyze how batching effectiveness changes during different time periods and demand levels.

**Expected Output**: Time-based performance analysis showing optimal batching strategies by hour and demand level.

### Solution:
```sql
WITH hourly_batching_analysis AS (
    SELECT 
        EXTRACT(HOUR FROM db.batch_started_time) as start_hour,
        EXTRACT(DOW FROM db.batch_started_time) as day_of_week, -- 0=Sunday, 6=Saturday
        DATE(db.batch_started_time) as batch_date,
        
        db.batch_id,
        db.total_orders as batch_size,
        db.total_duration_minutes,
        db.total_distance_miles,
        
        -- Performance metrics
        AVG(fbo.pickup_to_delivery_time_minutes) as avg_delivery_time,
        AVG(fbo.delivery_delay_minutes) as avg_delay,
        COUNT(CASE WHEN fbo.on_time_delivery = TRUE THEN 1 END)::DECIMAL / COUNT(*) as on_time_rate,
        
        -- Calculate concurrent batch volume (demand indicator)
        COUNT(*) OVER (
            PARTITION BY DATE(db.batch_started_time), EXTRACT(HOUR FROM db.batch_started_time)
        ) as concurrent_batches_in_hour
        
    FROM dim_batches db
    JOIN fact_batch_orders fbo ON db.batch_key = fbo.batch_key
    WHERE db.batch_completed_time >= CURRENT_DATE - 30
      AND db.batch_status = 'completed'
    GROUP BY db.batch_id, db.total_orders, db.total_duration_minutes, 
             db.total_distance_miles, db.batch_started_time
),
time_period_classification AS (
    SELECT 
        *,
        CASE 
            WHEN start_hour BETWEEN 7 AND 9 THEN 'Morning Peak'
            WHEN start_hour BETWEEN 11 AND 14 THEN 'Lunch Peak'  
            WHEN start_hour BETWEEN 17 AND 20 THEN 'Dinner Peak'
            WHEN start_hour BETWEEN 21 AND 23 THEN 'Evening'
            ELSE 'Off Peak'
        END as time_period,
        
        CASE 
            WHEN day_of_week IN (0, 6) THEN 'Weekend'
            ELSE 'Weekday'
        END as day_type,
        
        CASE 
            WHEN concurrent_batches_in_hour >= 50 THEN 'High Demand'
            WHEN concurrent_batches_in_hour >= 20 THEN 'Medium Demand'
            ELSE 'Low Demand'
        END as demand_level
    FROM hourly_batching_analysis
)
SELECT 
    time_period,
    day_type,
    demand_level,
    COUNT(*) as total_batches,
    
    -- Batch characteristics
    AVG(batch_size) as avg_batch_size,
    AVG(concurrent_batches_in_hour) as avg_concurrent_batches,
    
    -- Performance metrics
    ROUND(AVG(avg_delivery_time), 2) as avg_delivery_time_minutes,
    ROUND(AVG(avg_delay), 2) as avg_delay_minutes,
    ROUND(AVG(on_time_rate) * 100, 1) as on_time_delivery_pct,
    
    -- Efficiency metrics
    ROUND(AVG(batch_size::DECIMAL / (total_duration_minutes / 60.0)), 2) as avg_orders_per_hour,
    ROUND(AVG(total_distance_miles / batch_size), 2) as avg_distance_per_order,
    
    -- Performance variance (consistency indicator)
    ROUND(STDDEV(avg_delivery_time), 2) as delivery_time_std_dev,
    
    -- Batching effectiveness score
    ROUND(
        (AVG(batch_size::DECIMAL / (total_duration_minutes / 60.0)) / 
         NULLIF(AVG(total_distance_miles / batch_size), 0)) * 
        AVG(on_time_rate), 
        3
    ) as effectiveness_score
    
FROM time_period_classification
GROUP BY time_period, day_type, demand_level
ORDER BY 
    CASE time_period 
        WHEN 'Morning Peak' THEN 1 
        WHEN 'Lunch Peak' THEN 2 
        WHEN 'Dinner Peak' THEN 3 
        WHEN 'Evening' THEN 4 
        WHEN 'Off Peak' THEN 5 
    END,
    day_type,
    CASE demand_level 
        WHEN 'High Demand' THEN 1 
        WHEN 'Medium Demand' THEN 2 
        WHEN 'Low Demand' THEN 3 
    END;
```

---

## Question 5: Route Sequence Optimization Analysis

**Problem**: Analyze the effectiveness of pickup and delivery sequencing within batches to identify optimization opportunities.

**Expected Output**: Sequence analysis showing impact of route ordering on delivery performance.

### Solution:
```sql
WITH batch_sequence_analysis AS (
    SELECT 
        db.batch_id,
        db.total_orders,
        db.total_duration_minutes,
        
        fbo.order_key,
        fbo.pickup_sequence,
        fbo.delivery_sequence,
        fbo.pickup_to_delivery_time_minutes,
        fbo.delivery_delay_minutes,
        
        -- Calculate if pickup and delivery sequences are aligned
        CASE 
            WHEN fbo.pickup_sequence = fbo.delivery_sequence THEN 'FIFO'
            WHEN fbo.delivery_sequence < fbo.pickup_sequence THEN 'Impossible'  -- Error case
            ELSE 'Reordered'
        END as sequence_strategy,
        
        -- Calculate delays for orders based on their position
        LAG(fbo.pickup_to_delivery_time_minutes) OVER (
            PARTITION BY db.batch_id ORDER BY fbo.delivery_sequence
        ) as prev_order_delivery_time,
        
        -- Distance analysis (simplified - would need route segments in reality)
        ROW_NUMBER() OVER (PARTITION BY db.batch_id ORDER BY fbo.pickup_sequence) as pickup_position,
        ROW_NUMBER() OVER (PARTITION BY db.batch_id ORDER BY fbo.delivery_sequence) as delivery_position
        
    FROM dim_batches db
    JOIN fact_batch_orders fbo ON db.batch_key = fbo.batch_key
    WHERE db.batch_completed_time >= CURRENT_DATE - 30
      AND db.batch_status = 'completed'
      AND db.total_orders > 1  -- Only multi-order batches
),
sequence_performance AS (
    SELECT 
        batch_id,
        total_orders,
        sequence_strategy,
        
        -- Performance by sequence position
        AVG(CASE WHEN pickup_position = 1 THEN pickup_to_delivery_time_minutes END) as first_pickup_delivery_time,
        AVG(CASE WHEN pickup_position = total_orders THEN pickup_to_delivery_time_minutes END) as last_pickup_delivery_time,
        
        AVG(CASE WHEN delivery_position = 1 THEN pickup_to_delivery_time_minutes END) as first_delivery_time,
        AVG(CASE WHEN delivery_position = total_orders THEN pickup_to_delivery_time_minutes END) as last_delivery_time,
        
        -- Overall batch performance
        AVG(pickup_to_delivery_time_minutes) as avg_delivery_time,
        AVG(delivery_delay_minutes) as avg_delay,
        MAX(pickup_to_delivery_time_minutes) - MIN(pickup_to_delivery_time_minutes) as delivery_time_spread
        
    FROM batch_sequence_analysis
    GROUP BY batch_id, total_orders, sequence_strategy
)
SELECT 
    total_orders as batch_size,
    sequence_strategy,
    COUNT(*) as total_batches,
    
    -- Delivery time analysis
    ROUND(AVG(avg_delivery_time), 2) as avg_delivery_time_minutes,
    ROUND(AVG(avg_delay), 2) as avg_delay_minutes,
    ROUND(AVG(delivery_time_spread), 2) as avg_delivery_time_spread,
    
    -- First vs last pickup comparison  
    ROUND(AVG(first_pickup_delivery_time), 2) as first_pickup_avg_delivery_time,
    ROUND(AVG(last_pickup_delivery_time), 2) as last_pickup_avg_delivery_time,
    ROUND(
        (AVG(last_pickup_delivery_time) - AVG(first_pickup_delivery_time)) / 
        NULLIF(AVG(first_pickup_delivery_time), 0) * 100, 
        1
    ) as last_vs_first_pickup_delay_pct,
    
    -- First vs last delivery comparison
    ROUND(AVG(first_delivery_time), 2) as first_delivery_avg_time,
    ROUND(AVG(last_delivery_time), 2) as last_delivery_avg_time,
    ROUND(
        (AVG(last_delivery_time) - AVG(first_delivery_time)) / 
        NULLIF(AVG(first_delivery_time), 0) * 100, 
        1
    ) as delivery_sequence_delay_pct,
    
    -- Strategy effectiveness (lower spread is better)
    ROUND(AVG(delivery_time_spread), 2) as fairness_score  -- Lower is more fair to all customers
    
FROM sequence_performance
GROUP BY total_orders, sequence_strategy
ORDER BY total_orders, sequence_strategy;
```

## Practice Tips

1. **Multi-table Joins**: Practice joining batch, order, and performance tables efficiently
2. **Geographic Analysis**: Understand distance calculations and spatial clustering
3. **Time Series Analysis**: Analyze performance trends across different time periods
4. **Performance Optimization**: Consider appropriate indexes for geographic and time-based queries
5. **Business Logic**: Focus on delivery logistics and customer experience trade-offs 