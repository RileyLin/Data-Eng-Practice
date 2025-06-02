# Scenario 3: Streaming (Netflix/YouTube) - SQL Questions

## Database Schema Reference

Based on the Streaming data model:

### Dimension Tables
-   **`dim_users`**: `user_key`, `user_id`, `user_name`, `registration_date`, `region`, `subscription_tier`, `user_preferences`, `last_login_timestamp`
-   **`dim_content`**: `content_key`, `content_id`, `title`, `description`, `content_type`, `series_key`, `season_number`, `episode_number`, `duration_seconds`, `release_date`, `maturity_rating`, `primary_language`, `production_details`, `thumbnail_url`, `streaming_url`
-   **`dim_genres`**: `genre_key`, `genre_name`
-   **`dim_tags`**: `tag_key`, `tag_name`
-   **`dim_cast_crew`**: `person_key`, `person_name`, `person_role`
-   **`dim_date`**: `date_key`, `full_date`, `year`, `month`, `day_of_week`, `is_weekend`

### Fact Tables & Associative Entities
-   **`fact_content_genres`**: `content_key`, `genre_key`
-   **`fact_content_tags`**: `content_key`, `tag_key`
-   **`fact_content_cast_crew`**: `content_key`, `person_key`, `specific_role`
-   **`fact_viewing_history`**: `view_key`, `user_key`, `content_key`, `device_key`, `date_key`, `view_start_timestamp`, `view_end_timestamp`, `watch_duration_seconds`, `completion_percentage`, `was_completed`, `exit_reason`, `playback_events`
-   **`fact_user_ratings`**: `user_key`, `content_key`, `rating_value`, `rating_timestamp`
-   **`fact_user_watchlist`**: `user_key`, `content_key`, `added_timestamp`

---

## Question 1: Top 10 Most Watched Movies This Month

**Problem**: Identify the top 10 movies based on the total watch hours this month.

**Expected Output**: Movie title, total watch hours.

### Solution:
```sql
SELECT 
    dc.title AS movie_title,
    SUM(fvh.watch_duration_seconds) / 3600.0 AS total_watch_hours
FROM fact_viewing_history fvh
JOIN dim_content dc ON fvh.content_key = dc.content_key
JOIN dim_date dd ON fvh.date_key = dd.date_key
WHERE dc.content_type = 'movie'
  AND dd.year = EXTRACT(YEAR FROM CURRENT_DATE)
  AND dd.month = EXTRACT(MONTH FROM CURRENT_DATE)
GROUP BY dc.title
ORDER BY total_watch_hours DESC
LIMIT 10;
```

---

## Question 2: Average Watch Completion Rate for TV Series Premieres

**Problem**: Calculate the average watch completion rate for the first episode of all TV series that premiered in the last quarter.

**Expected Output**: Series title, premiere date, average completion rate for episode 1.

### Solution:
```sql
WITH series_premieres AS (
    -- Identify series that premiered last quarter
    SELECT 
        content_key AS series_content_key,
        title AS series_title,
        release_date AS series_premiere_date
    FROM dim_content
    WHERE content_type = 'series'
      AND release_date BETWEEN (CURRENT_DATE - INTERVAL '3 months' - (EXTRACT(DAY FROM CURRENT_DATE) -1) * INTERVAL '1 day')::date - INTERVAL '3 months' -- Start of previous quarter
                         AND (CURRENT_DATE - (EXTRACT(DAY FROM CURRENT_DATE)) * INTERVAL '1 day')::date - INTERVAL '1 day'         -- End of previous quarter
),
first_episodes AS (
    -- Get the first episode for these series
    SELECT 
        sp.series_title,
        sp.series_premiere_date,
        dc.content_key AS episode_content_key
    FROM series_premieres sp
    JOIN dim_content dc ON sp.series_content_key = dc.series_key
    WHERE dc.content_type = 'episode'
      AND dc.season_number = 1
      AND dc.episode_number = 1
)
SELECT 
    fe.series_title,
    fe.series_premiere_date,
    COALESCE(ROUND(AVG(fvh.completion_percentage) * 100, 2), 0) AS avg_completion_rate_episode1_pct
FROM first_episodes fe
LEFT JOIN fact_viewing_history fvh ON fe.episode_content_key = fvh.content_key
GROUP BY fe.series_title, fe.series_premiere_date
ORDER BY fe.series_premiere_date DESC, avg_completion_rate_episode1_pct DESC;
```

