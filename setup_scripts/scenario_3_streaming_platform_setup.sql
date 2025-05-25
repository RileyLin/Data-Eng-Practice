-- Setup script for Scenario 3: Streaming Platform (Netflix/Hulu)
-- Revised based on q003_viewing_sessions.mmd

-- Dimension Tables
DROP TABLE IF EXISTS dim_users_streaming;
CREATE TABLE dim_users_streaming (
    user_key INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR(50) UNIQUE NOT NULL,
    email TEXT UNIQUE,
    account_created_at TEXT, -- ISO 8601 format
    subscription_tier TEXT, -- e.g., 'basic', 'standard', 'premium'
    is_trial BOOLEAN,
    subscription_end_date TEXT, -- YYYY-MM-DD
    preferred_language VARCHAR(10),
    country_code VARCHAR(2),
    is_test_account BOOLEAN DEFAULT FALSE
    -- user_preferences TEXT -- JSON object
);

DROP TABLE IF EXISTS dim_content_type_streaming;
CREATE TABLE dim_content_type_streaming (
    content_type_key INTEGER PRIMARY KEY AUTOINCREMENT,
    content_type_name TEXT UNIQUE NOT NULL, -- 'Movie', 'TV Show Episode', 'Series', 'Trailer'
    description TEXT,
    is_premium BOOLEAN DEFAULT TRUE
);

DROP TABLE IF EXISTS dim_genres_streaming; -- To store unique genre names
CREATE TABLE dim_genres_streaming (
    genre_key INTEGER PRIMARY KEY AUTOINCREMENT,
    genre_name TEXT UNIQUE NOT NULL -- e.g., 'Action', 'Comedy', 'Drama', 'Sci-Fi', 'Animation', 'Crime'
);

DROP TABLE IF EXISTS dim_content_streaming; -- Movies, TV Shows, etc.
CREATE TABLE dim_content_streaming (
    content_key INTEGER PRIMARY KEY AUTOINCREMENT,
    content_id VARCHAR(50) UNIQUE NOT NULL,
    title TEXT NOT NULL,
    content_type_key INTEGER, -- FK to dim_content_type_streaming
    duration_seconds INTEGER, -- For movies or episode length
    release_year INTEGER,
    maturity_rating TEXT, -- e.g., 'PG-13', 'R', 'G'
    language VARCHAR(10),
    has_subtitles BOOLEAN DEFAULT FALSE,
    has_dubbing BOOLEAN DEFAULT FALSE,
    episode_number INTEGER, -- For TV Show Episodes
    season_number INTEGER, -- For TV Show Episodes
    series_id VARCHAR(50), -- For TV Shows, links episodes to a series. Could also be a FK to a series table if series are distinct entities.
    added_date TEXT, -- YYYY-MM-DD when content was added to platform
    avg_rating REAL, -- Could be pre-calculated or from a ratings table
    -- content_metadata TEXT, -- JSON object
    FOREIGN KEY (content_type_key) REFERENCES dim_content_type_streaming(content_type_key)
);

-- Bridge table for content genres as per MMD (dim_content_genre)
DROP TABLE IF EXISTS bridge_content_genre_streaming;
CREATE TABLE bridge_content_genre_streaming (
    content_genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
    content_key INTEGER, -- FK to dim_content_streaming
    genre_key INTEGER,   -- FK to dim_genres_streaming
    is_primary_genre BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (content_key) REFERENCES dim_content_streaming(content_key),
    FOREIGN KEY (genre_key) REFERENCES dim_genres_streaming(genre_key),
    UNIQUE (content_key, genre_key)
);

DROP TABLE IF EXISTS dim_devices_streaming;
CREATE TABLE dim_devices_streaming (
    device_key INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id VARCHAR(100) UNIQUE NOT NULL, -- MMD uses device_id as string
    device_type TEXT, -- e.g., 'tv', 'mobile', 'tablet', 'desktop'
    manufacturer TEXT,
    model TEXT,
    os_name TEXT,
    os_version TEXT,
    browser_name TEXT,
    browser_version TEXT,
    screen_resolution_width INTEGER,
    screen_resolution_height INTEGER
);

-- dim_date and dim_time are standard
DROP TABLE IF EXISTS dim_date; 
CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY, 
    calendar_date DATE UNIQUE, -- MMD uses calendar_date
    day_of_week INTEGER, 
    day_of_month INTEGER,
    month INTEGER,
    quarter INTEGER,
    year INTEGER,
    is_weekend BOOLEAN,
    is_holiday BOOLEAN
);

DROP TABLE IF EXISTS dim_time; 
CREATE TABLE dim_time (
    time_key INTEGER PRIMARY KEY, -- e.g. HHMM format for simplicity, or full time string
    time_of_day TIME UNIQUE, -- MMD uses time_of_day
    hour_of_day INTEGER,
    minute_of_hour INTEGER,
    day_part TEXT -- 'morning', 'afternoon', 'evening', 'night' (as per MMD)
);

