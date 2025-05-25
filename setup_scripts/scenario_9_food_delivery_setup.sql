-- Setup script for Scenario 9: Food Delivery (DoorDash) - Order Batching

-- Dimension Tables
DROP TABLE IF EXISTS dim_users_delivery; -- Customers
CREATE TABLE dim_users_delivery (
    user_key INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR(50) UNIQUE NOT NULL,
    username TEXT,
    phone_number TEXT,
    email TEXT,
    created_timestamp TEXT -- ISO 8601 format
);

DROP TABLE IF EXISTS dim_drivers_delivery;
CREATE TABLE dim_drivers_delivery (
    driver_key INTEGER PRIMARY KEY AUTOINCREMENT,
    driver_id VARCHAR(50) UNIQUE NOT NULL,
    driver_name TEXT,
    vehicle_type TEXT, -- e.g., 'Car', 'Scooter', 'Bike'
    current_status TEXT DEFAULT 'offline' -- e.g., 'online_available', 'online_in_delivery', 'offline'
);

DROP TABLE IF EXISTS dim_restaurants_delivery;
CREATE TABLE dim_restaurants_delivery (
    restaurant_key INTEGER PRIMARY KEY AUTOINCREMENT,
    restaurant_id VARCHAR(50) UNIQUE NOT NULL,
    restaurant_name TEXT NOT NULL,
    cuisine_type TEXT,
    address TEXT,
    city TEXT,
    latitude REAL,
    longitude REAL,
    avg_prep_time_minutes INTEGER -- Average food preparation time
);

DROP TABLE IF EXISTS dim_order_status_delivery;
CREATE TABLE dim_order_status_delivery (
    order_status_key INTEGER PRIMARY KEY AUTOINCREMENT,
    status_name TEXT UNIQUE NOT NULL, -- e.g., 'Pending Confirmation', 'Confirmed', 'Preparing', 'Ready for Pickup', 'Picked Up', 'Out for Delivery', 'Delivered', 'Cancelled', 'Failed Delivery'
    description TEXT,
    is_terminal BOOLEAN DEFAULT FALSE -- Is this a final state for an order?
);

DROP TABLE IF EXISTS dim_batch_status_delivery;
CREATE TABLE dim_batch_status_delivery (
    batch_status_key INTEGER PRIMARY KEY AUTOINCREMENT,
    status_name TEXT UNIQUE NOT NULL, -- e.g., 'Batch Created', 'Assigning Driver', 'Driver Assigned', 'En Route to Pickup', 'Picking Up Orders', 'En Route to Dropoff', 'Delivering Orders', 'Batch Completed', 'Batch Failed'
    is_terminal BOOLEAN DEFAULT FALSE
);

-- Re-using dim_date and dim_time.
DROP TABLE IF EXISTS dim_date; -- Included for standalone execution
CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY, 
    full_date DATE,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    day_of_month INTEGER,
    day_of_week INTEGER, 
    week_of_year INTEGER,
    is_weekend BOOLEAN
);

DROP TABLE IF EXISTS dim_time; -- Included for standalone execution
CREATE TABLE dim_time (
    time_key INTEGER PRIMARY KEY, 
    full_time TIME,
    hour INTEGER,
    minute INTEGER,
    second INTEGER,
    am_pm TEXT
);