---

## Question 3: User Binge-Watching Behavior

**Problem**: Identify users who watched 3 or more episodes of the same series on the same day. List the user, series, and number of episodes watched.

**Expected Output**: User ID, series title, date of binge, number of episodes binged.

### Solution:
```sql
WITH daily_series_watches AS (
    SELECT 
        fvh.user_key,
        dc_episode.series_key,
        dd.full_date AS watch_date,
        COUNT(DISTINCT dc_episode.content_key) AS episodes_watched_count -- Count distinct episodes
    FROM fact_viewing_history fvh
    JOIN dim_content dc_episode ON fvh.content_key = dc_episode.content_key
    JOIN dim_date dd ON fvh.date_key = dd.date_key
    WHERE dc_episode.content_type = 'episode'
      AND dc_episode.series_key IS NOT NULL
      AND fvh.completion_percentage > 0.7 -- Consider an episode 'watched' if >70% completed
    GROUP BY fvh.user_key, dc_episode.series_key, dd.full_date
)
SELECT 
    du.user_id,
    dc_series.title AS series_title,
    dsw.watch_date,
    dsw.episodes_watched_count
FROM daily_series_watches dsw
JOIN dim_users du ON dsw.user_key = du.user_key
JOIN dim_content dc_series ON dsw.series_key = dc_series.content_key
WHERE dsw.episodes_watched_count >= 3
  AND dsw.watch_date >= CURRENT_DATE - 30 -- Limit to last 30 days for relevance
ORDER BY dsw.watch_date DESC, dsw.episodes_watched_count DESC
LIMIT 200;
```

---

## Question 4: Most Common Genre Combinations in User Watchlists

**Problem**: Find the top 5 most common pairs of genres for content that users add to their watchlist.

**Expected Output**: Genre 1, Genre 2, combination count.

### Solution:
```sql
WITH content_genre_pairs AS (
    SELECT 
        fcg1.content_key,
        LEAST(dg1.genre_name, dg2.genre_name) as genre1, -- Ensure consistent order for pairs
        GREATEST(dg1.genre_name, dg2.genre_name) as genre2
    FROM fact_content_genres fcg1
    JOIN dim_genres dg1 ON fcg1.genre_key = dg1.genre_key
    JOIN fact_content_genres fcg2 ON fcg1.content_key = fcg2.content_key AND fcg1.genre_key < fcg2.genre_key
    JOIN dim_genres dg2 ON fcg2.genre_key = dg2.genre_key
)
SELECT 
    cgp.genre1,
    cgp.genre2,
    COUNT(DISTINCT fuw.user_key) AS distinct_users_watchlist_count -- Or COUNT(*) for total watchlist additions with this combo
FROM fact_user_watchlist fuw
JOIN content_genre_pairs cgp ON fuw.content_key = cgp.content_key
JOIN dim_date dd ON fuw.added_timestamp::date = dd.full_date
WHERE dd.full_date >= CURRENT_DATE - 90 -- Consider watchlists additions in last 90 days
GROUP BY cgp.genre1, cgp.genre2
HAVING COUNT(DISTINCT fuw.user_key) > 10 -- Minimum threshold for combo relevance
ORDER BY distinct_users_watchlist_count DESC
LIMIT 5;
```

---

## Question 5: Impact of Ratings on Content Completion

**Problem**: Analyze if content with higher average user ratings tends to have higher average watch completion rates.

