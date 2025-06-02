/*
Question 9.3.2: Geographic Batching Performance

Write a SQL query to analyze how batching performance varies by geographic density
and identify optimal batching zones based on delivery success rates.

Schema Reference:
- dim_customers: customer_key, delivery_latitude, delivery_longitude, address_type
- fact_delivery_routes: batch_key, segment_distance_miles, segment_duration_minutes
- fact_batch_performance: batch_key, avg_delivery_time_minutes, customer_satisfaction_score

Expected Output:
Geographic performance analysis showing optimal batching areas and distance thresholds.
*/

-- Write your SQL query here: 