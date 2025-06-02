/*
Question 12: DoorDash Restaurant Delivery Analysis - SQL Questions

Tables:
- restaurants: restaurant_id, name, location, avg_prep_time
- orders: order_id, restaurant_id, customer_id, order_time, pickup_time, delivery_time, total_amount
- deliveries: delivery_id, order_id, driver_id, pickup_time, delivery_time, distance_km
*/

-- Question 1: Calculate average order amount by restaurant
-- Find the average order amount for each restaurant, ordered by highest average first

SELECT 
    r.restaurant_id,
    r.name as restaurant_name,
    AVG(o.total_amount) as avg_order_amount
FROM restaurants r
JOIN orders o ON r.restaurant_id = o.restaurant_id
GROUP BY r.restaurant_id, r.name
ORDER BY avg_order_amount DESC;

-- Question 2: Find percentage of restaurants where pickup time > delivery time
-- Calculate what percentage of restaurants have average pickup time greater than average delivery time

WITH restaurant_times AS (
    SELECT 
        r.restaurant_id,
        r.name,
        AVG(EXTRACT(EPOCH FROM (o.pickup_time - o.order_time))/60) as avg_pickup_mins,
        AVG(EXTRACT(EPOCH FROM (d.delivery_time - d.pickup_time))/60) as avg_delivery_mins
    FROM restaurants r
    JOIN orders o ON r.restaurant_id = o.restaurant_id  
    JOIN deliveries d ON o.order_id = d.order_id
    WHERE o.pickup_time IS NOT NULL 
      AND o.delivery_time IS NOT NULL
      AND d.delivery_time IS NOT NULL
    GROUP BY r.restaurant_id, r.name
),
pickup_vs_delivery AS (
    SELECT 
        restaurant_id,
        name,
        avg_pickup_mins,
        avg_delivery_mins,
        CASE WHEN avg_pickup_mins > avg_delivery_mins THEN 1 ELSE 0 END as pickup_longer
    FROM restaurant_times
)
SELECT 
    COUNT(*) as total_restaurants,
    SUM(pickup_longer) as restaurants_pickup_longer,
    ROUND(
        (SUM(pickup_longer) * 100.0 / COUNT(*)), 2
    ) as percentage_pickup_longer
FROM pickup_vs_delivery;

-- Additional debugging query to see individual restaurant times
SELECT 
    r.restaurant_id,
    r.name,
    AVG(EXTRACT(EPOCH FROM (o.pickup_time - o.order_time))/60) as avg_pickup_mins,
    AVG(EXTRACT(EPOCH FROM (d.delivery_time - d.pickup_time))/60) as avg_delivery_mins,
    CASE 
        WHEN AVG(EXTRACT(EPOCH FROM (o.pickup_time - o.order_time))/60) > 
             AVG(EXTRACT(EPOCH FROM (d.delivery_time - d.pickup_time))/60) 
        THEN 'Pickup Longer' 
        ELSE 'Delivery Longer' 
    END as comparison
FROM restaurants r
JOIN orders o ON r.restaurant_id = o.restaurant_id  
JOIN deliveries d ON o.order_id = d.order_id
WHERE o.pickup_time IS NOT NULL 
  AND o.delivery_time IS NOT NULL
  AND d.delivery_time IS NOT NULL
GROUP BY r.restaurant_id, r.name
ORDER BY r.name; 