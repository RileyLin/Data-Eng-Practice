# Scenario 11: Food Delivery Platform (DoorDash) - Restaurant Focus

## Question 11.1.1: Restaurant Metrics & Dimensions Definition

**Interviewer:** "You're working on DoorDash's restaurant analytics. How would you define key metrics and dimensions to measure restaurant performance on the platform?"

**Candidate Answer (Structured Bullet Points):**

"For a food delivery platform like DoorDash, restaurant performance is critical to marketplace health. I'd structure metrics around revenue, operations, and user experience, with dimensions that allow for meaningful segmentation.

*   **I. Core Restaurant Metrics:**

    *   **Revenue Metrics:**
        *   **Restaurant Revenue:** Total revenue generated per restaurant over time periods.
        *   **Average Order Value (AOV):** Revenue per order - key driver of platform economics.
        *   **Revenue Per Available Hour:** Measures efficiency during operating hours.
        *   **Commission Revenue:** DoorDash's take rate from restaurant orders.
        *   **Revenue Growth Rate:** MoM/YoY growth trends by restaurant.

    *   **Volume & Frequency Metrics:**
        *   **Order Count:** Total orders per restaurant (daily/weekly/monthly).
        *   **Order Frequency:** Orders per time period, showing demand consistency.
        *   **Order Conversion Rate:** Orders / Restaurant page views (discovery to order).
        *   **Repeat Order Rate:** % of customers who reorder from the same restaurant.
        *   **New vs. Returning Customer Ratio:** Customer acquisition vs. retention balance.

    *   **Operational Metrics:**
        *   **Preparation Time:** Time from order receipt to pickup-ready status.
        *   **Pickup Success Rate:** % of orders picked up successfully without issues.
        *   **Order Accuracy Rate:** % of orders delivered correctly without complaints.
        *   **Restaurant Availability:** % of operating hours actually accepting orders.
        *   **Menu Completion Rate:** % of menu items available vs. marked as unavailable.

    *   **Customer Experience Metrics:**
        *   **Customer Rating:** Average rating per restaurant (typically 1-5 stars).
        *   **Review Sentiment:** Qualitative feedback analysis.
        *   **Customer Complaints Rate:** % of orders resulting in customer service issues.
        *   **Estimated vs. Actual Delivery Time Accuracy.**

*   **II. Key Dimensions for Segmentation:**

    *   **Restaurant Characteristics:**
        *   **Cuisine Type:** Italian, Chinese, Mexican, American, etc.
        *   **Restaurant Category:** Fast food, casual dining, fine dining, cloud kitchens.
        *   **Price Tier:** Budget ($), Mid-range ($$), Premium ($$$).
        *   **Restaurant Size:** Number of menu items, estimated capacity.
        *   **Partnership Type:** Marketplace, DashPass exclusive, commission structure.

    *   **Geographic Dimensions:**
        *   **Market Tier:** Tier 1 cities (NYC, SF), Tier 2 (Austin, Portland), Tier 3 (smaller markets).
        *   **Neighborhood Type:** Urban dense, suburban, college areas, business districts.
        *   **Population Density:** High, medium, low density areas.
        *   **Delivery Zone Coverage:** Radius size, geographic constraints.

    *   **Temporal Dimensions:**
        *   **Day Part:** Breakfast (6-11am), Lunch (11am-3pm), Dinner (5-10pm), Late night (10pm+).
        *   **Day of Week:** Weekday vs. weekend patterns, specific day trends.
        *   **Seasonality:** Holiday periods, weather impacts, local events.
        *   **Restaurant Operating Schedule:** Peak vs. off-peak hours.

*   **III. Why These Metrics & Dimensions Matter:**
    *   **Revenue metrics** drive platform profitability and restaurant sustainability.
    *   **Operational metrics** ensure reliable service quality and customer satisfaction.
    *   **Segmentation dimensions** enable targeted strategies (pricing, marketing, support).
    *   **Cross-dimensional analysis** reveals insights like 'Asian restaurants in college areas have higher late-night order volume.'

*   **IV. Implementation Considerations:**
    *   **Data Quality:** Ensure consistent tracking across restaurants and time periods.
    *   **Benchmarking:** Establish performance benchmarks by restaurant category and market.
    *   **Actionability:** Metrics should lead to clear actions for restaurant partners.
    *   **Privacy:** Aggregate individual restaurant data appropriately for competitive insights.

This framework provides a comprehensive view of restaurant performance while enabling data-driven decisions for marketplace optimization."

## Question 11.1.2: Revenue Decline Deep Dive Analysis

**Interviewer:** "A key restaurant partner is experiencing a 20% decline in revenue over the past month. Walk me through your analytical approach to identify the root cause and recommend solutions."

**Candidate Answer (Structured Bullet Points):**

"A 20% revenue decline for a key partner requires immediate, systematic investigation. I'd structure this as a diagnostic process, moving from broad patterns to specific root causes.

*   **I. Initial Metric Decomposition (Revenue = Volume × AOV × Completion Rate):**
    *   **Order Volume Analysis:**
        *   Is the decline driven by fewer orders or lower order values?
        *   Compare daily order counts: current month vs. previous month vs. same period last year.
        *   Segment by new vs. returning customers to see if it's acquisition or retention.
    *   **Average Order Value (AOV) Analysis:**
        *   Has AOV changed? Could indicate menu pricing changes or customer behavior shifts.
        *   Analyze by order composition: fewer items per order, shift to lower-priced items?
    *   **Order Completion Rate:**
        *   Are more orders being cancelled? By whom (customer, restaurant, delivery issues)?