-- Fact Tables
DROP TABLE IF EXISTS fact_viewing_sessions_streaming;
CREATE TABLE fact_viewing_sessions_streaming (
    viewing_session_id INTEGER PRIMARY KEY AUTOINCREMENT, -- MMD uses bigint
    user_key INTEGER, -- FK to dim_users_streaming
    content_key INTEGER, -- FK to dim_content_streaming
    device_key INTEGER, -- FK to dim_devices_streaming
    session_start_timestamp TEXT NOT NULL, -- ISO 8601 format
    session_end_timestamp TEXT, -- ISO 8601 format
    view_duration_seconds INTEGER, -- Total seconds content was actively viewed
    content_duration_seconds INTEGER, -- Total length of the content item (from dim_content_streaming)
    completion_percentage REAL, -- (view_duration_seconds / content_duration_seconds) * 100
    pause_count INTEGER DEFAULT 0,
    seek_count INTEGER DEFAULT 0,
    last_pause_timestamp TEXT, -- ISO 8601, if applicable
    watch_progress_seconds INTEGER, -- Furthest point reached in the content
    is_completed BOOLEAN DEFAULT FALSE, -- True if completion_percentage is high (e.g. >95%)
    date_key INTEGER, -- FK to dim_date (date of session_start_timestamp)
    time_key INTEGER, -- FK to dim_time (time of session_start_timestamp)
    session_guid TEXT UNIQUE, -- MMD has session_id (string)
    client_version TEXT,
    FOREIGN KEY (user_key) REFERENCES dim_users_streaming(user_key),
    FOREIGN KEY (content_key) REFERENCES dim_content_streaming(content_key),
    FOREIGN KEY (device_key) REFERENCES dim_devices_streaming(device_key),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (time_key) REFERENCES dim_time(time_key)
);

DROP TABLE IF EXISTS fact_ratings_streaming; -- Kept for Python challenge relevance
CREATE TABLE fact_ratings_streaming (
    rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_key INTEGER, 
    content_key INTEGER, 
    rating INTEGER CHECK (rating >= 1 AND rating <= 5), 
    rating_timestamp TEXT, 
    date_key INTEGER,
    time_key INTEGER,
    FOREIGN KEY (user_key) REFERENCES dim_users_streaming(user_key),
    FOREIGN KEY (content_key) REFERENCES dim_content_streaming(content_key),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (time_key) REFERENCES dim_time(time_key)
);

-- Sample Data Insertion

-- dim_date (Example for Jan 10-11, 2023)
INSERT INTO dim_date (date_key, calendar_date, day_of_week, day_of_month, month, quarter, year, is_weekend, is_holiday) VALUES
(20230110, '2023-01-10', 3, 10, 1, 1, 2023, FALSE, FALSE),
(20230111, '2023-01-11', 4, 11, 1, 1, 2023, FALSE, FALSE);

-- dim_time (Examples)
INSERT INTO dim_time (time_key, time_of_day, hour_of_day, minute_of_hour, day_part) VALUES
(1800, '18:00:00', 18, 0, 'evening'),
(1930, '19:30:00', 19, 30, 'evening'),
(2000, '20:00:00', 20, 0, 'evening'),
(2045, '20:45:00', 20, 45, 'evening'),
(2250, '22:50:00', 22, 50, 'night'),
(1942, '19:42:00', 19, 42, 'evening'),
(2100, '21:00:00', 21, 00, 'evening'),
(1943, '19:43:00', 19, 43, 'evening'),
(2101, '21:01:00', 21, 01, 'evening'),
(1946, '19:46:00', 19, 46, 'evening'),
(2255, '22:55:00', 22, 55, 'night'),
(2251, '22:51:00', 22, 51, 'night');


-- dim_users_streaming
INSERT INTO dim_users_streaming (user_id, email, account_created_at, subscription_tier, country_code) VALUES
('user001', 'pro@example.com', '2022-01-15 10:00:00', 'premium', 'US'),
('user002', 'casual@example.com', '2022-06-20 12:00:00', 'basic', 'CA'),
('user003', 'buff@example.com', '2021-11-01 08:00:00', 'standard', 'GB');

-- dim_content_type_streaming
INSERT INTO dim_content_type_streaming (content_type_name, description) VALUES
('Movie', 'Feature-length film'),
('TV Show Episode', 'Single episode of a television series'),
('Series', 'A collection of TV Show Episodes');

-- dim_genres_streaming
INSERT INTO dim_genres_streaming (genre_name) VALUES ('Sci-Fi'), ('Comedy'), ('Action'), ('Animation'), ('Crime'), ('Drama');

-- dim_content_streaming
INSERT INTO dim_content_streaming (content_id, title, content_type_key, duration_seconds, release_year, maturity_rating, series_id, season_number, episode_number) VALUES
('mov001', 'Galaxy Quest', 1, 102*60, 1999, 'PG', NULL, NULL, NULL),                -- Sci-Fi, Comedy
('mov002', 'The Matrix', 1, 136*60, 1999, 'R', NULL, NULL, NULL),                 -- Sci-Fi, Action
('mov003', 'Inception', 1, 148*60, 2010, 'PG-13', NULL, NULL, NULL),              -- Sci-Fi, Action, Drama
('mov004', 'Spirited Away', 1, 125*60, 2001, 'PG', NULL, NULL, NULL),             -- Animation, Drama
('mov005', 'Pulp Fiction', 1, 154*60, 1994, 'R', NULL, NULL, NULL);                -- Crime, Drama

