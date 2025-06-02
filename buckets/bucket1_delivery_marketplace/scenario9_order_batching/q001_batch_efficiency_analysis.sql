/*
Question 9.3.1: Batch Efficiency Analysis

Write a SQL query to analyze delivery efficiency by batch size, comparing
single orders vs batched orders in terms of delivery time and driver productivity.

Schema Reference:
- dim_batches: batch_key, batch_id, driver_key, total_orders, total_distance_miles
- fact_batch_orders: batch_key, order_key, pickup_time, delivery_time, on_time_delivery
- dim_orders: order_key, order_value, order_placed_time

Expected Output:
Efficiency metrics by batch size showing trade-offs between customer experience and operational efficiency.
*/

-- Write your SQL query here: 

