/*
Question 12: DoorDash Restaurant Delivery Analysis - Database Setup

This script creates the database schema and sample data for the DoorDash 
restaurant-focused SQL interview questions:
1. Average order amount by restaurant
2. Percentage of restaurants where pickup time > delivery time

Tables created:
- restaurants: Basic restaurant information
- orders: Order details with timing information
- deliveries: Delivery tracking information
*/

-- Create restaurants table
DROP TABLE IF EXISTS restaurants CASCADE;
CREATE TABLE restaurants (
    restaurant_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(50),
    cuisine_type VARCHAR(30),
    price_tier VARCHAR(5), -- $, $$, $$$
    avg_prep_time INTEGER -- average preparation time in minutes
);

-- Create orders table
DROP TABLE IF EXISTS orders CASCADE;
CREATE TABLE orders (
    order_id VARCHAR(10) PRIMARY KEY,
    restaurant_id VARCHAR(10) REFERENCES restaurants(restaurant_id),
    customer_id VARCHAR(10),
    order_time TIMESTAMP,
    pickup_time TIMESTAMP,
    delivery_time TIMESTAMP,
    total_amount DECIMAL(8,2)
);

-- Create deliveries table  
DROP TABLE IF EXISTS deliveries CASCADE;
CREATE TABLE deliveries (
    delivery_id VARCHAR(10) PRIMARY KEY,
    order_id VARCHAR(10) REFERENCES orders(order_id),
    driver_id VARCHAR(10),
    pickup_time TIMESTAMP,
    delivery_time TIMESTAMP,
    distance_km DECIMAL(5,2)
);

-- Insert sample restaurant data
INSERT INTO restaurants VALUES
('R001', 'Pizza Palace', 'Downtown', 'Italian', '$', 15),
('R002', 'Burger Barn', 'Midtown', 'American', '$', 10),
('R003', 'Sushi Spot', 'Uptown', 'Japanese', '$$', 20),
('R004', 'Taco Time', 'Eastside', 'Mexican', '$', 8),
('R005', 'Fine Dining Co', 'Downtown', 'French', '$$$', 30),
('R006', 'Quick Bites', 'Westside', 'Fast Food', '$', 5),
('R007', 'Pasta House', 'Midtown', 'Italian', '$$', 18),
('R008', 'BBQ Shack', 'Southside', 'American', '$$', 25),
('R009', 'Noodle Bar', 'Chinatown', 'Asian', '$', 12),
('R010', 'Steakhouse Elite', 'Downtown', 'American', '$$$', 35);

-- Insert sample order data
INSERT INTO orders VALUES
-- Restaurant R001 (Pizza Palace) - Slow pickup, fast delivery
('O001', 'R001', 'C001', '2024-01-15 12:00:00', '2024-01-15 12:20:00', '2024-01-15 12:30:00', 25.50),
('O002', 'R001', 'C002', '2024-01-15 18:30:00', '2024-01-15 18:50:00', '2024-01-15 19:05:00', 32.75),
('O003', 'R001', 'C003', '2024-01-16 19:00:00', '2024-01-16 19:18:00', '2024-01-16 19:25:00', 28.00),

-- Restaurant R002 (Burger Barn) - Fast pickup, slow delivery  
('O004', 'R002', 'C004', '2024-01-15 12:15:00', '2024-01-15 12:25:00', '2024-01-15 12:50:00', 18.25),
('O005', 'R002', 'C005', '2024-01-15 19:00:00', '2024-01-15 19:08:00', '2024-01-15 19:35:00', 22.50),
('O006', 'R002', 'C006', '2024-01-16 13:30:00', '2024-01-16 13:38:00', '2024-01-16 14:10:00', 15.75),

-- Restaurant R003 (Sushi Spot) - Slow pickup, fast delivery
('O007', 'R003', 'C007', '2024-01-15 20:00:00', '2024-01-15 20:25:00', '2024-01-15 20:35:00', 45.00),
('O008', 'R003', 'C008', '2024-01-16 19:30:00', '2024-01-16 19:55:00', '2024-01-16 20:08:00', 52.25),
('O009', 'R003', 'C009', '2024-01-16 18:00:00', '2024-01-16 18:22:00', '2024-01-16 18:30:00', 38.75),

-- Restaurant R004 (Taco Time) - Fast pickup, fast delivery
('O010', 'R004', 'C010', '2024-01-15 13:00:00', '2024-01-15 13:08:00', '2024-01-15 13:20:00', 12.50),
('O011', 'R004', 'C011', '2024-01-15 20:15:00', '2024-01-15 20:20:00', '2024-01-15 20:30:00', 16.25),
('O012', 'R004', 'C012', '2024-01-16 12:45:00', '2024-01-16 12:50:00', '2024-01-16 13:05:00', 14.00),

-- Restaurant R005 (Fine Dining Co) - Very slow pickup, moderate delivery
('O013', 'R005', 'C013', '2024-01-15 19:00:00', '2024-01-15 19:35:00', '2024-01-15 19:55:00', 85.00),
('O014', 'R005', 'C014', '2024-01-16 20:00:00', '2024-01-16 20:32:00', '2024-01-16 20:50:00', 92.50),
('O015', 'R005', 'C015', '2024-01-16 18:30:00', '2024-01-16 19:05:00', '2024-01-16 19:22:00', 78.75);

