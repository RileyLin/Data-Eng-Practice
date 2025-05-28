# The GSM-T Framework for Product Metrics (Meta DE Focus)

When tackling product sense questions in a Meta Data Engineering interview, a structured approach is crucial. Interviewers are particularly interested in your ability to translate product goals into precise, engineerable metrics and to articulate the data instrumentation and modeling required to bring those metrics to life.

The **GSM-T (Goals → Signals → Metrics → Targets)** framework, which evolved from Google's HEART methodology, is highly effective for this. It aligns well with how Meta engineers approach problem-solving and data system design.

## Understanding the GSM-T Framework

Here's a breakdown of each component:

1.  **G - Goals:**
    *   **Definition:** Start with a clear, high-level outcome you want to achieve for the user or the business. What does success look like in broad terms? What user problem are you solving, or what business opportunity are you pursuing?
    *   **DE Angle:** How does this goal inform the *kind* of data systems needed? For example, a goal to "improve real-time user interaction" immediately suggests a need for low-latency data processing and potentially stream-based analytics. A goal to "understand long-term user retention" might imply robust batch processing of historical data.

2.  **S - Signals:**
    *   **Definition:** These are the specific, observable user behaviors or system changes you expect to see if you're moving towards your goal. **Signals are the raw, loggable events or data points you need to capture.** They are the direct evidence of change.
    *   **DE Angle (Critical for DEs):**
        *   **Instrumentation:** What exact events must be logged? (e.g., `event_name: 'button_click'`, `event_name: 'page_view'`, `event_name: 'item_purchased'`).
        *   **Event Attributes/Schema:** What specific attributes (fields/properties) should each event log contain to be useful? (e.g., for `'button_click'`: `user_id`, `timestamp`, `button_id`, `page_url`, `session_id`). This directly informs the event schema design.
        *   **Data Sources:** Where will these signals originate? (Client-side app, server-side application, third-party integration).
        *   **Loggability:** Are these signals realistically loggable with current or planned instrumentation?

3.  **M - Metrics:**
    *   **Definition:** These are the quantifiable, trackable measures derived from your signals. Metrics turn raw signals into understandable indicators of performance. They tell you how much, how often, or how well something is happening.
    *   **DE Angle (Critical for DEs):**
        *   **Engineerability:** How will each metric be computed from the logged signals? (e.g., `Daily Active Users = COUNT(DISTINCT user_id WHERE signal.event_name = 'app_open' AND signal.date = TODAY)`). This defines the ETL/ELT logic, aggregation strategies, and potentially the data model for analytical tables.
        *   **Data Modeling:** How should data be structured in your warehouse or data lake to efficiently calculate these metrics? (e.g., fact tables for events, dimension tables for users/items, pre-aggregated summary tables).
        *   **Trade-offs:** What are the trade-offs in terms of latency vs. granularity, precision vs. recall, or cost vs. accuracy for each metric? (e.g., a real-time DAU metric might be an estimate, while a batch-calculated one is precise but delayed).
        *   **Dashboarding/Reporting:** How will these metrics be surfaced to stakeholders?

4.  **T - Targets:**
    *   **Definition:** These are the specific, measurable thresholds or values for your metrics that define what "success" or "winning" looks like for the goal. Targets make goals actionable and provide a benchmark for progress.
    *   **DE Angle:**
        *   **Monitoring & Alerting:** How do targets influence system monitoring requirements? What thresholds should trigger alerts if a metric is off-target?
        *   **Baseline:** What is the current baseline for these metrics (if available) to understand the required uplift?

## Why GSM-T Beats GOSST in a Meta DE Interview:

The GSM-T framework is preferred in this context because it aligns more directly with the engineering mindset expected:

| Criterion                                       | GSM‑T                                                | GOSST                                       |
| :---------------------------------------------- | :--------------------------------------------------- | :------------------------------------------ |
| **Forces you to state loggable events?**        | ✅ **Signals layer** (explicitly defines raw data)     | ❌ (Implied, less direct)                   |
| **Maps directly to schema / pipeline design?**  | ✅ **You define fields while naming signals/metrics**  | ⚠️ (More abstract, less direct data focus) |
| **Encourages trade‑off talk (latency vs. granularity etc.)** | ✅ **When choosing metrics & their computation** | ⚠️ (Optional, less emphasized)             |
| **Recognisable to Meta engineers**             | ✅ **Very common and used internally**               | 🤷‍♂️ (Not as common in DE context)        |

