/*
Question 4.3.1: Top Collaborative Files

Write a SQL query to find the top 10 files with the most unique users 
who performed any action on them in the last 7 days.

Schema (assumed):
file_actions:
- action_id (PK, optional)
- file_id (INTEGER) -- Identifier for the file
- user_id (INTEGER) -- Identifier for the user performing the action
- action_type (TEXT) -- e.g., 'view', 'edit', 'comment', 'share' (Not strictly needed for this query)
- action_timestamp (TIMESTAMP) -- Timestamp of the action

Expected Output:
- file_id
- unique_user_action_count
Ordered by unique_user_action_count DESC, then file_id ASC. Limited to 10 results.
*/

-- Write your SQL query here:
SELECT
    fa.file_id,
    COUNT(DISTINCT fa.user_id) AS unique_user_action_count
FROM
    file_actions fa
WHERE
    fa.action_timestamp >= CURRENT_DATE - INTERVAL '7 days' 
    AND fa.action_timestamp < CURRENT_DATE -- Actions in the last 7 full days
GROUP BY
    fa.file_id
ORDER BY
    unique_user_action_count DESC,
    fa.file_id ASC -- Secondary sort for tie-breaking
LIMIT 10; 