-- Insert corresponding delivery data
INSERT INTO deliveries VALUES
('D001', 'O001', 'DR001', '2024-01-15 12:20:00', '2024-01-15 12:30:00', 2.5),
('D002', 'O002', 'DR002', '2024-01-15 18:50:00', '2024-01-15 19:05:00', 3.2),
('D003', 'O003', 'DR001', '2024-01-16 19:18:00', '2024-01-16 19:25:00', 1.8),
('D004', 'O004', 'DR003', '2024-01-15 12:25:00', '2024-01-15 12:50:00', 4.1),
('D005', 'O005', 'DR002', '2024-01-15 19:08:00', '2024-01-15 19:35:00', 4.8),
('D006', 'O006', 'DR004', '2024-01-16 13:38:00', '2024-01-16 14:10:00', 5.2),
('D007', 'O007', 'DR001', '2024-01-15 20:25:00', '2024-01-15 20:35:00', 2.1),
('D008', 'O008', 'DR003', '2024-01-16 19:55:00', '2024-01-16 20:08:00', 2.7),
('D009', 'O009', 'DR002', '2024-01-16 18:22:00', '2024-01-16 18:30:00', 1.5),
('D010', 'O010', 'DR004', '2024-01-15 13:08:00', '2024-01-15 13:20:00', 1.9),
('D011', 'O011', 'DR001', '2024-01-15 20:20:00', '2024-01-15 20:30:00', 2.3),
('D012', 'O012', 'DR003', '2024-01-16 12:50:00', '2024-01-16 13:05:00', 2.8),
('D013', 'O013', 'DR002', '2024-01-15 19:35:00', '2024-01-15 19:55:00', 3.5),
('D014', 'O014', 'DR004', '2024-01-16 20:32:00', '2024-01-16 20:50:00', 3.0),
('D015', 'O015', 'DR001', '2024-01-16 19:05:00', '2024-01-16 19:22:00', 2.9);

-- Create indexes for better query performance
CREATE INDEX idx_orders_restaurant_id ON orders(restaurant_id);
CREATE INDEX idx_orders_times ON orders(order_time, pickup_time, delivery_time);
CREATE INDEX idx_deliveries_order_id ON deliveries(order_id);
CREATE INDEX idx_deliveries_times ON deliveries(pickup_time, delivery_time);

-- Verify data setup
SELECT 'Data Setup Verification' as status;

SELECT 
    'Total Restaurants' as metric,
    COUNT(*) as count
FROM restaurants
UNION ALL
SELECT 
    'Total Orders' as metric,
    COUNT(*) as count  
FROM orders
UNION ALL
SELECT 
    'Total Deliveries' as metric,
    COUNT(*) as count
FROM deliveries;

-- Sample the data to verify relationships
SELECT 
    r.name,
    o.order_id,
    o.total_amount,
    EXTRACT(EPOCH FROM (o.pickup_time - o.order_time))/60 as pickup_mins,
    EXTRACT(EPOCH FROM (d.delivery_time - d.pickup_time))/60 as delivery_mins
FROM restaurants r
JOIN orders o ON r.restaurant_id = o.restaurant_id
JOIN deliveries d ON o.order_id = d.order_id
ORDER BY r.name, o.order_id
LIMIT 10;

-- Show restaurants with their average times for verification
SELECT 
    r.name,
    ROUND(AVG(o.total_amount), 2) as avg_order_amount,
    ROUND(AVG(EXTRACT(EPOCH FROM (o.pickup_time - o.order_time))/60), 1) as avg_pickup_mins,
    ROUND(AVG(EXTRACT(EPOCH FROM (d.delivery_time - d.pickup_time))/60), 1) as avg_delivery_mins,
    CASE 
        WHEN AVG(EXTRACT(EPOCH FROM (o.pickup_time - o.order_time))/60) > 
             AVG(EXTRACT(EPOCH FROM (d.delivery_time - d.pickup_time))/60) 
        THEN 'Pickup > Delivery' 
        ELSE 'Delivery >= Pickup' 
    END as comparison
FROM restaurants r
JOIN orders o ON r.restaurant_id = o.restaurant_id
JOIN deliveries d ON o.order_id = d.order_id
GROUP BY r.restaurant_id, r.name
ORDER BY r.name;

/*
Expected Results Preview:

Question 1 (Average order amount by restaurant):
- Fine Dining Co: ~$85.42
- Sushi Spot: ~$45.33  
- Pizza Palace: ~$28.75
- Burger Barn: ~$18.83
- Taco Time: ~$14.25

Question 2 (Pickup > Delivery percentage):
Based on sample data:
- Pizza Palace: Pickup longer (18 mins vs 10 mins)
- Sushi Spot: Pickup longer (22 mins vs 11 mins) 
- Fine Dining Co: Pickup longer (32 mins vs 18 mins)
- Burger Barn: Delivery longer (8 mins vs 27 mins)
- Taco Time: Delivery longer (6 mins vs 12 mins)

Result: 3 out of 5 restaurants = 60% have pickup > delivery
*/ 