# Scenario 5: DAU/MAU Analysis - Beyond Stickiness

## Question 5.1.1: Beyond DAU/MAU Ratio

**Interviewer:** "DAU/MAU ratio is commonly used to measure engagement stickiness. But what metrics would you track beyond DAU/MAU to better understand user stickiness and engagement?"

**Candidate Answer (Structured Bullet Points):**

"While DAU/MAU is a valuable baseline metric, it doesn't capture the nuance of user engagement patterns. To get a more complete picture of stickiness and engagement quality, I'd track several complementary metrics across frequency, depth, and behavior patterns.

*   **I. Frequency & Consistency Metrics (Going Beyond Daily Active):**

    *   **Distribution of Active Days per Month:**
        *   Instead of just the ratio, look at the distribution: Are users active 1-2 days, 5-10 days, or 20+ days per month?
        *   Segments like: Casual (1-5 days), Regular (6-15 days), Core (16+ days per month).
        *   *Insight:* A DAU/MAU of 0.3 could come from 30% using daily OR 60% using every other day.

    *   **Session Frequency:**
        *   Average sessions per active day per user.
        *   Distribution of session frequency: Single-session users vs. multiple daily sessions.
        *   *Insight:* Multiple sessions suggest the app is becoming habitual.

    *   **Inter-Session Intervals:**
        *   How long between sessions for active users? 
        *   Percentage of users returning within 24 hours, 48 hours, week.
        *   *Insight:* Shorter intervals indicate stronger engagement loops.

*   **II. Depth & Quality of Engagement (How Much Users Do When Active):**

    *   **Time Spent per Session & per Active Day:**
        *   Average session duration and total time spent on active days.
        *   Distribution of session lengths: Quick check-ins vs. longer engaged sessions.

    *   **Actions per Session/Active Day:**
        *   Number of meaningful actions taken (posts, likes, comments, searches, purchases).
        *   Depth of navigation: How many screens/features accessed per session.

    *   **Feature Breadth:**
        *   Number of distinct features/sections used per week/month.
        *   Percentage of users who are single-feature vs. multi-feature users.
        *   *Insight:* Multi-feature usage often indicates stickier, more valuable users.

*   **III. Content Creation vs. Consumption Balance:**

    *   **Creator Participation Rate:**
        *   Percentage of active users who create content (posts, comments) vs. purely consume.
        *   Frequency of content creation among creators.

    *   **Social Interaction Metrics:**
        *   Percentage of users engaging with others (likes, comments, follows) vs. passive browsing.
        *   Network effects: Users with more connections tend to be stickier.

*   **IV. Retention & Lifecycle Patterns:**

    *   **L7, L14, L30 Retention Curves:**
        *   More granular than monthly averages - track users returning after 7, 14, 30 days.
        *   Cohort-based retention analysis by acquisition source, user segment.

    *   **Resurrection Patterns:**
        *   Rate of users returning after periods of inactivity (1 week, 1 month dormant).
        *   What brings dormant users back (notifications, friend activity, new features)?

    *   **Activity Progression/Regression:**
        *   Users moving between engagement tiers over time (casual → regular → core).
        *   Early warning indicators for users becoming less engaged.

*   **V. Quality Indicators & Satisfaction Proxies:**

    *   **Task Completion Rates:**
        *   Success rate for key user journeys (posting content, finding information, completing purchases).
        *   Abandonment rates at key friction points.

    *   **User-Initiated vs. Notification-Driven Sessions:**
        *   Organic usage (user opens app directly) vs. prompted usage (from notifications).
        *   *Insight:* Higher organic usage suggests stronger intrinsic engagement.

    *   **Negative Engagement Signals:**
        *   Rate of uninstalls, account deactivations, opting out of notifications.
        *   *Critical:* These are often stronger predictors of churn than decreased activity alone.

*   **VI. Cohort-Specific Analysis:**

    *   **New User Activation Patterns:**
        *   Time to first meaningful action, progression through onboarding.
        *   DAU/MAU progression for new user cohorts in their first 30-90 days.

    *   **Segment-Specific Stickiness:**
        *   Different engagement patterns by user demographics, acquisition channel, device type.
        *   Power users vs. casual users behavioral differences.

