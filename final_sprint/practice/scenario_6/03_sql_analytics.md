# Problem 3: SQL Analytics - Follow Success & PYMK Effectiveness
**Time Limit: 8 minutes**

## Scenario
Using your social graph schema, write SQL queries to analyze follow success rates, PYMK effectiveness, and identify opportunities to improve friend recommendations, especially considering private accounts.

## Sample Schema (Use this for your queries)
```sql
-- User relationship table (bidirectional for friends, unidirectional for follows)
-- For friendships, two rows exist: user_a -> user_b AND user_b -> user_a
-- For follows, one row: follower_user_id -> following_user_id
fact_user_relationships (
    user_id_from BIGINT,       -- e.g., follower_user_id or friend_user_id_a
    user_id_to BIGINT,         -- e.g., following_user_id or friend_user_id_b
    relationship_type VARCHAR(10), -- 'friend', 'follow'
    status VARCHAR(10),        -- 'active', 'pending_approval' (for private follows)
    created_timestamp TIMESTAMP,
    updated_timestamp TIMESTAMP,
    date_partition DATE,
    PRIMARY KEY (user_id_from, user_id_to, relationship_type) 
);

-- User privacy settings
dim_user_privacy (
    user_id BIGINT PRIMARY KEY,
    profile_visibility VARCHAR(10), -- 'public', 'private', 'friends_only'
    can_receive_follow_requests_from VARCHAR(10), -- 'everyone', 'friends_of_friends'
    updated_timestamp TIMESTAMP
);

-- PYMK suggestions shown to users
fact_pymk_suggestions (
    suggestion_id VARCHAR(50) PRIMARY KEY,
    suggester_user_id BIGINT,    -- User who sees the suggestion
    suggested_user_id BIGINT,  -- User being suggested
    suggestion_source VARCHAR(50), -- 'mutual_friends', 'contact_upload', 'group_membership'
    suggestion_timestamp TIMESTAMP,
    date_partition DATE
);

-- Follow/Friend requests sent (captures the initiation of a request)
fact_follow_requests (
    request_id VARCHAR(50) PRIMARY KEY,
    requester_user_id BIGINT,
    receiver_user_id BIGINT,
    request_status VARCHAR(10), -- 'pending', 'accepted', 'declined', 'ignored' 
    request_timestamp TIMESTAMP,
    resolved_timestamp TIMESTAMP, -- When the request was accepted/declined/ignored
    pymk_suggestion_id VARCHAR(50), -- If originated from a PYMK suggestion
    date_partition DATE
);

-- User dimension
dim_users (
    user_id BIGINT PRIMARY KEY,
    registration_date DATE,
    country_code VARCHAR(2),
    is_private_profile BOOLEAN, -- Derived from dim_user_privacy.profile_visibility = 'private'
    last_active_timestamp TIMESTAMP
);
```

## Your Task

### Query 1: Follow Request Acceptance Rate (3 minutes)
**Business Question**: What is the overall follow request acceptance rate in the last 30 days, and how does it differ for requests sent to public vs. private accounts?

**Requirements**:
- Calculate total requests sent and total requests accepted.
- Acceptance Rate = (Accepted Requests / Total Sent Requests) * 100.
- Break down by `receiver_user_id`'s profile type (public vs. private).

*Write the SQL query*

### Query 2: PYMK Suggestion Effectiveness (3 minutes)
**Business Question**: For PYMK suggestions shown in the last 7 days, what percentage led to a follow request being sent? How does this vary if the suggested user has a private profile?

**Requirements**:
- Identify PYMK suggestions that resulted in a follow request.
- Effectiveness = (Requests Sent from PYMK / Total PYMK Suggestions Shown) * 100.
- Segment by the `suggested_user_id`'s profile type.

*Write the SQL query*

### Query 3: Mutual Friends Count for Pending Requests (2 minutes)
**Business Question**: For pending follow requests to private accounts, what is the distribution of mutual friends between the requester and receiver? 

**Requirements**:
- Focus on `pending` requests where `receiver_user_id` has a private profile.
- Calculate the number of mutual friends for each such pending request.
- Show the count of requests for each mutual friend count (e.g., 0 mutual friends: X requests, 1 mutual friend: Y requests).

*Write the SQL query. Hint: You'll need to find common friends between requester and receiver.*

## Follow-up Questions
Be prepared to discuss:
- How would you define a "successful" PYMK suggestion if it involves a private account where the request is *not* accepted, but the receiver views the requester's profile?
- What are the limitations of using `is_private_profile` in `dim_users` if `dim_user_privacy` is the source of truth and can change?
- How would you optimize the mutual friends query for users with millions of friends?
- How can you identify PYMK suggestions that are leading to a high rate of declined/ignored requests, especially for private accounts?

## Technical Constraints
- **Data Volume**: User relationships can be in the trillions.
- **Performance**: Queries for dashboards need to be efficient.
- **Privacy**: Ensure no PII is exposed inadvertently.

## Success Criteria
- **Correct SQL logic** for calculating rates and segmenting by profile type.
- **Efficient querying of graph-like data** (e.g., mutual friends).
- **Understanding of privacy implications** in query design.

## Meta Context
- Understanding follow dynamics is key to social graph health.
- PYMK effectiveness is a core growth metric.
- Balancing suggestion relevance with user privacy for private accounts is a constant challenge. 