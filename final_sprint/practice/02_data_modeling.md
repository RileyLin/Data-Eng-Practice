# Problem 2: Data Modeling - Reels Analytics Schema
**Time Limit: 8 minutes**

## Scenario
You need to design a data warehouse schema to support Reels analytics. The system must track user viewing sessions, video interactions, and creator performance while handling Meta's massive scale.

## Requirements
- **Scale**: 2B+ events per day, 100M+ daily active users
- **Real-time**: Support sub-second recommendation updates
- **Analytics**: Enable complex session and creator analytics
- **Compliance**: Support data retention and user deletion policies

## Your Task

### Part A: Core Schema Design (4 minutes)
**Design the main fact and dimension tables for:**

1. **User Sessions**: Track how users move through multiple videos
2. **Video Interactions**: Capture all engagement events (views, likes, shares, comments)
3. **Creator Analytics**: Support creator dashboard metrics

**Required Events to Model:**
- `video_view_start`, `video_view_end`
- `like`, `unlike`, `share`, `comment`
- `session_start`, `session_end`
- `follow_creator`, `unfollow_creator`

### Part B: Partitioning Strategy (2 minutes)
**Question**: How would you partition your tables for optimal performance?

*Consider: Query patterns, data retention, and real-time requirements*

### Part C: Late Data Handling (2 minutes)
**Question**: How would you handle events that arrive hours or days late?

*Consider: Mobile offline scenarios and system failures*

## Follow-up Questions
Be prepared to discuss:
- How would you model viral share chains for videos?
- What indexes would you create for common queries?
- How would you handle schema evolution as features change?
- What's your strategy for real-time vs batch processing?

## Technical Constraints
- **Storage**: Optimize for both OLTP (real-time) and OLAP (analytics)
- **Privacy**: Support GDPR deletion and data anonymization
- **Performance**: Sub-100ms lookup for recommendation serving
- **Cost**: Minimize storage and compute costs at scale

## Success Criteria
- **Scalable design** that handles Meta's data volume
- **Clear fact/dimension separation** following best practices
- **Practical partitioning** strategy with justification
- **Operational considerations** for real-world deployment 