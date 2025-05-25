-- SQLite
-- Create a new database using the setup script from scenario_1_ridesharing_setup.sql

-- Drop existing tables if they exist
DROP TABLE IF EXISTS fact_ride_segments;
DROP TABLE IF EXISTS fact_rides;
DROP TABLE IF EXISTS dim_users;
DROP TABLE IF EXISTS dim_location;
DROP TABLE IF EXISTS dim_ride_type;
DROP TABLE IF EXISTS dim_vehicle;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS dim_time;

-- Create dimension tables
CREATE TABLE dim_users (
    user_key INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR(50) UNIQUE NOT NULL,
    user_name TEXT,
    user_type TEXT CHECK(user_type IN ('rider', 'driver'))
);

CREATE TABLE dim_location (
    location_key INTEGER PRIMARY KEY AUTOINCREMENT,
    latitude REAL,
    longitude REAL,
    address TEXT,
    city TEXT,
    zip_code TEXT
);

CREATE TABLE dim_ride_type (
    ride_type_key INTEGER PRIMARY KEY AUTOINCREMENT,
    ride_type_name TEXT UNIQUE NOT NULL
);

CREATE TABLE dim_vehicle (
    vehicle_key INTEGER PRIMARY KEY AUTOINCREMENT,
    license_plate TEXT UNIQUE NOT NULL,
    make TEXT,
    model TEXT,
    year INTEGER,
    color TEXT
);

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

CREATE TABLE dim_time (
    time_key INTEGER PRIMARY KEY,
    full_time TIME,
    hour INTEGER,
    minute INTEGER,
    second INTEGER,
    am_pm TEXT
);

-- Create fact tables
CREATE TABLE fact_rides (
    ride_id INTEGER PRIMARY KEY AUTOINCREMENT,
    driver_user_key INTEGER,
    ride_type_key INTEGER,
    vehicle_key INTEGER,
    start_location_key INTEGER,
    end_location_key INTEGER,
    start_timestamp TEXT,
    end_timestamp TEXT,
    total_fare REAL,
    total_distance REAL,
    total_duration INTEGER,
    date_key INTEGER,
    time_key INTEGER,
    FOREIGN KEY (driver_user_key) REFERENCES dim_users(user_key),
    FOREIGN KEY (ride_type_key) REFERENCES dim_ride_type(ride_type_key),
    FOREIGN KEY (vehicle_key) REFERENCES dim_vehicle(vehicle_key),
    FOREIGN KEY (start_location_key) REFERENCES dim_location(location_key),
    FOREIGN KEY (end_location_key) REFERENCES dim_location(location_key),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (time_key) REFERENCES dim_time(time_key)
);

CREATE TABLE fact_ride_segments (
    ride_segment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ride_id INTEGER,
    rider_user_key INTEGER,
    segment_pickup_timestamp TEXT,
    segment_dropoff_timestamp TEXT,
    segment_pickup_location_key INTEGER,
    segment_dropoff_location_key INTEGER,
    segment_fare REAL,
    segment_distance REAL,
    pickup_sequence_in_ride INTEGER,
    dropoff_sequence_in_ride INTEGER,
    FOREIGN KEY (ride_id) REFERENCES fact_rides(ride_id),
    FOREIGN KEY (rider_user_key) REFERENCES dim_users(user_key),
    FOREIGN KEY (segment_pickup_location_key) REFERENCES dim_location(location_key),
    FOREIGN KEY (segment_dropoff_location_key) REFERENCES dim_location(location_key)
);

-- Insert sample data
INSERT INTO dim_users (user_id, user_name, user_type) VALUES
('driver_001', 'John Doe', 'driver'),
('driver_002', 'Jane Smith', 'driver'),
('rider_101', 'Alice Brown', 'rider'),
('rider_102', 'Bob Green', 'rider'),
('rider_103', 'Charlie White', 'rider'),
('rider_104', 'Diana Black', 'rider');

INSERT INTO dim_location (latitude, longitude, address, city, zip_code) VALUES
(34.0522, -118.2437, '123 Main St', 'Los Angeles', '90001'),
(34.0560, -118.2500, '456 Oak Ave', 'Los Angeles', '90002'),
(34.0600, -118.2550, '789 Pine Ln', 'Los Angeles', '90003'),
(34.0640, -118.2600, '101 Maple Dr', 'Los Angeles', '90004'),
(34.0680, -118.2650, '202 Birch Rd', 'Los Angeles', '90005'),
(34.0720, -118.2700, '303 Cedar Ct', 'Los Angeles', '90006');

INSERT INTO dim_ride_type (ride_type_name) VALUES
('Regular'),
('Carpool'),
('Premium');

INSERT INTO dim_vehicle (license_plate, make, model, year, color) VALUES
('DRV001', 'Toyota', 'Camry', 2020, 'Red'),
('DRV002', 'Honda', 'Accord', 2021, 'Blue');

INSERT INTO dim_date (date_key, full_date, year, quarter, month, day_of_month, day_of_week, week_of_year, is_weekend) VALUES
(20230101, '2023-01-01', 2023, 1, 1, 1, 1, 1, TRUE),
(20230102, '2023-01-02', 2023, 1, 1, 2, 2, 1, FALSE);

INSERT INTO dim_time (time_key, full_time, hour, minute, second, am_pm) VALUES
(080000, '08:00:00', 8, 0, 0, 'AM'),
(081500, '08:15:00', 8, 15, 0, 'AM'),
(083500, '08:35:00', 8, 35, 0, 'AM'),
(085000, '08:50:00', 8, 50, 0, 'AM'),
(090500, '09:05:00', 9, 5, 0, 'AM'),
(093000, '09:30:00', 9, 30, 0, 'AM');

INSERT INTO fact_rides (driver_user_key, ride_type_key, vehicle_key, start_location_key, end_location_key, start_timestamp, end_timestamp, total_fare, total_distance, total_duration, date_key, time_key) VALUES
(1, 2, 1, 1, 6, '2023-01-01 08:00:00', '2023-01-01 09:05:00', 25.50, 15.2, 65, 20230101, 080000),
(2, 1, 2, 2, 5, '2023-01-01 09:30:00', '2023-01-01 09:55:00', 12.00, 5.5, 25, 20230101, 093000),
(1, 2, 1, 3, 5, '2023-01-02 08:35:00', '2023-01-02 09:30:00', 18.75, 10.0, 55, 20230102, 083500);

INSERT INTO fact_ride_segments (ride_id, rider_user_key, segment_pickup_timestamp, segment_dropoff_timestamp, segment_pickup_location_key, segment_dropoff_location_key, segment_fare, segment_distance, pickup_sequence_in_ride, dropoff_sequence_in_ride) VALUES
(1, 3, '2023-01-01 08:00:00', '2023-01-01 08:50:00', 1, 4, 10.00, 7.0, 1, 1),
(1, 4, '2023-01-01 08:15:00', '2023-01-01 09:05:00', 2, 6, 15.50, 8.2, 2, 2),
(2, 5, '2023-01-01 09:30:00', '2023-01-01 09:55:00', 2, 5, 12.00, 5.5, 1, 1),
(3, 6, '2023-01-02 08:35:00', '2023-01-02 09:30:00', 3, 5, 18.75, 10.0, 1, 1);

SELECT 'Scenario 1: Ridesharing setup complete. Tables created and sample data inserted.';
