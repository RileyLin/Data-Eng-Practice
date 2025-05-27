# Data Modeling Challenges

This document contains data modeling challenges from the study guide, organized by scenario.

## Scenario 1: Ride Sharing (Uber/Lyft) - Carpooling Feature

### Challenge 1.2.1: Carpool Ride Model

**Description:**  
How should the data model be designed to support carpool rides where a single ride (ride_id) can involve multiple passengers picked up and dropped off at potentially different locations and times within the same driver's trip? Discuss trade-offs.

**Key Considerations:**
- Core Tables: fact_rides, dim_users, dim_locations, dim_date, dim_time, dim_ride_type
- Handling Multiple Riders: Bridge table approach vs. array/JSON approach
- Trade-offs in normalization, query flexibility, and scalability

**Recommended Model:**
```
fact_rides:
- ride_id (PK)
- driver_user_key (FK)
- ride_type_key (FK)
- vehicle_key (FK)
- start_location_key (FK)
- end_location_key (FK)
- start_timestamp
- end_timestamp
- total_fare
- total_distance
- total_duration
- date_key (FK)
- time_key (FK)

fact_ride_segments:
- ride_segment_id (PK)
- ride_id (FK)
- rider_user_key (FK)
- segment_pickup_timestamp
- segment_dropoff_timestamp
- segment_pickup_location_key (FK)
- segment_dropoff_location_key (FK)
- segment_fare
- segment_distance
- pickup_sequence_in_ride
- dropoff_sequence_in_ride
```

## Scenario 2: Short Video (TikTok/Reels) - Sharing Focus

### Challenge 2.2.1: Engagement Events Model

**Description:**  
Design a data model for engagement events (like, comment, share, view) that can efficiently handle posts shared potentially thousands or millions of times, across multiple layers (User A shares Post P -> User B shares A's share -> User C shares B's share, etc.). The model must support efficiently counting total shares per original post and identifying the original poster and post time.

**Key Considerations:**
- **Share Chain/Tree Tracking:** How to represent the lineage of shares (e.g., parent_share_id, depth_level).
- **Original Post Identification:** Easy linkage from any share back to the original content item.
- **Aggregation Efficiency:** Designing for fast counts of total shares, likes, etc., per original post.
- **Viral Content Handling:** Ensuring the model scales for posts with massive engagement and share depth.
- **Event Types:** Clearly distinguishing between different engagement types (like, comment, view, different types of shares).
- **Timestamps:** Capturing timestamps for original post creation and each subsequent engagement event.
- **User Identification:** Linking events to the acting user (who liked, shared, commented) and the original content creator.

## Scenario 3: Streaming Platform (Netflix/Hulu)

### Challenge 3.2.1: Viewing Sessions Table

**Description:**  
Design the fact_viewing_sessions table. What are its key measures and foreign keys? How would you handle tracking view duration, pauses, and completion status?

**Key Considerations:**
- **Granularity:** What defines a "viewing session"? (e.g., a continuous block of viewing, or all viewing for a user-content pair within a day).
- **Core Measures:**
    - `view_duration_seconds` (total time content was played).
    - `max_viewed_progress_seconds` (furthest point reached in the content).
    - `completion_flag` (boolean: if content was fully watched).
    - `number_of_pauses`.
    - `total_pause_duration_seconds`.
- **Foreign Keys:**
    - `user_key` (linking to a user dimension).
    - `content_key` (linking to a content dimension - movie, episode).
    - `profile_key` (if multiple profiles per user account).
    - `device_key` (linking to a device dimension).
    - `date_key`, `time_key` (for start time of session).
- **Handling Pauses & Resumes:** May require logging discrete play/pause events and aggregating them into a session, or storing an array of pause intervals.
- **Tracking Partial Views:** `max_viewed_progress_seconds` and `view_duration_seconds` help quantify this.
- **Multiple Sessions for Same Content:** Users might watch content in multiple sittings; each sitting could be a distinct session or aggregated.
- **Support for Analytics:** Model should easily support queries for content popularity, user engagement patterns (e.g., average completion rates by genre), and identifying content with high drop-off rates.
- **Buffering/Errors:** Potentially include fields to track buffering events or playback errors within a session.

## Scenario 4: Cloud File Storage (Dropbox/Google Drive)

### Challenge 4.2.1: File Sharing Model

**Description:**  
Design a data model for a file sharing system that supports different permission levels (view, comment, edit) and both individual and group-based sharing. The model should efficiently support queries like "show all files shared with me" and "who has access to this file?"

**Key Considerations:**
- **Entities:** `files`, `users`, `groups`.
- **Permissions Management:**
    - `permission_levels` (e.g., 'view', 'comment', 'edit', 'owner').
    - Storing direct user-file permissions.
    - Storing group-file permissions.
