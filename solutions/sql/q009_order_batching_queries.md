# SQL Practice Questions: DoorDash Order Batching Analysis

This document contains practice SQL questions based on the DoorDash order batching data model. These questions test various aspects of batching analytics, from basic performance metrics to complex route optimization analysis.

## Setup
Before running these queries, ensure you've executed the setup script:
```bash
psql -d your_database -f setup_scripts/setup_order_batching_db.sql
```

---

## Question 1: Basic Batching Performance Overview
**Difficulty: Easy**

Write a query to compare the basic performance metrics between batched and individual deliveries for the last 30 days.

**Expected Output Columns:**
- delivery_type (batched/individual)
- total_deliveries
- avg_delivery_time_minutes
- avg_efficiency_score
- on_time_delivery_rate

### Solution:

```sql
SELECT 
    vdbc.delivery_type,
    COUNT(*) as total_deliveries,
    ROUND(AVG(vdbc.actual_delivery_time_minutes), 1) as avg_delivery_time_minutes,
    ROUND(AVG(CASE 
        WHEN vdbc.delivery_type = 'batched' 
        THEN vdbc.batch_efficiency_score 
        ELSE 1.0 
    END), 3) as avg_efficiency_score,
    ROUND(AVG(CASE 
        WHEN vdbc.actual_delivery_time_minutes <= vdbc.estimated_delivery_time_minutes + 5 
        THEN 1.0 
        ELSE 0.0 
    END) * 100, 1) as on_time_delivery_rate
FROM vw_delivery_batch_context vdbc
WHERE vdbc.date_partition >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY vdbc.delivery_type
ORDER BY vdbc.delivery_type;
```

---

## Question 2: Algorithm Performance Comparison
**Difficulty: Medium**

Compare the performance of different batching algorithms, including key metrics like batch size, efficiency, and cancellation rates.

**Expected Output Columns:**
- algorithm_name
- algorithm_version
- total_batches
- avg_batch_size
- avg_efficiency_score
- avg_delivery_delay_minutes
- cancellation_rate_pct

### Solution:

```sql
SELECT 
    ba.algorithm_name,
    ba.algorithm_version,
    COUNT(DISTINCT db.batch_id) as total_batches,
    ROUND(AVG(db.total_deliveries), 1) as avg_batch_size,
    ROUND(AVG(db.batch_efficiency_score), 3) as avg_efficiency_score,
    ROUND(AVG(bd.delivery_delay_minutes), 1) as avg_delivery_delay_minutes,
    ROUND(
        COUNT(CASE WHEN db.batch_status = 'cancelled' THEN 1 END) * 100.0 / COUNT(DISTINCT db.batch_id), 
        2
    ) as cancellation_rate_pct
    
FROM dim_batching_algorithms ba
JOIN fact_delivery_batches db ON ba.batching_algorithm_key = db.batching_algorithm_key
JOIN fact_batch_deliveries bd ON db.batch_id = bd.batch_id
WHERE db.date_partition >= CURRENT_DATE - INTERVAL '30 days'
  AND ba.algorithm_name != 'no_batching'
GROUP BY ba.algorithm_name, ba.algorithm_version
ORDER BY avg_efficiency_score DESC;
```

---

## Question 3: Restaurant Batching Impact Analysis
**Difficulty: Medium-Hard**

Analyze how batching affects different restaurants, comparing pickup wait times and order volumes between restaurants that can handle batch pickups vs. those that cannot.

**Expected Output Columns:**
- restaurant_name
- can_handle_batch_pickups
- total_orders
- batched_orders_pct
- avg_batch_pickup_wait_minutes
- avg_individual_pickup_wait_minutes
- pickup_efficiency_improvement

### Solution:

