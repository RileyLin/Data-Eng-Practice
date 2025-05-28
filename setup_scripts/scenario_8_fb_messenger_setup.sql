-- Setup script for Scenario 8: FB Messenger

-- Dimension Tables
DROP TABLE IF EXISTS dim_users_msg;
CREATE TABLE dim_users_msg (
    user_key INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR(50) UNIQUE NOT NULL,
    username TEXT,
    created_timestamp TEXT, -- ISO 8601 format
    account_status TEXT DEFAULT 'active' -- e.g., 'active', 'inactive', 'suspended'
);

DROP TABLE IF EXISTS dim_conversation_types_msg;
CREATE TABLE dim_conversation_types_msg (
    conversation_type_key INTEGER PRIMARY KEY AUTOINCREMENT,
    type_name TEXT UNIQUE NOT NULL, -- e.g., 'one_to_one', 'group_chat', 'channel_broadcast'
    description TEXT,
    supports_group BOOLEAN DEFAULT FALSE
);

DROP TABLE IF EXISTS dim_conversations_msg;
CREATE TABLE dim_conversations_msg (
    conversation_key INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id VARCHAR(50) UNIQUE NOT NULL,
    conversation_type_key INTEGER, -- FK to dim_conversation_types_msg
    created_timestamp TEXT, -- ISO 8601 format
    last_activity_timestamp TEXT, -- ISO 8601 format
    conversation_name TEXT, -- For group chats
    is_encrypted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (conversation_type_key) REFERENCES dim_conversation_types_msg(conversation_type_key)
);

DROP TABLE IF EXISTS dim_message_types_msg;
CREATE TABLE dim_message_types_msg (
    message_type_key INTEGER PRIMARY KEY AUTOINCREMENT,
    type_name TEXT UNIQUE NOT NULL, -- e.g., 'text', 'image', 'video', 'audio', 'sticker', 'reaction', 'system'
    category TEXT, -- e.g., 'user_generated', 'system_notification'
    contains_media BOOLEAN DEFAULT FALSE
);

DROP TABLE IF EXISTS dim_message_status_msg;
CREATE TABLE dim_message_status_msg (
    message_status_key INTEGER PRIMARY KEY AUTOINCREMENT,
    status_name TEXT UNIQUE NOT NULL, -- e.g., 'sent', 'delivered_to_server', 'delivered_to_recipient', 'read', 'failed_to_send'
    description TEXT
);

