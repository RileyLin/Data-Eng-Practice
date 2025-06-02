# Interview Preparation - Bucket Organization

## Overview
This directory contains interview preparation materials organized into 3 realistic buckets based on actual tech company interview patterns. Each scenario includes 4 comprehensive question types that mirror real interview experiences.

## Bucket Structure

### 🚛 Bucket 1: Delivery & Marketplace Platforms
**Focus**: Logistics optimization, marketplace dynamics, operational efficiency

#### ✅ Scenario 1: Ridesharing (Uber/Lyft) - COMPLETE
- **Product Sense**: Carpool feature development, market expansion strategy
- **Data Modeling**: Star schema with ride, driver, passenger entities
- **SQL Questions**: 6 comprehensive queries covering capacity, efficiency, matching
- **Python Questions**: 3 algorithmic challenges (overlapping rides, route optimization, driver matching)

#### ✅ Scenario 5: DAU/MAU Analysis - COMPLETE  
- **Product Sense**: Beyond basic stickiness metrics, engagement depth analysis
- **Data Modeling**: User activity tracking with detailed engagement events
- **SQL Questions**: 6 complex queries for user retention and engagement patterns
- **Python Questions**: Session processing and engagement calculation algorithms

#### ✅ Scenario 9: Order Batching (DoorDash) - COMPLETE
- **Product Sense**: Delivery optimization strategy, stakeholder metrics framework
- **Data Modeling**: Batch-centric design with route optimization support  
- **SQL Questions**: 5 delivery efficiency and geographic analysis queries
- **Python Questions**: Batch feasibility, route optimization, and performance analytics

#### ✅ Scenario 11: Restaurant Focus (DoorDash) - COMPLETE
- **Product Sense**: Restaurant metrics, revenue decline analysis, dashboard design
- **Data Modeling**: Restaurant-focused analytics with performance tracking
- **SQL Questions**: Restaurant averages and delivery time comparisons
- **Python Questions**: Delivery time calculation with driver action tracking

### 📱 Bucket 2: Social & Content Platforms  
**Focus**: User engagement, content virality, social graph optimization

#### ✅ Scenario 2: Short Video (TikTok/Reels) - COMPLETE
- **Product Sense**: Content creator metrics, engagement optimization, viral growth
- **Data Modeling**: Content-centric design with engagement and recommendation support
- **SQL Questions**: 6 viral content, creator performance, and discovery analysis queries
- **Python Questions**: Video view validation, recommendation engine, viral detection

#### ✅ Scenario 6: News Feed (Facebook/LinkedIn) - COMPLETE
- **Product Sense**: Feed ranking algorithm, engagement optimization
- **Data Modeling**: News feed interaction model with content sources and ranking signals
- **SQL Questions**: 6 queries on valid reads, source performance, negative feedback, feed position, and peak hours.
- **Python Questions**: Newsfeed view validation, feed ranking algorithm, content diversity algorithm

#### ✅ Scenario 7: Photo Upload (Instagram/Snapchat) - COMPLETE
- **Product Sense**: Optimizing photo upload experience, metrics for AI enhancement.
- **Data Modeling**: Tracking photo upload events, image metadata, editing, and success/failure.
- **SQL Questions**: 6 queries on upload success by device/network, impact of image attributes, editing tool adoption, funnel analysis, and retry behavior.
- **Python Questions**: Photo upload processing, EXIF data extraction, and upload failure risk prediction.

#### ✅ Scenario 8: Messenger (WhatsApp/Telegram) - COMPLETE
- **Product Sense**: Ephemeral messaging feature development, metrics for message reactions.
- **Data Modeling**: Core messaging entities, interactions, group dynamics, reactions, ephemeral settings.
- **SQL Questions**: 6 queries on DAU/message volume, group vs 1:1 activity, reaction popularity, ephemeral usage, unread analysis, time-to-read.
- **Python Questions**: Message stream processing, E2EE simulation, user message rate limiting.

#### ✅ Scenario 10: PYMK (People You May Know) - COMPLETE
- **Product Sense**: Social graph optimization, privacy-aware recommendations
- **Data Modeling**: [Planned]
- **SQL Questions**: User connections analysis (q011 available)
- **Python Questions**: Friend recommendation algorithm, social graph analysis, privacy filtering

### 🎬 Bucket 3: Consumption & Storage Platforms
**Focus**: Content delivery, storage optimization, user viewing patterns

