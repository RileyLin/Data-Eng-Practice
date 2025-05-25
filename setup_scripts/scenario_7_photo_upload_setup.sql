-- Setup script for Scenario 7: Photo Upload (Instagram-like)

-- Dimension Tables
DROP TABLE IF EXISTS dim_users_photo;
CREATE TABLE dim_users_photo (
    user_key INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR(50) UNIQUE NOT NULL,
    username TEXT,
    registration_timestamp TEXT -- ISO 8601 format
);

DROP TABLE IF EXISTS dim_devices_photo;
CREATE TABLE dim_devices_photo (
    device_key INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id VARCHAR(50) UNIQUE NOT NULL, -- e.g., UDID or a client-generated ID
    device_type TEXT, -- 'Mobile', 'Tablet', 'Web'
    platform TEXT, -- 'iOS', 'Android', 'Web'
    os_version TEXT
);

DROP TABLE IF EXISTS dim_app_versions_photo;
CREATE TABLE dim_app_versions_photo (
    app_version_key INTEGER PRIMARY KEY AUTOINCREMENT,
    app_version TEXT UNIQUE NOT NULL, -- e.g., '3.14.0'
    platform TEXT, -- 'iOS', 'Android', 'Web'
    release_date TEXT -- ISO 8601 format
);

