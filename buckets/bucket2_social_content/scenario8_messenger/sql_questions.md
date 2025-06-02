# Scenario 8: Messenger (WhatsApp/Telegram) - SQL Questions

## Database Schema Reference

Based on the Messenger data model:

### Dimension Tables
-   **`dim_users`**: `user_key`, `user_id`, `user_name`, `registration_date`, `last_active_timestamp`, `user_profile_info`
-   **`dim_chats`**: `chat_key`, `chat_id`, `chat_type`, `creation_timestamp`, `last_message_timestamp`, `chat_name`, `chat_settings`
-   **`dim_messages`**: `message_key`, `message_id`, `chat_key`, `sender_user_key`, `message_type`, `message_content`, `message_metadata`, `sent_timestamp`, `server_received_timestamp`, `edited_timestamp`, `is_ephemeral`, `disappears_at`, `reply_to_message_key`
-   **`dim_reactions`**: `reaction_key`, `reaction_emoji`, `reaction_name`
-   **`dim_date`**: `date_key`, `full_date`, `hour`, `minute`

### Fact Tables
-   **`fact_chat_participants`**: `chat_key`, `user_key`, `joined_timestamp`, `role`, `last_read_message_timestamp`, `has_muted_chat`
-   **`fact_message_recipients_status`**: `message_key`, `recipient_user_key`, `delivered_timestamp`, `read_timestamp`
-   **`fact_message_reactions`**: `message_key`, `reacting_user_key`, `reaction_key`, `reaction_timestamp`

---

## Question 1: Daily Active Users (DAU) and Message Volume

**Problem**: Calculate the Daily Active Users (DAU) who sent at least one message and the total number of messages sent per day for the last 30 days.

**Expected Output**: Date, DAU count, total messages sent.

### Solution:
```sql
SELECT 
    d.full_date,
    COUNT(DISTINCT dm.sender_user_key) as dau_sending_users,
    COUNT(dm.message_key) as total_messages_sent
FROM dim_messages dm
JOIN dim_date d ON dm.sent_timestamp::date = d.full_date -- Assuming sent_timestamp can be cast to date for joining
WHERE d.full_date >= CURRENT_DATE - 30
GROUP BY d.full_date
ORDER BY d.full_date DESC;
```

---

## Question 2: Group Chat vs. 1:1 Chat Activity

**Problem**: Compare user activity (average messages per user, number of active users) between group chats and 1:1 chats over the past week.

**Expected Output**: Chat type, total active users in type, total messages in type, average messages per active user in type.

### Solution:
```sql
WITH chat_activity AS (
    SELECT 
        dc.chat_type,
        dm.sender_user_key,
        dm.message_key,
        d.full_date
    FROM dim_messages dm
    JOIN dim_chats dc ON dm.chat_key = dc.chat_key
    JOIN dim_date d ON dm.sent_timestamp::date = d.full_date
    WHERE d.full_date >= CURRENT_DATE - 7
)
SELECT 
    chat_type,
    COUNT(DISTINCT sender_user_key) as total_active_users,
    COUNT(message_key) as total_messages,
    ROUND(COUNT(message_key) * 1.0 / COUNT(DISTINCT sender_user_key), 2) as avg_messages_per_user
FROM chat_activity
GROUP BY chat_type
ORDER BY chat_type;
```

---

## Question 3: Message Reaction Popularity and Impact

**Problem**: Identify the most popular message reactions and analyze if messages with reactions tend to have fewer direct text replies within a certain timeframe (implying reactions might serve as quick acknowledgments).

**Expected Output**: Reaction emoji, total times used. A separate query might explore the reply impact.

### Solution (Popularity):
```sql
SELECT 
    dr.reaction_emoji,
    dr.reaction_name,
    COUNT(fmr.reaction_key) as total_times_used
FROM fact_message_reactions fmr
JOIN dim_reactions dr ON fmr.reaction_key = dr.reaction_key
JOIN dim_messages dm ON fmr.message_key = dm.message_key -- To filter by recent reactions
JOIN dim_date d ON fmr.reaction_timestamp::date = d.full_date
WHERE d.full_date >= CURRENT_DATE - 30
GROUP BY dr.reaction_emoji, dr.reaction_name
ORDER BY total_times_used DESC;
```

