# Scenario 1: Ridesharing SQL Questions (Uber/Lyft) - Carpooling Feature

## Database Schema Reference

Based on `setup_scripts/scenario_1_ridesharing_setup.sql`:

### Dimension Tables
- **dim_users**: user_key, user_id, user_name, user_type ('rider'/'driver')
- **dim_location**: location_key, latitude, longitude, address, city, zip_code
- **dim_ride_type**: ride_type_key, ride_type_name ('Regular'/'Carpool'/'Premium')
- **dim_vehicle**: vehicle_key, license_plate, make, model, year, color
- **dim_date**: date_key, full_date, year, quarter, month, day_of_month, day_of_week, week_of_year, is_weekend
- **dim_time**: time_key, full_time, hour, minute, second, am_pm

### Fact Tables
- **fact_rides**: ride_id, driver_user_key, ride_type_key, vehicle_key, start_location_key, end_location_key, start_timestamp, end_timestamp, total_fare, total_distance, total_duration, date_key, time_key
- **fact_ride_segments**: ride_segment_id, ride_id, rider_user_key, segment_pickup_timestamp, segment_dropoff_timestamp, segment_pickup_location_key, segment_dropoff_location_key, segment_fare, segment_distance, pickup_sequence_in_ride, dropoff_sequence_in_ride

---

## Question 1: Carpool Segment Percentage

**Problem**: Calculate the percentage of ride segments that belong to 'Carpool' ride type.

**Expected Output**: Single row with percentage value showing proportion of carpool segments.

### Solution:
```sql
SELECT
    (COUNT(CASE WHEN drt.ride_type_name = 'Carpool' THEN frs.ride_segment_id ELSE NULL END) * 100.0)
    / NULLIF(COUNT(frs.ride_segment_id), 0) AS carpool_segment_percentage
FROM
    fact_ride_segments frs
JOIN
    fact_rides fr ON frs.ride_id = fr.ride_id
JOIN
    dim_ride_type drt ON fr.ride_type_key = drt.ride_type_key;
```

---

## Question 2: Drivers Preferring Carpool

**Problem**: Find drivers who have completed more carpool rides than regular rides.

**Expected Output**: Driver information with ride counts showing carpool preference.

### Solution:
```sql
WITH driver_ride_counts AS (
    SELECT 
        du.user_key,
        du.user_id,
        du.user_name,
        drt.ride_type_name,
        COUNT(fr.ride_id) as ride_count
    FROM 
        dim_users du
    JOIN 
        fact_rides fr ON du.user_key = fr.driver_user_key
    JOIN 
        dim_ride_type drt ON fr.ride_type_key = drt.ride_type_key
    WHERE 
        du.user_type = 'driver'
        AND drt.ride_type_name IN ('Carpool', 'Regular')
    GROUP BY 
        du.user_key, du.user_id, du.user_name, drt.ride_type_name
),
pivot_counts AS (
    SELECT 
        user_key,
        user_id,
        user_name,
        SUM(CASE WHEN ride_type_name = 'Carpool' THEN ride_count ELSE 0 END) as carpool_rides,
        SUM(CASE WHEN ride_type_name = 'Regular' THEN ride_count ELSE 0 END) as regular_rides
    FROM 
        driver_ride_counts
    GROUP BY 
        user_key, user_id, user_name
)
SELECT 
    user_id,
    user_name,
    carpool_rides,
    regular_rides,
    (carpool_rides * 100.0 / NULLIF(carpool_rides + regular_rides, 0)) as carpool_percentage
FROM 
    pivot_counts
WHERE 
    carpool_rides > regular_rides
ORDER BY 
    carpool_percentage DESC, carpool_rides DESC;
```

---

## Question 3: Carpool Efficiency Analysis

**Problem**: Calculate average passengers per carpool ride and compare revenue efficiency.

**Expected Output**: Carpool metrics showing utilization and revenue per mile.

