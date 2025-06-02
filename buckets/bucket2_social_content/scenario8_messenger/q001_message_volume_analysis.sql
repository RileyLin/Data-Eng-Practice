/*
Question 8.3.1: Message Volume and Activity Analysis

Write a SQL query to analyze daily message volume, active users,
and messaging patterns across different chat types (1:1 vs group chats).

Schema Reference:
- fact_messages: message_key, chat_key, sender_user_key, message_timestamp, message_type
- dim_chats: chat_key, chat_type, participant_count, creation_timestamp
- dim_users: user_key, user_id, registration_date

Expected Output:
Daily messaging activity trends with breakdown by chat type and user engagement patterns.
*/

-- Write your SQL query here: 