```sql
WITH restaurant_metrics AS (
    SELECT 
        r.restaurant_id,
        r.restaurant_name,
        r.can_handle_batch_pickups,
        
        -- Order counts
        COUNT(DISTINCT o.order_id) as total_orders,
        COUNT(DISTINCT CASE WHEN vdbc.delivery_type = 'batched' THEN o.order_id END) as batched_orders,
        
        -- Pickup wait times
        AVG(CASE 
            WHEN vdbc.delivery_type = 'batched' 
            THEN bd.pickup_wait_time_minutes 
        END) as avg_batch_pickup_wait,
        
        AVG(CASE 
            WHEN vdbc.delivery_type = 'individual' 
            THEN EXTRACT(EPOCH FROM (del.picked_up_at - del.assigned_to_driver_at))/60
        END) as avg_individual_pickup_wait
        
    FROM dim_restaurants r
    JOIN fact_orders o ON r.restaurant_id = o.restaurant_id
    JOIN fact_deliveries del ON o.order_id = del.order_id
    JOIN vw_delivery_batch_context vdbc ON del.delivery_id = vdbc.delivery_id
    LEFT JOIN fact_batch_deliveries bd ON del.delivery_id = bd.delivery_id
    WHERE o.date_partition >= CURRENT_DATE - INTERVAL '30 days'
      AND del.delivery_status = 'delivered'
    GROUP BY r.restaurant_id, r.restaurant_name, r.can_handle_batch_pickups
    HAVING COUNT(DISTINCT o.order_id) >= 10 -- Filter for restaurants with significant volume
)
SELECT 
    restaurant_name,
    can_handle_batch_pickups,
    total_orders,
    ROUND(batched_orders * 100.0 / total_orders, 1) as batched_orders_pct,
    ROUND(avg_batch_pickup_wait, 1) as avg_batch_pickup_wait_minutes,
    ROUND(avg_individual_pickup_wait, 1) as avg_individual_pickup_wait_minutes,
    ROUND(
        (avg_individual_pickup_wait - avg_batch_pickup_wait) / NULLIF(avg_individual_pickup_wait, 0) * 100, 
        1
    ) as pickup_efficiency_improvement_pct
FROM restaurant_metrics
ORDER BY can_handle_batch_pickups DESC, batched_orders_pct DESC;
```

---

## Question 4: Route Optimization Analysis
**Difficulty: Hard**

Analyze route efficiency by comparing planned vs actual distances and identifying which algorithms perform best at route optimization.

**Expected Output Columns:**
- algorithm_name
- total_batches
- avg_planned_distance_miles
- avg_actual_distance_miles
- route_efficiency_ratio
- avg_time_variance_minutes
- best_route_efficiency
- worst_route_efficiency

### Solution:

```sql
WITH route_analysis AS (
    SELECT 
        db.batch_id,
        ba.algorithm_name,
        db.total_deliveries,
        db.planned_total_distance_miles,
        
        -- Calculate actual distance from waypoints
        SUM(bw.distance_to_next_miles) as actual_total_distance,
        
        -- Time variance analysis
        SUM(
            EXTRACT(EPOCH FROM (bw.actual_arrival_time - bw.estimated_arrival_time))/60
        ) as total_time_variance_minutes,
        
        -- Route efficiency (lower is better - actual vs planned)
        CASE 
            WHEN db.planned_total_distance_miles > 0 
            THEN SUM(bw.distance_to_next_miles) / db.planned_total_distance_miles 
            ELSE NULL 
        END as route_efficiency_ratio
        
    FROM fact_delivery_batches db
    JOIN dim_batching_algorithms ba ON db.batching_algorithm_key = ba.batching_algorithm_key
    JOIN fact_batch_waypoints bw ON db.batch_id = bw.batch_id
    WHERE db.batch_status = 'completed'
      AND db.date_partition >= CURRENT_DATE - INTERVAL '14 days'
      AND bw.waypoint_type != 'driver_end' -- Exclude final waypoint (no distance_to_next)
    GROUP BY db.batch_id, ba.algorithm_name, db.total_deliveries, db.planned_total_distance_miles
    HAVING db.planned_total_distance_miles > 0 -- Only include batches with planned routes
)
SELECT 
    algorithm_name,
    COUNT(*) as total_batches,
    ROUND(AVG(planned_total_distance_miles), 2) as avg_planned_distance_miles,
    ROUND(AVG(actual_total_distance), 2) as avg_actual_distance_miles,
    ROUND(AVG(route_efficiency_ratio), 3) as route_efficiency_ratio,
    ROUND(AVG(total_time_variance_minutes), 1) as avg_time_variance_minutes,
    ROUND(MIN(route_efficiency_ratio), 3) as best_route_efficiency,
    ROUND(MAX(route_efficiency_ratio), 3) as worst_route_efficiency
    
FROM route_analysis
WHERE route_efficiency_ratio IS NOT NULL
GROUP BY algorithm_name
ORDER BY route_efficiency_ratio ASC; -- Lower ratio = better efficiency
```

