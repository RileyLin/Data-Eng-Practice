# Scenario 2: Short Video (TikTok/Reels) - Sharing Focus

## Question 2.1.1: Measuring Success

**Interviewer:** "You are launching Reels/Shorts. What are the key metrics for platform health and user engagement?"

**Candidate Answer (Structured Bullet Points):**

"Launching a short-form video feature like Reels/Shorts aims to boost user engagement, attract new users, and open monetization channels. To measure its success, I'd track metrics across several key areas:

*   **I. Content Creation Metrics:** (Are users making content?)
    *   **Volume & Frequency:**
        *   **Number of Reels/Shorts Created (per day/week):** Overall content pipeline.
        *   **Average Creations per Creating User:** Depth of creator engagement.
        *   *Critical Question:* Is creation concentrated among a few power users or widely distributed?
    *   **Creator Activation & Onboarding:**
        *   **Creator Activation Rate:** `% of active platform users creating their first Reel/Short within X days`.
        *   **Time to Create First Reel/Short:** Measures ease of use of creation tools.
    *   **Tool Usage & Creation Quality:**
        *   **Adoption Rate of Creative Tools (filters, sounds, effects):** Which tools are valuable?
        *   **Drafts Started vs. Published Ratio:** High ratio might indicate friction in finalizing content.
        *   **Content Diversity (Qualitative/Topic Modeling):** Is content varied or homogenous?

*   **II. Content Consumption Metrics:** (Are users watching and engaging?)
    *   **Overall Consumption:**
        *   **Reels/Shorts Views per User (per day/week).**
        *   **Total Time Spent in Reels/Shorts Tab/Feed per User (per day/week).**
            *   *Critical Question:* Is this time additive to platform time, or cannibalizing other features?
    *   **Engagement per Video:**
        *   **Average View Duration per Reel/Short & Completion Rate (% watched to end).**
        *   **Rewatch Rate:** How often are users re-watching content?
        *   **Engagement Rate per Reel/Short:** `(Likes + Comments + Shares + Saves) / Views`.
            *   *Consideration:* Weight different interactions (e.g., a 'save' or 'share' is often more valuable than a 'like').
    *   **Session Behavior:**
        *   **Scroll Depth / Number of Swipes per Session in Feed.**
    *   **Content Discovery Effectiveness:**
        *   **Impressions from "For You" Page (FYP) vs. Following Feed:** Measures algorithm effectiveness.
        *   **CTR on Reels/Shorts from other surfaces (e.g., stories, main feed).**

*   **III. User Retention & Growth Metrics:** (Is it keeping users and attracting new ones?)
    *   **Feature-Specific Activity:**
        *   **DAU/MAU of Reels/Shorts Users.**
    *   **Impact on Overall Retention:**
        *   **Retention Rate of Reels/Shorts Users vs. Non-Users (Cohort Analysis).**
        *   **Churn Rate of Reels/Shorts Non-Users vs. Users.**
    *   **User Acquisition:**
        *   **New User Acquisition Attributed to Reels/Shorts** (via surveys, referral tracking if possible).
        *   **Resurrection Rate:** Are inactive users returning due to Reels/Shorts?

*   **IV. Platform Health & Monetization Metrics:** (Broader impact)
    *   **Impact on Other Features (Guardrail Metrics):**
        *   **Cannibalization Analysis:** Monitor engagement changes (time spent, interaction rates) in primary feed, stories, DMs post-Reels launch. Requires A/B testing or careful pre/post analysis.
        *   **Halo Effect Analysis:** Is Reels driving increased engagement in *other* parts of the app?
    *   **Content Moderation & Safety:**
        *   **Volume of Reported Content/Violations in Reels/Shorts.**
    *   **Monetization (If applicable):**
        *   **Ad Impressions & CTR in Reels/Shorts feed.**
        *   **Advertiser Demand & CPMs for Reels/Shorts inventory.**
    *   **Technical Performance:**
        *   **Server Load, Latency, Crash Rates within the Reels/Shorts experience.**