-- bridge_content_genre_streaming
-- Galaxy Quest (content_key 1): Sci-Fi (key 1), Comedy (key 2)
INSERT INTO bridge_content_genre_streaming (content_key, genre_key, is_primary_genre) VALUES (1, 1, TRUE), (1, 2, FALSE);
-- The Matrix (content_key 2): Sci-Fi (key 1), Action (key 3)
INSERT INTO bridge_content_genre_streaming (content_key, genre_key, is_primary_genre) VALUES (2, 1, TRUE), (2, 3, FALSE);
-- Inception (content_key 3): Sci-Fi (key 1), Action (key 3), Drama (key 6)
INSERT INTO bridge_content_genre_streaming (content_key, genre_key, is_primary_genre) VALUES (3, 1, TRUE), (3, 3, FALSE), (3, 6, FALSE);
-- Spirited Away (content_key 4): Animation (key 4), Drama (key 6)
INSERT INTO bridge_content_genre_streaming (content_key, genre_key, is_primary_genre) VALUES (4, 4, TRUE), (4, 6, FALSE);
-- Pulp Fiction (content_key 5): Crime (key 5), Drama (key 6)
INSERT INTO bridge_content_genre_streaming (content_key, genre_key, is_primary_genre) VALUES (5, 5, TRUE), (5, 6, FALSE);


-- dim_devices_streaming
INSERT INTO dim_devices_streaming (device_id, device_type, manufacturer, os_name) VALUES
('tv123', 'tv', 'Samsung', 'Tizen'),
('mob456', 'mobile', 'Google', 'Android'),
('web789', 'desktop', 'N/A', 'Windows'); -- Web could be desktop or other

-- fact_viewing_sessions_streaming
-- User1 watches Galaxy Quest (content_key 1) fully
INSERT INTO fact_viewing_sessions_streaming (user_key, content_key, device_key, session_start_timestamp, session_end_timestamp, view_duration_seconds, content_duration_seconds, completion_percentage, is_completed, date_key, time_key, session_guid, client_version, watch_progress_seconds) VALUES
(1, 1, 1, '2023-01-10 18:00:00', '2023-01-10 19:42:00', 102*60, 102*60, 100.0, TRUE, 20230110, 1800, 'sess_guid_1', '1.2.3', 102*60);

-- User2 watches The Matrix (content_key 2) partially
INSERT INTO fact_viewing_sessions_streaming (user_key, content_key, device_key, session_start_timestamp, session_end_timestamp, view_duration_seconds, content_duration_seconds, completion_percentage, is_completed, date_key, time_key, session_guid, client_version, pause_count, watch_progress_seconds) VALUES
(2, 2, 2, '2023-01-10 20:00:00', '2023-01-10 21:00:00', 55*60, 136*60, (55.0/136.0)*100, FALSE, 20230110, 2000, 'sess_guid_2', 'app_v2', 2, 55*60);

-- User1 watches Inception (content_key 3), starts it
INSERT INTO fact_viewing_sessions_streaming (user_key, content_key, device_key, session_start_timestamp, session_end_timestamp, view_duration_seconds, content_duration_seconds, completion_percentage, is_completed, date_key, time_key, session_guid, client_version, watch_progress_seconds) VALUES
(1, 3, 3, '2023-01-11 19:30:00', '2023-01-11 19:45:00', 15*60, 148*60, (15.0/148.0)*100, FALSE, 20230111, 1930, 'sess_guid_3', 'web_client_101', 15*60);

-- User3 watches Spirited Away (content_key 4) fully
INSERT INTO fact_viewing_sessions_streaming (user_key, content_key, device_key, session_start_timestamp, session_end_timestamp, view_duration_seconds, content_duration_seconds, completion_percentage, is_completed, date_key, time_key, session_guid, client_version, watch_progress_seconds) VALUES
(3, 4, 1, '2023-01-11 20:45:00', '2023-01-11 22:50:00', 125*60, 125*60, 100.0, TRUE, 20230111, 2045, 'sess_guid_4', '1.3.0', 125*60);

-- fact_ratings_streaming (kept for python challenge q005_average_rating_category.py, q006_top_n_movies.py, q007_average_movie_ratings.py)
INSERT INTO fact_ratings_streaming (user_key, content_key, rating, rating_timestamp, date_key, time_key) VALUES
(1, 1, 5, '2023-01-10 19:43:00', 20230110, 1943),
(2, 2, 4, '2023-01-10 21:01:00', 20230110, 2101),
(1, 3, 5, '2023-01-11 19:46:00', 20230111, 1946),
(3, 1, 4, '2023-01-11 22:55:00', 20230111, 2255), 
(3, 4, 5, '2023-01-11 22:51:00', 20230111, 2251);

SELECT 'Scenario 3: Streaming Platform setup (revised) complete. Tables created and sample data inserted.'; 