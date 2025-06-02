-- DoorDash Order Batching Data Model Setup Script
-- This script creates the complete data model for order batching analysis
-- Run this script to set up the full environment for testing and analysis

-- =============================================================================
-- SECTION 1: Core DoorDash Tables (Foundation)
-- =============================================================================

-- Drop existing tables if they exist (for clean setup)
DROP TABLE IF EXISTS fact_batch_state_changes;
DROP TABLE IF EXISTS fact_batch_waypoints;
DROP TABLE IF EXISTS fact_batch_deliveries;
DROP TABLE IF EXISTS fact_delivery_batches;
DROP TABLE IF EXISTS dim_batching_algorithms;
DROP TABLE IF EXISTS fact_deliveries;
DROP TABLE IF EXISTS fact_orders;
DROP TABLE IF EXISTS dim_restaurants;
DROP TABLE IF EXISTS dim_drivers;
DROP TABLE IF EXISTS dim_customers;

-- Create core dimension tables first

-- Customer dimension
CREATE TABLE dim_customers (
    customer_id BIGINT PRIMARY KEY,
    customer_external_id VARCHAR(50) UNIQUE NOT NULL,
    customer_since_date DATE NOT NULL,
    customer_tier VARCHAR(20) DEFAULT 'standard', -- 'new', 'standard', 'premium'
    delivery_address_lat DECIMAL(10, 8),
    delivery_address_lng DECIMAL(11, 8),
    avg_order_value_cents INT DEFAULT 0,
    total_orders INT DEFAULT 0,
    customer_rating DECIMAL(3,2) DEFAULT 5.0
);

