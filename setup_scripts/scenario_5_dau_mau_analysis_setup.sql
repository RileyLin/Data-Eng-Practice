-- Setup script for Scenario 5: DAU/MAU Analysis

-- Dimension Tables
DROP TABLE IF EXISTS dim_user_segments_dau;
CREATE TABLE dim_user_segments_dau (
    user_segment_key INTEGER PRIMARY KEY AUTOINCREMENT,
    segment_name TEXT UNIQUE NOT NULL, -- e.g., 'New Users', 'Power Users', 'Casual Users', 'Churn Risk'
    segment_description TEXT
);

DROP TABLE IF EXISTS dim_users_dau;
CREATE TABLE dim_users_dau (
    user_key INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR(50) UNIQUE NOT NULL,
    registration_timestamp TEXT, -- ISO 8601 format
    user_segment_key INTEGER, -- FK to dim_user_segments_dau
    gender TEXT, -- 'Male', 'Female', 'Other', 'Prefer not to say'
    birth_date TEXT, -- YYYY-MM-DD
    account_status TEXT DEFAULT 'active', -- e.g., 'active', 'suspended', 'deactivated'
    is_test_account BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_segment_key) REFERENCES dim_user_segments_dau(user_segment_key)
);

DROP TABLE IF EXISTS dim_features_dau;
CREATE TABLE dim_features_dau (
    feature_key INTEGER PRIMARY KEY AUTOINCREMENT,
    feature_id VARCHAR(50) UNIQUE NOT NULL,
    feature_name TEXT NOT NULL, -- e.g., 'Photo Upload', 'Video Playback', 'User Profile Edit', 'Search'
    feature_category TEXT, -- e.g., 'Core', 'Social', 'Monetization'
    is_core_feature BOOLEAN DEFAULT FALSE
);

DROP TABLE IF EXISTS dim_devices_dau;
CREATE TABLE dim_devices_dau (
    device_key INTEGER PRIMARY KEY AUTOINCREMENT,
    device_identifier TEXT UNIQUE NOT NULL, -- Could be a hash or a unique ID from client
    device_type TEXT, -- e.g., 'Mobile', 'Desktop', 'Tablet', 'Web'
    platform TEXT, -- e.g., 'iOS', 'Android', 'Windows', 'macOS', 'Web'
    os_version TEXT,
    app_version TEXT
);

DROP TABLE IF EXISTS dim_geographies_dau;
CREATE TABLE dim_geographies_dau (
    geography_key INTEGER PRIMARY KEY AUTOINCREMENT,
    country_code VARCHAR(2) NOT NULL,
    country_name TEXT NOT NULL,
    region_name TEXT, -- State / Province
    city_name TEXT
);

