-- Setup script for Scenario 2: Short Video (TikTok/Reels) - Sharing Focus

-- Dimension Tables
DROP TABLE IF EXISTS dim_users_shortvideo;
CREATE TABLE dim_users_shortvideo (
    user_key INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR(50) UNIQUE NOT NULL,
    username TEXT,
    created_at TEXT, -- ISO 8601 format
    user_type TEXT, -- e.g., 'creator', 'viewer'
    is_internal BOOLEAN DEFAULT FALSE
);

DROP TABLE IF EXISTS dim_posts_shortvideo;
CREATE TABLE dim_posts_shortvideo (
    post_key INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id VARCHAR(50) UNIQUE NOT NULL, -- Public facing ID if different from post_key
    creator_user_key INTEGER, -- FK to dim_users_shortvideo
    original_post_key INTEGER, -- FK to dim_posts_shortvideo (self-reference for the original post)
    parent_post_key INTEGER, -- FK to dim_posts_shortvideo (the post that was shared to create this one)
    share_depth_level INTEGER DEFAULT 0,
    created_timestamp TEXT, -- ISO 8601 format
    is_original BOOLEAN DEFAULT TRUE,
    content_text TEXT, -- Simplified content
    video_url TEXT,
    FOREIGN KEY (creator_user_key) REFERENCES dim_users_shortvideo(user_key),
    FOREIGN KEY (original_post_key) REFERENCES dim_posts_shortvideo(post_key),
    FOREIGN KEY (parent_post_key) REFERENCES dim_posts_shortvideo(post_key)
);

DROP TABLE IF EXISTS dim_engagement_types_shortvideo;
CREATE TABLE dim_engagement_types_shortvideo (
    engagement_type_key INTEGER PRIMARY KEY AUTOINCREMENT,
    engagement_type_name TEXT UNIQUE NOT NULL, -- e.g., 'view', 'like', 'comment', 'share', 'follow'
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE
);

-- Re-using dim_date and dim_time from Scenario 1 for consistency, or define them if run standalone.
-- For this script, we assume they might exist or can be created if needed.
-- If you created them in scenario_1_ridesharing_setup.sql, you might not need to recreate.

DROP TABLE IF EXISTS dim_date; -- Included for standalone execution
CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY, -- YYYYMMDD format
    full_date DATE,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    day_of_month INTEGER,
    day_of_week INTEGER, -- 1 (Sunday) to 7 (Saturday)
    week_of_year INTEGER,
    is_weekend BOOLEAN
);

DROP TABLE IF EXISTS dim_time; -- Included for standalone execution
CREATE TABLE dim_time (
    time_key INTEGER PRIMARY KEY, -- HHMMSS format
    full_time TIME,
    hour INTEGER,
    minute INTEGER,
    second INTEGER,
    am_pm TEXT
);


