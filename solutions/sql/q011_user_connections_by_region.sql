/*
Solution to Question 7.3.1: User Connections by Region

Write a SQL query to find the number of user connections where both users are from the same region.
*/

-- Schema (from scenario_7_social_network_setup.sql):
-- dim_users_social (user_key, region)
-- fact_connections_social (connection_id, user1_key, user2_key)

SELECT
    u1.region,
    COUNT(fc.connection_id) AS number_of_intra_region_connections
    -- Each row in fact_connections_social represents one unique connection.
    -- If user1_key < user2_key is enforced, then COUNT(*) or COUNT(fc.connection_id) is fine.
    -- If connections can be (A,B) and (B,A), and we want to count them as one, then we might need to count distinct pairs like COUNT(DISTINCT LEAST(user1_key, user2_key), GREATEST(user1_key, user2_key))
    -- However, the question implies counting established connections as they are in the fact table.
FROM
    fact_connections_social fc
JOIN
    dim_users_social u1 ON fc.user1_key = u1.user_key -- Get region for user1
JOIN
    dim_users_social u2 ON fc.user2_key = u2.user_key -- Get region for user2
WHERE
    u1.region = u2.region -- Filter for connections where both users are from the same region
GROUP BY
    u1.region -- Group by region to count connections per region
ORDER BY
    number_of_intra_region_connections DESC, -- Primary sort: by count of connections, descending
    u1.region ASC; -- Secondary sort: by region name, ascending (for tie-breaking)

/*
Explanation:

1.  The query selects from `fact_connections_social` (aliased as `fc`), which stores pairs of connected users.

2.  It performs two joins with `dim_users_social`:
    *   `JOIN dim_users_social u1 ON fc.user1_key = u1.user_key`: This join retrieves the region for the first user (`user1_key`) in each connection.
    *   `JOIN dim_users_social u2 ON fc.user2_key = u2.user_key`: This join retrieves the region for the second user (`user2_key`) in each connection.

3.  `WHERE u1.region = u2.region`:
    *   This is the crucial filtering condition. It ensures that only connections where both `user1` and `user2` belong to the same region are considered for counting.

4.  `GROUP BY u1.region`:
    *   After filtering, the remaining connections are grouped by the common region of the connected users. This allows the aggregate function `COUNT()` to operate per region.
    *   Since `u1.region = u2.region` is enforced by the `WHERE` clause, grouping by `u1.region` is equivalent to grouping by `u2.region` or by the pair (`u1.region`, `u2.region`).

5.  `SELECT u1.region, COUNT(fc.connection_id) AS number_of_intra_region_connections`:
    *   `u1.region`: Selects the region name for which the count is being reported.
    *   `COUNT(fc.connection_id)`: Counts the number of connection records within each group (i.e., for each region where both users of the connection are from that region). Assuming `connection_id` is a non-null primary key for `fact_connections_social`, this counts the number of such intra-region connections.
        *   Note on Connection Duplicates: If the `fact_connections_social` table could store connections bidirectionally (e.g., a row for UserA-UserB and another for UserB-UserA for the same friendship), and each should be counted, then `COUNT(fc.connection_id)` is appropriate. If such pairs should only be counted once, a more complex distinct pair counting mechanism would be needed (e.g., using `LEAST` and `GREATEST` on `user1_key`, `user2_key`), but the problem description doesn't imply this complexity and usually connection tables store unique pairs.

6.  `ORDER BY number_of_intra_region_connections DESC, u1.region ASC`:
    *   Orders the final results. Primarily by `number_of_intra_region_connections` in descending order (regions with more connections first).
    *   Secondarily by `u1.region` in ascending order (alphabetically by region name) to ensure a consistent order for regions that might have the same number of connections.

This query efficiently identifies and counts connections where both participants share the same geographical region, providing insights into the density of local connections within different areas.
*/ 