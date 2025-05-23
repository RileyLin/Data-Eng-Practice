# Solution to Question 8.2.1: Messaging Activity Model

## Question

Design a data model for tracking messaging activity that efficiently supports analytics around user engagement patterns, popular conversation topics, and message delivery performance.

## Solution

### Core Structure

An effective messaging activity data model must balance analytical needs with privacy considerations, collecting meaningful engagement metrics without compromising message content privacy. The model below is optimized for analytical workflows while maintaining appropriate data boundaries.

### Table Definitions

```mermaid
erDiagram
    fact_message_events }o--|| dim_users : sent_by
    fact_message_events }o--|| dim_conversations : in_conversation
    fact_message_events }o--|| dim_message_types : categorized_as
    fact_message_events }o--|| dim_dates : on_date
    fact_message_events }o--|| dim_message_status : has_status
    fact_message_events }o--|| dim_devices : from_device
    fact_message_derived_topics ||--|| fact_message_events : derived_from
    fact_message_derived_topics }o--|| dim_topics : about_topic
    fact_conversation_metrics ||--|| dim_conversations : for_conversation
    fact_conversation_metrics ||--|| dim_dates : for_date
    fact_user_metrics ||--|| dim_users : for_user
    fact_user_metrics ||--|| dim_dates : for_date
    dim_conversations }o--|| dim_conversation_types : categorized_as
    dim_users ||--o{ dim_conversation_participants : participates_in
    dim_conversations ||--o{ dim_conversation_participants : has_participants

    fact_message_events {
        bigint message_event_id PK
        bigint conversation_key FK
        bigint sender_user_key FK
        bigint message_type_key FK
        bigint date_key FK
        bigint time_key FK
        bigint device_key FK
        bigint message_status_key FK
        timestamp message_timestamp
        timestamp server_received_timestamp
        int message_size_bytes
        int character_count
        int media_count
        int message_sequence
        boolean is_reply
        bigint replied_to_message_id
        decimal sentiment_score
        json metadata
    }

    fact_message_derived_topics {
        bigint topic_assignment_id PK
        bigint message_event_id FK
        bigint topic_key FK
        decimal topic_confidence
        string extraction_method
        string topic_extraction_version
        timestamp processed_timestamp
    }

    fact_conversation_metrics {
        bigint metric_id PK
        bigint conversation_key FK
        bigint date_key FK
        int total_messages
        int total_participants
        int active_participants
        int total_characters
        int total_media
        decimal avg_response_time_seconds
        decimal avg_read_receipt_time_seconds
        decimal engagement_score
        json top_topics_json
        int messages_per_participant
    }

    fact_user_metrics {
        bigint user_metric_id PK
        bigint user_key FK
        bigint date_key FK
        int messages_sent
        int conversations_participated
        int new_conversations_started
        int total_recipients
        decimal avg_messaging_session_length
        int total_active_conversations
        int read_receipts_sent
        decimal avg_response_time_seconds
        json messaging_pattern_json
    }

    dim_message_types {
        bigint message_type_key PK
        string message_type_name
        string message_category
        boolean contains_media
        boolean is_ephemeral
        boolean is_system_message
        string rendering_requirements
    }

    dim_message_status {
        bigint message_status_key PK
        string status_name
        string status_description
        boolean is_terminal_state
        int status_sequence
    }

    dim_conversations {
        bigint conversation_key PK
        string conversation_id
        bigint conversation_type_key FK
        timestamp created_timestamp
        timestamp last_activity_timestamp
        string conversation_name
        boolean is_encrypted
        boolean is_group_conversation
        int participant_count
        string privacy_level
        json conversation_metadata
    }

    dim_conversation_types {
        bigint conversation_type_key PK
        string type_name
        string type_description
        boolean supports_group_chat
        boolean supports_encryption
        int max_participants
    }

    dim_conversation_participants {
        bigint participant_id PK
        bigint conversation_key FK
        bigint user_key FK
        timestamp joined_timestamp
        timestamp last_active_timestamp
        string role_in_conversation
        boolean notifications_enabled
        boolean is_active
    }

    dim_users {
        bigint user_key PK
        string user_id
        timestamp user_created_at
        string account_type
        string messaging_status
        boolean is_test_account
        json user_preferences
    }

    dim_topics {
        bigint topic_key PK
        string topic_name
        string topic_category
        bigint parent_topic_key FK
        int hierarchy_level
        json topic_keywords
        decimal topic_prevalence
    }

    dim_devices {
        bigint device_key PK
        string device_id
        string device_type
        string platform
        string app_version
        string os_version
        string network_type
    }
```

### Key Design Features

1. **Message Event Tracking**:
   - `fact_message_events` captures messaging activity without storing message content
   - Records technical metadata like size, character count, and timestamps
   - Tracks message status through its lifecycle (sent, delivered, read)
   - Supports message threading with reply relationships

2. **Topic Derivation**:
   - `fact_message_derived_topics` stores topics extracted from messages
   - Uses separate table to maintain privacy (no direct content storage)
   - Supports multiple topics per message with confidence scores
   - Tracks extraction method and version for analytical consistency