DROP TABLE IF EXISTS dim_devices_msg; -- Added based on the model
CREATE TABLE dim_devices_msg (
    device_key INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id VARCHAR(100) UNIQUE NOT NULL,
    device_type TEXT, -- e.g., 'Mobile', 'Web', 'Desktop'
    platform TEXT,    -- e.g., 'iOS', 'Android', 'Windows', 'MacOS', 'Chrome'
    app_version TEXT
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

-- Bridge Table
DROP TABLE IF EXISTS bridge_conversation_participants_msg;
CREATE TABLE bridge_conversation_participants_msg (
    participation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_key INTEGER, -- FK to dim_conversations_msg
    user_key INTEGER, -- FK to dim_users_msg
    joined_timestamp TEXT, -- ISO 8601 format
    role_in_conversation TEXT, -- e.g., 'participant', 'admin' (for groups)
    notifications_enabled BOOLEAN DEFAULT TRUE,
    is_active_participant BOOLEAN DEFAULT TRUE, -- If they left the conversation
    FOREIGN KEY (conversation_key) REFERENCES dim_conversations_msg(conversation_key),
    FOREIGN KEY (user_key) REFERENCES dim_users_msg(user_key),
    UNIQUE (conversation_key, user_key)
);

-- Fact Table
DROP TABLE IF EXISTS fact_messages_msg;
CREATE TABLE fact_messages_msg (
    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_guid VARCHAR(50) UNIQUE NOT NULL, -- A unique ID for the message itself
    conversation_key INTEGER, -- FK to dim_conversations_msg
    sender_user_key INTEGER, -- FK to dim_users_msg
    message_type_key INTEGER, -- FK to dim_message_types_msg
    message_status_key INTEGER, -- FK to dim_message_status_msg
    device_key INTEGER, -- FK to dim_devices_msg
    message_timestamp TEXT NOT NULL, -- Client-side timestamp when message was sent/created
    server_received_timestamp TEXT, -- Server-side timestamp
    date_key INTEGER, -- FK to dim_date (based on message_timestamp)
    time_key INTEGER, -- FK to dim_time (based on message_timestamp)
    character_count INTEGER,
    media_count INTEGER DEFAULT 0, -- Number of media items (photos, videos)
    is_reply BOOLEAN DEFAULT FALSE,
    replied_to_message_guid VARCHAR(50), -- GUID of the message being replied to
    platform_specific_payload TEXT, -- For fields like 'text_content' from q010 (SQL generation question)
    FOREIGN KEY (conversation_key) REFERENCES dim_conversations_msg(conversation_key),
    FOREIGN KEY (sender_user_key) REFERENCES dim_users_msg(user_key),
    FOREIGN KEY (message_type_key) REFERENCES dim_message_types_msg(message_type_key),
    FOREIGN KEY (message_status_key) REFERENCES dim_message_status_msg(message_status_key),
    FOREIGN KEY (device_key) REFERENCES dim_devices_msg(device_key),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (time_key) REFERENCES dim_time(time_key)
);

-- Sample Data Insertion

-- dim_date (Example for May 1-2, 2023)
INSERT INTO dim_date (date_key, full_date, year, quarter, month, day_of_month, day_of_week, week_of_year, is_weekend) VALUES
(20230501, '2023-05-01', 2023, 2, 5, 1, 2, 18, FALSE),
(20230502, '2023-05-02', 2023, 2, 5, 2, 3, 18, FALSE);

-- dim_time (Examples)
INSERT INTO dim_time (time_key, full_time, hour, minute, second, am_pm) VALUES
(150000, '15:00:00', 15, 0, 0, 'PM'),
(150230, '15:02:30', 15, 2, 30, 'PM'),
(161000, '16:10:00', 16, 10, 0, 'PM');

-- dim_users_msg
INSERT INTO dim_users_msg (user_id, username, created_timestamp) VALUES
('msg_user_1', 'ChattyCathy', '2023-01-01 12:00:00'),
('msg_user_2', 'SilentSam', '2023-02-10 10:00:00'),
('msg_user_3', 'GroupGreg', '2023-03-15 09:00:00');

-- dim_conversation_types_msg
INSERT INTO dim_conversation_types_msg (type_name, description, supports_group) VALUES
('one_to_one', 'Direct message between two users', FALSE),
('group_chat', 'Chat involving three or more users', TRUE);

-- dim_conversations_msg
INSERT INTO dim_conversations_msg (conversation_id, conversation_type_key, created_timestamp, last_activity_timestamp, conversation_name) VALUES
('convo_1_2', 1, '2023-05-01 14:55:00', '2023-05-01 15:03:00', NULL), -- Cathy and Sam
('convo_group_xyz', 2, '2023-05-02 10:00:00', '2023-05-02 16:11:00', 'Project Team Alpha'); -- Cathy, Sam, Greg

-- bridge_conversation_participants_msg
INSERT INTO bridge_conversation_participants_msg (conversation_key, user_key, joined_timestamp, role_in_conversation) VALUES
(1, 1, '2023-05-01 14:55:00', 'participant'), -- Cathy in convo_1_2
(1, 2, '2023-05-01 14:55:00', 'participant'), -- Sam in convo_1_2
(2, 1, '2023-05-02 10:00:00', 'admin'),       -- Cathy in convo_group_xyz (admin)
(2, 2, '2023-05-02 10:00:00', 'participant'), -- Sam in convo_group_xyz
(2, 3, '2023-05-02 10:01:00', 'participant'); -- Greg in convo_group_xyz

-- dim_message_types_msg
INSERT INTO dim_message_types_msg (type_name, category, contains_media) VALUES
('text', 'user_generated', FALSE),
('image', 'user_generated', TRUE),
('reaction', 'user_generated', FALSE),
('member_joined', 'system_notification', FALSE);

-- dim_message_status_msg
INSERT INTO dim_message_status_msg (status_name, description) VALUES
('sent', 'Message sent from client'),
('delivered_server', 'Message received by server'),
('delivered_recipient', 'Message delivered to recipient client'),
('read', 'Recipient has read the message'),
('failed', 'Message failed to send');

-- dim_devices_msg
INSERT INTO dim_devices_msg (device_id, device_type, platform, app_version) VALUES
('ios_cathy_1', 'Mobile', 'iOS', '10.5.1'),
('android_sam_1', 'Mobile', 'Android', '10.4.0'),
('web_greg_1', 'Web', 'Chrome', '112.0.5615.137');

-- fact_messages_msg
-- Cathy sends a text to Sam in convo_1_2
INSERT INTO fact_messages_msg (message_guid, conversation_key, sender_user_key, message_type_key, message_status_key, device_key, message_timestamp, server_received_timestamp, date_key, time_key, character_count, platform_specific_payload) VALUES
('msg_guid_001', 1, 1, 1, 4, 1, '2023-05-01 15:00:00', '2023-05-01 15:00:01', 20230501, 150000, 25, '{"text_content": "Hello Sam! How are you?"}');

-- Sam replies to Cathy in convo_1_2
INSERT INTO fact_messages_msg (message_guid, conversation_key, sender_user_key, message_type_key, message_status_key, device_key, message_timestamp, server_received_timestamp, date_key, time_key, character_count, is_reply, replied_to_message_guid, platform_specific_payload) VALUES
('msg_guid_002', 1, 2, 1, 3, 2, '2023-05-01 15:02:30', '2023-05-01 15:02:31', 20230501, 150230, 18, TRUE, 'msg_guid_001', '{"text_content": "I am good, Cathy!"}');

-- Cathy sends an image in group chat convo_group_xyz
INSERT INTO fact_messages_msg (message_guid, conversation_key, sender_user_key, message_type_key, message_status_key, device_key, message_timestamp, server_received_timestamp, date_key, time_key, media_count, platform_specific_payload) VALUES
('msg_guid_003', 2, 1, 2, 2, 1, '2023-05-02 16:10:00', '2023-05-02 16:10:05', 20230502, 161000, 1, '{"image_url": "http://example.com/image.jpg"}');

-- Greg sends a reaction to Cathy's image
INSERT INTO fact_messages_msg (message_guid, conversation_key, sender_user_key, message_type_key, message_status_key, device_key, message_timestamp, server_received_timestamp, date_key, time_key, is_reply, replied_to_message_guid, platform_specific_payload) VALUES
('msg_guid_004', 2, 3, 3, 2, 3, '2023-05-02 16:11:00', '2023-05-02 16:11:01', 20230502, 161000, TRUE, 'msg_guid_003', '{"reaction_emoji": "👍"}');

SELECT 'Scenario 8: FB Messenger setup complete. Tables created and sample data inserted.'; 