**Take‑away:** Use GSM‑T for structuring your answers to product metric questions. You can sprinkle in tactical execution steps (like A/B testing strategy or specific stakeholder concerns, similar to GOSST's "Tracking & Trade-offs" or "Objectives") if the conversation naturally drifts into those areas, but root your thinking in GSM-T.

## How to Practice Product Sense for Metrics (GSM-T Approach):

1.  **Deconstruct Provided Examples (from `docs/product_sense.md` or elsewhere):**
    *   Take a product sense question. Before looking at any provided answer, apply the GSM-T framework.
    *   **Goal:** What's the core objective?
    *   **Signals:** Brainstorm *specific loggable events and their attributes*. This is key for DE.
    *   **Metrics:** How would you *calculate* metrics from those signals?
    *   **Targets:** What would be a reasonable success threshold?
    *   Compare your GSM-T breakdown with any provided answers, noting differences in signal definition or metric calculation.

2.  **Use Everyday Apps:**
    *   Pick an app you use daily. Imagine a new feature.
    *   "If [App] launches [New Feature X]..."
        *   **Goal:** What is the goal of Feature X?
        *   **Signals:** What new user actions or system events would Feature X generate? What attributes would these event logs need? (e.g., `feature_X_impression`, `feature_X_interaction_type_A`, `feature_X_completion_status`).
        *   **Metrics:** How would you measure adoption (e.g., % DAU using Feature X), engagement (e.g., interactions per user of Feature X), and impact (e.g., Feature X's effect on overall session time or conversion)? Define the calculation.
        *   **Targets:** What would signify a successful launch of Feature X?

3.  **Focus on the "Why" and "How" (DE Perspective):**
    *   For every Signal: "Why this signal? What data points does it need to capture?"
    *   For every Metric: "How is this engineered from the signals? What's the SQL/pseudocode logic? What are the data modeling implications (e.g., new columns, aggregate tables)?"
    *   "What are the trade-offs (e.g., real-time vs. batch for this metric)?"

4.  **Think Data Systems:**
    *   When defining Signals and Metrics, briefly consider:
        *   **Instrumentation:** Client-side vs. server-side logging.
        *   **Data Pipeline:** Ingestion, ETL/ELT processes needed.
        *   **Data Storage:** How would raw signals and aggregated metrics be stored?
        *   **Data Quality:** How would you ensure the accuracy of these signals/metrics?
        *   **Scale:** How would your system handle large volumes of these signals?

5.  **Practice Articulation & Structure (GSM-T Order):**
    *   Explain your thinking out loud, following the G -> S -> M -> T structure.
    *   Clearly differentiate between a high-level goal, the raw behavioral signals, the calculated metrics, and the success targets.

6.  **Discuss Trade-offs, Guardrails, and Counter-Metrics:**
    *   Under "Metrics" or "Targets," discuss potential negative impacts.
    *   **Guardrail Metrics:** What existing key metrics should not be harmed? (e.g., launching a new feature shouldn't significantly degrade overall app performance). These also need Signals -> Metrics.
    *   **Counter Metrics:** What metrics would indicate unintended negative behavior?

7.  **Time Yourself:**
    *   Practice generating a GSM-T breakdown within a reasonable timeframe (e.g., 10-15 minutes per question).

8.  **Peer Practice:**
    *   Work with others, focusing on the clarity of signals and the engineerability of metrics.

By consistently applying GSM-T and focusing on the data engineering aspects of instrumentation, computation, and system design, you'll be well-prepared for Meta's product sense questions.

## GSM-T Examples from Product Sense Scenarios

Here are examples of applying the GSM-T framework to the product sense questions found in `docs/product_sense.md`. These are concise illustrations of how to structure your thinking.

---

### Scenario 1: Ride Sharing (Uber/Lyft) - Carpooling Feature

**Question 1.1.2: Imagine you launched the Carpool feature. How would you track its performance? What are the key metrics, and how would you slice the data?**

**Overall Goal:** Ensure the Carpool feature is a successful, adopted, and efficient addition for riders, drivers, and the platform.

**1. Adoption & Usage:**
    *   **G (Goal):** Maximize user adoption and regular usage of the Carpool feature.
    *   **S (Signals):**
        *   `event: carpool_ride_request`, `attributes: user_id, timestamp, origin_lat, origin_lon, destination_lat, destination_lon`
        *   `event: carpool_ride_match_success`, `attributes: request_id, driver_id, matched_user_ids_list, initial_eta_seconds`
        *   `event: carpool_ride_match_failure`, `attributes: request_id, reason_code (e.g., no_drivers, no_match)`
        *   `event: ride_completion`, `attributes: ride_id, ride_type ('carpool', 'standard'), user_id, driver_id, fare_usd, distance_km, duration_seconds, carpool_rider_count (if carpool)`
        *   `event: user_first_ride`, `attributes: user_id, ride_id, ride_type`
    *   **M (Metrics):**
        *   **Carpool Ride Penetration:** `COUNT(DISTINCT ride_id WHERE ride_type='carpool') / COUNT(DISTINCT ride_id)` (daily/weekly).
        *   **Carpool Request Success Rate:** `COUNT(carpool_ride_match_success events) / COUNT(carpool_ride_request events)`.
        *   **DAU/WAU/MAU of Carpool Users:** `COUNT(DISTINCT user_id FROM ride_completion WHERE ride_type='carpool')`.
        *   **New User Adoption of Carpool:** `COUNT(DISTINCT user_id FROM user_first_ride WHERE ride_type='carpool') / COUNT(DISTINCT user_id FROM user_first_ride)`.
    *   **T (Targets):**
        *   Carpool Penetration: Achieve 15% of all rides within 6 months.
        *   Request Success Rate: >80%.
        *   Grow Carpool DAU by 20% quarter-over-quarter.

**2. Efficiency & Economics:**
    *   **G (Goal):** Ensure Carpool is efficient for the system and economically beneficial for drivers and the platform.
    *   **S (Signals):**
        *   (From `ride_completion`): `carpool_rider_count`, `distance_km`, `duration_seconds`, `fare_usd_driver_share`, `fare_usd_platform_share`
        *   `event: carpool_leg_details`, `attributes: ride_id, leg_user_id, leg_pickup_timestamp, leg_dropoff_timestamp, leg_intended_detour_seconds`
    *   **M (Metrics):**
        *   **Average Fill Rate:** `AVG(carpool_rider_count)` for completed carpool rides.
        *   **Average Detour Time per Rider:** `AVG(leg_intended_detour_seconds)` (requires careful attribution of detour to specific legs if multiple pickups).
        *   **Driver Earnings per Hour (Carpool vs. Standard):** `SUM(fare_usd_driver_share) / SUM(duration_seconds/3600)` for carpool vs. standard rides, per driver.
        *   **Platform Revenue per Carpool Ride:** `AVG(fare_usd_platform_share)` for carpool rides.
    *   **T (Targets):**
        *   Average Fill Rate: >1.8 riders per carpool segment.
        *   Average Detour Time: < 7 minutes per rider.
        *   Increase average driver earnings per hour for carpool participants by 10% vs. non-carpool hours.

**3. User Experience:**
    *   **G (Goal):** Maintain high satisfaction for both riders and drivers using Carpool.
    *   **S (Signals):**
        *   `event: ride_rating_submitted`, `attributes: ride_id, user_id (who rated), rated_entity_id (driver/rider), rating_score (1-5), ride_type, feedback_tags_list`
        *   `event: ride_cancellation`, `attributes: ride_id, user_id (who cancelled), stage_of_cancellation (e.g., 'before_match', 'after_match_before_pickup'), reason_code, ride_type`
        *   `event: support_ticket_created`, `attributes: user_id, ride_id (if applicable), issue_category, ride_type`
    *   **M (Metrics):**
        *   **Rider CSAT for Carpool:** `AVG(rating_score WHERE rated_entity_type='driver' AND ride_type='carpool')`.
        *   **Driver Satisfaction for Carpool:** `AVG(rating_score WHERE rated_entity_type='rider' AND ride_type='carpool')`.
        *   **Carpool Cancellation Rate:** `COUNT(ride_cancellation events WHERE ride_type='carpool') / COUNT(carpool_ride_match_success events)`.
        *   **Carpool-Related Support Tickets:** `COUNT(support_ticket_created WHERE ride_type='carpool') per 1000 carpool rides`.
    *   **T (Targets):**
        *   Carpool Rider CSAT >= 4.5.
        *   Carpool Driver CSAT >= 4.6.
        *   Carpool Cancellation Rate < 10%.

---

### Scenario 2: Short Video (TikTok/Reels) - Sharing Focus

**Question 2.1.1: You are launching Reels/Shorts. What are the key metrics for platform health and user engagement?**

**Overall Goal:** Successfully launch and grow a short-form video feature that increases user engagement, content creation, and overall platform health.

**1. Content Creation:**
    *   **G (Goal):** Encourage a high volume and frequency of diverse content creation.
    *   **S (Signals):**
        *   `event: reel_creation_started`, `attributes: user_id, timestamp, entry_point`
        *   `event: reel_tool_used`, `attributes: user_id, reel_session_id, tool_name (e.g., 'filter_X', 'sound_Y')`
        *   `event: reel_draft_saved`, `attributes: user_id, reel_session_id`
        *   `event: reel_published`, `attributes: user_id, reel_id, timestamp, creation_time_ms, tools_used_list, content_length_sec`
        *   `event: user_signup_completed`, `attributes: user_id, timestamp` (for new user tracking)
        *   `event: user_active_session_start`, `attributes: user_id, timestamp` (to identify active users)
    *   **M (Metrics):**
        *   **Number of Reels Created per Day/Week:** `COUNT(DISTINCT reel_id FROM reel_published events)`.
        *   **Creator Activation Rate:** `(COUNT(DISTINCT user_id FROM reel_published WHERE user_id IN (users active in last X days who had 0 previous reel_published events))) / COUNT(DISTINCT user_id FROM user_active_session_start in last X days)`. (Needs careful cohort definition).
        *   **Average Creative Tools Used per Published Reel:** `AVG(COUNT(tools_used_list))` from `reel_published`.
    *   **T (Targets):**
        *   Achieve 1 million Reels created per day within 3 months.
        *   Creator Activation Rate of 5% of DAU within 1 month.

**2. Content Consumption & Engagement:**
    *   **G (Goal):** Maximize user consumption and deep engagement with Reels content.
    *   **S (Signals):**
        *   `event: reel_view_impression`, `attributes: user_id, reel_id, timestamp, view_source (e.g., 'fyp', 'following', 'share')`
        *   `event: reel_view_progress`, `attributes: user_id, reel_id, session_id, watch_time_ms, percentage_watched (e.g., 25, 50, 75, 100), is_rewatch (boolean)`
        *   `event: reel_interaction`, `attributes: user_id, reel_id, interaction_type ('like', 'comment', 'share', 'save'), timestamp`
        *   `event: reel_session_summary`, `attributes: user_id, session_id, total_reels_viewed, total_watch_time_ms_in_reels, scroll_depth`
    *   **M (Metrics):**
        *   **Daily/Weekly Reels Views per User:** `SUM(reel_view_impression events) / DAU_Reels`. (DAU_Reels = users with >=1 `reel_view_impression`).
        *   **Average Time Spent in Reels per User:** `AVG(total_watch_time_ms_in_reels FROM reel_session_summary)`.
        *   **Reel Completion Rate:** `COUNT(reel_view_progress events WHERE percentage_watched=100) / COUNT(DISTINCT reel_id, user_id FROM reel_view_progress WHERE percentage_watched>=25)`. (Or based on `reel_view_impression`).
        *   **Engagement Rate per Reel:** `(SUM(reel_interaction events of type like/comment/share/save for a reel_id)) / COUNT(reel_view_impression events for that reel_id)`.
    *   **T (Targets):**
        *   Average Time Spent in Reels: 20 minutes per DAU within 3 months.
        *   Reel Completion Rate > 60%.
        *   Engagement Rate: Achieve an average of 10 engagements per 100 views.

**3. User Retention & Growth (Impact of Reels):**
    *   **G (Goal):** Ensure Reels contributes positively to overall user retention and attracts new users.
    *   **S (Signals):**
        *   (Existing user activity logs for overall platform usage, `reel_view_impression` to identify Reels users)
        *   `event: user_signup_referral`, `attributes: user_id, source, referred_by_feature ('reels_share_link')` (if possible)
    *   **M (Metrics):**
        *   **Retention Rate of Reels Users vs. Non-Reels Users (Cohort Analysis):** `D1/D7/D30 retention for users who engage with Reels vs. those who don't`.
        *   **DAU/MAU of Reels Feature:** `COUNT(DISTINCT user_id FROM reel_view_impression or reel_published events)`.
        *   **New User Acquisition Attributed to Reels:** Track users whose first meaningful interaction or acquisition path involves Reels. (Challenging, often needs survey/heuristics).
    *   **T (Targets):**
        *   Reels Users D30 Retention: +5% lift compared to Non-Reels Users within 6 months.
        *   Grow Reels MAU to 50% of platform MAU within 1 year.

**4. Platform Health & Guardrails:**
    *   **G (Goal):** Ensure Reels launch doesn't negatively impact other core features and maintains platform stability.
    *   **S (Signals):**
        *   (Existing logs for time spent/engagement on other features e.g., `main_feed_time_spent`, `stories_viewed`)
        *   `event: content_report`, `attributes: user_id_reporter, content_id, content_type ('reel', 'post'), reason_code, report_timestamp`
        *   `event: system_performance_log`, `attributes: service_name ('reels_backend', 'reels_feed_service'), latency_ms, error_rate, cpu_utilization`
    *   **M (Metrics):**
        *   **Time Spent on Core Feed (Guardrail):** Monitor `AVG(time_spent_main_feed)` for Reels users vs. non-Reels users.
        *   **Volume of Reported Reels:** `COUNT(content_report events WHERE content_type='reel') per 1M views`.
        *   **Reels Service Latency (p95/p99):** `PERCENTILE(latency_ms, 95/99) FROM system_performance_log WHERE service_name LIKE '%reels%'`.
    *   **T (Targets):**
        *   No more than a 5% decrease in average time spent on the core feed for active Reels users.
        *   Reported Reels < 100 per 1M views.
        *   Reels feed service p95 latency < 200ms.

---

**Question 2.1.2: How would you track if a user significantly changes their 'regular' location (e.g., moves cities) based on their activity?**

**Overall Goal:** Accurately and efficiently detect significant changes in a user's primary location to enable personalized experiences and understand user mobility, while respecting privacy.

*   **G (Goal):** Identify when a user has genuinely changed their primary operating city/region.
*   **S (Signals):**
    *   **Primary (Direct Location):**
        *   `event: app_session_start_with_gps`, `attributes: user_id, timestamp, lat, lon, accuracy_meters` (foreground app, permissioned)
        *   `event: ip_address_seen`, `attributes: user_id, timestamp, ip_address` (server-side)
        *   `event: user_profile_location_update`, `attributes: user_id, timestamp, new_city, old_city`
        *   `event: content_geotagged`, `attributes: user_id, content_id, lat, lon, timestamp`
    *   **Secondary (Indirect/Behavioral Location):**
        *   `event: local_search_query`, `attributes: user_id, timestamp, query_terms, inferred_query_location`
        *   `event: local_business_interaction`, `attributes: user_id, business_id, interaction_type, business_location`
        *   `event: network_change`, `attributes: user_id, timestamp, wifi_ssid_hashed, cell_tower_id` (if available and permissioned)
*   **M (Metrics) / Approach:**
    *   **1. Define 'Current Dominant Location (CDL)':**
        *   For each user, aggregate location signals (GPS, IP-geo, Wi-Fi/cell-geo) over a trailing window (e.g., 30 days).
        *   Weight signals by recency and accuracy (GPS > Wi-Fi > IP).
        *   Cluster these signals to determine a primary city/region for that period.
        *   **Metric:** `User_CDL_City (user_id, date, city_name, confidence_score)` - updated daily/weekly.
    *   **2. Detect 'Stable New Location Candidate':**
        *   If a user's CDL shifts to a new city (New_CDL_City) and remains consistent in that new city for a sustained period (e.g., > N days out of M recent days, say 20 out of 30 days).
        *   Cross-reference with secondary signals (local searches, interactions in New_CDL_City).
        *   **Metric:** `User_Potential_Move_Flag (user_id, old_city, new_city, detection_date, consistency_score)`
    *   **3. Confirm 'Significant Location Change':**
        *   If `User_Potential_Move_Flag` persists for a longer confirmation window (e.g., New_CDL_City is dominant for 45 out of last 60 days).
        *   AND/OR if explicit signals (profile update) or strong secondary signals corroborate.
        *   **Output:** `event: user_significant_location_change_detected`, `attributes: user_id, old_city, new_city, effective_date, detection_method_flags`
    *   **System Monitoring Metrics:**
        *   **Accuracy of Detection:** (Hard to get ground truth) Periodically sample and manually review, or compare against users who explicitly update their profile location. `% of auto-detected moves confirmed by subsequent profile update`.
        *   **Latency of Change Detection:** `AVG(time_diff between actual move start (estimated) and detection_date)`.
        *   **False Positive Rate:** `% of detected moves that revert to old location or were temporary travel`.
*   **T (Targets):**
    *   Detect >80% of actual long-term moves (based on validation samples) within 45 days of the move stabilizing.
    *   False Positive Rate (flagging travel as a move) < 5%.
    *   System can process location signals and update CDL for all active users daily.

---

**Question 2.1.3: How would you compare the engagement (e.g., likes) of original content versus content that is shared (i.e., a re-share of an original post)? What insights would this provide?**

**Overall Goal:** Understand the difference in engagement dynamics between original content (OC) and shared content (SC) to evaluate virality, sharing value, and content flow.

*   **G (Goal):** Determine if shared content drives comparable or different engagement patterns than original content, and quantify the amplification effect of sharing.
*   **S (Signals):**
    *   `event: content_created`, `attributes: user_id_creator, content_id_original, creation_timestamp, content_type`
    *   `event: content_shared`, `attributes: user_id_sharer, content_id_original, shared_instance_id, share_timestamp, share_platform (e.g., 'native_reshare', 'external_link'), sharing_user_comment`
    *   `event: engagement_on_content`, `attributes: user_id_engager, content_id_original, (optional) shared_instance_id_if_applicable, engagement_type ('like', 'comment', 'save', 'view'), engagement_timestamp`
    *   `event: view_on_content`, `attributes: user_id_viewer, content_id_original, (optional) shared_instance_id_if_applicable, view_timestamp, view_duration_ms`
    *   *(Critical DE Task: Ensure `engagement_on_content` and `view_on_content` can be correctly attributed to *either* the original post *or* a specific shared instance).* For a native reshare, the `shared_instance_id` is key. For views on OC, `shared_instance_id` would be null.
*   **M (Metrics):**
    *   **For Original Content (OC):**
        *   `Direct_Engagement_Rate_OC`: `SUM(engagements on OC where shared_instance_id IS NULL) / SUM(views on OC where shared_instance_id IS NULL)`
        *   `Total_Reach_OC`: `COUNT(DISTINCT user_id_viewer/engager for OC, including all its SC instances)`
    *   **For Shared Content (SC - per share instance, or aggregated for all shares of an OC):**
        *   `Engagement_Rate_SC`: `SUM(engagements on SC where shared_instance_id IS NOT NULL) / SUM(views on SC where shared_instance_id IS NOT NULL)` (Can be calculated per share, or averaged across shares of an OC).
        *   `Click_Through_To_Original_From_SC`: `COUNT(users clicking from SC to OC) / COUNT(views on SC)`
    *   **Comparative Metrics:**
        *   `Engagement_Lift_from_Sharing`: `(Total engagements on all SC instances of an OC) / (Total direct engagements on OC)`
        *   `Audience_Expansion_Ratio`: `COUNT(DISTINCT users engaging with SC of an OC who did NOT engage with OC directly) / COUNT(DISTINCT users engaging with OC directly)`
*   **T (Targets):**
    *   Achieve an average Engagement_Rate_SC that is at least 70% of Engagement_Rate_OC (indicating shares retain good engagement).
    *   Identify top 5% of OCs by Engagement_Lift_from_Sharing monthly (to understand viral drivers).
    *   Target Audience_Expansion_Ratio > 0.5 for successful shares (meaning shares reach a significant new audience).

---

**Question 2.1.4: How would you design a dashboard visualization to show how the launch of Reels is affecting engagement with other platform features (e.g., standard posts, image uploads, long-form videos)?**

**Overall Goal:** Provide a clear, actionable dashboard to monitor the impact (cannibalization or halo effect) of Reels on other key platform features.

*   **G (Goal):** Understand if Reels introduction is positively or negatively impacting engagement with existing features like Feed, Stories, etc.
*   **S (Signals):** (Need consistent instrumentation across all features)
    *   `event: user_session_start`, `attributes: user_id, session_id, timestamp, device_type`
    *   `event: feature_interaction`, `attributes: user_id, session_id, timestamp, feature_name ('Reels', 'Feed', 'Stories', 'Image_Upload'), interaction_type ('view', 'create', 'like', 'comment', 'share'), content_id (if applicable), time_spent_on_interaction_ms (for views/creations)`
    *   `event: content_creation`, `attributes: user_id, session_id, timestamp, feature_name, content_id`
*   **M (Metrics) - To be displayed on the dashboard, often comparing Reels users vs. Non-Reels users, or Pre/Post Reels launch cohorts:**
    *   **Overall Platform Metrics:**
        *   `Total Platform Time Spent per User`: `SUM(time_spent_on_interaction_ms) / DAU` (Line chart over time, with Reels launch marked).
        *   `DAU/MAU of Reels vs. Other Features`: Stacked area chart.
    *   **Feature-Specific Metrics (for each existing feature like 'Feed', 'Stories'):**
        *   `Average Time Spent per User on [Feature X]`: `SUM(time_spent where feature_name='[Feature X]') / COUNT(DISTINCT user_id interacting with [Feature X])`. (Compare for Reels Adopters vs. Non-Adopters; Pre vs. Post launch for all users).
        *   `Content Creations per User on [Feature X]`: `COUNT(content_creation where feature_name='[Feature X]') / COUNT(DISTINCT user_id interacting with [Feature X])`. (Same comparisons).
        *   `Engagement Rate on [Feature X]`: `SUM(likes/comments/shares on [Feature X]) / SUM(views on [Feature X])`. (Same comparisons).
    *   **Transition Metrics (Advanced):**
        *   `% of Sessions with Reels Interaction that also have [Feature X] Interaction`.
        *   `User Flow Sankey Diagram`: Visualizing user navigation paths between Reels and other features (e.g., `Feed -> Reels`, `Reels -> Feed`).
*   **T (Targets) / Thresholds for Dashboard:**
    *   **Guardrail Target:** No more than X% decrease in `Average Time Spent on Feed` for Reels adopters compared to a control group or pre-launch baseline within Y months.
    *   **Halo Target:** Identify if `Content Creations on Image_Upload` increases by Z% for active Reels creators (potential positive spillover).
    *   Set alerts if engagement on a critical feature drops by >N% post-Reels for specific user segments.

---

### Scenario 3: Streaming Platform (Netflix/Hulu)

**Question 3.1.1: For a video streaming platform, what are the different types of user engagement you could track? Define key metrics at the Platform, User, and Video levels.**

**Overall Goal:** Comprehensively track user engagement across platform, user, and content dimensions to understand service health, user satisfaction, and content performance.

**A. Platform-Level Engagement:**
*   **G (Goal):** Maintain a healthy, growing, and active subscriber base that regularly consumes content.
*   **S (Signals):**
    *   `event: user_login_success`, `attributes: user_id, timestamp, device_id`
    *   `event: streaming_session_start`, `attributes: user_id, session_id, timestamp, device_id`
    *   `event: streaming_session_end`, `attributes: user_id, session_id, timestamp, total_watch_time_ms_in_session, titles_watched_count_in_session`
    *   `event: subscription_change`, `attributes: user_id, timestamp, old_plan, new_plan, event_type ('new_sub', 'churn', 'upgrade', 'downgrade')`
    *   `event: feature_used`, `attributes: user_id, feature_name ('download', 'profile_creation', 'watchlist_add')`
*   **M (Metrics):**
    *   **DAU/MAU:** `COUNT(DISTINCT user_id FROM user_login_success OR streaming_session_start)` (daily/monthly).
    *   **Stickiness:** `DAU/MAU Ratio`.
    *   **Total Streaming Hours per Day/Week:** `SUM(total_watch_time_ms_in_session) / (1000*60*60)`.
    *   **Average Session Duration:** `AVG(total_watch_time_ms_in_session)`.
    *   **Churn Rate:** `COUNT(user_id FROM subscription_change WHERE event_type='churn' in period T) / COUNT(active subscribers at start of period T)`.
    *   **Content Library Utilization:** `(COUNT(DISTINCT title_id watched in period) / COUNT(DISTINCT title_id in catalog)) * 100%`.
*   **T (Targets):**
    *   MAU Growth: +X% quarter-over-quarter.
    *   Churn Rate: < Y% monthly.
    *   Average Streaming Hours per DAU: > Z hours.

**B. User-Level Engagement:**
*   **G (Goal):** Ensure individual users are finding value, consuming diverse content, and forming sticky viewing habits.
*   **S (Signals):**
    *   (From `streaming_session_end`): `total_watch_time_ms_in_session`, `titles_watched_count_in_session`
    *   `event: playback_completion_milestone`, `attributes: user_id, title_id, episode_id (if series), percentage_watched (e.g., 25, 50, 75, 90, 100), timestamp`
    *   `event: series_ binge_segment_detected`, `attributes: user_id, series_id, episode_ids_list, start_timestamp, end_timestamp, episode_count` (derived signal)
    *   `event: watchlist_add_remove`, `attributes: user_id, title_id, action ('add', 'remove')`
    *   `event: content_rating`, `attributes: user_id, title_id, rating (e.g., thumbs_up/down)`
*   **M (Metrics):**
    *   **Average Watch Time per User:** `SUM(total_watch_time_ms_in_session FOR user) / Number of days active` (per day/week/month).
    *   **Content Diversity per User:** `COUNT(DISTINCT title_id FROM playback_completion_milestone WHERE user_id=X AND percentage_watched > 10)` over a period.
    *   **Binge Frequency:** `COUNT(series_binge_segment_detected events FOR user_id=X) per month`.
    *   **User-Level Series Completion Rate:** `% of series started by user where user watches > N% of episodes (e.g., 80%)`.
    *   **Watchlist Engagement:** `COUNT(title_id viewed from watchlist) / COUNT(title_id added to watchlist)`.
*   **T (Targets):**
    *   Increase % of MAU watching > M unique titles per month by X%.
    *   Target Y% of series starters to complete >80% of episodes.
    *   Maintain average watchlist conversion > Z%.

**C. Video/Content-Level Engagement:**
*   **G (Goal):** Evaluate the performance of individual content titles in attracting and retaining viewers.
*   **S (Signals):**
    *   (From `playback_completion_milestone`): `user_id`, `title_id`, `episode_id`, `percentage_watched`
    *   `event: playback_start`, `attributes: user_id, title_id, episode_id, timestamp, source ('browse', 'search', 'recommendation_X')`
    *   `event: playback_stop_or_abandon`, `attributes: user_id, title_id, episode_id, timestamp, last_watched_position_ms, total_duration_ms`
    *   `event: in_video_interaction`, `attributes: user_id, title_id, interaction_type ('skip_intro', 'seek_forward', 'pause')`
*   **M (Metrics):**
    *   **Total Views/Streams per Title:** `COUNT(DISTINCT user_id FROM playback_start WHERE title_id=X AND watch_time > N seconds)`.
    *   **Average View Duration (AVD) per Title:** `AVG(watch_time from playback_stop_or_abandon) for title_id=X`.
    *   **Percentage Completion per Title:** `AVD / total_duration_ms for title_id=X`.
    *   **Audience Retention Curve (for a title):** `% of viewers remaining at T minute/percentage point of the video`. (Plot of `COUNT(users watching at point P) / COUNT(users who started at point 0)`).
    *   **Hook Rate (1st Episode Completion for Series):** `COUNT(users completing episode 1) / COUNT(users starting episode 1)`.
    *   **Rewatch Rate:** `COUNT(users with >1 playback_start for title_id=X) / COUNT(users with >=1 playback_start for title_id=X)`.
*   **T (Targets):**
    *   New premiere titles to achieve >X unique viewers in the first week.
    *   Target AVD for feature films > Y% of total duration.
    *   Series Hook Rate > Z% for new flagship series.

---

### Scenario 4: Cloud File Storage (Dropbox/Google Drive)

**Question 4.1.1: You're considering adding a new "Quick Access" feature that uses ML to predict which files a user might need next. How would you measure the success of this feature? What metrics would you track?**

**Overall Goal:** Ensure the "Quick Access" ML feature demonstrably improves user efficiency and satisfaction in finding files.

**1. Prediction Accuracy & Relevance (ML Model Quality):**
*   **G (Goal):** The Quick Access feature accurately predicts and surfaces files relevant to the user's current needs.
*   **S (Signals):**
    *   `event: quick_access_impression`, `attributes: user_id, session_id, timestamp, suggested_file_ids_list_ordered, model_version`
    *   `event: quick_access_click`, `attributes: user_id, session_id, timestamp, clicked_file_id, rank_of_clicked_file, model_version`
    *   `event: quick_access_negative_feedback`, `attributes: user_id, session_id, timestamp, unhelpful_file_id (optional), feedback_type ('not_relevant', 'dismiss')`
    *   `event: file_opened`, `attributes: user_id, session_id, timestamp, file_id, open_method ('quick_access', 'search', 'browse')`
*   **M (Metrics):**
    *   **Click-Through Rate (CTR) on Quick Access:** `COUNT(quick_access_click events) / COUNT(quick_access_impression events)`.
    *   **Mean Reciprocal Rank (MRR):** `AVG(1 / rank_of_clicked_file FOR each quick_access_click)` (Measures if relevant files are ranked high).
    *   **File Open Conversion from Quick Access:** `COUNT(file_opened events WHERE open_method='quick_access') / COUNT(quick_access_click events)`.
    *   **Negative Feedback Rate:** `COUNT(quick_access_negative_feedback events) / COUNT(quick_access_impression events)`.
*   **T (Targets):**
    *   CTR > X% (benchmark against similar features or A/B test variants).
    *   MRR > Y (e.g., 0.7, indicating high relevance in top ranks).
    *   File Open Conversion > Z%.
    *   Negative Feedback Rate < A%.

**2. User Efficiency & Time Savings:**
*   **G (Goal):** Quick Access demonstrably reduces the time and effort users spend finding files.
*   **S (Signals):**
    *   (From `file_opened`): `open_method`
    *   `event: search_query_executed`, `attributes: user_id, session_id, timestamp, search_terms`
    *   `event: navigation_action`, `attributes: user_id, session_id, timestamp, action_type ('folder_open', 'sort_files'), depth`
    *   (A/B test group assignment: `user_id, experiment_id, variant ('control', 'treatment_quick_access')`)
*   **M (Metrics) - Primarily via A/B Testing:**
    *   **Reduction in Manual Searches:** `AVG(COUNT(search_query_executed events per user))` in Treatment vs. Control.
    *   **Reduction in Navigation Actions:** `AVG(COUNT(navigation_action events per user))` in Treatment vs. Control before file open.
    *   **Time to File Open (for target files):** `AVG(timestamp_file_opened - timestamp_session_start_or_previous_action)` for files opened via Quick Access vs. other methods (needs careful definition of task start).
*   **T (Targets) - Based on A/B test results:**
    *   Statistically significant reduction (e.g., >10%) in searches per user for the treatment group.
    *   Statistically significant reduction in time to open commonly accessed files for treatment group.

**3. User Engagement & Adoption:**
*   **G (Goal):** Users actively adopt and frequently use the Quick Access feature.
*   **S (Signals):**
    *   (From `quick_access_impression`, `quick_access_click`)
    *   `event: user_first_quick_access_click`, `attributes: user_id, timestamp`
*   **M (Metrics):**
    *   **Adoption Rate:** `COUNT(DISTINCT user_id FROM user_first_quick_access_click) / COUNT(DISTINCT user_id FROM quick_access_impression)` within N days of first impression.
    *   **DAU/MAU of Quick Access:** `COUNT(DISTINCT user_id FROM quick_access_click events)` (daily/monthly).
    *   **Frequency of Use:** `AVG(COUNT(quick_access_click events per user) FOR active Quick Access users)`.
*   **T (Targets):**
    *   Adoption Rate: >X% of users exposed.
    *   Quick Access DAU as Y% of overall platform DAU.

---

### Scenario 5: DAU/MAU Analysis

**Question 5.1.1: Besides the DAU/MAU ratio, what other metrics would you use to measure user stickiness and engagement for a social media platform?**

**Overall Goal:** Gain a deeper, multi-dimensional understanding of user stickiness and engagement beyond simple DAU/MAU for a social media platform.

**1. Enhanced Frequency & Recency:**
*   **G (Goal):** Understand the true regularity and recency of user activity.
*   **S (Signals):**
    *   `event: app_open` or `session_start`, `attributes: user_id, timestamp`
    *   `event: user_active_event` (any significant interaction, e.g., view, like, post), `attributes: user_id, timestamp`
*   **M (Metrics):**
    *   **WAU/MAU, X-day Active Users / MAU (e.g., 3-day/MAU):** To capture users active on N out of M days.
    *   **Distribution of Active Days per Month:** Histogram showing `% users active 1 day, 2 days, ..., 30 days`.
    *   **Session Frequency per User:** `COUNT(session_start events for user_X) / period_days` (daily/weekly avg).
    *   **Time Between Sessions (Inter-Session Interval):** `AVG(timestamp_current_session - timestamp_previous_session)`.
    *   **L-ness (e.g., L7):** `DAU_today / COUNT(Unique users active exactly 7 days ago)`.
*   **T (Targets):**
    *   Increase % of MAU active >15 days a month by X%.
    *   Decrease average inter-session interval for engaged users by Y%.

**2. Depth of Engagement:**
*   **G (Goal):** Measure how deeply users are interacting with the platform's content and features.
*   **S (Signals):**
    *   `event: content_viewed`, `attributes: user_id, content_id, view_duration_ms, scroll_depth_percentage (if applicable)`
    *   `event: content_created`, `attributes: user_id, content_id, creation_type ('post', 'comment', 'story')`
    *   `event: social_interaction`, `attributes: user_id, target_user_id (optional), interaction_type ('like', 'share', 'dm_sent', 'friend_request_sent')`
    *   `event: feature_used`, `attributes: user_id, feature_name`
*   **M (Metrics):**
    *   **Time Spent per Active User per Day:** `SUM(session_durations for user_X on Day_Y)`.
    *   **Average Content Views per User per Session/Day.**
    *   **% of DAU/MAU Creating Content.**
    *   **% of DAU/MAU with Social Interactions.**
    *   **Number of Distinct Features Used per User per Week/Month.**
*   **T (Targets):**
    *   Increase % of DAU creating content by X%.
    *   Increase average distinct features used per MAU to Y.

**3. Granular Retention & User Tiers:**
*   **G (Goal):** Understand detailed retention patterns and the flow of users between engagement levels.
*   **S (Signals):**
    *   (User signup date from user dimension table)
    *   (Daily activity flags derived from `app_open` or `user_active_event`)
*   **M (Metrics):**
    *   **Day N Retention (D1, D7, D30 Cohorts):** `% of new users returning`.
    *   **Rolling N-Day Window Retention:** `% of users active in period X also active in period X+N_days`.
    *   **Resurrection Rate:** `% of previously churned users (inactive for >M days) becoming active again`.
    *   **Engagement Tiers (e.g., Power, Core, Casual, Dormant):** Defined by rules on active days/month, sessions/week, content created. Track `% of users in each tier` and `flow rates between tiers`.
*   **T (Targets):**
    *   Improve D7 retention for new users by X%.
    *   Increase the proportion of users in "Core" and "Power" tiers by Y%.

---

### Scenario 6: News Feed

**Question 6.1.1: If you were to optimize the News Feed algorithm, what metrics would you track to ensure a good user experience? How would you balance content diversity with engagement?**

**Overall Goal:** Optimize the News Feed algorithm to maximize positive user experience by delivering relevant, engaging, and diverse content.

**A. Core User Experience & Engagement (Is the feed enjoyable & engaging?):**
*   **G (Goal):** Users find the feed highly engaging and spend quality time on it.
*   **S (Signals):**
    *   `event: feed_session_start`, `attributes: user_id, session_id, timestamp`
    *   `event: feed_scroll`, `attributes: user_id, session_id, scroll_depth_pixels, scroll_velocity`
    *   `event: item_impression_in_feed`, `attributes: user_id, session_id, item_id, position_in_feed, timestamp, item_attributes (e.g., type, source, predicted_score)`
    *   `event: item_interaction_in_feed`, `attributes: user_id, session_id, item_id, interaction_type ('click', 'like', 'comment', 'share', 'hide', 'report', 'dwell_time_gt_threshold'), timestamp`
    *   `event: feed_session_end`, `attributes: user_id, session_id, duration_ms, items_viewed_count`
*   **M (Metrics):**
    *   **Time Spent in Feed per Session/Day:** `AVG(duration_ms FROM feed_session_end)`.
    *   **Scroll Depth per Session:** `AVG(max scroll_depth_pixels FROM feed_scroll)`.
    *   **Content Dwell Time:** `AVG(dwell_time_ms)` on items where `interaction_type='dwell_time_gt_threshold'`.
    *   **Positive Interaction Rate:** `(COUNT(item_interaction_in_feed WHERE interaction_type IN ('like', 'comment', 'share'))) / COUNT(item_impression_in_feed)`.
    *   **Negative Interaction Rate:** `(COUNT(item_interaction_in_feed WHERE interaction_type IN ('hide', 'report'))) / COUNT(item_impression_in_feed)`.
    *   **Items Viewed per Session:** `AVG(items_viewed_count FROM feed_session_end)`.
*   **T (Targets):**
    *   Increase Positive Interaction Rate by X% (A/B test).
    *   Decrease Negative Interaction Rate by Y% (A/B test).
    *   Maintain or increase Time Spent in Feed while improving positive interactions.

**B. Content Diversity & Discovery (Are users seeing varied and new content?):**
*   **G (Goal):** The feed exposes users to a healthy variety of content types, sources, and topics, preventing filter bubbles.
*   **S (Signals):**
    *   (From `item_impression_in_feed`): `item_attributes (content_type, source_id, topic_id)`
    *   `event: user_follow_action`, `attributes: user_id, target_source_id, action ('follow', 'unfollow')`
*   **M (Metrics):**
    *   **Number of Unique Content Sources Seen per User per Day/Week:** `COUNT(DISTINCT source_id FROM item_impression_in_feed)`.
    *   **Distribution of Content Types Seen:** `% of impressions from type A, type B, type C`.
    *   **Content Freshness:** `AVG(time_since_creation)` of items shown in feed.
    *   **Serendipity/Discovery Rate:** `% of impressions from sources/topics user hasn't interacted with recently or doesn't follow`. (Needs careful definition).
    *   **Follow Rate from Feed Impressions:** `COUNT(user_follow_action WHERE action='follow') / COUNT(item_impression_in_feed from unfollowed sources)`.
*   **T (Targets):**
    *   Ensure user sees items from at least N unique sources per week.
    *   Maintain a target distribution for key content types (e.g., no single type > X% of impressions).
    *   Increase Discovery Rate by Y% (A/B test new diversification algorithm components).

**C. Content Relevance & Personalization (Is content right for the user?):**
*   **G (Goal):** The feed content is highly relevant and personalized to individual user preferences and context.
*   **S (Signals):**
    *   (From `item_interaction_in_feed`): `interaction_type ('click', 'like', 'comment', 'share', 'hide', 'report', 'dwell_time_gt_threshold', 'profile_click_from_item', 'expand_item')`
    *   `event: item_seen_long_enough_to_evaluate`, `attributes: user_id, item_id, duration_on_screen_ms`
*   **M (Metrics):**
    *   **Personalized Positive Interaction Rate:** Same as Positive Interaction Rate, but weighted by user's predicted affinity for the item, or compared against a baseline non-personalized feed in A/B tests.
    *   **Profile Click Rate from Feed:** `COUNT(item_interaction_in_feed WHERE interaction_type='profile_click_from_item') / COUNT(item_impression_in_feed)`.
    *   **"See More" / Expand Rate:** `COUNT(item_interaction_in_feed WHERE interaction_type='expand_item') / COUNT(item_impression_in_feed where item was contractable)`.
    *   **Engagement with Diverse Topics per User:** `COUNT(DISTINCT topic_id FROM item_interaction_in_feed WHERE interaction_type is positive) per user per week`.
*   **T (Targets):**
    *   A/B tests show statistically significant lift in positive interactions for personalized algorithm vs. baseline.
    *   Increase engagement with X diverse topics per user per week by Y%.

**D. Counter-Metrics & Negative Outcomes:**
*   **G (Goal):** Ensure feed optimization doesn't lead to negative user experiences or unintended platform harm.
*   **S (Signals):**
    *   (From `item_interaction_in_feed`): `interaction_type ('hide', 'report', 'unfollow_source_from_item')`
    *   `event: user_survey_response`, `attributes: user_id, survey_id ('feed_satisfaction'), question_id, response_value (e.g., complaints about echo chambers, boredom)`
    *   `event: app_uninstall`, `attributes: user_id, reason (if captured)`
*   **M (Metrics):**
    *   **Negative Feedback Rate (hides, reports, unfollows from item).**
    *   **Surveyed User Complaints about Echo Chambers/Boredom.**
    *   **Creator Complaints about Reduced Reach (monitored via community channels/surveys).**
    *   **Correlation of High Engagement with Potentially Harmful Content Categories (requires content classifiers).**
*   **T (Targets):**
    *   Keep Negative Feedback Rate below X%.
    *   No significant increase in user complaints about feed quality post-algorithm change.

---

### Scenario 7: Photo Upload (Instagram-like)

**Question 7.1.1: How would you measure the quality of the photo upload experience for users? What metrics would help identify friction points in the process?**

**Overall Goal:** Ensure a fast, reliable, and easy-to-use photo upload experience that maximizes successful content creation.

**1. Success & Completion Rates (Overall Health):**
*   **G (Goal):** Users can successfully complete the photo upload process with minimal failures.
*   **S (Signals):**
    *   `event: upload_flow_initiated`, `attributes: user_id, session_id, timestamp, source ('gallery', 'camera')`
    *   `event: upload_media_selected`, `attributes: user_id, session_id, media_id, file_size_kb, media_type`
    *   `event: upload_edit_screen_opened`, `attributes: user_id, session_id`
    *   `event: upload_caption_screen_opened`, `attributes: user_id, session_id`
    *   `event: upload_attempt_started` (actual data transfer), `attributes: user_id, session_id, media_id`
    *   `event: upload_success`, `attributes: user_id, session_id, media_id, post_id, upload_duration_ms, final_file_size_kb`
    *   `event: upload_failure`, `attributes: user_id, session_id, media_id (if available), failure_step ('selection', 'editing', 'transfer', 'processing'), error_code, network_type`
*   **M (Metrics):**
    *   **Overall Upload Success Rate:** `COUNT(upload_success events) / COUNT(upload_flow_initiated events)`.
    *   **Funnel Conversion Rates:** E.g., `(COUNT(upload_media_selected) / COUNT(upload_flow_initiated))`, `(COUNT(upload_attempt_started) / COUNT(upload_caption_screen_opened))` etc.
    *   **Abandonment Rate at each Key Step:** `1 - Funnel Conversion Rate` for that step.
*   **T (Targets):**
    *   Overall Upload Success Rate > 99.X%.
    *   Identify and reduce the largest percentage drop-off point in the funnel by Y%.

**2. Speed & Performance (User Perception & Technical Health):**
*   **G (Goal):** The photo upload process feels fast and responsive to the user.
*   **S (Signals):**
    *   (From `upload_success`): `upload_duration_ms` (end-to-end)
    *   Timestamped events for each step: `upload_flow_initiated_ts`, `upload_media_selected_ts`, `upload_edit_screen_opened_ts`, ..., `upload_success_ts`.
    *   `event: client_performance_metric`, `attributes: user_id, metric_name ('time_to_load_gallery_ms', 'filter_apply_time_ms'), value`
    *   `event: app_responsiveness_issue`, `attributes: user_id, issue_type ('ANR', 'frame_drop_burst'), during_flow ('upload')`
*   **M (Metrics):**
    *   **P50, P90, P95 End-to-End Upload Time:** `PERCENTILE(upload_duration_ms, 50/90/95)` from `upload_success`.
    *   **Duration of Key Steps (P50, P90):** E.g., Time from `upload_media_selected_ts` to `upload_edit_screen_opened_ts`.
    *   **App Responsiveness:** `COUNT(app_responsiveness_issue WHERE during_flow='upload') / COUNT(upload_flow_initiated)`.
*   **T (Targets):**
    *   P90 End-to-End Upload Time < X seconds (segmented by region/network type).
    *   Reduce P90 time for critical slow steps (e.g., media processing) by Y%.

**3. Error & Failure Analysis (Diagnosing Problems):**
*   **G (Goal):** Minimize upload failures and understand the root causes of errors.
*   **S (Signals):**
    *   (From `upload_failure`): `failure_step`, `error_code`, `network_type`, `file_size_kb`
    *   `event: upload_retry_attempt`, `attributes: user_id, original_media_id`
*   **M (Metrics):**
    *   **Overall Failure Rate:** `COUNT(upload_failure events) / COUNT(upload_flow_initiated events)`.
    *   **Failure Rate by Step:** `COUNT(upload_failure WHERE failure_step='X') / COUNT(events reaching step X)`.
    *   **Top Error Codes:** Distribution of failures by `error_code`.
    *   **Retry Success Rate:** `COUNT(upload_success after retry) / COUNT(upload_retry_attempt)`.
*   **T (Targets):**
    *   Overall Failure Rate < X%.
    *   Reduce failure rate for the most common error codes by Y%.

**4. Engagement with Upload Features (Ease of Use & Value):**
*   **G (Goal):** Users easily discover and utilize valuable upload features like editing and tagging.
*   **S (Signals):**
    *   `event: upload_edit_action`, `attributes: user_id, session_id, edit_tool_used ('filter_X', 'crop', 'brightness')`
    *   `event: upload_metadata_added`, `attributes: user_id, session_id, metadata_type ('caption', 'user_tag', 'location_tag')`
    *   `event: upload_draft_saved`, `attributes: user_id, session_id`
*   **M (Metrics):**
    *   **Adoption of Editing Tools:** `% of successful uploads where COUNT(upload_edit_action events) > 0`.
    *   **Adoption of Metadata Features:** `% of successful uploads where COUNT(upload_metadata_added for type X) > 0`.
    *   **Draft Save Rate:** `COUNT(upload_draft_saved events) / COUNT(upload_caption_screen_opened events)`.
*   **T (Targets):**
    *   Increase adoption of key editing tool Y by X%.
    *   Ensure caption adoption rate is above Z%.

---

### Scenario 8: FB Messenger

**Question 8.1.1: What metrics would you use to analyze messaging patterns and identify highly engaged users versus users at risk of churning?**

**Overall Goal:** Understand messaging engagement deeply to identify valuable users and proactively detect/mitigate churn risk.

**A. Core Engagement Metrics (User Level):**
*   **G (Goal):** Quantify the breadth, depth, and richness of individual user messaging activity.
*   **S (Signals):** (From `fact_messages_msg` table or similar event stream)
    *   `event: message_sent`, `attributes: sender_user_key, conversation_key, message_type_key (text, image, reaction), timestamp, character_count, media_count`
    *   `event: message_received`, `attributes: receiver_user_key, conversation_key, message_type_key, timestamp` (often inferred from sent messages)
    *   `event: app_session_start`, `attributes: user_key, timestamp, session_type ('messenger')`
    *   `event: conversation_created`, `attributes: user_key_creator, conversation_key, participant_user_keys_list`
*   **M (Metrics):**
    *   **Messages Sent per User (MSU) per Day/Week.**
    *   **Active Messaging Days per Week/Month.**
    *   **Number of Unique Active Conversations (Threads) per User per Week.**
    *   **Rich Media Usage Rate:** `% of sent messages containing media/reactions`.
    *   **Conversations Initiated per User per Week.**
*   **T (Targets - for defining baseline/healthy):**
    *   Establish baseline P25/P50/P75 values for MSU, Active Days, Unique Convos for the user base.

**B. Identifying Highly Engaged Users:**
*   **G (Goal):** Define and identify users exhibiting patterns of high, consistent, and rich interaction.
*   **S (Signals):** (Aggregated from core signals over a period, e.g., last 28 days)
    *   `user_daily_activity_summary: user_key, date, messages_sent_count, unique_conversations_active_count, rich_media_sent_count, sessions_count`
*   **M (Metrics) - User-level features for segmentation/scoring:**
    *   **High Message Volume:** Consistently in top Xth percentile for MSU.
    *   **High Active Days:** E.g., active >Y days out of last 28.
    *   **Diverse Conversations:** Active in >Z unique conversations weekly.
    *   **High Rich Media Usage:** Top Xth percentile for rich media rate.
    *   **Composite Engagement Score:** Weighted sum/model output based on these features.
*   **T (Targets):**
    *   Identify top 5-10% of users as "Power Users" based on composite score.
    *   Track stability of this Power User segment over time.

**C. Identifying Users at Risk of Churn:**
*   **G (Goal):** Proactively identify users showing declining engagement or consistently low activity, indicating churn risk.
*   **S (Signals):** (Trends and absolute values from `user_daily_activity_summary`)
    *   Week-over-week change in `messages_sent_count`.
    *   Week-over-week change in `active_conversations_count`.
    *   Days since last `message_sent` event.
    *   `event: app_uninstall` (if available)
    *   `event: notification_settings_change` (e.g., user turns off all notifications)
*   **M (Metrics) - User-level flags/scores for churn risk:**
    *   **Significant Drop in MSU/Active Days:** E.g., >50% WoW decrease for 2 consecutive weeks.
    *   **Sustained Low Activity:** E.g., < N messages sent in last 28 days AND < M active days.
    *   **High Inactivity Period:** Last message sent > X days ago.
    *   **Churn Prediction Score:** Output of an ML model trained on historical churners and their preceding activity patterns.
*   **T (Targets):**
    *   Identify X% of users as "At Risk" monthly.
    *   Achieve Y% precision/recall for churn prediction model in identifying actual churners within Z days.

---

### Scenario 9: Food Delivery (DoorDash) - Order Batching

**Question 9.1.1: How would you measure the success of a new order batching algorithm for a food delivery platform? What metrics would you track from the customer, driver, and platform perspectives?**

**Overall Goal:** Optimize order batching to improve system efficiency and economics while maintaining or improving customer and driver satisfaction.

**A. Customer Perspective (Focus: Experience & Satisfaction):**
*   **G (Goal):** Batching does not significantly degrade timeliness, food quality, or accuracy for customers.
*   **S (Signals):**
    *   `event: order_placed`, `attributes: order_id, user_id, restaurant_id, estimated_delivery_time_ts, is_batched_order (boolean, if known at placement, or enriched later)`
    *   `event: order_delivered`, `attributes: order_id, actual_delivery_time_ts`
    *   `event: customer_support_ticket`, `attributes: order_id, user_id, issue_type ('late_delivery', 'cold_food', 'wrong_item'), refund_amount_usd`
    *   `event: customer_rating_order`, `attributes: order_id, user_id, overall_rating, food_quality_rating`
*   **M (Metrics) - Compare Batched vs. Non-Batched cohorts, or A/B test algorithm versions:**
    *   **Average Delivery Time Increase for Batched Orders:** `AVG(Actual_Delivery_Time_Batched) - AVG(Actual_Delivery_Time_Non_Batched)` (controlling for distance/prep).
    *   **ETA Accuracy for Batched Orders:** `AVG(Actual_Delivery_Time - Predicted_ETA)` for batched.
    *   **Cold Food / Wrong Item Report Rate for Batched Orders:** `COUNT(tickets with issue_type 'cold_food'/'wrong_item' on batched orders) / COUNT(batched_orders)`.
    *   **Average Food Quality Rating for Batched Orders.**
*   **T (Targets):**
    *   Mean delivery time increase for batched orders < X minutes.
    *   Cold food report rate for batched orders <= Y% (parity or small defined increase over non-batched).

**B. Driver Perspective (Focus: Earnings & Efficiency):**
*   **G (Goal):** Batching increases driver earnings per hour and operational efficiency without undue burden.
*   **S (Signals):**
    *   `event: driver_batch_offer_received`, `attributes: driver_id, batch_id, order_ids_list, offered_pay_usd`
    *   `event: driver_batch_offer_response`, `attributes: driver_id, batch_id, response ('accepted', 'rejected')`
    *   `event: driver_pickup_complete`, `attributes: driver_id, order_id, timestamp`
    *   `event: driver_delivery_complete`, `attributes: driver_id, order_id, timestamp, distance_driven_km_for_order, tips_usd`
    *   `event: driver_online_session`, `attributes: driver_id, start_ts, end_ts, total_online_time_ms, total_active_delivery_time_ms`
*   **M (Metrics) - Compare for batches vs. single orders, or A/B test algorithm versions:**
    *   **Driver Earnings per Hour (Online Time or Active Time):** `(SUM(offer_pay + tips)) / SUM(online_time_hours OR active_time_hours)`.
    *   **Deliveries per Hour (Active Time).**
    *   **Mileage per Delivery / per Dollar Earned.**
    *   **Batch Offer Acceptance Rate.**
    *   **Average Time per Batched Delivery (from first pickup to last dropoff).**
*   **T (Targets):**
    *   Increase average driver earnings per hour by X% for batched routes.
    *   Maintain Batch Offer Acceptance Rate > Y%.

**C. Platform Perspective (Focus: Economics & Marketplace Health):**
*   **G (Goal):** Improve overall system efficiency, reduce costs, and grow order volume through effective batching.
*   **S (Signals):**
    *   (From `order_placed`): `is_batched_order`, `order_value_usd`, `platform_fee_usd`
    *   (From `driver_delivery_complete`): `distance_driven_km_for_order` (can sum for batch vs. sum if unbatched)
    *   `event: batch_creation_details`, `attributes: batch_id, order_ids_list, algorithm_version, predicted_efficiency_gain_km, predicted_time_savings_ms`
*   **M (Metrics):**
    *   **Batching Rate:** `% of orders that are batched`.
    *   **Cost per Delivery (CPD):** Compare average driver payout + incentives for batched vs. unbatched deliveries.
    *   **Marketplace Efficiency Gain:** `(Total_distance_if_unbatched - Total_distance_batched) / Total_deliveries_in_batches` (km saved per delivery).
    *   **Order Throughput / Capacity Increase:** Increase in total deliveries completed per hour in a region with the new batching algorithm.
    *   **Impact on Average Delivery Fees for Customers (if dynamic).**
*   **T (Targets):**
    *   Increase Batching Rate to X% of eligible orders.
    *   Reduce average Cost per Delivery by Y% through batching.
    *   Achieve Z km average distance saved per batched delivery.