3. **Multi-level Metrics**:
   - `fact_conversation_metrics` aggregates at the conversation level
   - `fact_user_metrics` captures user engagement patterns
   - Daily aggregation balances detail with query performance
   - JSON fields store complex metrics that don't fit relational model

4. **Conversation Context**:
   - `dim_conversations` tracks conversation metadata and properties
   - `dim_conversation_participants` maintains participant relationships
   - Supports both group and one-on-one conversation analysis
   - Records temporal dynamics (join time, last activity)

### Analytical Scenarios

1. **User Engagement Patterns**:
   ```sql
   -- Daily active messaging users trend
   SELECT d.full_date, COUNT(DISTINCT um.user_key) as daily_active_messengers
   FROM fact_user_metrics um
   JOIN dim_dates d ON um.date_key = d.date_key
   WHERE d.full_date BETWEEN '2023-07-01' AND '2023-07-31'
   AND um.messages_sent > 0
   GROUP BY d.full_date
   ORDER BY d.full_date;
   ```

2. **Conversation Topic Analysis**:
   ```sql
   -- Top conversation topics by message volume
   SELECT t.topic_name, t.topic_category,
          COUNT(*) as message_count,
          COUNT(DISTINCT mdt.message_event_id) as unique_messages,
          COUNT(DISTINCT me.conversation_key) as unique_conversations
   FROM fact_message_derived_topics mdt
   JOIN dim_topics t ON mdt.topic_key = t.topic_key
   JOIN fact_message_events me ON mdt.message_event_id = me.message_event_id
   JOIN dim_dates d ON me.date_key = d.date_key
   WHERE d.full_date BETWEEN '2023-07-01' AND '2023-07-31'
   AND mdt.topic_confidence >= 0.7
   GROUP BY t.topic_name, t.topic_category
   ORDER BY message_count DESC
   LIMIT 20;
   ```

3. **Message Delivery Performance**:
   ```sql
   -- Message delivery performance by device type and network
   SELECT dd.device_type, dd.network_type,
          COUNT(*) as message_count,
          AVG(me.server_received_timestamp - me.message_timestamp) as avg_delivery_latency,
          PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY 
             (me.server_received_timestamp - me.message_timestamp)) as p95_latency
   FROM fact_message_events me
   JOIN dim_devices dd ON me.device_key = dd.device_key
   JOIN dim_dates d ON me.date_key = d.date_key
   WHERE d.full_date = CURRENT_DATE - INTERVAL '1 day'
   GROUP BY dd.device_type, dd.network_type
   ORDER BY avg_delivery_latency DESC;
   ```

### Privacy Considerations

1. **Message Content Handling**:
   - No storage of raw message content in the data model
   - Topic derivation performed in a secure pipeline before storage
   - Sentiment scores and other derived fields don't retain original text
   - End-to-end encrypted conversations marked as such for appropriate handling

2. **Data Retention**:
   - Implement appropriate retention policies by table
   - Consider different retention for events vs. aggregates
   - Support purging of individual user data for compliance
   - Aggregate data at higher levels for long-term storage

3. **Access Controls**:
   - Define strict access policies for raw event data
   - Prefer access to aggregated metrics tables for general analytics
   - Implement row-level security for user-specific data
   - Log all access to messaging analytics for audit purposes

### Implementation Considerations

1. **Data Collection Pipeline**:
   - Client-side logging with privacy filtering before transmission
   - Server-side event processing with topic extraction
   - Daily aggregation processes for metrics tables
   - Real-time streams for operational monitoring

2. **Performance Optimization**:
   - Partitioning of fact tables by date
   - Clustered indexes on high-cardinality joins
   - Materialized views for common analytical queries
   - Consider columnar storage for analytical workloads

3. **Sampling Strategy**:
   - For very high volume messaging platforms, consider:
     - 100% capture of metadata but sampled topic extraction
     - Full data for recent periods (7-30 days)
     - Sampled data for historical analysis
     - Stratified sampling to ensure representation

### Trade-offs and Alternatives

1. **Derived Topics Approach**:
   - Current model uses a separate table for derived topics
   - Alternative: Store topic vectors in fact_message_events
   - Trade-off: Simpler queries vs. flexibility for multiple topics

2. **Aggregation Levels**:
   - Current model uses daily aggregation
   - Alternatives:
     - Real-time counters for operational metrics
     - Hourly aggregation for more granular patterns
     - Weekly/monthly rollups for long-term trends

3. **Conversation Hierarchies**:
   - Current model treats each conversation independently
   - Alternative approaches:
     - Model conversation splitting/merging
     - Track conversation groups/folders
     - Implement hierarchical conversation relationships

### Extensibility Considerations

1. **Supporting New Message Types**:
   - Flexible message_type dimension allows adding new types
   - JSON metadata field accommodates type-specific attributes
   - New derived topics can be added without schema changes

2. **International Considerations**:
   - Support for language identification in topic extraction
   - Character count tracking considers multi-byte characters
   - Time fields include timezone information for global analysis

3. **Feature Experimentation**:
   - Device dimension includes app version for feature segmentation
   - Conversation metadata can store experiment assignments
   - User preferences capture feature opt-ins/settings

This comprehensive model balances analytical needs with privacy considerations, providing robust support for messaging pattern analysis, topic identification, and performance monitoring without compromising user privacy by storing message content. 