### Solution:
```sql
WITH carpool_metrics AS (
    SELECT 
        fr.ride_id,
        fr.total_fare,
        fr.total_distance,
        fr.total_duration,
        COUNT(frs.ride_segment_id) as passenger_count,
        SUM(frs.segment_fare) as total_segment_fares
    FROM 
        fact_rides fr
    JOIN 
        dim_ride_type drt ON fr.ride_type_key = drt.ride_type_key
    JOIN 
        fact_ride_segments frs ON fr.ride_id = frs.ride_id
    WHERE 
        drt.ride_type_name = 'Carpool'
    GROUP BY 
        fr.ride_id, fr.total_fare, fr.total_distance, fr.total_duration
)
SELECT 
    COUNT(*) as total_carpool_rides,
    AVG(passenger_count) as avg_passengers_per_ride,
    AVG(total_fare) as avg_total_fare,
    AVG(total_distance) as avg_total_distance,
    AVG(total_fare / NULLIF(total_distance, 0)) as avg_revenue_per_mile,
    AVG(total_duration) as avg_duration_minutes,
    SUM(passenger_count) as total_passenger_trips,
    SUM(total_distance * passenger_count) as total_passenger_miles
FROM 
    carpool_metrics;
```

---

## Question 4: Peak Carpool Hours

**Problem**: Identify the most popular hours for carpool rides.

**Expected Output**: Hours ranked by carpool ride frequency.

### Solution:
```sql
SELECT 
    dt.hour,
    dt.am_pm,
    COUNT(fr.ride_id) as carpool_rides,
    AVG(passenger_count.passengers) as avg_passengers_per_ride,
    SUM(passenger_count.passengers) as total_passenger_pickups
FROM 
    fact_rides fr
JOIN 
    dim_ride_type drt ON fr.ride_type_key = drt.ride_type_key
JOIN 
    dim_time dt ON fr.time_key = dt.time_key
JOIN (
    SELECT 
        ride_id,
        COUNT(*) as passengers
    FROM 
        fact_ride_segments
    GROUP BY 
        ride_id
) passenger_count ON fr.ride_id = passenger_count.ride_id
WHERE 
    drt.ride_type_name = 'Carpool'
GROUP BY 
    dt.hour, dt.am_pm
ORDER BY 
    carpool_rides DESC
LIMIT 10;
```

---

## Question 5: Geographic Carpool Hotspots

**Problem**: Find locations with highest carpool pickup activity.

**Expected Output**: Top pickup locations for carpool rides.

### Solution:
```sql
SELECT 
    dl.city,
    dl.zip_code,
    dl.address,
    COUNT(frs.ride_segment_id) as total_carpool_pickups,
    COUNT(DISTINCT frs.ride_id) as unique_carpool_rides,
    AVG(frs.segment_fare) as avg_segment_fare,
    COUNT(DISTINCT frs.rider_user_key) as unique_riders
FROM 
    fact_ride_segments frs
JOIN 
    fact_rides fr ON frs.ride_id = fr.ride_id
JOIN 
    dim_ride_type drt ON fr.ride_type_key = drt.ride_type_key
JOIN 
    dim_location dl ON frs.segment_pickup_location_key = dl.location_key
WHERE 
    drt.ride_type_name = 'Carpool'
GROUP BY 
    dl.city, dl.zip_code, dl.address, dl.location_key
ORDER BY 
    total_carpool_pickups DESC
LIMIT 15;
```

---

## Question 6: Weekend vs Weekday Carpool Usage

**Problem**: Compare carpool adoption between weekdays and weekends.

**Expected Output**: Carpool usage patterns by day type.

### Solution:
```sql
SELECT 
    dd.is_weekend,
    CASE 
        WHEN dd.is_weekend = 1 THEN 'Weekend'
        ELSE 'Weekday'
    END as day_type,
    COUNT(fr.ride_id) as total_rides,
    SUM(CASE WHEN drt.ride_type_name = 'Carpool' THEN 1 ELSE 0 END) as carpool_rides,
    SUM(CASE WHEN drt.ride_type_name = 'Regular' THEN 1 ELSE 0 END) as regular_rides,
    ROUND(
        (SUM(CASE WHEN drt.ride_type_name = 'Carpool' THEN 1 ELSE 0 END) * 100.0) / 
        NULLIF(COUNT(fr.ride_id), 0), 2
    ) as carpool_adoption_rate
FROM 
    fact_rides fr
JOIN 
    dim_ride_type drt ON fr.ride_type_key = drt.ride_type_key
JOIN 
    dim_date dd ON fr.date_key = dd.date_key
GROUP BY 
    dd.is_weekend
ORDER BY 
    dd.is_weekend;
```

## Practice Tips

1. **Understand the Schema**: Study the relationship between fact_rides and fact_ride_segments
2. **Carpool Logic**: Remember that carpool rides have multiple segments (passengers)
3. **Aggregation Levels**: Choose appropriate granularity (ride-level vs segment-level)
4. **Performance**: Use appropriate indexes on foreign keys and date columns
5. **Edge Cases**: Handle division by zero and NULL values appropriately 