*   **V. Slicing Dimensions for All Metrics:**
    *   **User Segment:** New vs. Existing, Demographics (Age, Location), Creator vs. Consumer.
    *   **Content Category/Genre (if identifiable).**
    *   **Device Type/OS.**
    *   **Time (hour of day, day of week, seasonality).**
    *   **Creator Tier (professional, casual).**

*   **VI. Critical Success Factors & Trade-offs to Monitor:**
    *   **Creator vs. Consumer Experience Balance.**
    *   **Content Quality vs. Quantity (especially early on).**
    *   **Impact of Monetization on User Experience.**
    *   **Recommendation Algorithm Performance (vital for discovery and satisfaction).**

By comprehensively tracking these areas, we can assess the true impact of Reels/Shorts and iterate towards a successful and healthy feature."

## Question 2.1.2: Dashboard Visualization for Cross-Platform Impact

**Interviewer:** "How would you design a dashboard visualization to show how the launch of Reels is affecting engagement with other platform features (e.g., standard posts, image uploads, long-form videos)?"

**Candidate Answer (Structured Bullet Points):**

"To visualize Reels' impact on other features, I'd design a dashboard focused on identifying cannibalization, halo effects, and shifts in user behavior, aiming for clarity and actionability.

*   **I. Dashboard Goals:**
    *   Monitor overall platform health post-Reels launch.
    *   Pinpoint features gaining/losing engagement due to Reels.
    *   Identify user segments most affected by Reels introduction.
    *   Enable data-driven decisions about feature prioritization and resource allocation.

*   **II. Top-Level Overview (Executive Summary):**
    *   **Overall Engagement Trend:** Line chart (Total Platform Time Spent, DAU/MAU, Composite Engagement Score) with Reels launch marked. *Include pre-launch baseline.*
    *   **Reels Adoption vs. Overall Active Users:** Stacked area chart (Total Active Users, with segment for Reels Active Users).
    *   **High-Level Impact KPIs:** % change pre/post Reels for: Time Spent (Reels vs. Feature X), Content Creation (Reels vs. Feature X), Engagement Rate (Reels vs. Feature X). *Use clear color-coding (green/red/yellow) and up/down arrows.*

*   **III. Feature-by-Feature Impact Analysis:**
    *   **Time Spent Comparison:** Grouped line chart (Time on [Existing Feature] vs. Time on Reels). Segment by users of both, only existing, only Reels.
    *   **Engagement Actions Trends:** Multi-line chart (likes, comments, shares, etc. for the feature) comparing pre-Reels, post-Reels (all users), and post-Reels (Reels users vs. non-Reels users).
    *   **Engagement Rate Trends:** Line chart (Engagement rate for existing feature over time) with Reels launch marked.
    *   **User Flow/Transition (Advanced):** Sankey diagram (From Main Feed -> Reels, Reels -> Main Feed, etc.) comparing pre/post launch flows.

*   **IV. User Segmentation Analysis:**
    *   **Cohort Performance Matrix:** Heatmap showing engagement changes for different user segments (new vs. existing, demographics, behavior-based) across features.
    *   **User Journey Changes:** Before/after flow charts showing typical session paths and time allocation.
    *   **Feature-Specific Churn/Retention:** Cohort retention curves for users of existing features (compare pre/post Reels cohorts). Are Reels adopters more/less retained on other features?

*   **V. Interaction & Cross-Pollination Effects:**
    *   **Content Cross-Posting:** Track users posting Reels content to other features (Stories, main feed) and engagement performance.
    *   **Creator Behavior Changes:** Analyze how content creators are splitting time/effort between Reels and traditional content formats.
    *   **Discovery Impact:** How is content in traditional feeds performing when creators also produce Reels?

*   **VI. Key Design Principles:**
    *   **Time-Based Toggle:** Easy switching between weekly, monthly, and custom date ranges.
    *   **Baseline Comparison:** Always show pre-Reels performance as reference.
    *   **Novelty Effect:** Monitor long-term trends beyond initial Reels surge.
    *   **Segmentation Filters:** Ability to slice all views by user demographics, behavior, and feature usage patterns.
    *   **Alert System:** Automated flags for significant negative changes in existing feature performance.

This dashboard would be a central tool for understanding the interplay between Reels and the existing platform ecosystem." 