- **Membership:** `group_memberships` table linking users to groups.
- **Query Efficiency:**
    - For "files shared with me": Requires checking direct shares and shares via groups the user belongs to. This can be complex if groups are nested.
    - For "who has access to this file": Requires checking direct shares and expanding group shares to individual users.
- **Inheritance (Folder-based sharing):** If sharing a folder implies sharing its contents, how is this modeled and queried? (e.g., recursive queries or denormalized access lists).
- **Storage Efficiency for Popular Files:** Avoid massive duplication of permission entries for widely shared files.
- **Revoking Access:** How efficiently can permissions be revoked for a user or group?
- **Audit Trail:** Optionally, track when permissions were granted/revoked.

## Scenario 5: DAU/MAU Analysis

### Challenge 5.2.1: User Activity Tracking

**Description:**  
Design a data model to efficiently support DAU, WAU, and MAU calculations across different product features, allowing slicing by user demographics, device types, and geographic regions.

**Key Considerations:**
- **Event Granularity:** Log individual user actions with `user_id`, `timestamp`, `feature_name_used`, and other relevant dimensions.
- **User Activity Fact Table:** A central table like `fact_user_activity` with:
    - `user_key` (FK to `dim_users`).
    - `date_key` (FK to `dim_date`).
    - `feature_key` (FK to `dim_features`).
    - `device_key` (FK to `dim_devices`).
    - `geo_key` (FK to `dim_geography`).
    - Potentially a flag or distinct event type for "active session start" or "key feature interaction."
- **Time Grain of Data Collection:** Events should be timestamped accurately. For DAU/WAU/MAU, daily aggregation is the minimum.
- **Pre-aggregation Strategies:**
    - A daily active user table (`fact_daily_active_users`) with `user_key`, `date_key`, and dimension keys can speed up DAU/WAU/MAU. This table would have one row per active user per day.
    - This pre-aggregated table makes `COUNT(DISTINCT user_key)` queries very fast for specific date ranges.
- **Handling High Cardinality Dimensions:** Slicing by many dimensions can lead to performance issues. Careful indexing and possibly further aggregation might be needed.
- **Definition of "Active":** Clearly define what constitutes an "active" user for a given feature or overall (e.g., app open, specific interaction).
- **Dimension Tables:** `dim_users` (with demographics), `dim_features`, `dim_devices`, `dim_geography`, `dim_date`.
- **Scalability:** Model should handle billions of events and millions of users.

## Scenario 6: News Feed

### Challenge 6.2.1: Feed Events Logging

**Description:**  
Design a data model for logging user interactions with a news feed, including impressions, views, scrolls, and engagement events. The model should support analyzing content performance and personalizing the feed algorithm.

**Key Considerations:**
- **Event Granularity:** Each interaction (impression, view, click, like, share, comment, scroll depth reached) should be a distinct event.
- **Core Entities:** `users`, `content_items`, `events`.
- **Fact Table (`fact_feed_events`):**
    - `user_key`, `content_item_key`, `event_type_key`, `timestamp`, `session_id`.
    - `position_in_feed` (important for CTR, visibility analysis).
    - `view_duration_ms` (for view events).
    - `visibility_percentage` (for impression/view events).
    - `scroll_depth_pixels_or_percentage` (for scroll events).
- **Dimension Tables:** `dim_users`, `dim_content_items` (with metadata like publisher, topic), `dim_event_types`, `dim_date`, `dim_time`.
- **Handling High Volume of Impression Events:** Impressions can be massive. Consider sampling, aggregation strategies, or partitioning if raw event storage is too costly/slow for all use cases.
- **Sessionization:** Grouping events by `session_id` is crucial for understanding user journeys within the feed.
- **Supporting Personalization:** The model must capture signals that feed into ML models (e.g., positive/negative interactions, dwell time).
- **Content Performance Analytics:** Enable calculation of CTR, engagement rates, view-through rates per content item, topic, publisher.

## Scenario 7: Photo Upload (Instagram-like)

### Challenge 7.2.1: Photo Upload Pipeline

**Description:**  
Design a data model to track the photo upload process from initiation to completion, including failure points and metadata extraction. The model should support analyzing upload success rates by device type, network connection, and app version.

**Key Considerations:**
- **Upload Event Funnel:** Track distinct stages of the upload:
    - `upload_initiated`, `media_selected`, `editing_started`, `metadata_added` (caption, tags), `upload_transfer_started`, `upload_transfer_progress`, `upload_completed` (client-side), `upload_processed_server_side` (server-side confirmation).
