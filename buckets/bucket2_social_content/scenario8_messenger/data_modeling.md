# Scenario 8: Messenger (WhatsApp/Telegram) - Data Model

## Overview
This data model supports a messaging application, focusing on users, chats (1:1 and group), messages, read statuses, reactions, and settings like ephemeral messaging.

## Core Design Principles
1.  **Scalability**: Handle a large volume of users, messages, and interactions.
2.  **Flexibility**: Accommodate different message types (text, media, system messages).
3.  **Real-time Features**: Support for read receipts, typing indicators (though not explicitly modeled here, schema should allow it).
4.  **User Privacy**: Design with privacy considerations for ephemeral messages and user data.
5.  **Feature Extensibility**: Allow for new features like reactions, replies, and polls.

## Entity Relationship Diagram

```mermaid
erDiagram
    dim_users {
        int user_key PK
        varchar user_id UK
        varchar user_name
        timestamp registration_date
        timestamp last_active_timestamp
        varchar user_profile_info "JSON for avatar_url, status_message etc."
    }

    dim_chats {
        int chat_key PK
        varchar chat_id UK
        varchar chat_type "1:1, group"
        timestamp creation_timestamp
        timestamp last_message_timestamp
        varchar chat_name "For group chats"
        varchar chat_settings "JSON for ephemeral_duration_seconds, notification_prefs etc."
    }

    dim_messages {
        int message_key PK
        varchar message_id UK
        int chat_key FK
        int sender_user_key FK
        varchar message_type "text, image, video, audio, file, system_notification"
        text message_content "Actual text or URL to media"
        json message_metadata "e.g., for media: {size_bytes, duration_sec, thumbnail_url}, for system: {event_type}"
        timestamp sent_timestamp
        timestamp server_received_timestamp
        timestamp edited_timestamp "Null if not edited"
        boolean is_ephemeral
        timestamp disappears_at "For ephemeral messages, calculated based on chat_settings & sent/read time"
        int reply_to_message_key FK "Self-referencing for replies"
    }

    dim_reactions {
        int reaction_key PK
        varchar reaction_emoji UK "e.g., 👍, ❤️, 😂"
        varchar reaction_name "e.g., thumbs_up, love, laugh"
    }

    dim_date {
        int date_key PK
        date full_date
        int hour
        int minute
    }

    fact_chat_participants {
        int chat_key PK
        int user_key PK
        timestamp joined_timestamp
        varchar role "member, admin (for group chats)"
        timestamp last_read_message_timestamp "Tracks up to which message user has read in this chat"
        boolean has_muted_chat
    }

    fact_message_recipients_status {
        int message_key PK
        int recipient_user_key PK
        timestamp delivered_timestamp
        timestamp read_timestamp
    }
    
    fact_message_reactions {
        int message_key PK
        int reacting_user_key PK
        int reaction_key PK
        timestamp reaction_timestamp
    }

    dim_users ||--o{ fact_chat_participants : "participates_in"
    dim_chats ||--o{ fact_chat_participants : "has_participant"
    dim_chats ||--o{ dim_messages : "contains"
    dim_users ||--o{ dim_messages : "sends"
    dim_messages }o--o{ dim_messages : "is_reply_to"

    dim_messages ||--o{ fact_message_recipients_status : "has_status_for"
    dim_users ||--o{ fact_message_recipients_status : "is_recipient_of"

    dim_messages ||--o{ fact_message_reactions : "receives"
    dim_users ||--o{ fact_message_reactions : "reacts_with"
    dim_reactions ||--o{ fact_message_reactions : "is_type_of"
    
    dim_date ||--|| dim_messages : "related_to_message_time"
    dim_date ||--|| fact_chat_participants : "related_to_join_time"
    dim_date ||--|| fact_message_reactions : "related_to_reaction_time"

```

## Table Specifications

### Dimension Tables

#### `dim_users`
-   **Purpose**: Stores information about registered users.
-   **Key Fields**:
    -   `last_active_timestamp`: For presence and activity analysis.
    -   `user_profile_info`: Flexible JSON for profile details.

#### `dim_chats`
-   **Purpose**: Represents a conversation, either 1:1 or group.
-   **Key Fields**:
    -   `chat_type`: Distinguishes between 1:1 and group conversations.
    -   `chat_settings`: JSON field to store chat-specific settings like ephemeral message duration, custom notifications.

#### `dim_messages`
-   **Purpose**: Stores individual messages sent within chats.
-   **Key Fields**:
    -   `message_type`: Type of content in the message.
    -   `message_content`: Text or link to media.
    -   `message_metadata`: Additional structured info about the message.
    -   `is_ephemeral`, `disappears_at`: Manages disappearing messages.
    -   `reply_to_message_key`: Links a message to the one it replies to.

#### `dim_reactions`
-   **Purpose**: Lookup table for available reaction types.

#### `dim_date`
-   **Purpose**: Standard date dimension for time-based analysis.

### Fact Tables

#### `fact_chat_participants`
-   **Purpose**: Links users to the chats they are part of.
-   **Granularity**: One record per user per chat.
-   **Key Fields**:
    -   `role`: User's role in group chats.
    -   `last_read_message_timestamp`: Essential for unread counts and read receipts.

#### `fact_message_recipients_status`
-   **Purpose**: Tracks the delivery and read status of each message for each recipient.
-   **Granularity**: One record per message per recipient.
-   **Key Fields**:
    -   `delivered_timestamp`, `read_timestamp`: Core for read receipts.

#### `fact_message_reactions`
-   **Purpose**: Records user reactions to messages.
-   **Granularity**: One record per user per reaction type on a message.

## Key Business Rules & Considerations

1.  **Ephemeral Message Logic**: The `disappears_at` timestamp in `dim_messages` would be calculated based on `dim_chats.chat_settings` (ephemeral duration) and either `dim_messages.sent_timestamp` or `fact_message_recipients_status.read_timestamp` for the relevant user(s).
2.  **Read Receipts**: `fact_message_recipients_status.read_timestamp` is the source for 'seen' status. For group chats, this means all participants who have read it.
3.  **Unread Counts**: Can be derived by comparing `fact_chat_participants.last_read_message_timestamp` with `dim_messages.sent_timestamp` within a chat.
4.  **System Messages**: `dim_messages.message_type = 'system_notification'` can be used for events like "User X joined the group", "Chat name changed".
5.  **Scalability of `fact_message_recipients_status`**: This table can grow very large. Partitioning by date or chat_key might be necessary. For very large groups, individual read receipts might be sampled or aggregated.

## Analytics Use Cases
-   **User Activity**: Daily/monthly active users, message sending frequency, session duration.
-   **Chat Engagement**: Messages per chat, participant activity in groups, popular group sizes.
-   **Feature Adoption**: Usage of reactions, replies, ephemeral messaging.
-   **Message Lifecycle**: Time to deliver, time to read, lifespan of ephemeral messages.
-   **Reaction Analysis**: Popular reactions, impact of reactions on reply rates.
-   **Notification Effectiveness**: If system message events are analyzed.
-   **Churn Indicators**: Decreased activity, leaving groups.

## Implementation Notes
-   Timestamps should be stored in UTC.
-   Consider using NoSQL databases for `dim_messages` or `fact_message_recipients_status` if extreme write scalability or flexible schemas are needed, though this model is relational.
-   Indexing will be critical on foreign keys, timestamps, and `chat_id`