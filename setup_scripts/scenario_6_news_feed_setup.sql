-- Setup script for Scenario 6: News Feed

-- Dimension Tables
DROP TABLE IF EXISTS dim_users_feed;
CREATE TABLE dim_users_feed (
    user_key INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR(50) UNIQUE NOT NULL,
    username TEXT,
    registration_date TEXT -- ISO 8601 format
    -- Add other relevant user attributes like demographics, preferences if needed
);

DROP TABLE IF EXISTS dim_topics_feed;
CREATE TABLE dim_topics_feed (
    topic_key INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_name TEXT UNIQUE NOT NULL, -- e.g., 'Technology', 'Sports', 'Politics', 'Entertainment'
    topic_category TEXT
);

DROP TABLE IF EXISTS dim_publishers_feed;
CREATE TABLE dim_publishers_feed (
    publisher_key INTEGER PRIMARY KEY AUTOINCREMENT,
    publisher_name TEXT UNIQUE NOT NULL, -- e.g., 'Tech News Daily', 'Sports Illustrated', 'Global Times'
    publisher_category TEXT -- e.g., 'News Outlet', 'Blog', 'Magazine'
);

DROP TABLE IF EXISTS dim_content_items_feed;
CREATE TABLE dim_content_items_feed (
    content_item_key INTEGER PRIMARY KEY AUTOINCREMENT,
    content_id VARCHAR(50) UNIQUE NOT NULL,
    title TEXT NOT NULL,
    content_type TEXT, -- e.g., 'article', 'video', 'short_post'
    publisher_key INTEGER, -- FK to dim_publishers_feed
    topic_key INTEGER,     -- FK to dim_topics_feed
    created_timestamp TEXT, -- ISO 8601 format for when the content was published
    url TEXT, -- URL to the content if applicable
    tags TEXT -- Comma-separated tags, or use a separate bridge table for many-to-many
);

