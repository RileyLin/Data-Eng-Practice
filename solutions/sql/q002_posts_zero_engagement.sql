/*
Solution to Question 2.3.1: Posts with Zero Engagement on Creation Day

Write a SQL query to find post_ids for posts that received zero 'like' or 'react' events 
on the same calendar day they were created.
*/

-- Using NOT EXISTS approach
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

1. We select all posts from the posts table.

2. We filter using a NOT EXISTS subquery:
   - This is an efficient way to find posts that didn't receive any 'like' or 'react' events
   - The subquery checks if there are any matching rows in engagement_events
   - If no rows are found, the NOT EXISTS condition is true and the post is included in the result

3. The subquery conditions:
   - e.post_id = p.post_id: Match the event to the post
   - e.event_type IN ('like', 'react'): Only consider 'like' or 'react' events
   - DATE(e.created_at) = DATE(p.created_at): Ensure the event occurred on the same day as post creation
   
4. DATE() function extracts just the date portion from timestamps, ignoring time components.

5. We order the results by post_id for readability.

Alternative approach using LEFT JOIN:

SELECT p.post_id
FROM posts p
LEFT JOIN engagement_events e ON p.post_id = e.post_id
    AND e.event_type IN ('like', 'react')
    AND DATE(e.created_at) = DATE(p.created_at)
WHERE e.event_id IS NULL
ORDER BY p.post_id;

The LEFT JOIN approach works by:
1. Joining all posts with matching engagement events
2. Keeping all posts even if there are no matching events (LEFT JOIN behavior)
3. Filtering to keep only posts where no matching events were found (e.event_id IS NULL)

Both approaches produce the same result, but the NOT EXISTS version is often more 
efficient for large datasets as it can stop searching once it finds a matching event.
*/ 