-- Fact Table
DROP TABLE IF EXISTS fact_engagement_events_shortvideo;
CREATE TABLE fact_engagement_events_shortvideo (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_key INTEGER, -- FK to dim_users_shortvideo (user performing the engagement)
    post_key INTEGER, -- FK to dim_posts_shortvideo (the post being engaged with)
    engagement_type_key INTEGER, -- FK to dim_engagement_types_shortvideo
    event_timestamp TEXT, -- ISO 8601 format
    event_date_key INTEGER, -- FK to dim_date
    event_time_key INTEGER, -- FK to dim_time
    event_metadata TEXT, -- JSON stored as TEXT for simplicity in SQLite
    FOREIGN KEY (user_key) REFERENCES dim_users_shortvideo(user_key),
    FOREIGN KEY (post_key) REFERENCES dim_posts_shortvideo(post_key),
    FOREIGN KEY (engagement_type_key) REFERENCES dim_engagement_types_shortvideo(engagement_type_key),
    FOREIGN KEY (event_date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (event_time_key) REFERENCES dim_time(time_key)
);

-- Sample Data Insertion

-- dim_date (Example for Jan 1-3, 2023)
INSERT INTO dim_date (date_key, full_date, year, quarter, month, day_of_month, day_of_week, week_of_year, is_weekend) VALUES
(20230101, '2023-01-01', 2023, 1, 1, 1, 1, 1, TRUE),
(20230102, '2023-01-02', 2023, 1, 1, 2, 2, 1, FALSE),
(20230103, '2023-01-03', 2023, 1, 1, 3, 3, 1, FALSE);

-- dim_time (Examples)
INSERT INTO dim_time (time_key, full_time, hour, minute, second, am_pm) VALUES
(100000, '10:00:00', 10, 0, 0, 'AM'),
(100500, '10:05:00', 10, 5, 0, 'AM'),
(101000, '10:10:00', 10, 10, 0, 'AM'),
(113000, '11:30:00', 11, 30, 0, 'AM'),
(113200, '11:32:00', 11, 32, 0, 'AM');

-- dim_users_shortvideo
INSERT INTO dim_users_shortvideo (user_id, username, created_at, user_type, is_internal) VALUES
('userA', 'AliceCreator', '2023-01-01 08:00:00', 'creator', FALSE),
('userB', 'BobViewer', '2023-01-01 08:05:00', 'viewer', FALSE),
('userC', 'CharlieSharer', '2023-01-01 08:10:00', 'viewer', FALSE),
('userD', 'DavidInternal', '2023-01-01 08:15:00', 'viewer', TRUE),
('userE', 'EvaEngager', '2023-01-01 08:20:00', 'creator', FALSE);

-- dim_engagement_types_shortvideo
INSERT INTO dim_engagement_types_shortvideo (engagement_type_name, description) VALUES
('view', 'User viewed the post'),
('like', 'User liked the post'),
('comment', 'User commented on the post'),
('share', 'User shared the post');

-- dim_posts_shortvideo
-- Original Post P1 by userA (AliceCreator - user_key 1)
INSERT INTO dim_posts_shortvideo (post_id, creator_user_key, original_post_key, parent_post_key, share_depth_level, created_timestamp, is_original, content_text, video_url) VALUES
('P1', 1, NULL, NULL, 0, '2023-01-01 10:00:00', TRUE, 'My first amazing video!', 'http://example.com/v/p1.mp4');
-- P1 has post_key = 1 (implicitly due to AUTOINCREMENT)
UPDATE dim_posts_shortvideo SET original_post_key = 1 WHERE post_key = 1;

-- Original Post P2 by userE (EvaEngager - user_key 5)
INSERT INTO dim_posts_shortvideo (post_id, creator_user_key, original_post_key, parent_post_key, share_depth_level, created_timestamp, is_original, content_text, video_url) VALUES
('P2', 5, NULL, NULL, 0, '2023-01-02 11:30:00', TRUE, 'Travel highlights 2023', 'http://example.com/v/p2.mp4');
-- P2 has post_key = 2
UPDATE dim_posts_shortvideo SET original_post_key = 2 WHERE post_key = 2;

-- Share: userC (CharlieSharer - user_key 3) shares P1. This creates a new post P1_S1.
-- P1_S1 is created by userC, original is P1 (post_key 1), parent is P1 (post_key 1)
INSERT INTO dim_posts_shortvideo (post_id, creator_user_key, original_post_key, parent_post_key, share_depth_level, created_timestamp, is_original, content_text, video_url) VALUES
('P1_S1', 3, 1, 1, 1, '2023-01-01 10:05:00', FALSE, 'Wow, check this out! #amazing (Shared from P1)', NULL);
-- P1_S1 has post_key = 3

-- Share: userB (BobViewer - user_key 2) shares P1_S1 (post_key 3). This creates P1_S2.
-- P1_S2 is created by userB, original is P1 (post_key 1), parent is P1_S1 (post_key 3)
INSERT INTO dim_posts_shortvideo (post_id, creator_user_key, original_post_key, parent_post_key, share_depth_level, created_timestamp, is_original, content_text, video_url) VALUES
('P1_S2', 2, 1, 3, 2, '2023-01-01 10:10:00', FALSE, 'You gotta see this! (Shared from P1_S1)', NULL);
-- P1_S2 has post_key = 4


-- fact_engagement_events_shortvideo
-- Views for P1 (post_key 1)
INSERT INTO fact_engagement_events_shortvideo (user_key, post_key, engagement_type_key, event_timestamp, event_date_key, event_time_key, event_metadata) VALUES
(2, 1, 1, '2023-01-01 10:00:00', 20230101, 100000, '{ \"view_duration_ms\": 15000 }'), -- Bob views P1
(3, 1, 1, '2023-01-01 10:01:00', 20230101, 100000, '{ \"view_duration_ms\": 30000 }'); -- Charlie views P1

-- Like for P1 by Bob (user_key 2)
INSERT INTO fact_engagement_events_shortvideo (user_key, post_key, engagement_type_key, event_timestamp, event_date_key, event_time_key) VALUES
(2, 1, 2, '2023-01-01 10:02:00', 20230101, 100000);

-- Charlie (user_key 3) shares P1 (post_key 1) - this is the action of sharing, creating P1_S1 (post_key 3)
INSERT INTO fact_engagement_events_shortvideo (user_key, post_key, engagement_type_key, event_timestamp, event_date_key, event_time_key, event_metadata) VALUES
(3, 1, 4, '2023-01-01 10:05:00', 20230101, 100500, '{ \"shared_to_post_id\": "P1_S1", \"shared_to_post_key\": 3 }');

-- Eva (user_key 5) views the shared post P1_S1 (post_key 3)
INSERT INTO fact_engagement_events_shortvideo (user_key, post_key, engagement_type_key, event_timestamp, event_date_key, event_time_key, event_metadata) VALUES
(5, 3, 1, '2023-01-01 10:06:00', 20230101, 100500, '{ \"view_duration_ms\": 12000 }');

-- Eva (user_key 5) likes the shared post P1_S1 (post_key 3)
INSERT INTO fact_engagement_events_shortvideo (user_key, post_key, engagement_type_key, event_timestamp, event_date_key, event_time_key) VALUES
(5, 3, 2, '2023-01-01 10:07:00', 20230101, 100500);

-- Bob (user_key 2) shares P1_S1 (post_key 3) - this is the action of sharing, creating P1_S2 (post_key 4)
INSERT INTO fact_engagement_events_shortvideo (user_key, post_key, engagement_type_key, event_timestamp, event_date_key, event_time_key, event_metadata) VALUES
(2, 3, 4, '2023-01-01 10:10:00', 20230101, 101000, '{ \"shared_to_post_id\": "P1_S2", \"shared_to_post_key\": 4 }');

-- Views for P2 (post_key 2)
INSERT INTO fact_engagement_events_shortvideo (user_key, post_key, engagement_type_key, event_timestamp, event_date_key, event_time_key, event_metadata) VALUES
(1, 2, 1, '2023-01-02 11:30:00', 20230102, 113000, '{ \"view_duration_ms\": 25000 }'), -- Alice views P2
(2, 2, 1, '2023-01-02 11:32:00', 20230102, 113200, '{ \"view_duration_ms\": 22000 }'); -- Bob views P2

-- Alice (user_key 1) likes P2 (post_key 2)
INSERT INTO fact_engagement_events_shortvideo (user_key, post_key, engagement_type_key, event_timestamp, event_date_key, event_time_key) VALUES
(1, 2, 2, '2023-01-02 11:33:00', 20230102, 113200);

-- Internal user (userD - user_key 4) views P1 - should be excludable in queries via dim_users_shortvideo.is_internal
INSERT INTO fact_engagement_events_shortvideo (user_key, post_key, engagement_type_key, event_timestamp, event_date_key, event_time_key, event_metadata) VALUES
(4, 1, 1, '2023-01-03 09:00:00', 20230103, 090000, '{ \"view_duration_ms\": 5000 }');

SELECT 'Scenario 2: Short Video setup complete. Tables created and sample data inserted.'; 