---

## Question 5: Driver Performance in Batching Context
**Difficulty: Medium-Hard**

Identify which drivers perform best with batching by analyzing their efficiency scores, delay times, and adaptation to batch deliveries.

**Expected Output Columns:**
- driver_external_id
- vehicle_type
- total_deliveries
- batched_delivery_pct
- avg_batch_efficiency
- avg_batch_delay_minutes
- individual_vs_batch_time_diff
- adaptation_rating

### Solution:

```sql
WITH driver_performance AS (
    SELECT 
        d.driver_id,
        d.driver_external_id,
        d.vehicle_type,
        
        -- Delivery counts
        COUNT(*) as total_deliveries,
        COUNT(CASE WHEN vdbc.delivery_type = 'batched' THEN 1 END) as batched_deliveries,
        
        -- Performance metrics
        AVG(CASE 
            WHEN vdbc.delivery_type = 'batched' 
            THEN vdbc.batch_efficiency_score 
        END) as avg_batch_efficiency,
        
        AVG(CASE 
            WHEN vdbc.delivery_type = 'batched' 
            THEN vdbc.delivery_delay_minutes 
        END) as avg_batch_delay,
        
        -- Time comparison
        AVG(CASE 
            WHEN vdbc.delivery_type = 'individual' 
            THEN del.actual_delivery_time_minutes 
        END) as avg_individual_time,
        
        AVG(CASE 
            WHEN vdbc.delivery_type = 'batched' 
            THEN del.actual_delivery_time_minutes 
        END) as avg_batched_time
        
    FROM dim_drivers d
    JOIN fact_deliveries del ON d.driver_id = del.driver_id
    JOIN vw_delivery_batch_context vdbc ON del.delivery_id = vdbc.delivery_id
    WHERE del.date_partition >= CURRENT_DATE - INTERVAL '30 days'
      AND del.delivery_status = 'delivered'
    GROUP BY d.driver_id, d.driver_external_id, d.vehicle_type
    HAVING COUNT(*) >= 20 -- Minimum deliveries for statistical significance
       AND COUNT(CASE WHEN vdbc.delivery_type = 'batched' THEN 1 END) >= 5 -- At least 5 batched deliveries
)
SELECT 
    driver_external_id,
    vehicle_type,
    total_deliveries,
    ROUND(batched_deliveries * 100.0 / total_deliveries, 1) as batched_delivery_pct,
    ROUND(avg_batch_efficiency, 3) as avg_batch_efficiency,
    ROUND(avg_batch_delay, 1) as avg_batch_delay_minutes,
    ROUND(avg_batched_time - avg_individual_time, 1) as individual_vs_batch_time_diff,
    
    -- Adaptation rating based on delay and efficiency
    CASE 
        WHEN avg_batch_delay <= 3 AND avg_batch_efficiency >= 0.85 THEN 'excellent'
        WHEN avg_batch_delay <= 5 AND avg_batch_efficiency >= 0.80 THEN 'good'
        WHEN avg_batch_delay <= 8 AND avg_batch_efficiency >= 0.75 THEN 'average'
        ELSE 'needs_improvement'
    END as adaptation_rating
    
FROM driver_performance
ORDER BY avg_batch_efficiency DESC, avg_batch_delay ASC;
```

