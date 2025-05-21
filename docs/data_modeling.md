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
- Tracking share chains/trees
- Optimizing for counting aggregations
- Handling viral content efficiently

## Scenario 3: Streaming Platform (Netflix/Hulu)

### Challenge 3.2.1: Viewing Sessions Table

**Description:**  
Design the fact_viewing_sessions table. What are its key measures and foreign keys? How would you handle tracking view duration, pauses, and completion status?

**Key Considerations:**
- Tracking partial views
- Handling multiple viewing sessions of the same content
- Supporting analytics for content popularity and user engagement

## Scenario 4: Cloud File Storage (Dropbox/Google Drive)

### Challenge 4.2.1: File Sharing Model

**Description:**  
Design a data model for a file sharing system that supports different permission levels (view, comment, edit) and both individual and group-based sharing. The model should efficiently support queries like "show all files shared with me" and "who has access to this file?"

**Key Considerations:**
- Permission inheritance
- Group vs. individual permissions
- Storage efficiency for popular files

## Scenario 5: DAU/MAU Analysis

### Challenge 5.2.1: User Activity Tracking

**Description:**  
Design a data model to efficiently support DAU, WAU, and MAU calculations across different product features, allowing slicing by user demographics, device types, and geographic regions.

**Key Considerations:**
- Time grain of data collection
- Pre-aggregation strategies
- Handling high cardinality dimensions

## Scenario 6: News Feed

### Challenge 6.2.1: Feed Events Logging

**Description:**  
Design a data model for logging user interactions with a news feed, including impressions, views, scrolls, and engagement events. The model should support analyzing content performance and personalizing the feed algorithm.

**Key Considerations:**
- Event granularity
- Handling high volume of impression events
- Supporting session-based analysis

## Scenario 7: Photo Upload (Instagram-like)

### Challenge 7.2.1: Photo Upload Pipeline

**Description:**  
Design a data model to track the photo upload process from initiation to completion, including failure points and metadata extraction. The model should support analyzing upload success rates by device type, network connection, and app version.

**Key Considerations:**
- Event sequence tracking
- Error classification
- Metadata storage optimization

## Scenario 8: FB Messenger

### Challenge 8.2.1: Messaging Activity Model

**Description:**  
Design a data model for tracking messaging activity that efficiently supports analytics around user engagement patterns, popular conversation topics, and message delivery performance.

**Key Considerations:**
- Message content privacy
- High-volume write performance
- Conversation threading

## Scenario 9: Food Delivery (DoorDash) - Order Batching

### Challenge 9.2.1: Order Batching Model

**Description:**  
Design a data model for order batching that can track orders grouped together for delivery, including pick-up and drop-off sequence, timing data, and driver information. The model should support analyzing the efficiency of different batching algorithms and their impact on delivery times.

**Key Considerations:**
- Representing order sequences within batches
- Tracking planned vs. actual routes
- Supporting optimization algorithms 