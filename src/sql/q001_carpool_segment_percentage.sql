/*
Question 1.3.1 (Carpool Segment Percentage):

Write a SQL query to calculate the percentage of ride segments that belong to a 'Carpool' ride type.
Assume fact_ride_segments links to fact_rides, and fact_rides links to dim_ride_type.

Schema:

fact_ride_segments:
- ride_segment_id (PK)
- ride_id (FK -> fact_rides)
- rider_user_key
- ...

fact_rides:
- ride_id (PK)
- ride_type_key (FK -> dim_ride_type)
- driver_user_key
- ...

dim_ride_type:
- ride_type_key (PK)
- ride_type_name ('Carpool', 'Regular', etc.)
- ...

Expected Output:
The query should return a single row with a percentage value showing what proportion
of all ride segments (from fact_ride_segments) belong to 'Carpool' rides.
*/

-- Write your SQL query here:
SELECT
    (COUNT(CASE WHEN drt.ride_type_name = 'Carpool' THEN frs.ride_segment_id ELSE NULL END) * 100.0)
    / NULLIF(COUNT(frs.ride_segment_id), 0) AS carpool_segment_percentage
FROM
    fact_ride_segments frs
JOIN
    fact_rides fr ON frs.ride_id = fr.ride_id
JOIN
    dim_ride_type drt ON fr.ride_type_key = drt.ride_type_key;