By tracking these richer metrics alongside DAU/MAU, we can identify users who appear 'active' in DAU counts but aren't truly engaged, spot early churn warning signs, and understand what drives different types of valuable engagement."

## Question 5.1.2: Analyzing DAU/MAU Decline

**Interviewer:** "Your platform's DAU/MAU ratio has declined from 0.65 to 0.58 over the past month. Walk through your analysis approach to identify the root cause."

**Candidate Answer (Structured Bullet Points):**

"A 7-percentage-point drop in DAU/MAU ratio is significant and needs immediate investigation. I'd approach this systematically by decomposing the metric, analyzing user segments, and examining external factors.

*   **I. Metric Decomposition & Initial Data Validation:**

    *   **Verify Data Quality:**
        *   Check for tracking issues, data pipeline problems, or definition changes.
        *   Compare raw DAU and MAU numbers vs. just the ratio to see if it's a numerator or denominator issue.

    *   **Time Series Analysis:**
        *   When exactly did the decline start? Gradual vs. sudden drop?
        *   Correlate with any known events (feature launches, marketing campaigns, external events).

    *   **DAU vs MAU Contribution Analysis:**
        *   Is DAU declining faster than normal, or is MAU growing in a way that dilutes the ratio?
        *   New user influx without corresponding daily engagement could lower the ratio.

*   **II. User Segment Analysis:**

    *   **Cohort Breakdown:**
        *   Analyze by user registration cohorts: Are newer users less sticky, or are tenured users becoming less active?
        *   Different acquisition channels may have varying engagement patterns.

    *   **Geographic & Demographic Segmentation:**
        *   Is the decline uniform across regions, age groups, device types?
        *   Seasonal or cultural factors affecting specific user segments?

    *   **Engagement Tier Analysis:**
        *   How are different user segments (casual, regular, core) contributing to the decline?
        *   Are core users becoming regular, or regular users becoming casual?

*   **III. User Behavior Deep Dive:**

    *   **Session Pattern Changes:**
        *   Are users having fewer sessions per active day?
        *   Changes in session duration or actions per session?

    *   **Feature Usage Analysis:**
        *   Which features are showing decreased engagement?
        *   New feature launches that might be cannibalizing existing engagement?

    *   **Content & Feed Quality:**
        *   Algorithm changes affecting content relevance?
        *   Supply-side issues (fewer creators, lower content quality)?

*   **IV. External Factor Investigation:**

    *   **Competitive Landscape:**
        *   Major competitor launches or marketing campaigns?
        *   Market share shifts in app downloads or time spent?

    *   **Seasonal & Environmental Factors:**
        *   Expected seasonal patterns (back to school, holidays)?
        *   External events affecting user behavior (news, economic changes)?

    *   **Platform & Technical Issues:**
        *   App performance degradation, increased crash rates?
        *   Changes in app store rankings or discovery?

*   **V. Hypothesis Development & Testing:**

    *   **Develop Specific Hypotheses:**
        *   H1: New user onboarding changes reduced first-week engagement
        *   H2: Algorithm changes decreased content relevance for regular users
        *   H3: Increased competition from TikTok/other apps
        *   H4: Seasonal return-to-school pattern affecting college-age users

    *   **Test Each Hypothesis:**
        *   Use data to validate or reject systematically
        *   A/B test historical changes if possible
        *   User surveys or qualitative research for behavioral insights

*   **VI. Recovery Strategy & Monitoring:**

    *   **Immediate Actions:**
        *   Revert recent changes if they're causing the decline
        *   Improve onboarding or re-engagement campaigns for affected segments

    *   **Long-term Solutions:**
        *   Product improvements based on root cause analysis
        *   Enhanced personalization or content recommendation systems

    *   **Monitoring Plan:**
        *   Daily tracking of DAU/MAU and related metrics
        *   Early warning systems for future declines
        *   Regular cohort and segment analysis

The key is moving quickly but systematically, using data to guide decisions while considering that DAU/MAU changes often reflect deeper user experience issues that require product-level solutions." 