DROP TABLE IF EXISTS dim_event_types_feed;
CREATE TABLE dim_event_types_feed (
    event_type_key INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT UNIQUE NOT NULL, -- e.g., 'impression', 'click', 'view', 'like', 'share', 'comment', 'scroll_deep'
    event_category TEXT -- e.g., 'Exposure', 'Engagement', 'Navigation'
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
DROP TABLE IF EXISTS fact_feed_events_feed;
CREATE TABLE fact_feed_events_feed (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_key INTEGER, -- FK to dim_users_feed
    content_item_key INTEGER, -- FK to dim_content_items_feed
    event_type_key INTEGER, -- FK to dim_event_types_feed
    event_timestamp TEXT NOT NULL, -- ISO 8601 format
    date_key INTEGER, -- FK to dim_date
    time_key INTEGER, -- FK to dim_time
    session_id VARCHAR(100), -- To group events within a user session
    position_in_feed INTEGER, -- Where the item appeared in the feed (e.g., 1, 2, 3...)
    view_time_ms INTEGER, -- For 'view' events, how long it was viewed
    visibility_percent REAL, -- For 'impression' or 'view' events, % of item visible
    is_sponsored BOOLEAN DEFAULT FALSE,
    metadata_json TEXT, -- For any other event-specific details
    FOREIGN KEY (user_key) REFERENCES dim_users_feed(user_key),
    FOREIGN KEY (content_item_key) REFERENCES dim_content_items_feed(content_item_key),
    FOREIGN KEY (event_type_key) REFERENCES dim_event_types_feed(event_type_key),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (time_key) REFERENCES dim_time(time_key)
);

-- Sample Data Insertion

-- dim_date (Example for Mar 1-2, 2023)
INSERT INTO dim_date (date_key, full_date, year, quarter, month, day_of_month, day_of_week, week_of_year, is_weekend) VALUES
(20230301, '2023-03-01', 2023, 1, 3, 1, 4, 9, FALSE),
(20230302, '2023-03-02', 2023, 1, 3, 2, 5, 9, FALSE);

-- dim_time (Examples)
INSERT INTO dim_time (time_key, full_time, hour, minute, second, am_pm) VALUES
(110000, '11:00:00', 11, 0, 0, 'AM'),
(110500, '11:05:00', 11, 5, 0, 'AM'),
(111000, '11:10:00', 11, 10, 0, 'AM');

-- dim_users_feed
INSERT INTO dim_users_feed (user_id, username, registration_date) VALUES
('feed_user_A', 'AliceFeedReader', '2023-01-10'),
('feed_user_B', 'BobScroller', '2023-02-15');

-- dim_topics_feed
INSERT INTO dim_topics_feed (topic_name, topic_category) VALUES
('Technology', 'Science & Tech'),
('World News', 'News'),
('Healthy Living', 'Lifestyle');

-- dim_publishers_feed
INSERT INTO dim_publishers_feed (publisher_name, publisher_category) VALUES
('Tech Chronicle', 'Tech Blog'),
('Global News Agency', 'News Wire'),
('Wellness Today', 'Magazine');

-- dim_content_items_feed
INSERT INTO dim_content_items_feed (content_id, title, content_type, publisher_key, topic_key, created_timestamp, url, tags) VALUES
('C001', 'New AI Breakthroughs', 'article', 1, 1, '2023-03-01 09:00:00', 'http://example.com/ai-breakthroughs', 'AI,Machine Learning,Innovation'),
('C002', 'Global Summit Highlights', 'article', 2, 2, '2023-03-01 10:00:00', 'http://example.com/global-summit', 'Politics,World Affairs'),
('C003', 'Top 5 Healthy Recipes', 'video', 3, 3, '2023-03-01 11:00:00', 'http://example.com/healthy-recipes', 'Food,Health,Video');

-- dim_event_types_feed
INSERT INTO dim_event_types_feed (event_name, event_category) VALUES
('impression', 'Exposure'),
('click', 'Engagement'),
('view_start', 'View'),         -- When user starts viewing (e.g. >50% visible for >1s)
('view_complete', 'View'),    -- When user views a significant portion (e.g. 80% or full duration for video)
('like', 'Engagement'),
('share_intent', 'Engagement'); -- User clicked share button

-- fact_feed_events_feed
-- User A session
INSERT INTO fact_feed_events_feed (user_key, content_item_key, event_type_key, event_timestamp, date_key, time_key, session_id, position_in_feed, visibility_percent, is_sponsored) VALUES
(1, 1, 1, '2023-03-01 11:00:00', 20230301, 110000, 'sessA_01', 1, 100.0, FALSE), -- Impression C001
(1, 2, 1, '2023-03-01 11:00:05', 20230301, 110000, 'sessA_01', 2, 80.0, TRUE),  -- Impression C002 (sponsored)
(1, 1, 3, '2023-03-01 11:00:10', 20230301, 110000, 'sessA_01', 1, 100.0, FALSE), -- View Start C001
(1, 1, 2, '2023-03-01 11:00:15', 20230301, 110000, 'sessA_01', 1, NULL, FALSE),   -- Click C001
(1, 1, 4, '2023-03-01 11:05:00', 20230301, 110500, 'sessA_01', 1, NULL, FALSE),   -- View Complete C001 (read for 5 mins)
(1, 2, 3, '2023-03-01 11:05:05', 20230301, 110500, 'sessA_01', 2, 90.0, TRUE);   -- View Start C002

-- User B session
INSERT INTO fact_feed_events_feed (user_key, content_item_key, event_type_key, event_timestamp, date_key, time_key, session_id, position_in_feed, visibility_percent) VALUES
(2, 3, 1, '2023-03-02 11:10:00', 20230302, 111000, 'sessB_01', 1, 100.0), -- Impression C003
(2, 1, 1, '2023-03-02 11:10:05', 20230302, 111000, 'sessB_01', 2, 70.0),  -- Impression C001
(2, 3, 3, '2023-03-02 11:10:10', 20230302, 111000, 'sessB_01', 1, 100.0), -- View Start C003
(2, 3, 5, '2023-03-02 11:10:45', 20230302, 111000, 'sessB_01', 1, NULL);   -- Like C003

SELECT 'Scenario 6: News Feed setup complete. Tables created and sample data inserted.'; 