-- Driver dimension with batching capabilities
CREATE TABLE dim_drivers (
    driver_id BIGINT PRIMARY KEY,
    driver_external_id VARCHAR(50) UNIQUE NOT NULL,
    driver_since_date DATE NOT NULL,
    driver_status VARCHAR(20) DEFAULT 'active', -- 'active', 'inactive', 'suspended'
    
    -- Vehicle and capacity info
    vehicle_type VARCHAR(20) NOT NULL, -- 'car', 'bike', 'scooter', 'walking'
    has_insulated_bag BOOLEAN DEFAULT TRUE,
    max_batch_capacity INT DEFAULT 4,
    driver_tier VARCHAR(10) DEFAULT 'standard', -- 'new', 'standard', 'premium'
    
    -- Performance metrics
    lifetime_deliveries INT DEFAULT 0,
    avg_delivery_rating DECIMAL(3,2) DEFAULT 5.0,
    on_time_delivery_rate DECIMAL(5,4) DEFAULT 0.95,
    acceptance_rate DECIMAL(5,4) DEFAULT 0.90,
    
    -- Current location
    current_lat DECIMAL(10, 8),
    current_lng DECIMAL(11, 8),
    last_location_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Restaurant dimension with batching support
CREATE TABLE dim_restaurants (
    restaurant_id BIGINT PRIMARY KEY,
    restaurant_external_id VARCHAR(50) UNIQUE NOT NULL,
    restaurant_name VARCHAR(200) NOT NULL,
    cuisine_type VARCHAR(50),
    
    -- Location
    restaurant_lat DECIMAL(10, 8) NOT NULL,
    restaurant_lng DECIMAL(11, 8) NOT NULL,
    phone_number VARCHAR(20),
    
    -- Operational characteristics for batching
    avg_prep_time_minutes INT DEFAULT 15,
    prep_time_std_dev_minutes INT DEFAULT 5,
    can_handle_batch_pickups BOOLEAN DEFAULT TRUE,
    max_concurrent_orders INT DEFAULT 10,
    
    -- Performance metrics
    on_time_prep_rate DECIMAL(5,4) DEFAULT 0.85,
    avg_rating DECIMAL(3,2) DEFAULT 4.5,
    is_partner_restaurant BOOLEAN DEFAULT FALSE
);

-- =============================================================================
-- SECTION 2: Core Order and Delivery Tables
-- =============================================================================

-- Orders table with batching-relevant attributes
CREATE TABLE fact_orders (
    order_id BIGINT PRIMARY KEY,
    customer_id BIGINT NOT NULL REFERENCES dim_customers(customer_id),
    restaurant_id BIGINT NOT NULL REFERENCES dim_restaurants(restaurant_id),
    order_timestamp TIMESTAMP NOT NULL,
    order_total_cents INT NOT NULL,
    item_count INT NOT NULL DEFAULT 1,
    special_instructions TEXT,
    order_status VARCHAR(20) DEFAULT 'placed', -- 'placed', 'confirmed', 'preparing', 'ready', 'picked_up', 'delivered', 'cancelled'
    
    -- Order characteristics affecting batching
    estimated_prep_time_minutes INT DEFAULT 15,
    has_hot_items BOOLEAN DEFAULT TRUE,
    has_cold_items BOOLEAN DEFAULT FALSE,
    has_alcohol BOOLEAN DEFAULT FALSE,
    requires_id_check BOOLEAN DEFAULT FALSE,
    
    -- Delivery details
    delivery_fee_cents INT DEFAULT 199,
    tip_amount_cents INT DEFAULT 0,
    delivery_address_lat DECIMAL(10, 8) NOT NULL,
    delivery_address_lng DECIMAL(11, 8) NOT NULL,
    delivery_instructions TEXT,
    
    -- Partitioning
    date_partition DATE NOT NULL
);

-- Add partitioning (PostgreSQL syntax)
-- CREATE TABLE fact_orders_partitioned (LIKE fact_orders) PARTITION BY RANGE (date_partition);

-- Deliveries table - core tracking
CREATE TABLE fact_deliveries (
    delivery_id BIGINT PRIMARY KEY,
    order_id BIGINT NOT NULL REFERENCES fact_orders(order_id),
    driver_id BIGINT REFERENCES dim_drivers(driver_id),
    
    -- Delivery lifecycle timestamps
    delivery_created_at TIMESTAMP NOT NULL,
    assigned_to_driver_at TIMESTAMP,
    driver_arrived_at_restaurant_at TIMESTAMP,
    picked_up_at TIMESTAMP,
    delivered_at TIMESTAMP,
    
    -- Performance metrics
    estimated_delivery_time_minutes INT DEFAULT 30,
    actual_delivery_time_minutes INT,
    delivery_distance_miles DECIMAL(6,2) DEFAULT 0,
    driver_to_restaurant_distance_miles DECIMAL(6,2) DEFAULT 0,
    restaurant_to_customer_distance_miles DECIMAL(6,2) DEFAULT 0,
    
    -- Status tracking
    delivery_status VARCHAR(20) DEFAULT 'created', -- 'created', 'assigned', 'en_route_to_restaurant', 'at_restaurant', 'picked_up', 'en_route_to_customer', 'delivered', 'cancelled'
    cancellation_reason VARCHAR(50),
    
    -- Partitioning
    date_partition DATE NOT NULL
);

-- =============================================================================
-- SECTION 3: Batching Extension Tables
-- =============================================================================

-- Batching algorithms configuration
CREATE TABLE dim_batching_algorithms (
    batching_algorithm_key BIGINT PRIMARY KEY,
    algorithm_name VARCHAR(100) NOT NULL,
    algorithm_version VARCHAR(20) NOT NULL,
    
    -- Algorithm metadata
    algorithm_description TEXT,
    optimization_objectives TEXT, -- JSON-like string for simple setup
    
    -- Configuration parameters
    max_batch_size INT DEFAULT 4,
    max_total_distance_miles DECIMAL(6,2) DEFAULT 10.0,
    max_total_time_minutes INT DEFAULT 60,
    max_prep_time_variance_minutes INT DEFAULT 15,
    
    -- Geographic and restaurant constraints
    max_restaurants_per_batch INT DEFAULT 3,
    allow_cross_zone_batching BOOLEAN DEFAULT FALSE,
    
    -- Deployment info
    deployed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deprecated_at TIMESTAMP,
    traffic_percentage DECIMAL(5,4) DEFAULT 0.0, -- for A/B testing
    
    UNIQUE (algorithm_name, algorithm_version)
);

-- Delivery batches - container for grouped deliveries
CREATE TABLE fact_delivery_batches (
    batch_id BIGINT PRIMARY KEY,
    driver_id BIGINT NOT NULL REFERENCES dim_drivers(driver_id),
    batching_algorithm_key BIGINT NOT NULL REFERENCES dim_batching_algorithms(batching_algorithm_key),
    
    -- Batch lifecycle
    batch_created_at TIMESTAMP NOT NULL,
    batch_assigned_at TIMESTAMP,
    batch_started_at TIMESTAMP,  -- driver starts first pickup
    batch_completed_at TIMESTAMP, -- last delivery completed
    
    -- Batch composition
    total_deliveries INT NOT NULL DEFAULT 0,
    total_orders INT NOT NULL DEFAULT 0,  -- can differ if multi-order deliveries exist
    
    -- Routing and performance
    planned_total_distance_miles DECIMAL(8,2) DEFAULT 0,
    actual_total_distance_miles DECIMAL(8,2) DEFAULT 0,
    planned_total_time_minutes INT DEFAULT 0,
    actual_total_time_minutes INT DEFAULT 0,
    
    -- Business metrics
    total_delivery_fees_cents BIGINT DEFAULT 0,
    total_tips_cents BIGINT DEFAULT 0,
    batch_efficiency_score DECIMAL(5,4) DEFAULT 0, -- algorithm-specific score
    
    -- Status tracking
    batch_status VARCHAR(20) DEFAULT 'created', -- 'created', 'assigned', 'in_progress', 'completed', 'cancelled'
    cancellation_reason VARCHAR(100),
    
    -- Partitioning
    date_partition DATE NOT NULL
);

-- Junction table connecting deliveries to batches
CREATE TABLE fact_batch_deliveries (
    batch_delivery_id BIGINT PRIMARY KEY,
    batch_id BIGINT NOT NULL REFERENCES fact_delivery_batches(batch_id),
    delivery_id BIGINT NOT NULL REFERENCES fact_deliveries(delivery_id),
    
    -- Sequencing within batch
    pickup_sequence INT NOT NULL,    -- order for restaurant visits
    dropoff_sequence INT NOT NULL,   -- order for customer deliveries
    
    -- Timing estimates vs actuals
    estimated_pickup_time TIMESTAMP,
    actual_pickup_time TIMESTAMP,
    estimated_dropoff_time TIMESTAMP, 
    actual_dropoff_time TIMESTAMP,
    
    -- Individual delivery performance within batch
    pickup_wait_time_minutes INT DEFAULT 0,
    delivery_delay_minutes INT DEFAULT 0, -- vs original single-delivery estimate
    
    -- Food quality impact
    estimated_food_temp_at_delivery DECIMAL(5,2),
    customer_satisfaction_score INT CHECK (customer_satisfaction_score BETWEEN 1 AND 5),
    
    UNIQUE (batch_id, delivery_id)
);

-- Detailed waypoint tracking for route optimization
CREATE TABLE fact_batch_waypoints (
    waypoint_id BIGINT PRIMARY KEY,
    batch_id BIGINT NOT NULL REFERENCES fact_delivery_batches(batch_id),
    delivery_id BIGINT REFERENCES fact_deliveries(delivery_id), -- NULL for driver start/end
    
    waypoint_type VARCHAR(20) NOT NULL, -- 'driver_start', 'restaurant', 'customer', 'driver_end'
    sequence_order INT NOT NULL,
    
    -- Location and timing
    waypoint_lat DECIMAL(10, 8) NOT NULL,
    waypoint_lng DECIMAL(11, 8) NOT NULL,
    estimated_arrival_time TIMESTAMP,
    actual_arrival_time TIMESTAMP,
    estimated_departure_time TIMESTAMP,
    actual_departure_time TIMESTAMP,
    
    -- Distance to next waypoint
    distance_to_next_miles DECIMAL(6,2) DEFAULT 0,
    drive_time_to_next_minutes INT DEFAULT 0
);

-- State change tracking for operational monitoring
CREATE TABLE fact_batch_state_changes (
    state_change_id BIGINT PRIMARY KEY,
    batch_id BIGINT NOT NULL REFERENCES fact_delivery_batches(batch_id),
    
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    previous_state VARCHAR(20),
    new_state VARCHAR(20) NOT NULL,
    change_trigger VARCHAR(50), -- 'driver_action', 'system_timeout', 'customer_request', 'restaurant_delay'
    
    -- Context
    driver_lat DECIMAL(10, 8),
    driver_lng DECIMAL(11, 8),
    affected_delivery_id BIGINT REFERENCES fact_deliveries(delivery_id)
);

-- =============================================================================
-- SECTION 4: Indexes for Performance
-- =============================================================================

-- Core delivery indexes
CREATE INDEX idx_orders_date_restaurant ON fact_orders(date_partition, restaurant_id);
CREATE INDEX idx_orders_customer_date ON fact_orders(customer_id, date_partition);
CREATE INDEX idx_deliveries_date_driver ON fact_deliveries(date_partition, driver_id);
CREATE INDEX idx_deliveries_order_id ON fact_deliveries(order_id);
CREATE INDEX idx_deliveries_status ON fact_deliveries(delivery_status);

-- Batching indexes
CREATE INDEX idx_batches_driver_date ON fact_delivery_batches(driver_id, date_partition);
CREATE INDEX idx_batches_algorithm_date ON fact_delivery_batches(batching_algorithm_key, date_partition);
CREATE INDEX idx_batches_status ON fact_delivery_batches(batch_status);
CREATE INDEX idx_batch_deliveries_batch ON fact_batch_deliveries(batch_id);
CREATE INDEX idx_batch_deliveries_delivery ON fact_batch_deliveries(delivery_id);
CREATE INDEX idx_batch_deliveries_pickup_seq ON fact_batch_deliveries(batch_id, pickup_sequence);
CREATE INDEX idx_batch_deliveries_dropoff_seq ON fact_batch_deliveries(batch_id, dropoff_sequence);

-- Waypoint indexes
CREATE INDEX idx_waypoints_batch_sequence ON fact_batch_waypoints(batch_id, sequence_order);
CREATE INDEX idx_waypoints_delivery ON fact_batch_waypoints(delivery_id);

-- State change indexes
CREATE INDEX idx_state_changes_batch_time ON fact_batch_state_changes(batch_id, timestamp);

-- =============================================================================
-- SECTION 5: Views for Easy Analysis
-- =============================================================================

-- Unified view of all deliveries with batch context
CREATE VIEW vw_delivery_batch_context AS
SELECT 
    d.delivery_id,
    d.order_id,
    d.driver_id,
    d.delivery_status,
    d.actual_delivery_time_minutes,
    d.estimated_delivery_time_minutes,
    d.date_partition,
    
    -- Batch information (NULL if not batched)
    bd.batch_id,
    bd.pickup_sequence,
    bd.dropoff_sequence,
    bd.pickup_wait_time_minutes,
    bd.delivery_delay_minutes,
    
    -- Batch performance
    db.total_deliveries as batch_size,
    db.batch_efficiency_score,
    db.batch_status,
    
    -- Algorithm used (NULL if not batched)
    ba.algorithm_name,
    ba.algorithm_version,
    
    -- Performance comparison
    COALESCE(bd.estimated_dropoff_time, d.delivered_at) as batch_delivery_time,
    
    -- Determine if delivery was batched
    CASE WHEN bd.batch_id IS NOT NULL THEN 'batched' ELSE 'individual' END as delivery_type
    
FROM fact_deliveries d
LEFT JOIN fact_batch_deliveries bd ON d.delivery_id = bd.delivery_id
LEFT JOIN fact_delivery_batches db ON bd.batch_id = db.batch_id
LEFT JOIN dim_batching_algorithms ba ON db.batching_algorithm_key = ba.batching_algorithm_key;

-- =============================================================================
-- SECTION 6: Sample Data for Testing
-- =============================================================================

-- Insert sample customers
INSERT INTO dim_customers VALUES
(301, 'CUST001', '2023-01-15', 'standard', 37.7800, -122.4100, 2500, 45, 4.8),
(302, 'CUST002', '2023-02-20', 'premium', 37.7820, -122.4120, 3200, 78, 4.9),
(303, 'CUST003', '2023-03-10', 'standard', 37.7780, -122.4080, 1800, 23, 4.7),
(304, 'CUST004', '2023-01-05', 'new', 37.7750, -122.4150, 1200, 5, 4.6),
(305, 'CUST005', '2023-04-01', 'standard', 37.7830, -122.4090, 2100, 34, 4.8);

-- Insert sample drivers
INSERT INTO dim_drivers VALUES
(101, 'DRV001', '2023-01-01', 'active', 'car', TRUE, 4, 'premium', 523, 4.9, 0.96, 0.92, 37.7749, -122.4194, '2024-01-15 12:00:00'),
(102, 'DRV002', '2023-02-15', 'active', 'bike', TRUE, 2, 'standard', 287, 4.7, 0.89, 0.95, 37.7849, -122.4094, '2024-01-15 12:00:00'),
(103, 'DRV003', '2023-01-20', 'active', 'car', TRUE, 5, 'standard', 445, 4.8, 0.93, 0.88, 37.7649, -122.4294, '2024-01-15 12:00:00'),
(104, 'DRV004', '2023-03-01', 'active', 'scooter', TRUE, 3, 'new', 89, 4.6, 0.85, 0.90, 37.7749, -122.4100, '2024-01-15 12:00:00');

-- Insert sample restaurants
INSERT INTO dim_restaurants VALUES
(201, 'REST001', 'Pizza Palace', 'italian', 37.7759, -122.4180, '+1-555-0101', 20, 5, TRUE, 8, 0.88, 4.5, TRUE),
(202, 'REST002', 'Burger Barn', 'american', 37.7770, -122.4160, '+1-555-0102', 15, 3, TRUE, 12, 0.92, 4.3, FALSE),
(203, 'REST003', 'Sushi Spot', 'japanese', 37.7740, -122.4200, '+1-555-0103', 25, 8, FALSE, 6, 0.85, 4.7, TRUE),
(204, 'REST004', 'Taco Time', 'mexican', 37.7730, -122.4110, '+1-555-0104', 12, 4, TRUE, 15, 0.90, 4.4, FALSE);

-- Insert sample batching algorithms
INSERT INTO dim_batching_algorithms VALUES
(1, 'nearest_neighbor', 'v1.0', 'Simple nearest neighbor algorithm', 'minimize_distance', 4, 8.0, 45, 10, 3, FALSE, '2024-01-01 00:00:00', NULL, 0.25),
(2, 'genetic_algorithm', 'v2.1', 'Genetic algorithm optimization', 'minimize_time_maximize_orders', 5, 12.0, 60, 15, 4, TRUE, '2024-01-15 00:00:00', NULL, 0.25),
(3, 'ml_optimized', 'v1.5', 'Machine learning optimized routing', 'maximize_efficiency', 4, 10.0, 50, 12, 3, FALSE, '2024-02-01 00:00:00', NULL, 0.30),
(4, 'no_batching', 'v1.0', 'Individual delivery only', 'minimize_delivery_time', 1, 0.0, 30, 0, 1, FALSE, '2024-01-01 00:00:00', NULL, 0.20);

-- Insert sample orders for January 15, 2024
INSERT INTO fact_orders VALUES
(1001, 301, 201, '2024-01-15 12:00:00', 2500, 3, 'Extra cheese please', 'delivered', 20, TRUE, FALSE, FALSE, FALSE, 199, 400, 37.7800, -122.4100, 'Ring doorbell', '2024-01-15'),
(1002, 302, 201, '2024-01-15 12:05:00', 1800, 2, NULL, 'delivered', 20, TRUE, FALSE, FALSE, FALSE, 199, 300, 37.7820, -122.4120, 'Leave at door', '2024-01-15'),
(1003, 303, 202, '2024-01-15 12:08:00', 1200, 1, NULL, 'delivered', 15, TRUE, FALSE, FALSE, FALSE, 199, 200, 37.7780, -122.4080, NULL, '2024-01-15'),
(1004, 304, 203, '2024-01-15 12:15:00', 3200, 4, 'No wasabi', 'delivered', 25, FALSE, TRUE, FALSE, FALSE, 299, 500, 37.7750, -122.4150, 'Apt 2B', '2024-01-15'),
(1005, 305, 204, '2024-01-15 12:20:00', 1500, 2, 'Mild sauce', 'delivered', 12, TRUE, FALSE, FALSE, FALSE, 199, 250, 37.7830, -122.4090, NULL, '2024-01-15');

-- Insert corresponding deliveries
INSERT INTO fact_deliveries VALUES
(2001, 1001, 101, '2024-01-15 12:00:00', '2024-01-15 12:10:00', '2024-01-15 12:30:00', '2024-01-15 12:35:00', '2024-01-15 13:05:00', 45, 48, 3.2, 1.5, 1.7, 'delivered', NULL, '2024-01-15'),
(2002, 1002, 101, '2024-01-15 12:05:00', '2024-01-15 12:10:00', '2024-01-15 12:35:00', '2024-01-15 12:40:00', '2024-01-15 13:15:00', 50, 52, 3.8, 0.8, 3.0, 'delivered', NULL, '2024-01-15'),
(2003, 1003, 102, '2024-01-15 12:08:00', '2024-01-15 12:15:00', '2024-01-15 12:40:00', '2024-01-15 12:45:00', '2024-01-15 13:10:00', 40, 38, 2.8, 1.2, 1.6, 'delivered', NULL, '2024-01-15'),
(2004, 1004, 103, '2024-01-15 12:15:00', '2024-01-15 12:25:00', '2024-01-15 12:50:00', '2024-01-15 12:58:00', '2024-01-15 13:25:00', 55, 53, 4.1, 1.8, 2.3, 'delivered', NULL, '2024-01-15'),
(2005, 1005, 104, '2024-01-15 12:20:00', '2024-01-15 12:30:00', '2024-01-15 12:50:00', '2024-01-15 12:55:00', '2024-01-15 13:20:00', 35, 37, 2.5, 1.0, 1.5, 'delivered', NULL, '2024-01-15');

-- Create a sample batch (orders 1001 and 1002 batched together)
INSERT INTO fact_delivery_batches VALUES
(3001, 101, 1, '2024-01-15 12:10:00', '2024-01-15 12:10:00', '2024-01-15 12:15:00', '2024-01-15 13:15:00', 2, 2, 5.2, 5.8, 65, 70, 798, 700, 0.85, 'completed', NULL, '2024-01-15');

-- Link deliveries to batch
INSERT INTO fact_batch_deliveries VALUES
(4001, 3001, 2001, 1, 1, '2024-01-15 12:30:00', '2024-01-15 12:35:00', '2024-01-15 13:00:00', '2024-01-15 13:05:00', 5, 3, 98.5, 4),
(4002, 3001, 2002, 1, 2, '2024-01-15 12:35:00', '2024-01-15 12:40:00', '2024-01-15 13:10:00', '2024-01-15 13:15:00', 5, 2, 96.2, 5);

-- Add sample waypoints for the batch
INSERT INTO fact_batch_waypoints VALUES
(5001, 3001, NULL, 'driver_start', 1, 37.7749, -122.4194, '2024-01-15 12:15:00', '2024-01-15 12:15:00', '2024-01-15 12:17:00', '2024-01-15 12:18:00', 0.8, 3),
(5002, 3001, 2001, 'restaurant', 2, 37.7759, -122.4180, '2024-01-15 12:30:00', '2024-01-15 12:30:00', '2024-01-15 12:35:00', '2024-01-15 12:35:00', 1.7, 8),
(5003, 3001, 2001, 'customer', 3, 37.7800, -122.4100, '2024-01-15 13:00:00', '2024-01-15 13:05:00', '2024-01-15 13:02:00', '2024-01-15 13:07:00', 3.0, 10),
(5004, 3001, 2002, 'customer', 4, 37.7820, -122.4120, '2024-01-15 13:10:00', '2024-01-15 13:15:00', '2024-01-15 13:12:00', '2024-01-15 13:17:00', 0.0, 0);

-- Add sample state changes
INSERT INTO fact_batch_state_changes VALUES
(6001, 3001, '2024-01-15 12:10:00', NULL, 'created', 'system_timeout', 37.7749, -122.4194, NULL),
(6002, 3001, '2024-01-15 12:10:00', 'created', 'assigned', 'driver_action', 37.7749, -122.4194, NULL),
(6003, 3001, '2024-01-15 12:15:00', 'assigned', 'in_progress', 'driver_action', 37.7749, -122.4194, NULL),
(6004, 3001, '2024-01-15 13:15:00', 'in_progress', 'completed', 'driver_action', 37.7820, -122.4120, 2002);

-- =============================================================================
-- SECTION 7: Verification Queries
-- =============================================================================

-- Verify setup with some basic queries
-- These will be commented out for the script but can be run manually

/*
-- Check table row counts
SELECT 'dim_customers' as table_name, COUNT(*) as row_count FROM dim_customers
UNION ALL
SELECT 'dim_drivers', COUNT(*) FROM dim_drivers
UNION ALL  
SELECT 'dim_restaurants', COUNT(*) FROM dim_restaurants
UNION ALL
SELECT 'fact_orders', COUNT(*) FROM fact_orders
UNION ALL
SELECT 'fact_deliveries', COUNT(*) FROM fact_deliveries
UNION ALL
SELECT 'fact_delivery_batches', COUNT(*) FROM fact_delivery_batches
UNION ALL
SELECT 'fact_batch_deliveries', COUNT(*) FROM fact_batch_deliveries;

-- Test the unified view
SELECT 
    delivery_type,
    COUNT(*) as delivery_count,
    AVG(actual_delivery_time_minutes) as avg_delivery_time
FROM vw_delivery_batch_context 
GROUP BY delivery_type;

-- Check batch performance
SELECT 
    ba.algorithm_name,
    COUNT(db.batch_id) as total_batches,
    AVG(db.total_deliveries) as avg_batch_size,
    AVG(db.batch_efficiency_score) as avg_efficiency
FROM fact_delivery_batches db
JOIN dim_batching_algorithms ba ON db.batching_algorithm_key = ba.batching_algorithm_key
GROUP BY ba.algorithm_name;
*/

-- =============================================================================
-- Script Complete
-- =============================================================================

-- Print completion message
SELECT 'DoorDash Order Batching Database Setup Complete!' as status,
       'Tables Created: ' || (
           SELECT COUNT(*) FROM information_schema.tables 
           WHERE table_schema = CURRENT_SCHEMA()
           AND table_name LIKE 'fact_%' OR table_name LIKE 'dim_%'
       ) as table_count; 