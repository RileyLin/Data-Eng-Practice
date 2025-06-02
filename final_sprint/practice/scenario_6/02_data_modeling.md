# Problem 2: Data Modeling - Friendships, Follows & Privacy
**Time Limit: 8 minutes**

## Scenario
Design a data model to represent user relationships (friendships, follows), follow requests, and privacy settings. This schema needs to support the PYMK feature, including suggestions for both public and private accounts, and allow for analysis of follow success rates.

## Requirements
- **Scale**: Billions of users, trillions of potential relationships.
- **Relationship Types**: Support Facebook-style friendships (bidirectional) and Instagram-style follows (unidirectional).
- **Privacy Settings**: Model user profile privacy (public, private) and who can send follow/friend requests.
- **Request Lifecycle**: Track follow/friend requests (pending, accepted, declined, ignored).
- **PYMK Support**: Schema should efficiently query for mutual friends and other signals for friend recommendations.

## Your Task

### Part A: Core Schema Design (5 minutes)
**Design the main fact and dimension tables for:**

1.  **User Relationships**: Store established friendships and follows.
2.  **User Privacy Settings**: Capture individual user privacy preferences.
3.  **Follow/Friend Requests**: Track the state and outcome of connection attempts.

*Consider how to efficiently query for a user's friends/followers, and how to check if a follow request is allowed based on privacy settings.*

### Part B: Handling Private Accounts (3 minutes)
**Question**: How does your schema specifically address the challenges of private accounts in the context of follow requests and PYMK?

*Consider: How do you prevent unauthorized profile data exposure for private accounts when they appear in PYMK? How do you model the "request to follow" flow for private accounts?*

## Follow-up Questions
Be prepared to discuss:
- How would you model "Close Friends" or other custom friend lists?
- How would your schema handle blocking users?
- What indexing strategy would you use for querying mutual friends between two users efficiently?
- How would you ensure data consistency if a user changes their privacy settings frequently?
- How would you denormalize parts of this schema for faster PYMK candidate generation?

## Technical Constraints
- **Query Latency**: Checking friendship status or follow status should be <10ms.
- **Storage Efficiency**: Minimize redundancy given the scale.
- **Write Throughput**: Support millions of new follow requests and relationship changes per minute.
- **Data Integrity**: Ensure that relationships and privacy rules are consistently enforced.

## Success Criteria
- **Comprehensive schema** that covers all specified entities and relationships.
- **Efficient design** for common queries (e.g., fetching friends, checking privacy).
- **Clear handling of private account logic** within the data model.
- **Scalability and performance considerations** evident in the design choices.

## Meta Context
- The social graph is the core of Meta's platforms.
- Efficiently querying relationships is critical for many features beyond PYMK.
- Privacy-by-design is a fundamental principle for any social graph data model at Meta. 