---

## Question 6: Customer Experience Impact Analysis
**Difficulty: Hard**

Analyze how batching affects customer experience by looking at delivery delays, satisfaction scores, and the relationship between batch size and customer satisfaction.

**Expected Output Columns:**
- batch_size_range
- delivery_count
- avg_delivery_delay_minutes
- avg_customer_satisfaction
- on_time_delivery_rate
- satisfaction_vs_individual_diff

### Solution:

```sql
WITH customer_experience AS (
    SELECT 
        vdbc.delivery_id,
        vdbc.delivery_type,
        vdbc.batch_size,
        vdbc.delivery_delay_minutes,
        bd.customer_satisfaction_score,
        
        -- Calculate if delivery was on time (within 10 minutes of estimate)
        CASE 
            WHEN vdbc.actual_delivery_time_minutes <= vdbc.estimated_delivery_time_minutes + 10 
            THEN 1 
            ELSE 0 
        END as on_time_delivery,
        
        -- Batch size categorization
        CASE 
            WHEN vdbc.batch_size IS NULL THEN 'individual'
            WHEN vdbc.batch_size = 2 THEN '2_orders'
            WHEN vdbc.batch_size = 3 THEN '3_orders'
            WHEN vdbc.batch_size >= 4 THEN '4+_orders'
            ELSE 'other'
        END as batch_size_range
        
    FROM vw_delivery_batch_context vdbc
    LEFT JOIN fact_batch_deliveries bd ON vdbc.delivery_id = bd.delivery_id
    WHERE vdbc.date_partition >= CURRENT_DATE - INTERVAL '30 days'
),
individual_baseline AS (
    SELECT 
        AVG(customer_satisfaction_score) as avg_individual_satisfaction
    FROM customer_experience
    WHERE delivery_type = 'individual'
      AND customer_satisfaction_score IS NOT NULL
)
SELECT 
    ce.batch_size_range,
    COUNT(*) as delivery_count,
    ROUND(AVG(COALESCE(ce.delivery_delay_minutes, 0)), 1) as avg_delivery_delay_minutes,
    ROUND(AVG(ce.customer_satisfaction_score), 2) as avg_customer_satisfaction,
    ROUND(AVG(ce.on_time_delivery) * 100, 1) as on_time_delivery_rate,
    ROUND(
        AVG(ce.customer_satisfaction_score) - ib.avg_individual_satisfaction, 
        2
    ) as satisfaction_vs_individual_diff
    
FROM customer_experience ce
CROSS JOIN individual_baseline ib
WHERE ce.customer_satisfaction_score IS NOT NULL
GROUP BY ce.batch_size_range, ib.avg_individual_satisfaction
ORDER BY 
    CASE 
        WHEN ce.batch_size_range = 'individual' THEN 1
        WHEN ce.batch_size_range = '2_orders' THEN 2
        WHEN ce.batch_size_range = '3_orders' THEN 3
        WHEN ce.batch_size_range = '4+_orders' THEN 4
        ELSE 5
    END;
```

---

## Question 7: Temporal Batching Patterns
**Difficulty: Medium**

Analyze batching patterns by hour of day to understand when batching is most effective and identify peak efficiency periods.

**Expected Output Columns:**
- hour_of_day
- total_deliveries
- batched_deliveries
- batch_rate_pct
- avg_batch_size
- avg_efficiency_score
- peak_efficiency_indicator

### Solution:

```sql
WITH hourly_patterns AS (
    SELECT 
        EXTRACT(HOUR FROM del.delivery_created_at) as hour_of_day,
        
        COUNT(*) as total_deliveries,
        COUNT(CASE WHEN vdbc.delivery_type = 'batched' THEN 1 END) as batched_deliveries,
        
        AVG(CASE 
            WHEN vdbc.delivery_type = 'batched' 
            THEN vdbc.batch_size 
        END) as avg_batch_size,
        
        AVG(CASE 
            WHEN vdbc.delivery_type = 'batched' 
            THEN vdbc.batch_efficiency_score 
        END) as avg_efficiency_score
        
    FROM fact_deliveries del
    JOIN vw_delivery_batch_context vdbc ON del.delivery_id = vdbc.delivery_id
    WHERE del.date_partition >= CURRENT_DATE - INTERVAL '14 days'
      AND del.delivery_status = 'delivered'
    GROUP BY EXTRACT(HOUR FROM del.delivery_created_at)
),
efficiency_stats AS (
    SELECT 
        AVG(avg_efficiency_score) as overall_avg_efficiency,
        STDDEV(avg_efficiency_score) as efficiency_stddev
    FROM hourly_patterns
    WHERE avg_efficiency_score IS NOT NULL
)
SELECT 
    hp.hour_of_day,
    hp.total_deliveries,
    hp.batched_deliveries,
    ROUND(hp.batched_deliveries * 100.0 / hp.total_deliveries, 1) as batch_rate_pct,
    ROUND(hp.avg_batch_size, 1) as avg_batch_size,
    ROUND(hp.avg_efficiency_score, 3) as avg_efficiency_score,
    
    -- Identify peak efficiency hours
    CASE 
        WHEN hp.avg_efficiency_score > (es.overall_avg_efficiency + es.efficiency_stddev) 
        THEN 'high_efficiency'
        WHEN hp.avg_efficiency_score < (es.overall_avg_efficiency - es.efficiency_stddev) 
        THEN 'low_efficiency'
        ELSE 'normal'
    END as peak_efficiency_indicator
    
FROM hourly_patterns hp
CROSS JOIN efficiency_stats es
ORDER BY hp.hour_of_day;
```

---

## Question 8: Advanced Route Sequence Analysis
**Difficulty: Hard**

Analyze the relationship between pickup/dropoff sequence efficiency and batch performance. Identify patterns in successful route sequencing.

**Expected Output Columns:**
- algorithm_name
- sequence_pattern
- pattern_frequency
- avg_efficiency_score
- avg_total_time_minutes
- sequence_optimization_score

### Solution:

```sql
WITH sequence_analysis AS (
    SELECT 
        db.batch_id,
        ba.algorithm_name,
        db.batch_efficiency_score,
        db.actual_total_time_minutes,
        
        -- Create sequence pattern string
        STRING_AGG(
            bd.pickup_sequence || '->' || bd.dropoff_sequence, 
            ',' 
            ORDER BY bd.pickup_sequence, bd.dropoff_sequence
        ) as sequence_pattern,
        
        -- Calculate sequence efficiency metrics
        COUNT(*) as deliveries_in_batch,
        
        -- Check for optimal patterns (pickup all, then deliver in reverse geographic order)
        CASE 
            WHEN COUNT(DISTINCT bd.pickup_sequence) = 1 THEN 'single_restaurant'
            WHEN MAX(bd.pickup_sequence) <= 2 AND COUNT(*) >= 3 THEN 'efficient_pickup'
            WHEN MAX(bd.pickup_sequence) > COUNT(*) * 0.7 THEN 'inefficient_pickup'
            ELSE 'mixed_pattern'
        END as pattern_type
        
    FROM fact_delivery_batches db
    JOIN dim_batching_algorithms ba ON db.batching_algorithm_key = ba.batching_algorithm_key
    JOIN fact_batch_deliveries bd ON db.batch_id = bd.batch_id
    WHERE db.batch_status = 'completed'
      AND db.date_partition >= CURRENT_DATE - INTERVAL '14 days'
      AND ba.algorithm_name != 'no_batching'
    GROUP BY db.batch_id, ba.algorithm_name, db.batch_efficiency_score, db.actual_total_time_minutes
    HAVING COUNT(*) >= 2 -- Only multi-delivery batches
),
pattern_aggregation AS (
    SELECT 
        algorithm_name,
        sequence_pattern,
        pattern_type,
        COUNT(*) as pattern_frequency,
        AVG(batch_efficiency_score) as avg_efficiency_score,
        AVG(actual_total_time_minutes) as avg_total_time_minutes,
        
        -- Calculate sequence optimization score
        AVG(batch_efficiency_score) * (1.0 / AVG(actual_total_time_minutes)) * 1000 as sequence_optimization_score
        
    FROM sequence_analysis
    GROUP BY algorithm_name, sequence_pattern, pattern_type
    HAVING COUNT(*) >= 3 -- Patterns that occur at least 3 times
)
SELECT 
    algorithm_name,
    sequence_pattern,
    pattern_frequency,
    ROUND(avg_efficiency_score, 3) as avg_efficiency_score,
    ROUND(avg_total_time_minutes, 1) as avg_total_time_minutes,
    ROUND(sequence_optimization_score, 2) as sequence_optimization_score,
    
    -- Rank patterns within each algorithm
    RANK() OVER (
        PARTITION BY algorithm_name 
        ORDER BY sequence_optimization_score DESC
    ) as pattern_rank
    
FROM pattern_aggregation
ORDER BY algorithm_name, sequence_optimization_score DESC;
```

