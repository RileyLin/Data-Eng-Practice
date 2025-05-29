# Problem 2: Data Modeling - News Feed User Activity Schema
**Time Limit: 8 minutes**

## Scenario
Design a data warehouse schema to track user activity across Meta's News Feed for calculating DAU/MAU metrics and supporting retention analysis. The system must handle billions of daily interactions while supporting real-time engagement scoring.

## Requirements
- **Scale**: 3B+ daily user interactions across Facebook, Instagram
- **Real-time**: Support sub-second user activity updates
- **Analytics**: Enable cohort analysis, retention tracking, churn prediction
- **Cross-platform**: Track activity across Facebook, Instagram, WhatsApp
- **Privacy**: Support user data deletion and anonymization

## Your Task

### Part A: Core Schema Design (4 minutes)
**Design the main fact and dimension tables for:**

1. **User Sessions**: Track user engagement sessions across platforms
2. **Content Interactions**: Capture all engagement with posts, stories, ads
3. **User Journey**: Support funnel analysis and retention calculations

**Required Events to Model:**
- `session_start`, `session_end`
- `post_view`, `post_like`, `post_share`, `post_comment`
- `story_view`, `story_reaction`
- `feed_scroll`, `feed_refresh`
- `friend_request`, `message_sent`

**Key Metrics to Support:**
- DAU/MAU calculations by platform and globally
- Session duration and engagement depth
- User lifecycle stage transitions
- Content interaction rates

### Part B: Partitioning Strategy (2 minutes)
**Question**: How would you partition your tables for optimal DAU/MAU query performance?

*Consider: Time-based queries dominate, need for real-time updates, data retention policies*

### Part C: Cross-Platform Unification (2 minutes)
**Question**: How would you handle users active across multiple Meta platforms (Facebook + Instagram + WhatsApp)?

*Consider: Unified user identity, cross-platform activity aggregation, privacy constraints*

## Follow-up Questions
Be prepared to discuss:
- How would you model user lifecycle stages (new, active, at-risk, churned)?
- What approach would you take for incrementally updating DAU/MAU metrics?
- How would you handle time zone differences for global DAU calculations?
- What schema optimizations would support real-time churn prediction?

## Technical Constraints
- **Query Performance**: DAU/MAU queries must complete in <10 seconds
- **Storage Cost**: Optimize for 2+ years of historical data retention
- **Real-time Updates**: Support streaming inserts with <1 minute latency
- **Privacy Compliance**: Enable efficient user data deletion
- **Cross-region**: Support data residency requirements

## Success Criteria
- **Scalable design** for Meta's user base (3B+ monthly actives)
- **Efficient schema** optimized for time-series analysis
- **Cross-platform strategy** with unified user identity
- **Performance considerations** for real-time and batch workloads

## Meta Context
- DAU/MAU is calculated across all Meta platforms globally
- Different platforms have different engagement patterns
- Real-time alerting needed when DAU/MAU drops significantly
- Schema must support ML feature generation for personalization 