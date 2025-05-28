/*
Question 7.3.1: User Connections by Region

Write a SQL query to find the number of user connections where both users are from the same region.

Schema (from scenario_7_social_network_setup.sql):

dim_users_social:
- user_key (PK)
- user_id (VARCHAR)
- region (VARCHAR) -- e.g., 'North America', 'Europe', 'Asia'
- ...

fact_connections_social:
- connection_id (PK)
- user1_key (FK to dim_users_social) -- Key of the first user in the connection
- user2_key (FK to dim_users_social) -- Key of the second user in the connection
- connection_date (DATE)
- ...

Expected Output:
- region
- number_of_intra_region_connections
Ordered by number_of_intra_region_connections DESC, then region ASC.
*/

-- Write your SQL query here:
SELECT
    u1.region,
    COUNT(fc.connection_id) AS number_of_intra_region_connections
FROM
    fact_connections_social fc
JOIN
    dim_users_social u1 ON fc.user1_key = u1.user_key
JOIN
    dim_users_social u2 ON fc.user2_key = u2.user_key
WHERE
    u1.region = u2.region
GROUP BY
    u1.region
ORDER BY
    number_of_intra_region_connections DESC,
    u1.region ASC; 