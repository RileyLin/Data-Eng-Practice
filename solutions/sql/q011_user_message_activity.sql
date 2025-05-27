/*
Solution to Question 8.3.1: User Message Activity

Write a SQL query to find the top 5 user_ids who sent the most messages in the last 30 days, 
along with their message count and the percentage of the total messages they represent.
*/

-- Assume a `messages` table with `message_id`, `sender_user_id`, `message_timestamp`.

WITH UserMessageCounts AS (
    -- Count messages sent by each user in the last 30 days
    SELECT
        m.sender_user_id,
        COUNT(m.message_id) AS messages_sent_count
    FROM
        messages m
    WHERE
        m.message_timestamp >= CURRENT_DATE - INTERVAL '30 days'
        AND m.message_timestamp < CURRENT_DATE
    GROUP BY
        m.sender_user_id
),
TotalMessagesInPeriod AS (
    -- Calculate the total number of messages sent in the period
    SELECT
        SUM(umc.messages_sent_count) AS total_messages
    FROM
        UserMessageCounts umc
)
SELECT
    umc.sender_user_id,
    umc.messages_sent_count,
    CASE
        WHEN (SELECT total_messages FROM TotalMessagesInPeriod) = 0 THEN 0.0
        ELSE ROUND((umc.messages_sent_count * 100.0) / (SELECT total_messages FROM TotalMessagesInPeriod), 2)
    END AS percentage_of_total_messages
FROM
    UserMessageCounts umc
ORDER BY
    umc.messages_sent_count DESC
LIMIT 5;

/*
Explanation:

1.  `UserMessageCounts` CTE:
    *   Selects from the `messages` table (aliased as `m`).
    *   Filters messages to include only those sent within the last 30 full days (`message_timestamp >= CURRENT_DATE - INTERVAL '30 days' AND message_timestamp < CURRENT_DATE`).
    *   Groups the records by `sender_user_id`.
    *   `COUNT(m.message_id) AS messages_sent_count` calculates the number of messages sent by each user in that period.

2.  `TotalMessagesInPeriod` CTE:
    *   Calculates the sum of all `messages_sent_count` from the `UserMessageCounts` CTE. This gives the grand total of messages sent by all users in the last 30 days.
    *   This is done in a separate CTE to avoid calculating the sum repeatedly for each row in the final select if it were a subquery in the select list.

3.  Final `SELECT` Statement:
    *   Selects `sender_user_id` and their `messages_sent_count` from `UserMessageCounts`.
    *   Calculates `percentage_of_total_messages`:
        *   (`messages_sent_count` * 100.0) / `total_messages` (from `TotalMessagesInPeriod`).
        *   Multiplying by `100.0` ensures floating-point division for the percentage.
        *   A `CASE` statement is used to handle the edge case where `total_messages` might be 0 (e.g., no messages in the period), returning 0.0 to avoid division by zero.
        *   `ROUND(..., 2)` formats the percentage to two decimal places.
    *   `ORDER BY umc.messages_sent_count DESC` sorts the users by the number of messages they sent in descending order.
    *   `LIMIT 5` restricts the output to the top 5 users.

Schema Assumptions:
messages:
- message_id (PK)
- conversation_id (FK, optional)
- sender_user_id (Identifier for the user who sent the message)
- message_timestamp (Timestamp when the message was sent)
- content (Optional)

Example DDL & DML for testing:

DROP TABLE IF EXISTS messages;
CREATE TABLE messages (
    message_id SERIAL PRIMARY KEY,
    sender_user_id INTEGER,
    message_timestamp TIMESTAMP
);

-- Sample data for the last 30 days (assume CURRENT_DATE is '2023-04-15')
INSERT INTO messages (sender_user_id, message_timestamp) VALUES
(101, CURRENT_DATE - INTERVAL '1 day'), (101, CURRENT_DATE - INTERVAL '1 day'), (101, CURRENT_DATE - INTERVAL '2 days'), -- User 101: 30 messages
(102, CURRENT_DATE - INTERVAL '1 day'), (102, CURRENT_DATE - INTERVAL '3 days'), -- User 102: 20 messages
(103, CURRENT_DATE - INTERVAL '4 days'), -- User 103: 15 messages
(104, CURRENT_DATE - INTERVAL '5 days'), -- User 104: 10 messages
(105, CURRENT_DATE - INTERVAL '6 days'), -- User 105: 8 messages
(106, CURRENT_DATE - INTERVAL '7 days'); -- User 106: 5 messages

-- For simplicity, let's make counts more distinct for top 5
DELETE FROM messages;
INSERT INTO messages (sender_user_id, message_timestamp) VALUES
(101, CURRENT_DATE - INTERVAL '1 day'), (101, CURRENT_DATE - INTERVAL '1 day'), (101, CURRENT_DATE - INTERVAL '1 day'), (101, CURRENT_DATE - INTERVAL '1 day'), (101, CURRENT_DATE - INTERVAL '1 day'), -- User 101: 5 msgs
(101, CURRENT_DATE - INTERVAL '2 days'), (101, CURRENT_DATE - INTERVAL '2 days'), (101, CURRENT_DATE - INTERVAL '2 days'), (101, CURRENT_DATE - INTERVAL '2 days'), (101, CURRENT_DATE - INTERVAL '2 days'), -- Total 10 for 101
(102, CURRENT_DATE - INTERVAL '1 day'), (102, CURRENT_DATE - INTERVAL '1 day'), (102, CURRENT_DATE - INTERVAL '1 day'), (102, CURRENT_DATE - INTERVAL '1 day'), -- User 102: 4 msgs
(102, CURRENT_DATE - INTERVAL '3 days'), (102, CURRENT_DATE - INTERVAL '3 days'), (102, CURRENT_DATE - INTERVAL '3 days'), -- Total 7 for 102
(103, CURRENT_DATE - INTERVAL '4 days'), (103, CURRENT_DATE - INTERVAL '4 days'), (103, CURRENT_DATE - INTERVAL '4 days'), (103, CURRENT_DATE - INTERVAL '4 days'), (103, CURRENT_DATE - INTERVAL '4 days'), (103, CURRENT_DATE - INTERVAL '4 days'), -- User 103: 6 msgs
(104, CURRENT_DATE - INTERVAL '5 days'),(104, CURRENT_DATE - INTERVAL '5 days'),(104, CURRENT_DATE - INTERVAL '5 days'), -- User 104: 3 msgs
(105, CURRENT_DATE - INTERVAL '6 days'), (105, CURRENT_DATE - INTERVAL '6 days'), -- User 105: 2 msgs
(106, CURRENT_DATE - INTERVAL '7 days'); -- User 106: 1 msg
(107, CURRENT_DATE - INTERVAL '35 days'); -- Outside period

-- Total messages in period = 10 (U101) + 7 (U102) + 6 (U103) + 3 (U104) + 2 (U105) + 1 (U106) = 29

-- Expected Output:
-- sender_user_id | messages_sent_count | percentage_of_total_messages
-- ---------------|---------------------|-------------------------------
-- 101            | 10                  | 34.48 ( (10/29)*100 )
-- 102            | 7                   | 24.14 ( (7/29)*100 )
-- 103            | 6                   | 20.69 ( (6/29)*100 )
-- 104            | 3                   | 10.34 ( (3/29)*100 )
-- 105            | 2                   | 6.90  ( (2/29)*100 )
*/ 