DROP TABLE IF EXISTS dim_activity_types_dau;
CREATE TABLE dim_activity_types_dau (
    activity_type_key INTEGER PRIMARY KEY AUTOINCREMENT,
    activity_name TEXT UNIQUE NOT NULL, -- e.g., 'app_open', 'screen_view', 'button_click', 'item_purchase'
    activity_category TEXT -- e.g., 'System Event', 'Navigation', 'Engagement', 'Transaction'
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

-- Fact Table
DROP TABLE IF EXISTS fact_user_activity_dau;
CREATE TABLE fact_user_activity_dau (
    activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_key INTEGER, -- FK to dim_users_dau
    date_key INTEGER, -- FK to dim_date
    time_key INTEGER, -- FK to dim_time
    feature_key INTEGER, -- FK to dim_features_dau (can be NULL if activity is not feature-specific)
    device_key INTEGER, -- FK to dim_devices_dau
    geography_key INTEGER, -- FK to dim_geographies_dau
    activity_type_key INTEGER, -- FK to dim_activity_types_dau
    activity_timestamp TEXT NOT NULL, -- ISO 8601 format
    session_id VARCHAR(100), -- To group activities within a session
    duration_seconds INTEGER, -- Duration of this specific activity/event if applicable
    FOREIGN KEY (user_key) REFERENCES dim_users_dau(user_key),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (time_key) REFERENCES dim_time(time_key),
    FOREIGN KEY (feature_key) REFERENCES dim_features_dau(feature_key),
    FOREIGN KEY (device_key) REFERENCES dim_devices_dau(device_key),
    FOREIGN KEY (geography_key) REFERENCES dim_geographies_dau(geography_key),
    FOREIGN KEY (activity_type_key) REFERENCES dim_activity_types_dau(activity_type_key)
);

-- Sample Data Insertion

-- dim_date (Example for Feb 1-3, 2023)
INSERT INTO dim_date (date_key, full_date, year, quarter, month, day_of_month, day_of_week, week_of_year, is_weekend) VALUES
(20230201, '2023-02-01', 2023, 1, 2, 1, 4, 5, FALSE),
(20230202, '2023-02-02', 2023, 1, 2, 2, 5, 5, FALSE),
(20230203, '2023-02-03', 2023, 1, 2, 3, 6, 5, FALSE);

-- dim_time (Examples)
INSERT INTO dim_time (time_key, full_time, hour, minute, second, am_pm) VALUES
(090000, '09:00:00', 9, 0, 0, 'AM'),
(090530, '09:05:30', 9, 5, 30, 'AM'),
(101500, '10:15:00', 10, 15, 0, 'AM'),
(102015, '10:20:15', 10, 20, 15, 'AM');

-- dim_user_segments_dau
INSERT INTO dim_user_segments_dau (segment_name, segment_description) VALUES
('New Users', 'Users registered in the last 30 days'),
('Power Users', 'Users with high activity levels'),
('Casual Users', 'Users with moderate or infrequent activity');

-- dim_users_dau
INSERT INTO dim_users_dau (user_id, registration_timestamp, user_segment_key, gender, birth_date) VALUES
('dau_user_1', '2023-02-01 08:00:00', 1, 'Female', '1990-05-15'),
('dau_user_2', '2022-11-10 10:00:00', 2, 'Male', '1985-11-20'),
('dau_user_3', '2023-01-15 12:30:00', 1, 'Other', '2000-01-01'),
('dau_user_4', '2022-07-01 14:00:00', 3, 'Male', '1995-07-30');

-- dim_features_dau
INSERT INTO dim_features_dau (feature_id, feature_name, feature_category, is_core_feature) VALUES
('F001', 'Dashboard View', 'Core', TRUE),
('F002', 'Profile Edit', 'User Management', FALSE),
('F003', 'Content Upload', 'Content Creation', TRUE),
('F004', 'Search Content', 'Discovery', TRUE);

-- dim_devices_dau
INSERT INTO dim_devices_dau (device_identifier, device_type, platform, os_version, app_version) VALUES
('dev_ios_123', 'Mobile', 'iOS', '16.1', '2.5.0'),
('dev_android_456', 'Mobile', 'Android', '13.0', '2.4.1'),
('dev_web_789', 'Web', 'Web', 'Windows 10', 'Chrome 110');

-- dim_geographies_dau
INSERT INTO dim_geographies_dau (country_code, country_name, region_name, city_name) VALUES
('US', 'United States', 'California', 'San Francisco'),
('US', 'United States', 'New York', 'New York City'),
('CA', 'Canada', 'Ontario', 'Toronto'),
('GB', 'United Kingdom', 'England', 'London');

-- dim_activity_types_dau
INSERT INTO dim_activity_types_dau (activity_name, activity_category) VALUES
('app_launch', 'System'),
('screen_view', 'Navigation'),
('feature_use', 'Engagement'),
('item_click', 'Engagement');

-- fact_user_activity_dau
-- User 1 (New User, SF, iOS)
INSERT INTO fact_user_activity_dau (user_key, date_key, time_key, feature_key, device_key, geography_key, activity_type_key, activity_timestamp, session_id) VALUES
(1, 20230201, 090000, 1, 1, 1, 1, '2023-02-01 09:00:00', 'sess_u1_1'), -- App Launch, Dashboard View (feature)
(1, 20230201, 090000, 1, 1, 1, 2, '2023-02-01 09:00:10', 'sess_u1_1'), -- Screen View (Dashboard)
(1, 20230201, 090530, 2, 1, 1, 3, '2023-02-01 09:05:30', 'sess_u1_1'); -- Feature Use (Profile Edit)

-- User 2 (Power User, NYC, Android)
INSERT INTO fact_user_activity_dau (user_key, date_key, time_key, feature_key, device_key, geography_key, activity_type_key, activity_timestamp, session_id) VALUES
(2, 20230201, 101500, 3, 2, 2, 1, '2023-02-01 10:15:00', 'sess_u2_1'), -- App Launch, Content Upload (feature)
(2, 20230201, 101500, 3, 2, 2, 2, '2023-02-01 10:15:05', 'sess_u2_1'), -- Screen View (Upload Form)
(2, 20230201, 102015, 3, 2, 2, 3, '2023-02-01 10:20:15', 'sess_u2_1'); -- Feature Use (Content Upload)

-- User 1 again on a different day (Feb 2nd)
INSERT INTO fact_user_activity_dau (user_key, date_key, time_key, feature_key, device_key, geography_key, activity_type_key, activity_timestamp, session_id) VALUES
(1, 20230202, 090000, 4, 1, 1, 1, '2023-02-02 09:00:00', 'sess_u1_2'), -- App Launch, Search Content (feature)
(1, 20230202, 090000, 4, 1, 1, 3, '2023-02-02 09:00:45', 'sess_u1_2'); -- Feature Use (Search)

-- User 3 (New User, Toronto, Web)
INSERT INTO fact_user_activity_dau (user_key, date_key, time_key, feature_key, device_key, geography_key, activity_type_key, activity_timestamp, session_id) VALUES
(3, 20230202, 101500, 1, 3, 3, 1, '2023-02-02 10:15:00', 'sess_u3_1'); -- App Launch, Dashboard View

-- User 4 (Casual User, London, iOS) - activity on Feb 1st & 3rd
INSERT INTO fact_user_activity_dau (user_key, date_key, time_key, feature_key, device_key, geography_key, activity_type_key, activity_timestamp, session_id) VALUES
(4, 20230201, 090000, 1, 1, 4, 1, '2023-02-01 09:00:00', 'sess_u4_1'),
(4, 20230203, 102015, 4, 1, 4, 3, '2023-02-03 10:20:15', 'sess_u4_2');

SELECT 'Scenario 5: DAU/MAU Analysis setup complete. Tables created and sample data inserted.'; 