- **Fact Table (`fact_upload_attempts` or `fact_upload_events`):**
    - Each row could represent an upload attempt or a specific event within an attempt.
    - `upload_attempt_id` (to group events for one attempt).
    - `user_key`, `timestamp_event`, `event_name` (stage name).
    - `status` (success, failure, in_progress for the event or overall attempt).
    - `failure_reason` (if applicable, categorized).
    - `error_code`.
- **Dimensions:**
    - `dim_users`.
    - `dim_devices` (including `os_version`, `app_version`).
    - `dim_network_types` (Wi-Fi, 4G, 5G).
    - `dim_date`, `dim_time`.
- **Metadata Storage:**
    - `file_size`, `image_resolution`, `video_duration` (if applicable).
    - Extracted metadata (e.g., EXIF data, number of faces detected) could be stored with the final uploaded item or linked to the upload attempt.
- **Error Classification:** Standardized error codes and reasons for better analysis of failure points.
- **Performance Metrics:** Track duration of each stage (e.g., `edit_time_ms`, `transfer_time_ms`).
- **Scalability:** Handle potentially millions of upload attempts daily.

## Scenario 8: FB Messenger

### Challenge 8.2.1: Messaging Activity Model

**Description:**  
Design a data model for tracking messaging activity that efficiently supports analytics around user engagement patterns, popular conversation topics, and message delivery performance.

**Key Considerations:**
- **Core Entities:** `users`, `conversations` (or `threads`), `messages`.
- **`fact_messages` Table:**
    - `message_id` (PK).
    - `conversation_id` (FK).
    - `sender_user_key` (FK).
    - `timestamp_sent`, `timestamp_delivered_to_recipient`, `timestamp_read_by_recipient`.
    - `message_type` (text, image, video, reaction, etc.).
    - `message_length` (for text messages).
- **`dim_conversations` Table:**
    - `conversation_id` (PK).
    - `conversation_type` (one-on-one, group).
    - `creation_timestamp`.
    - `last_activity_timestamp`.
- **Participant Bridge Table (for group conversations):** `bridge_conversation_participants(conversation_id, user_key, joined_timestamp)`.
- **Message Content Privacy:** Message content itself is usually not stored in analytical data models for privacy reasons. Analysis focuses on metadata.
- **High-Volume Write Performance:** Messaging systems generate vast amounts of data; schema should be optimized for writes.
- **Conversation Threading:** Ensuring messages are correctly linked to their conversations.
- **Engagement Metrics Support:** Model should allow calculating messages sent/received per user, active conversations, use of rich media, response times (metadata-based).
- **Topic Analysis (Metadata-based):** If messages are tagged with topics (e.g., using NLP on aggregated, anonymized data, or if users use topic tags), this could be linked. More likely, topic analysis happens outside the core transactional model.
- **Delivery Performance:** Use timestamps to analyze delivery speed and failure rates.

## Scenario 9: Food Delivery (DoorDash) - Order Batching

### Challenge 9.2.1: Order Batching Model

**Description:**  
Design a data model for order batching that can track orders grouped together for delivery, including pick-up and drop-off sequence, timing data, and driver information. The model should support analyzing the efficiency of different batching algorithms and their impact on delivery times.

**Key Considerations:**
- **Core Entities:** `orders`, `drivers`, `batches`, `restaurants`, `customers`.
- **`fact_orders` Table:** Standard order details.
- **`dim_batches` Table (or `fact_batched_trips`):**
    - `batch_id` (PK) or `batched_trip_id`.
    - `driver_key` (FK).
    - `batch_creation_timestamp`.
    - `algorithm_version_used` (to compare different batching algorithms).
    - `planned_total_duration`, `actual_total_duration`.
    - `planned_total_distance`, `actual_total_distance`.
- **Order-Batch Bridge Table:** `bridge_batch_orders`
    - `batch_id` (FK).
    - `order_id` (FK).
    - `pickup_sequence_in_batch` (e.g., 1st restaurant, 2nd restaurant).
    - `dropoff_sequence_in_batch` (e.g., 1st customer, 2nd customer).
    - `planned_pickup_time`, `actual_pickup_time`.
    - `planned_dropoff_time`, `actual_dropoff_time`.
- **Restaurant Pickups within a Batch:** May need a separate table or details in `bridge_batch_orders` if multiple pickups from same or different restaurants occur for a batch.
- **Tracking Planned vs. Actual:** Crucial for analyzing algorithm efficiency and real-world deviations.
- **Timing Data:** Granular timestamps for all key events (batch assigned, arrival at restaurant, order picked up, arrival at customer, order delivered) for each order within the batch.
- **Supporting Optimization Algorithms:** The model should provide data to evaluate and improve batching logic (e.g., what types of orders are best batched, optimal batch sizes).
- **Driver Route Information:** Potentially link to planned vs. actual GPS route data. 