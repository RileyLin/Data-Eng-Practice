/*
Question 4.3.1: Top Collaborative Files

Write a SQL query to find the top 10 files with the most unique users 
who performed any action on them in the last 7 days.

Schema (based on setup_scripts/scenario_4_cloud_storage_setup.sql):

fact_files_storage:
- file_key (INTEGER PRIMARY KEY AUTOINCREMENT)
- file_id (VARCHAR(50) UNIQUE NOT NULL) -- Public facing ID, to be used in output
- owner_user_key (INTEGER, FK to dim_users_storage)
- folder_key (INTEGER, FK to dim_folders_storage)
- file_name (TEXT NOT NULL)
- file_type (TEXT)
- size_bytes (INTEGER)
- created_at_timestamp (TEXT) -- ISO 8601 format
- last_modified_timestamp (TEXT) -- ISO 8601 format, can indicate an action by owner/editor
- created_date_key (INTEGER)
- created_time_key (INTEGER)
- is_deleted (BOOLEAN DEFAULT FALSE)

fact_file_shares_storage: (Represents sharing actions)
- share_id (INTEGER PRIMARY KEY AUTOINCREMENT)
- file_key (INTEGER, FK to fact_files_storage)
- shared_with_user_key (INTEGER, FK to dim_users_storage) -- A user involved in action
- shared_with_group_key (INTEGER, FK to dim_groups_storage)
- permission_level_key (INTEGER, FK to dim_permission_levels_storage)
- shared_by_user_key (INTEGER, FK to dim_users_storage) -- Another user involved in action
- shared_at_timestamp (TEXT) -- ISO 8601 format, use for 7-day window
- shared_date_key (INTEGER)
- shared_time_key (INTEGER)

-- To determine "any action", we consider users involved in shares (shared_by_user_key, shared_with_user_key)
-- and users who modify files (owner_user_key if last_modified_timestamp is recent).
-- The question is simplified if we assume `file_actions` implies a direct log of varied interactions.
-- Given the schema, we'll focus on unique users involved via `fact_file_shares_storage` and `fact_files_storage.owner_user_key` for modifications.

Expected Output:
- file_id (from fact_files_storage.file_id)
- unique_user_action_count
Ordered by unique_user_action_count DESC, then file_id ASC. Limited to 10 results.
*/

-- Write your SQL query here:
WITH UserFileActions AS (
    -- Users who shared a file
    SELECT
        ffss.file_key,
        ffss.shared_by_user_key AS user_key,
        ffss.shared_at_timestamp AS action_timestamp
    FROM
        fact_file_shares_storage ffss
    WHERE ffss.shared_at_timestamp >= CURRENT_DATE - INTERVAL '7 days'
      AND ffss.shared_at_timestamp < CURRENT_DATE

    UNION

    -- Users with whom a file was shared (individual share)
    SELECT
        ffss.file_key,
        ffss.shared_with_user_key AS user_key,
        ffss.shared_at_timestamp AS action_timestamp
    FROM
        fact_file_shares_storage ffss
    WHERE ffss.shared_with_user_key IS NOT NULL
      AND ffss.shared_at_timestamp >= CURRENT_DATE - INTERVAL '7 days'
      AND ffss.shared_at_timestamp < CURRENT_DATE

    UNION

    -- Users who are members of a group with which a file was shared
    SELECT
        ffss.file_key,
        bgms.user_key AS user_key,
        ffss.shared_at_timestamp AS action_timestamp
    FROM
        fact_file_shares_storage ffss
    JOIN
        bridge_group_memberships_storage bgms ON ffss.shared_with_group_key = bgms.group_key
    WHERE ffss.shared_with_group_key IS NOT NULL AND bgms.is_active = TRUE
      AND ffss.shared_at_timestamp >= CURRENT_DATE - INTERVAL '7 days'
      AND ffss.shared_at_timestamp < CURRENT_DATE
      
    UNION
    
    -- Owners of files modified in the last 7 days (modification is an action)
    SELECT 
        ffs.file_key,
        ffs.owner_user_key AS user_key,
        ffs.last_modified_timestamp AS action_timestamp
    FROM 
        fact_files_storage ffs
    WHERE ffs.last_modified_timestamp >= CURRENT_DATE - INTERVAL '7 days'
      AND ffs.last_modified_timestamp < CURRENT_DATE
)
SELECT
    ffs.file_id,
    COUNT(DISTINCT ufa.user_key) AS unique_user_action_count
FROM
    UserFileActions ufa
JOIN
    fact_files_storage ffs ON ufa.file_key = ffs.file_key
GROUP BY
    ffs.file_id
ORDER BY
    unique_user_action_count DESC,
    ffs.file_id ASC
LIMIT 10; 