-- Fact Tables
DROP TABLE IF EXISTS fact_orders_delivery;
CREATE TABLE fact_orders_delivery (
    order_key INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id VARCHAR(50) UNIQUE NOT NULL,
    user_key INTEGER, -- FK to dim_users_delivery (customer)
    restaurant_key INTEGER, -- FK to dim_restaurants_delivery
    order_status_key INTEGER, -- FK to dim_order_status_delivery
    order_placed_timestamp TEXT NOT NULL, -- ISO 8601 format
    order_placed_date_key INTEGER,
    order_placed_time_key INTEGER,
    estimated_delivery_time TEXT, -- ISO 8601 format (initial estimate)
    actual_delivery_time TEXT,    -- ISO 8601 format (when actually delivered)
    pickup_location_lat REAL,
    pickup_location_lon REAL,
    dropoff_location_lat REAL,
    dropoff_location_lon REAL,
    order_total_amount REAL,
    delivery_fee REAL,
    special_instructions TEXT,
    pickup_deadline TEXT, -- For q011
    dropoff_deadline TEXT, -- For q011
    order_items_volume INTEGER, -- For q011 (e.g. 1=small, 2=medium, 3=large)
    FOREIGN KEY (user_key) REFERENCES dim_users_delivery(user_key),
    FOREIGN KEY (restaurant_key) REFERENCES dim_restaurants_delivery(restaurant_key),
    FOREIGN KEY (order_status_key) REFERENCES dim_order_status_delivery(order_status_key),
    FOREIGN KEY (order_placed_date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (order_placed_time_key) REFERENCES dim_time(time_key)
);

DROP TABLE IF EXISTS fact_delivery_batches_delivery;
CREATE TABLE fact_delivery_batches_delivery (
    batch_key INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_id VARCHAR(50) UNIQUE NOT NULL,
    driver_key INTEGER, -- FK to dim_drivers_delivery
    batch_status_key INTEGER, -- FK to dim_batch_status_delivery
    created_timestamp TEXT NOT NULL, -- ISO 8601 format
    assigned_timestamp TEXT,
    completed_timestamp TEXT,
    created_date_key INTEGER,
    created_time_key INTEGER,
    FOREIGN KEY (driver_key) REFERENCES dim_drivers_delivery(driver_key),
    FOREIGN KEY (batch_status_key) REFERENCES dim_batch_status_delivery(batch_status_key),
    FOREIGN KEY (created_date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (created_time_key) REFERENCES dim_time(time_key)
);

DROP TABLE IF EXISTS bridge_batch_order_items_delivery;
CREATE TABLE bridge_batch_order_items_delivery (
    batch_order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_key INTEGER, -- FK to fact_delivery_batches_delivery
    order_key INTEGER, -- FK to fact_orders_delivery
    pickup_sequence INTEGER, -- Sequence for picking up this order in the batch
    dropoff_sequence INTEGER, -- Sequence for dropping off this order in the batch
    FOREIGN KEY (batch_key) REFERENCES fact_delivery_batches_delivery(batch_key),
    FOREIGN KEY (order_key) REFERENCES fact_orders_delivery(order_key),
    UNIQUE (batch_key, order_key) -- An order is typically in one batch at a time
);

-- Sample Data Insertion

-- dim_date (Example for June 1-2, 2023)
INSERT INTO dim_date (date_key, full_date, year, quarter, month, day_of_month, day_of_week, week_of_year, is_weekend) VALUES
(20230601, '2023-06-01', 2023, 2, 6, 1, 5, 22, FALSE),
(20230602, '2023-06-02', 2023, 2, 6, 2, 6, 22, FALSE);

-- dim_time (Examples)
INSERT INTO dim_time (time_key, full_time, hour, minute, second, am_pm) VALUES
(180000, '18:00:00', 18, 0, 0, 'PM'),
(180500, '18:05:00', 18, 5, 0, 'PM'),
(181500, '18:15:00', 18, 15, 0, 'PM'),
(183000, '18:30:00', 18, 30, 0, 'PM'),
(190000, '19:00:00', 19, 0, 0, 'PM');

-- dim_users_delivery
INSERT INTO dim_users_delivery (user_id, username, phone_number, email, created_timestamp) VALUES
('cust_A', 'HungryHarry', '555-0101', 'harry@example.com', '2023-01-10 10:00:00'),
('cust_B', 'SpeedySally', '555-0102', 'sally@example.com', '2023-02-15 11:00:00');

-- dim_drivers_delivery
INSERT INTO dim_drivers_delivery (driver_id, driver_name, vehicle_type, current_status) VALUES
('driver_001', 'Dave Dasher', 'Car', 'online_available'),
('driver_002', 'Rita Rider', 'Scooter', 'online_available');

-- dim_restaurants_delivery
INSERT INTO dim_restaurants_delivery (restaurant_id, restaurant_name, cuisine_type, address, city, latitude, longitude, avg_prep_time_minutes) VALUES
('rest_pizza_palace', 'Pizza Palace', 'Italian', '123 Pepperoni Way', 'Foodville', 34.0522, -118.2437, 20),
('rest_sushi_spot', 'Sushi Spot', 'Japanese', '456 Wasabi Ave', 'Foodville', 34.0580, -118.2500, 15);

-- dim_order_status_delivery
INSERT INTO dim_order_status_delivery (status_name, is_terminal) VALUES
('Pending Confirmation', FALSE), ('Confirmed', FALSE), ('Preparing', FALSE), ('Ready for Pickup', FALSE),
('Picked Up', FALSE), ('Out for Delivery', FALSE), ('Delivered', TRUE), ('Cancelled', TRUE);

-- dim_batch_status_delivery
INSERT INTO dim_batch_status_delivery (status_name, is_terminal) VALUES
('Batch Created', FALSE), ('Driver Assigned', FALSE), ('Picking Up', FALSE), ('Delivering', FALSE), ('Batch Completed', TRUE), ('Batch Failed', TRUE);

-- fact_orders_delivery
INSERT INTO fact_orders_delivery (order_id, user_key, restaurant_key, order_status_key, order_placed_timestamp, order_placed_date_key, order_placed_time_key, order_total_amount, delivery_fee, pickup_location_lat, pickup_location_lon, dropoff_location_lat, dropoff_location_lon, pickup_deadline, dropoff_deadline, order_items_volume) VALUES
('ORD1001', 1, 1, 2, '2023-06-01 18:00:00', 20230601, 180000, 25.50, 3.99, 34.0522, -118.2437, 34.0700, -118.2600, '2023-06-01 18:30:00', '2023-06-01 19:00:00', 2),
('ORD1002', 2, 2, 2, '2023-06-01 18:05:00', 20230601, 180500, 32.00, 2.99, 34.0580, -118.2500, 34.0800, -118.2700, '2023-06-01 18:35:00', '2023-06-01 19:05:00', 1),
('ORD1003', 1, 2, 1, '2023-06-01 18:15:00', 20230601, 181500, 15.75, 4.50, 34.0580, -118.2500, 34.0750, -118.2650, '2023-06-01 18:45:00', '2023-06-01 19:15:00', 1);

-- fact_delivery_batches_delivery (Assume ORD1001 and ORD1002 are batched)
INSERT INTO fact_delivery_batches_delivery (batch_id, driver_key, batch_status_key, created_timestamp, created_date_key, created_time_key, assigned_timestamp) VALUES
('BATCH001', 1, 2, '2023-06-01 18:10:00', 20230601, 180500, '2023-06-01 18:12:00');

-- bridge_batch_order_items_delivery
INSERT INTO bridge_batch_order_items_delivery (batch_key, order_key, pickup_sequence, dropoff_sequence) VALUES
(1, 1, 1, 2), -- Batch 1, Order ORD1001 (key 1), pickup 1st, dropoff 2nd
(1, 2, 2, 1); -- Batch 1, Order ORD1002 (key 2), pickup 2nd, dropoff 1st

SELECT 'Scenario 9: Food Delivery setup complete. Tables created and sample data inserted.'; 