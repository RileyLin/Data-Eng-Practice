/*
Corrected Solution: Top 5 Message Senders (Last 30 Days)
Original attempt had good structure but missing time filters and syntax issues
*/

WITH total_messages_last_30 AS (
    SELECT COUNT(DISTINCT message_id) AS total_messages 
    FROM messages 
    WHERE message_timestamp >= CURRENT_DATE - INTERVAL '30 days'
),

top_5_users AS (
    SELECT 
        sender_user_id,
        COUNT(message_id) AS messages_sent
    FROM messages
    WHERE message_timestamp >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY sender_user_id
    ORDER BY messages_sent DESC
    LIMIT 5
)

SELECT 
    tu.sender_user_id,
    tu.messages_sent,
    ROUND(tu.messages_sent * 100.0 / tml.total_messages, 2) AS percentage_of_total
FROM top_5_users tu
CROSS JOIN total_messages_last_30 tml
ORDER BY tu.messages_sent DESC;

-- Alternative: More efficient single-pass version
/*
WITH user_stats AS (
    SELECT 
        sender_user_id,
        COUNT(message_id) AS messages_sent,
        COUNT(message_id) * 100.0 / SUM(COUNT(message_id)) OVER() AS percentage_of_total
    FROM messages
    WHERE message_timestamp >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY sender_user_id
    ORDER BY messages_sent DESC
    LIMIT 5
)
SELECT * FROM user_stats;
*/ 