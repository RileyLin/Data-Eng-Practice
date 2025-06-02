/*
Question 8.3.2: Message Reaction Engagement Trends

Write a SQL query to analyze message reaction usage patterns,
popular reaction types, and their impact on conversation engagement.

Schema Reference:
- fact_message_reactions: reaction_key, message_key, user_key, reaction_type, reaction_timestamp
- fact_messages: message_key, chat_key, sender_user_key, message_timestamp
- dim_reaction_types: reaction_type, reaction_category, display_order

Expected Output:
Reaction usage trends and their correlation with message engagement and chat activity.
*/

-- Write your SQL query here: 