### Solution (Reaction vs. Reply - Conceptual, requires careful definition of 'reply timeframe'):
```sql
-- This is more complex as it requires defining what constitutes a "reply" to a reacted message
-- and a relevant timeframe. This is a conceptual start.
WITH reacted_messages AS (
    SELECT DISTINCT message_key
    FROM fact_message_reactions
    WHERE reaction_timestamp >= CURRENT_DATE - 7 -- focus on recent reactions
),
messages_with_reply_info AS (
    SELECT 
        dm.message_key,
        dm.chat_key,
        dm.sent_timestamp,
        EXISTS (SELECT 1 FROM reacted_messages rm WHERE rm.message_key = dm.message_key) as has_reaction,
        LEAD(dm.sent_timestamp, 1) OVER (PARTITION BY dm.chat_key ORDER BY dm.sent_timestamp) as next_message_timestamp,
        LEAD(dm.sender_user_key, 1) OVER (PARTITION BY dm.chat_key ORDER BY dm.sent_timestamp) as next_message_sender_key,
        dm.sender_user_key as original_sender_key
    FROM dim_messages dm
    JOIN dim_date d ON dm.sent_timestamp::date = d.full_date
    WHERE d.full_date >= CURRENT_DATE - 7 -- focus on recent messages
)
SELECT 
    has_reaction,
    COUNT(message_key) as total_messages,
    SUM(CASE 
            WHEN next_message_timestamp IS NOT NULL AND 
                 next_message_sender_key != original_sender_key AND -- Reply from a different user
                 (EXTRACT(EPOCH FROM (next_message_timestamp - sent_timestamp))) < 300 -- Reply within 5 minutes
            THEN 1 ELSE 0 
        END) as quick_text_replies,
    ROUND(SUM(CASE 
            WHEN next_message_timestamp IS NOT NULL AND 
                 next_message_sender_key != original_sender_key AND 
                 (EXTRACT(EPOCH FROM (next_message_timestamp - sent_timestamp))) < 300 
            THEN 1 ELSE 0 
        END) * 100.0 / COUNT(message_key), 2) as pct_with_quick_text_reply
FROM messages_with_reply_info
GROUP BY has_reaction;
```

---

## Question 4: Ephemeral Messaging Usage

**Problem**: Determine the percentage of messages sent that are ephemeral, and the most common timer settings for ephemeral messages in chats where it's enabled.

**Expected Output**: Percentage of ephemeral messages. For chats with ephemeral settings, the distribution of timer durations.

### Solution (Percentage of Ephemeral Messages):
```sql
SELECT 
    SUM(CASE WHEN dm.is_ephemeral THEN 1 ELSE 0 END) as total_ephemeral_messages,
    COUNT(dm.message_key) as total_messages,
    ROUND(SUM(CASE WHEN dm.is_ephemeral THEN 1 ELSE 0 END) * 100.0 / COUNT(dm.message_key), 2) as pct_ephemeral_messages
FROM dim_messages dm
JOIN dim_date d ON dm.sent_timestamp::date = d.full_date
WHERE d.full_date >= CURRENT_DATE - 30;
```

### Solution (Common Timer Durations - assumes `chat_settings` JSON has `ephemeral_duration_seconds`):
```sql
SELECT 
    json_extract_path_text(dc.chat_settings, 'ephemeral_duration_seconds') as ephemeral_duration_setting,
    COUNT(DISTINCT dc.chat_key) as number_of_chats_with_setting
FROM dim_chats dc
WHERE dc.chat_settings LIKE '%ephemeral_duration_seconds%' -- Filter for chats with the setting
  AND dc.chat_type = 'group' -- Example: Focus on group chats or all as needed
  AND EXISTS (SELECT 1 FROM dim_messages dm WHERE dm.chat_key = dc.chat_key AND dm.is_ephemeral AND dm.sent_timestamp >= CURRENT_DATE - 30)
GROUP BY ephemeral_duration_setting
ORDER BY number_of_chats_with_setting DESC;
```

---

## Question 5: Unread Message Analysis

**Problem**: For users active in the last 24 hours, identify the average number of unread messages they have across all their chats.

**Expected Output**: Average unread messages per active user.

### Solution:
```sql
WITH user_last_activity AS (
    SELECT user_key
    FROM dim_users
    WHERE last_active_timestamp >= CURRENT_DATE - INTERVAL '1 day'
),
chat_unread_counts AS (
    SELECT 
        fcp.user_key,
        fcp.chat_key,
        COUNT(DISTINCT dm.message_key) as unread_messages_in_chat
    FROM fact_chat_participants fcp
    JOIN dim_messages dm ON fcp.chat_key = dm.chat_key
    WHERE fcp.user_key IN (SELECT user_key FROM user_last_activity)
      AND dm.sent_timestamp > fcp.last_read_message_timestamp
      AND dm.sender_user_key != fcp.user_key -- Don't count user's own messages as unread for them
    GROUP BY fcp.user_key, fcp.chat_key
),
user_total_unread AS (
    SELECT 
        user_key,
        SUM(unread_messages_in_chat) as total_unread_for_user
    FROM chat_unread_counts
    GROUP BY user_key
)
SELECT 
    ROUND(AVG(total_unread_for_user), 2) as avg_unread_messages_per_active_user
FROM user_total_unread;
```

---

## Question 6: Average Time to Read a Message in 1:1 Chats

**Problem**: Calculate the average time it takes for a recipient to read a message in 1:1 chats after it has been delivered.

**Expected Output**: Average read time in seconds/minutes.

### Solution:
```sql
SELECT 
    ROUND(AVG(EXTRACT(EPOCH FROM (fmrs.read_timestamp - fmrs.delivered_timestamp))), 2) as avg_time_to_read_seconds
FROM fact_message_recipients_status fmrs
JOIN dim_messages dm ON fmrs.message_key = dm.message_key
JOIN dim_chats dc ON dm.chat_key = dc.chat_key
JOIN dim_date d ON dm.sent_timestamp::date = d.full_date
WHERE dc.chat_type = '1:1'
  AND fmrs.read_timestamp IS NOT NULL
  AND fmrs.delivered_timestamp IS NOT NULL
  AND fmrs.read_timestamp > fmrs.delivered_timestamp -- Ensure logical consistency
  AND d.full_date >= CURRENT_DATE - 7; -- Analyze recent messages
``` 