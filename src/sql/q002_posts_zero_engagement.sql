/*
Question 2.3.1: Posts with Zero Engagement on Creation Day

Write a SQL query to find post_ids for posts that received zero 'like' or 'react' events on the same calendar day they were created.

Schema:
posts:
- post_id (PK)
- creator_id
- content_type
- created_at (timestamp)
- ...

engagement_events:
- event_id (PK)
- post_id (FK -> posts)
- user_id
- event_type ('like', 'comment', 'share', 'react')
- created_at (timestamp)
- ...

Expected Output:
A list of post_ids that were created but received no 'like' or 'react' events on their creation day.
*/

-- Write your SQL query here:
SELECT p.post_id
FROM posts p
WHERE NOT EXISTS (
    SELECT 1
    FROM engagement_events e
    WHERE e.post_id = p.post_id
    AND e.event_type IN ('like', 'react')
    AND DATE(e.created_at) = DATE(p.created_at)
)
ORDER BY p.post_id;

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