**Expected Output**: Rating bucket (e.g., 1-2, 2-3, 3-4, 4-5 stars), average completion percentage for content in that rating bucket.

### Solution:
```sql
WITH content_avg_ratings AS (
    SELECT 
        content_key,
        AVG(rating_value) as avg_rating
    FROM fact_user_ratings
    WHERE rating_timestamp >= CURRENT_DATE - 365 -- Consider ratings in the last year
    GROUP BY content_key
    HAVING COUNT(user_key) >= 10 -- Only content with at least 10 ratings
),
content_avg_completion AS (
    SELECT 
        content_key,
        AVG(completion_percentage) as avg_completion_pct
    FROM fact_viewing_history
    WHERE view_start_timestamp >= CURRENT_DATE - 365 -- Consider views in the last year
      AND watch_duration_seconds > 60 -- Only views longer than a minute
    GROUP BY content_key
)
SELECT 
    CASE 
        WHEN car.avg_rating < 2 THEN '1-2 Stars'
        WHEN car.avg_rating >= 2 AND car.avg_rating < 3 THEN '2-3 Stars'
        WHEN car.avg_rating >= 3 AND car.avg_rating < 4 THEN '3-4 Stars'
        WHEN car.avg_rating >= 4 THEN '4-5 Stars'
        ELSE 'Not Rated Enough'
    END as rating_bucket,
    COUNT(DISTINCT car.content_key) as number_of_content_items,
    ROUND(AVG(cac.avg_completion_pct) * 100, 2) as overall_avg_completion_in_bucket_pct
FROM content_avg_ratings car
JOIN content_avg_completion cac ON car.content_key = cac.content_key
GROUP BY rating_bucket
ORDER BY rating_bucket;
```

---

## Question 6: Content Drop-off Analysis (Movies)

**Problem**: For movies, identify common drop-off points. For instance, what percentage of viewers who start a movie make it past 25%, 50%, and 75% of its duration?

**Expected Output**: Movie title, percentage of viewers reaching 25%, 50%, 75%.

### Solution:
```sql
WITH movie_view_milestones AS (
    SELECT 
        fvh.user_key,
        fvh.content_key,
        dc.title as movie_title,
        MAX(CASE WHEN fvh.completion_percentage >= 0.25 THEN 1 ELSE 0 END) as reached_25_pct,
        MAX(CASE WHEN fvh.completion_percentage >= 0.50 THEN 1 ELSE 0 END) as reached_50_pct,
        MAX(CASE WHEN fvh.completion_percentage >= 0.75 THEN 1 ELSE 0 END) as reached_75_pct,
        MAX(CASE WHEN fvh.was_completed THEN 1 ELSE 0 END) as reached_100_pct -- or fvh.completion_percentage >= 0.95 for 'near completion'
    FROM fact_viewing_history fvh
    JOIN dim_content dc ON fvh.content_key = dc.content_key
    WHERE dc.content_type = 'movie'
      AND fvh.view_start_timestamp >= CURRENT_DATE - 90 -- Analyze recent views
    GROUP BY fvh.user_key, fvh.content_key, dc.title
)
SELECT 
    movie_title,
    COUNT(DISTINCT user_key) as total_unique_viewers, -- Unique users who started the movie
    ROUND(SUM(reached_25_pct) * 100.0 / COUNT(DISTINCT user_key), 2) as pct_reached_25,
    ROUND(SUM(reached_50_pct) * 100.0 / COUNT(DISTINCT user_key), 2) as pct_reached_50,
    ROUND(SUM(reached_75_pct) * 100.0 / COUNT(DISTINCT user_key), 2) as pct_reached_75,
    ROUND(SUM(reached_100_pct) * 100.0 / COUNT(DISTINCT user_key), 2) as pct_reached_100
FROM movie_view_milestones
GROUP BY movie_title
HAVING COUNT(DISTINCT user_key) >= 100 -- Only movies with significant unique viewers
ORDER BY total_unique_viewers DESC, movie_title
LIMIT 100;
``` 