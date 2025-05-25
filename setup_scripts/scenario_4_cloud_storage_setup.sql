-- Setup script for Scenario 4: Cloud File Storage (Dropbox/Google Drive)

-- Dimension Tables
DROP TABLE IF EXISTS dim_users_storage;
CREATE TABLE dim_users_storage (
    user_key INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR(50) UNIQUE NOT NULL,
    username TEXT,
    email TEXT UNIQUE NOT NULL,
    created_at TEXT -- ISO 8601 format
);

DROP TABLE IF EXISTS dim_groups_storage;
CREATE TABLE dim_groups_storage (
    group_key INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id VARCHAR(50) UNIQUE NOT NULL,
    group_name TEXT NOT NULL,
    created_by_user_key INTEGER,
    created_at TEXT, -- ISO 8601 format
    FOREIGN KEY (created_by_user_key) REFERENCES dim_users_storage(user_key)
);

DROP TABLE IF EXISTS dim_permission_levels_storage;
CREATE TABLE dim_permission_levels_storage (
    permission_level_key INTEGER PRIMARY KEY AUTOINCREMENT,
    permission_name TEXT UNIQUE NOT NULL, -- e.g., 'view', 'comment', 'edit', 'owner'
    can_view BOOLEAN DEFAULT FALSE,
    can_comment BOOLEAN DEFAULT FALSE,
    can_edit BOOLEAN DEFAULT FALSE,
    can_share BOOLEAN DEFAULT FALSE
);

DROP TABLE IF EXISTS dim_folders_storage;
CREATE TABLE dim_folders_storage (
    folder_key INTEGER PRIMARY KEY AUTOINCREMENT,
    folder_id VARCHAR(50) UNIQUE NOT NULL,
    folder_name TEXT NOT NULL,
    parent_folder_key INTEGER, -- Self-referential for subfolders
    owner_user_key INTEGER, -- FK to dim_users_storage
    created_at TEXT, -- ISO 8601 format
    FOREIGN KEY (parent_folder_key) REFERENCES dim_folders_storage(folder_key),
    FOREIGN KEY (owner_user_key) REFERENCES dim_users_storage(user_key)
);

-- Re-using dim_date and dim_time from Scenario 1 for consistency.
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