DROP TABLE IF EXISTS dim_upload_status_photo;
CREATE TABLE dim_upload_status_photo (
    upload_status_key INTEGER PRIMARY KEY AUTOINCREMENT,
    status_name TEXT UNIQUE NOT NULL, -- e.g., 'Success', 'Failed - Network', 'Failed - Server', 'Failed - Client Validation', 'Pending'
    is_success BOOLEAN NOT NULL
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
DROP TABLE IF EXISTS fact_photo_uploads;
CREATE TABLE fact_photo_uploads (
    upload_attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
    photo_id VARCHAR(50) UNIQUE, -- Populated on successful upload, could be NULL for failed attempts before ID generation
    user_key INTEGER, -- FK to dim_users_photo
    device_key INTEGER, -- FK to dim_devices_photo
    app_version_key INTEGER, -- FK to dim_app_versions_photo
    upload_status_key INTEGER, -- FK to dim_upload_status_photo
    attempt_start_timestamp TEXT NOT NULL, -- ISO 8601 format
    attempt_end_timestamp TEXT, -- ISO 8601 format, NULL if still pending or crashed
    upload_duration_ms INTEGER, -- Calculated as end - start
    file_size_bytes INTEGER,
    photo_width_px INTEGER, -- Extracted metadata after successful processing
    photo_height_px INTEGER, -- Extracted metadata
    mime_type TEXT, -- e.g., 'image/jpeg', 'image/png'
    network_type TEXT, -- e.g., 'WiFi', '4G', '5G', 'Offline'
    failure_reason TEXT, -- Populated if status is a failure type
    date_key INTEGER, -- FK to dim_date (date of attempt_start_timestamp)
    time_key INTEGER, -- FK to dim_time (time of attempt_start_timestamp)
    FOREIGN KEY (user_key) REFERENCES dim_users_photo(user_key),
    FOREIGN KEY (device_key) REFERENCES dim_devices_photo(device_key),
    FOREIGN KEY (app_version_key) REFERENCES dim_app_versions_photo(app_version_key),
    FOREIGN KEY (upload_status_key) REFERENCES dim_upload_status_photo(upload_status_key),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (time_key) REFERENCES dim_time(time_key)
);

-- Sample Data Insertion

-- dim_date (Example for Apr 1-2, 2023)
INSERT INTO dim_date (date_key, full_date, year, quarter, month, day_of_month, day_of_week, week_of_year, is_weekend) VALUES
(20230401, '2023-04-01', 2023, 2, 4, 1, 7, 13, TRUE),
(20230402, '2023-04-02', 2023, 2, 4, 2, 1, 14, TRUE);

-- dim_time (Examples)
INSERT INTO dim_time (time_key, full_time, hour, minute, second, am_pm) VALUES
(130000, '13:00:00', 13, 0, 0, 'PM'),
(130500, '13:05:00', 13, 5, 0, 'PM'),
(131000, '13:10:00', 13, 10, 0, 'PM');

-- dim_users_photo
INSERT INTO dim_users_photo (user_id, username, registration_timestamp) VALUES
('photo_user_X', 'XavierPixel', '2023-01-20 10:00:00'),
('photo_user_Y', 'YaraSnap', '2023-02-25 15:30:00');

-- dim_devices_photo
INSERT INTO dim_devices_photo (device_id, device_type, platform, os_version) VALUES
('dev_photo_ios1', 'Mobile', 'iOS', '16.2'),
('dev_photo_and1', 'Mobile', 'Android', '13'),
('dev_photo_web1', 'Web', 'Web', 'Chrome 111');

-- dim_app_versions_photo
INSERT INTO dim_app_versions_photo (app_version, platform, release_date) VALUES
('4.0.1', 'iOS', '2023-03-15'),
('4.0.0', 'iOS', '2023-03-01'),
('3.9.5', 'Android', '2023-03-10');

-- dim_upload_status_photo
INSERT INTO dim_upload_status_photo (status_name, is_success) VALUES
('Success', TRUE),
('Failed - Network Timeout', FALSE),
('Failed - Server Error 5xx', FALSE),
('Failed - Invalid File Type', FALSE),
('Pending', FALSE); -- Upload started but not yet resolved

-- fact_photo_uploads
-- Successful upload by User X
INSERT INTO fact_photo_uploads (
    photo_id, user_key, device_key, app_version_key, upload_status_key, 
    attempt_start_timestamp, attempt_end_timestamp, upload_duration_ms, file_size_bytes, 
    photo_width_px, photo_height_px, mime_type, network_type, date_key, time_key
) VALUES (
    'px1001', 1, 1, 1, 1, 
    '2023-04-01 13:00:00', '2023-04-01 13:00:15', 15000, 3145728, 
    4032, 3024, 'image/jpeg', 'WiFi', 20230401, 130000
);

-- Failed upload (network) by User Y
INSERT INTO fact_photo_uploads (
    photo_id, user_key, device_key, app_version_key, upload_status_key, 
    attempt_start_timestamp, attempt_end_timestamp, upload_duration_ms, file_size_bytes, 
    network_type, failure_reason, date_key, time_key
) VALUES (
    NULL, 2, 2, 3, 2, 
    '2023-04-01 13:05:00', '2023-04-01 13:05:45', 45000, 2097152, 
    '4G', 'Connection timed out during transfer', 20230401, 130500
);

-- Successful upload (older app version) by User X
INSERT INTO fact_photo_uploads (
    photo_id, user_key, device_key, app_version_key, upload_status_key, 
    attempt_start_timestamp, attempt_end_timestamp, upload_duration_ms, file_size_bytes, 
    photo_width_px, photo_height_px, mime_type, network_type, date_key, time_key
) VALUES (
    'px1002', 1, 1, 2, 1, 
    '2023-04-02 13:10:00', '2023-04-02 13:10:25', 25000, 4194304, 
    1920, 1080, 'image/png', '5G', 20230402, 131000
);

-- Failed upload (server error) by User Y from Web
INSERT INTO fact_photo_uploads (
    photo_id, user_key, device_key, app_version_key, upload_status_key, 
    attempt_start_timestamp, attempt_end_timestamp, upload_duration_ms, file_size_bytes, 
    network_type, failure_reason, date_key, time_key
) VALUES (
    NULL, 2, 3, 1, 3, -- Assuming app_version_key 1 can be used for web if not versioned same way
    '2023-04-02 13:15:00', '2023-04-02 13:15:10', 10000, 1048576, 
    'WiFi', 'Server error 503 - service unavailable', 20230402, 131000 -- Re-using time_key for simplicity here
);

SELECT 'Scenario 7: Photo Upload setup complete. Tables created and sample data inserted.'; 