/*
Solution to Question 1.3.1 (Carpool Segment Percentage)

Write a SQL query to calculate the percentage of ride segments that belong to a 'Carpool' ride type.
Assume fact_ride_segments links to fact_rides, and fact_rides links to dim_ride_type.
*/

-- Calculate percentage of ride segments that belong to 'Carpool' ride type
SELECT
    (COUNT(CASE WHEN drt.ride_type_name = 'Carpool' THEN frs.ride_segment_id ELSE NULL END) * 100.0)
    / NULLIF(COUNT(frs.ride_segment_id), 0) AS carpool_segment_percentage
FROM
    fact_ride_segments frs
JOIN
    fact_rides fr ON frs.ride_id = fr.ride_id
JOIN
    dim_ride_type drt ON fr.ride_type_key = drt.ride_type_key;

/*
Explanation:

1. The query starts from the fact_ride_segments table (frs) which contains individual segments of rides.

2. It joins to fact_rides (fr) to get information about each ride, including its type.

3. It then joins to dim_ride_type (drt) to get the ride type name ('Carpool', 'Regular', etc.).

4. In the SELECT clause:
   - The COUNT(CASE WHEN...) counts only the segments where ride_type_name is 'Carpool'
   - The COUNT(frs.ride_segment_id) counts all segments
   - We multiply by 100.0 to get a percentage value
   - The NULLIF function prevents division by zero if there are no segments

5. This gives us a single value representing the percentage of all ride segments that are part of carpool rides.

Note: The query could be filtered further with a WHERE clause to specify a time period, 
geography, or other dimensions if needed.
*/ 