-- Fact/Bridge Tables
DROP TABLE IF EXISTS fact_files_storage;
CREATE TABLE fact_files_storage (
    file_key INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id VARCHAR(50) UNIQUE NOT NULL,
    owner_user_key INTEGER, -- FK to dim_users_storage
    folder_key INTEGER, -- FK to dim_folders_storage (can be NULL for root files)
    file_name TEXT NOT NULL,
    file_type TEXT, -- e.g., 'document', 'image', 'video', 'spreadsheet'
    size_bytes INTEGER,
    created_at_timestamp TEXT, -- ISO 8601 format
    last_modified_timestamp TEXT, -- ISO 8601 format
    created_date_key INTEGER,
    created_time_key INTEGER,
    is_deleted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (owner_user_key) REFERENCES dim_users_storage(user_key),
    FOREIGN KEY (folder_key) REFERENCES dim_folders_storage(folder_key),
    FOREIGN KEY (created_date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (created_time_key) REFERENCES dim_time(time_key)
);

DROP TABLE IF EXISTS bridge_group_memberships_storage;
CREATE TABLE bridge_group_memberships_storage (
    membership_id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_key INTEGER, -- FK to dim_groups_storage
    user_key INTEGER, -- FK to dim_users_storage
    role_in_group TEXT, -- e.g., 'member', 'admin'
    joined_at TEXT, -- ISO 8601 format
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (group_key) REFERENCES dim_groups_storage(group_key),
    FOREIGN KEY (user_key) REFERENCES dim_users_storage(user_key),
    UNIQUE (group_key, user_key) -- A user is typically only in a group once
);

DROP TABLE IF EXISTS fact_file_shares_storage;
CREATE TABLE fact_file_shares_storage (
    share_id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_key INTEGER, -- FK to fact_files_storage
    shared_with_user_key INTEGER, -- FK to dim_users_storage (NULL if group share)
    shared_with_group_key INTEGER, -- FK to dim_groups_storage (NULL if user share)
    permission_level_key INTEGER, -- FK to dim_permission_levels_storage
    shared_by_user_key INTEGER, -- FK to dim_users_storage (who initiated the share)
    shared_at_timestamp TEXT, -- ISO 8601 format
    shared_date_key INTEGER,
    shared_time_key INTEGER,
    expires_at_timestamp TEXT, -- ISO 8601 format (NULL if no expiry)
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (file_key) REFERENCES fact_files_storage(file_key),
    FOREIGN KEY (shared_with_user_key) REFERENCES dim_users_storage(user_key),
    FOREIGN KEY (shared_with_group_key) REFERENCES dim_groups_storage(group_key),
    FOREIGN KEY (permission_level_key) REFERENCES dim_permission_levels_storage(permission_level_key),
    FOREIGN KEY (shared_by_user_key) REFERENCES dim_users_storage(user_key),
    FOREIGN KEY (shared_date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (shared_time_key) REFERENCES dim_time(time_key),
    CHECK ((shared_with_user_key IS NOT NULL AND shared_with_group_key IS NULL) OR 
           (shared_with_user_key IS NULL AND shared_with_group_key IS NOT NULL))
);

-- Sample Data Insertion

-- dim_date (Example for Jan 15-16, 2023)
INSERT INTO dim_date (date_key, full_date, year, quarter, month, day_of_month, day_of_week, week_of_year, is_weekend) VALUES
(20230115, '2023-01-15', 2023, 1, 1, 15, 1, 3, TRUE),
(20230116, '2023-01-16', 2023, 1, 1, 16, 2, 3, FALSE);

-- dim_time (Examples)
INSERT INTO dim_time (time_key, full_time, hour, minute, second, am_pm) VALUES
(140000, '14:00:00', 14, 0, 0, 'PM'),
(143000, '14:30:00', 14, 30, 0, 'PM'),
(150000, '15:00:00', 15, 0, 0, 'PM');

-- dim_users_storage
INSERT INTO dim_users_storage (user_id, username, email, created_at) VALUES
('u_store_1', 'OwnerAlice', 'alice.owner@example.com', '2023-01-01 10:00:00'),
('u_store_2', 'EditorBob', 'bob.editor@example.com', '2023-01-02 11:00:00'),
('u_store_3', 'ViewerCharlie', 'charlie.viewer@example.com', '2023-01-03 12:00:00'),
('u_store_4', 'GroupAdminDavid', 'david.admin@example.com', '2023-01-04 13:00:00');

-- dim_permission_levels_storage
INSERT INTO dim_permission_levels_storage (permission_name, can_view, can_comment, can_edit, can_share) VALUES
('Owner', TRUE, TRUE, TRUE, TRUE),
('Edit', TRUE, TRUE, TRUE, TRUE),
('Comment', TRUE, TRUE, FALSE, FALSE),
('View', TRUE, FALSE, FALSE, FALSE);

-- dim_folders_storage
INSERT INTO dim_folders_storage (folder_id, folder_name, parent_folder_key, owner_user_key, created_at) VALUES
('folder_root_alice', 'Alice Root', NULL, 1, '2023-01-15 14:00:00'),      -- key 1
('folder_proj_x', 'Project X', 1, 1, '2023-01-15 14:05:00');       -- key 2 (subfolder of Alice Root)

-- fact_files_storage
INSERT INTO fact_files_storage (file_id, owner_user_key, folder_key, file_name, file_type, size_bytes, created_at_timestamp, last_modified_timestamp, created_date_key, created_time_key) VALUES
('file_doc1', 1, 2, 'Proposal.docx', 'document', 102400, '2023-01-15 14:10:00', '2023-01-15 14:15:00', 20230115, 140000), -- key 1
('file_img1', 1, 2, 'TeamPhoto.jpg', 'image', 2048000, '2023-01-15 14:20:00', '2023-01-15 14:20:00', 20230115, 140000), -- key 2
('file_report1', 4, NULL, 'QuarterlyReport.pdf', 'document', 512000, '2023-01-16 09:00:00', '2023-01-16 09:30:00', 20230116, 090000); -- key 3, in Davids root

-- dim_groups_storage
INSERT INTO dim_groups_storage (group_id, group_name, created_by_user_key, created_at) VALUES
('grp_team_alpha', 'Team Alpha', 4, '2023-01-15 10:00:00'), -- key 1
('grp_readonly', 'Read Only Viewers', 1, '2023-01-15 11:00:00'); -- key 2

-- bridge_group_memberships_storage
INSERT INTO bridge_group_memberships_storage (group_key, user_key, role_in_group, joined_at) VALUES
(1, 1, 'member', '2023-01-15 10:01:00'), -- Alice in Team Alpha
(1, 2, 'member', '2023-01-15 10:02:00'), -- Bob in Team Alpha
(2, 3, 'member', '2023-01-15 11:01:00'); -- Charlie in Read Only Viewers

-- fact_file_shares_storage
-- Alice (user_key 1) owns Proposal.docx (file_key 1) and TeamPhoto.jpg (file_key 2)
-- Alice shares Proposal.docx (file_key 1) with Bob (user_key 2) with Edit permission (perm_key 2)
INSERT INTO fact_file_shares_storage (file_key, shared_with_user_key, permission_level_key, shared_by_user_key, shared_at_timestamp, shared_date_key, shared_time_key) VALUES
(1, 2, 2, 1, '2023-01-15 14:30:00', 20230115, 143000);

-- Alice shares TeamPhoto.jpg (file_key 2) with Charlie (user_key 3) with View permission (perm_key 4)
INSERT INTO fact_file_shares_storage (file_key, shared_with_user_key, permission_level_key, shared_by_user_key, shared_at_timestamp, shared_date_key, shared_time_key) VALUES
(2, 3, 4, 1, '2023-01-15 14:35:00', 20230115, 143000);

-- David (user_key 4) owns QuarterlyReport.pdf (file_key 3)
-- David shares QuarterlyReport.pdf with Team Alpha (group_key 1) with Comment permission (perm_key 3)
INSERT INTO fact_file_shares_storage (file_key, shared_with_group_key, permission_level_key, shared_by_user_key, shared_at_timestamp, shared_date_key, shared_time_key) VALUES
(3, 1, 3, 4, '2023-01-16 09:45:00', 20230116, 090000);

-- Alice shares Proposal.docx (file_key 1) with Read Only Viewers group (group_key 2) with View permission (perm_key 4)
INSERT INTO fact_file_shares_storage (file_key, shared_with_group_key, permission_level_key, shared_by_user_key, shared_at_timestamp, shared_date_key, shared_time_key) VALUES
(1, 2, 4, 1, '2023-01-16 10:00:00', 20230116, 100000);

SELECT 'Scenario 4: Cloud File Storage setup complete. Tables created and sample data inserted.'; 