/*
Question 2.3.1: Posts with Zero Engagement on Creation Day

Write a SQL query to find post_ids for posts that received zero 'like' or 'react' events on the same calendar day they were created.

Schema based on setup_scripts/scenario_2_short_video_setup.sql:

dim_posts_shortvideo:
- post_key (INTEGER PRIMARY KEY AUTOINCREMENT)
- post_id (VARCHAR(50) UNIQUE NOT NULL) -- Public facing ID if different from post_key
- creator_user_key (INTEGER, FK to dim_users_shortvideo)
- original_post_key (INTEGER, FK to dim_posts_shortvideo) -- Self-ref for original post
- parent_post_key (INTEGER, FK to dim_posts_shortvideo) -- Post that was shared
- share_depth_level (INTEGER DEFAULT 0)
- created_timestamp (TEXT, ISO 8601 format)
- is_original (BOOLEAN DEFAULT TRUE)
- content_text (TEXT)
- video_url (TEXT)
- FOREIGN KEY (creator_user_key) REFERENCES dim_users_shortvideo(user_key)
- FOREIGN KEY (original_post_key) REFERENCES dim_posts_shortvideo(post_key)
- FOREIGN KEY (parent_post_key) REFERENCES dim_posts_shortvideo(post_key)

fact_engagement_events_shortvideo:
- event_id (INTEGER PRIMARY KEY AUTOINCREMENT)
- user_key (INTEGER, FK to dim_users_shortvideo) -- User performing engagement
- post_key (INTEGER, FK to dim_posts_shortvideo) -- Post being engaged with
- engagement_type_key (INTEGER, FK to dim_engagement_types_shortvideo)
- event_timestamp (TEXT, ISO 8601 format)
- event_date_key (INTEGER, FK to dim_date)
- event_time_key (INTEGER, FK to dim_time)
- event_metadata (TEXT, JSON stored as TEXT)
- FOREIGN KEY (user_key) REFERENCES dim_users_shortvideo(user_key)
- FOREIGN KEY (post_key) REFERENCES dim_posts_shortvideo(post_key)
- FOREIGN KEY (engagement_type_key) REFERENCES dim_engagement_types_shortvideo(engagement_type_key)
- FOREIGN KEY (event_date_key) REFERENCES dim_date(date_key)
- FOREIGN KEY (event_time_key) REFERENCES dim_time(time_key)

dim_engagement_types_shortvideo:
- engagement_type_key (INTEGER PRIMARY KEY AUTOINCREMENT)
- engagement_type_name (TEXT UNIQUE NOT NULL) -- e.g., 'view', 'like', 'comment', 'share', 'follow'
- description (TEXT)
- is_active (BOOLEAN DEFAULT TRUE)

dim_users_shortvideo:
- user_key (INTEGER PRIMARY KEY AUTOINCREMENT)
- user_id (VARCHAR(50) UNIQUE NOT NULL)
- username (TEXT)
- created_at (TEXT, ISO 8601 format)
- user_type (TEXT) -- e.g., 'creator', 'viewer'
- is_internal (BOOLEAN DEFAULT FALSE)

The question mentions 'like' or 'react' events. The `dim_engagement_types_shortvideo` table has 'like', 'comment', 'share', 'view'.
Assuming 'react' is similar to 'like' or perhaps a broader category.
For this solution, we will focus on 'like' as 'react' is not explicitly in the setup. If 'react' were present, it would be included in the IN clause.

Expected Output:
A list of post_ids that were created but received no 'like' (or 'react') events on their creation day.
*/

-- Write your SQL query here:
SELECT dp.post_id
FROM dim_posts_shortvideo dp
WHERE NOT EXISTS (
    SELECT 1
    FROM fact_engagement_events_shortvideo fees
    JOIN dim_engagement_types_shortvideo dets ON fees.engagement_type_key = dets.engagement_type_key
    WHERE fees.post_key = dp.post_key
      AND dets.engagement_type_name IN ('like', 'react') -- Adjust if 'react' has a different name or is covered by 'like'
      AND DATE(fees.event_timestamp) = DATE(dp.created_timestamp)
)
ORDER BY dp.post_id;

/*
Explanation:

1. We select all posts from the posts table
2. We filter using a NOT EXISTS subquery to find posts that didn't receive any 'like' or 'react' events
3. The subquery joins engagement_events on post_id and checks if there are any 'like' or 'react' events
4. We use DATE() to compare only the date portion of the timestamps
5. We also ensure the events happened on the same day the post was created
6. Finally, we order the results by post_id for clarity

Alternative approach using LEFT JOIN:

SELECT p.post_id
FROM posts p
LEFT JOIN engagement_events e ON p.post_id = e.post_id
    AND e.event_type IN ('like', 'react')
    AND DATE(e.created_at) = DATE(p.created_at)
WHERE e.event_id IS NULL
ORDER BY p.post_id;
*/ 