#### ✅ Scenario 3: Streaming (Netflix/YouTube) - COMPLETE
- **Product Sense**: Content recommendation strategy, A/B testing new discovery UI.
- **Data Modeling**: Users, content hierarchy (movies, series, episodes), viewing history, ratings, recommendation support.
- **SQL Questions**: 6 queries on content popularity, user engagement, binge-watching, genre combinations, rating impact on completion, drop-off analysis.
- **Python Questions**: Average content ratings, content-based recommendations, simulating viewing sessions with dynamic recommendations.

#### ✅ Scenario 4: Cloud Storage (Dropbox/Google Drive) - COMPLETE
- **Product Sense**: Strategies for increasing collaboration feature adoption, metrics for a new "smart organization" feature.
- **Data Modeling**: Star schema for users, files, folders, sharing, collaboration activities, storage consumption.
- **SQL Questions**: 6 queries on storage utilization, file types, active collaborators, orphaned files, sharing activity, folder collaboration intensity.
- **Python Questions**: File deduplication, shared link management API, user activity report generator.

## Question Type Structure

Each scenario follows a consistent 4-question format:

### 1. Product Sense
- **Market Analysis**: Product positioning and competitive landscape
- **Feature Development**: Design rationale and success metrics
- **Stakeholder Considerations**: User, business, and technical perspectives
- **Growth Strategy**: Scaling and optimization approaches

### 2. Data Modeling  
- **Entity Relationship Diagrams**: Comprehensive data architecture using Mermaid
- **Star Schema Design**: Fact and dimension table specifications
- **Business Rules**: Key constraints and calculation logic
- **Performance Considerations**: Indexing and optimization strategies

### 3. SQL Questions
- **Complexity Range**: 4-6 questions from intermediate to advanced
- **Business Context**: Real-world analytics scenarios
- **Performance Focus**: Efficient query patterns and optimization
- **Schema Integration**: Leveraging the designed data model

### 4. Python Questions
- **Algorithm Design**: Core computational challenges
- **Data Processing**: Stream processing and aggregation
- **System Design**: Scalable solution architectures  
- **Testing**: Comprehensive test cases and validation

## Current Completion Status

**✅ Fully Implemented (11/11 scenarios):**
- Scenario 1: Ridesharing (Uber/Lyft)
- Scenario 2: Short Video (TikTok/Reels)
- Scenario 3: Streaming (Netflix/YouTube)
- Scenario 4: Cloud Storage (Dropbox/Google Drive)
- Scenario 5: DAU/MAU Analysis
- Scenario 6: News Feed (Facebook/LinkedIn)
- Scenario 7: Photo Upload (Instagram/Snapchat)
- Scenario 8: Messenger (WhatsApp/Telegram)
- Scenario 9: Order Batching (DoorDash)
- Scenario 10: PYMK (People You May Know)
- Scenario 11: Restaurant Focus (DoorDash)

**🚧 In Progress (0/11 scenarios):**

## Usage Instructions

### For Interview Preparation:
1. **Choose Your Target Bucket**: Select based on the type of company you're interviewing with
2. **Complete Full Scenarios**: Work through all 4 question types for comprehensive preparation  
3. **Time Yourself**: Practice with realistic time constraints
4. **Focus on Explanation**: Emphasize your thought process and trade-off considerations

### For Interviewers:
1. **Scenario Selection**: Pick scenarios matching your company's domain
2. **Progressive Difficulty**: Start with product sense, build up to technical implementation
3. **Adaptive Questioning**: Use follow-up questions based on candidate responses
4. **Comprehensive Evaluation**: Assess across product, analytical, and technical dimensions

## File Organization

```
buckets/
├── README.md (this file)
├── bucket1_delivery_marketplace/
│   ├── scenario1_ridesharing/
│   ├── scenario5_dau_mau/
│   ├── scenario9_order_batching/
│   └── scenario11_restaurant_focus/
├── bucket2_social_content/
│   ├── scenario2_short_video/
│   ├── scenario6_news_feed/
│   ├── scenario7_photo_upload/
│   ├── scenario8_messenger/
│   └── scenario10_pymk/
└── bucket3_consumption_storage/
    ├── scenario3_streaming/
    └── scenario4_cloud_storage/
```

Each scenario directory contains:
- `product_sense.md`
- `data_modeling.md` 
- `sql_questions.md`
- `python_questions.md`

## Next Steps

**Priority 1**: Add setup scripts for each scenario's database schema
**Priority 2**: Create comprehensive testing framework for Python solutions
**Priority 3**: Add difficulty ratings and time estimates for each question 