---

## Bonus Question 9: Real-time Operational Dashboard Query
**Difficulty: Expert**

Create a comprehensive query that would power a real-time operational dashboard showing current batch status, driver performance, and system health metrics.

### Solution:

```sql
WITH current_batches AS (
    -- Active batches in progress
    SELECT 
        db.batch_id,
        db.driver_id,
        dr.driver_external_id,
        ba.algorithm_name,
        db.batch_status,
        db.total_deliveries,
        db.batch_created_at,
        db.batch_started_at,
        
        -- Calculate elapsed time
        EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - db.batch_started_at))/60 as elapsed_minutes,
        
        -- Count completed deliveries
        COUNT(CASE WHEN bd.actual_dropoff_time IS NOT NULL THEN 1 END) as completed_deliveries,
        
        -- Next expected action
        MIN(CASE 
            WHEN bd.actual_pickup_time IS NULL THEN bd.estimated_pickup_time
            WHEN bd.actual_dropoff_time IS NULL THEN bd.estimated_dropoff_time
        END) as next_expected_time
        
    FROM fact_delivery_batches db
    JOIN dim_drivers dr ON db.driver_id = dr.driver_id
    JOIN dim_batching_algorithms ba ON db.batching_algorithm_key = ba.batching_algorithm_key
    LEFT JOIN fact_batch_deliveries bd ON db.batch_id = bd.batch_id
    WHERE db.batch_status IN ('assigned', 'in_progress')
      AND db.date_partition = CURRENT_DATE
    GROUP BY db.batch_id, db.driver_id, dr.driver_external_id, ba.algorithm_name, 
             db.batch_status, db.total_deliveries, db.batch_created_at, db.batch_started_at
),
driver_performance_today AS (
    -- Today's driver performance metrics
    SELECT 
        dr.driver_id,
        COUNT(DISTINCT db.batch_id) as batches_today,
        COUNT(DISTINCT bd.delivery_id) as deliveries_today,
        AVG(db.batch_efficiency_score) as avg_efficiency_today,
        
        -- Count late deliveries
        COUNT(CASE 
            WHEN bd.actual_dropoff_time > bd.estimated_dropoff_time + INTERVAL '10 minutes' 
            THEN 1 
        END) as late_deliveries_today
        
    FROM dim_drivers dr
    LEFT JOIN fact_delivery_batches db ON dr.driver_id = db.driver_id 
        AND db.date_partition = CURRENT_DATE
    LEFT JOIN fact_batch_deliveries bd ON db.batch_id = bd.batch_id
    WHERE dr.driver_status = 'active'
    GROUP BY dr.driver_id
),
system_health AS (
    -- System-wide health metrics
    SELECT 
        COUNT(CASE WHEN cb.batch_status = 'assigned' THEN 1 END) as batches_assigned,
        COUNT(CASE WHEN cb.batch_status = 'in_progress' THEN 1 END) as batches_in_progress,
        AVG(cb.elapsed_minutes) as avg_batch_duration_minutes,
        COUNT(CASE WHEN cb.next_expected_time < CURRENT_TIMESTAMP THEN 1 END) as overdue_actions,
        
        -- Driver utilization
        COUNT(DISTINCT cb.driver_id) as active_drivers,
        (SELECT COUNT(*) FROM dim_drivers WHERE driver_status = 'active') as total_available_drivers
    FROM current_batches cb
)
-- Main dashboard query combining all metrics
SELECT 
    'ACTIVE_BATCHES' as metric_category,
    cb.batch_id,
    cb.driver_external_id,
    cb.algorithm_name,
    cb.batch_status,
    cb.total_deliveries,
    cb.completed_deliveries,
    ROUND(cb.elapsed_minutes, 1) as elapsed_minutes,
    cb.next_expected_time,
    
    -- Performance indicators
    CASE 
        WHEN cb.next_expected_time < CURRENT_TIMESTAMP THEN 'overdue'
        WHEN cb.elapsed_minutes > 90 THEN 'long_running'
        ELSE 'normal'
    END as status_indicator,
    
    -- Driver performance context
    dpt.batches_today,
    dpt.deliveries_today,
    ROUND(dpt.avg_efficiency_today, 3) as driver_efficiency_today,
    dpt.late_deliveries_today

FROM current_batches cb
LEFT JOIN driver_performance_today dpt ON cb.driver_id = dpt.driver_id

UNION ALL

-- System health summary row
SELECT 
    'SYSTEM_HEALTH' as metric_category,
    NULL as batch_id,
    'SYSTEM' as driver_external_id,
    'ALL' as algorithm_name,
    'SUMMARY' as batch_status,
    sh.batches_assigned + sh.batches_in_progress as total_deliveries,
    NULL as completed_deliveries,
    sh.avg_batch_duration_minutes as elapsed_minutes,
    NULL as next_expected_time,
    
    CASE 
        WHEN sh.overdue_actions > 5 THEN 'high_alerts'
        WHEN sh.overdue_actions > 2 THEN 'medium_alerts'
        ELSE 'healthy'
    END as status_indicator,
    
    sh.active_drivers as batches_today,
    sh.total_available_drivers as deliveries_today,
    ROUND(sh.active_drivers::DECIMAL / sh.total_available_drivers, 3) as driver_efficiency_today,
    sh.overdue_actions as late_deliveries_today

FROM system_health sh

ORDER BY 
    metric_category,
    CASE WHEN status_indicator = 'overdue' THEN 1 ELSE 2 END,
    elapsed_minutes DESC;
```

---

## Practice Tips

1. **Start with the basic queries** (Questions 1-3) to understand the data model relationships
2. **Focus on JOIN patterns** - pay attention to how batch tables connect to core delivery tables
3. **Use the unified view** (`vw_delivery_batch_context`) for simpler analysis queries
4. **Practice window functions** for ranking and comparative analysis
5. **Test with different date ranges** to understand data volume impacts
6. **Experiment with the sample data** by adding more test records

## Common Gotchas

1. **LEFT JOINs for batch data** - not all deliveries are batched
2. **Date partition filtering** - always include for performance
3. **NULL handling** - batch metrics will be NULL for individual deliveries
4. **Aggregation levels** - decide whether to analyze at batch or delivery level
5. **Time zone considerations** - ensure consistent timestamp handling

This comprehensive set of queries demonstrates the power of the integrated batching data model for operational analytics and optimization insights. 