*   **II. External Factor Investigation:**
    *   **Competitive Landscape:**
        *   New competitors in the area? Promotional wars?
        *   Check if similar restaurants in the same area are also declining.
        *   Analyze market share changes within the cuisine category locally.
    *   **Seasonality & External Events:**
        *   Is this decline expected for the season/time of year?
        *   Local events, construction, weather changes affecting delivery accessibility?
        *   Economic factors in the local market (unemployment, consumer spending).
    *   **DoorDash Platform Changes:**
        *   Recent algorithm changes affecting restaurant visibility in search/recommendations?
        *   Changes to delivery fees or commission structure?
        *   App updates that might have affected user experience?

*   **III. Restaurant-Specific Deep Dive:**
    *   **Operational Changes:**
        *   Menu changes: items removed, prices increased, quality changes?
        *   Hours of operation changes or increased unavailability?
        *   Preparation time increases leading to longer delivery estimates?
        *   Staff changes affecting order accuracy or speed?
    *   **Customer Experience Degradation:**
        *   Recent rating decline or negative review patterns?
        *   Increased customer complaints about food quality, incorrect orders, or missing items?
        *   Analysis of review text sentiment over time.
    *   **Marketing & Visibility:**
        *   Reduced promotional activity or DashPass participation?
        *   Changes in restaurant's own marketing efforts?
        *   Photo quality or menu presentation issues affecting conversion?

*   **IV. Data Analysis Approach:**
    *   **Cohort Analysis:**
        *   Track customer retention: are existing customers ordering less frequently?
        *   New customer acquisition rate: is the restaurant attracting fewer first-time orderers?
    *   **Funnel Analysis:**
        *   Restaurant page views → Add to cart → Checkout → Payment → Successful delivery
        *   Identify where the biggest drop-offs are occurring.
    *   **Comparative Analysis:**
        *   Benchmark against similar restaurants (cuisine, price tier, location).
        *   Compare performance across different day parts and days of week.
    *   **Time Series Analysis:**
        *   Identify when the decline started and if it correlates with any specific events.

*   **V. Hypothesis Testing & Root Cause Identification:**
    *   **Develop Hypotheses:**
        *   H1: Menu price increases reduced order frequency
        *   H2: Operational issues (longer prep times) hurt customer experience
        *   H3: Increased competition from new restaurant openings
        *   H4: DoorDash algorithm changes reduced organic visibility
    *   **Test Each Hypothesis:**
        *   Use data to validate or reject each hypothesis systematically.
        *   Interview restaurant staff for qualitative insights on operational changes.

*   **VI. Solution Recommendations Based on Root Cause:**
    *   **If Competitive Pressure:**
        *   Promotional campaigns, DashPass enrollment, loyalty programs.
        *   Menu optimization to offer unique value propositions.
    *   **If Operational Issues:**
        *   Staff training, kitchen process optimization, menu simplification.
        *   Technology solutions for order management and preparation timing.
    *   **If Discovery/Visibility Issues:**
        *   SEO optimization, photo refresh, menu description improvements.
        *   Paid advertising campaigns during peak hours.
    *   **If Customer Experience Issues:**
        *   Quality control measures, customer feedback systems.
        *   Proactive customer service outreach for recent negative experiences.

*   **VII. Implementation & Monitoring:**
    *   **Establish Success Metrics:** Target revenue recovery timeline and milestones.
    *   **A/B Testing:** Test solutions with control groups where possible.
    *   **Regular Check-ins:** Weekly performance reviews during recovery period.
    *   **Long-term Prevention:** Implement early warning systems for similar issues.

The key is moving quickly but systematically, using data to guide decisions while maintaining the restaurant partnership relationship throughout the recovery process."

## Question 11.1.3: Dashboard Visualization Design

**Interviewer:** "Design a dashboard for restaurant performance monitoring. How would you structure the visualization to provide actionable insights for different stakeholders?"

**Candidate Answer (Structured Bullet Points):**

"A restaurant performance dashboard needs to serve multiple stakeholders with different information needs and decision-making contexts. I'd design a multi-layered approach with role-based views and drill-down capabilities.

*   **I. Dashboard Architecture (Three-Tier Approach):**

    *   **Executive Summary Level (Top-Level KPIs):**
        *   Card-based layout with key performance indicators and trend indicators
        *   Time period comparison capabilities (WoW, MoM, YoY)
        *   Geographic aggregation with ability to drill down

    *   **Operational Detail Level (Feature-Specific Analysis):**
        *   Restaurant segmentation and performance matrices
        *   Time-series trending with anomaly detection
        *   Comparative analysis across restaurant cohorts

    *   **Individual Restaurant Level (Deep Dive Analysis):**
        *   Single restaurant detailed performance
        *   Customer journey and conversion funnel analysis
        *   Actionable recommendations based on performance patterns

*   **II. Executive Dashboard (Leadership & Strategy Teams):**

    *   **Top-Level KPI Cards:**
        ```
        ┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
        │   Total Revenue │   Active Rest.  │   Avg Order Val │   Completion %  │
        │   $2.3M (+5%)   │   1,247 (-2%)   │   $23.50 (+8%) │   94.2% (-1%)   │
        └─────────────────┴─────────────────┴─────────────────┴─────────────────┘
        ```
        *   Color-coded with green/yellow/red indicators for performance vs. targets
        *   Percentage change from previous period with trend arrows

    *   **Geographic Performance Map:**
        *   Heat map overlay showing revenue density by market/neighborhood
        *   Bubble size representing order volume, color representing AOV
        *   Click-through to market-specific deep dives

    *   **Time Series Trends:**
        *   Revenue trend line with YoY comparison and seasonality indicators
        *   Order volume stacked area chart by restaurant category
        *   Performance funnel showing conversion rates at each step

The goal is creating a unified view that serves different information needs while maintaining consistency and enabling collaborative decision-making across teams." 