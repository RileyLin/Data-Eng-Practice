# Question 12: DoorDash Restaurant Metrics - Product Sense & Data Modeling

## Interview Focus Areas
Based on the actual DoorDash interview experience, this section covers:
1. **Metrics & Dimensions Definition** for restaurants
2. **Deep Dive Analysis** when revenue/orders decline  
3. **Visualization Design** for restaurant performance

---

## 1. Core Restaurant Metrics & Dimensions

### Primary Metrics

#### Revenue Metrics
- **Restaurant Revenue**: Total revenue generated per restaurant
- **Average Order Value (AOV)**: Revenue per order
- **Revenue Per Available Hour**: Revenue efficiency during operating hours
- **Commission Revenue**: DoorDash's take from restaurant orders

#### Volume Metrics  
- **Order Count**: Total orders per restaurant
- **Order Frequency**: Orders per time period (daily/weekly/monthly)
- **Order Conversion Rate**: Orders / Restaurant page views
- **Repeat Order Rate**: Returning customer order percentage

#### Operational Metrics
- **Preparation Time**: Time from order receipt to pickup ready
- **Pickup Success Rate**: % of orders picked up successfully
- **Order Accuracy Rate**: % of orders delivered correctly
- **Restaurant Availability**: % of operating hours actually accepting orders

### Key Dimensions for Segmentation

#### Restaurant Dimensions
- **Cuisine Type**: (Italian, Chinese, Mexican, etc.)
- **Restaurant Category**: (Fast food, casual dining, fine dining)
- **Price Tier**: (Budget: $, Mid-range: $$, Premium: $$$)
- **Restaurant Size**: (Number of menu items, seating capacity)
- **Partnership Type**: (Marketplace, DashPass exclusive, etc.)

#### Geographic Dimensions
- **Market Tier**: (Tier 1, 2, 3 cities)
- **Neighborhood Type**: (Urban, suburban, college area)
- **Population Density**: (High, medium, low)
- **Delivery Zone Size**: (Radius coverage area)

#### Temporal Dimensions
- **Day Part**: (Breakfast, lunch, dinner, late night)
- **Day of Week**: (Weekday vs weekend patterns)
- **Seasonality**: (Holiday periods, weather impacts)
- **Restaurant Operating Hours**: (Peak vs off-peak)

---

## 2. Deep Dive Framework: Revenue/Order Decline Analysis

### Step 1: Metric Decomposition
```
Revenue Decline = 
  ↓ Order Volume × ↓ Average Order Value × ↓ Successful Completion Rate

Order Volume Decline =
  ↓ New Customers × ↓ Returning Customers × ↓ Order Frequency
```

### Step 2: Hypothesis Generation & Testing

#### External Factors
- **Competitive Pressure**: New competitors, promotional wars
- **Seasonality**: Weather, holidays, local events
- **Economic Factors**: Consumer spending, unemployment rates
- **Operational Issues**: Driver shortages, delivery delays

#### Internal Factors  
- **Product Changes**: Menu updates, pricing changes, app modifications
- **Restaurant Quality**: Food quality decline, poor ratings
- **Service Issues**: Long wait times, delivery problems
- **Marketing Changes**: Reduced advertising, promotion changes

### Step 3: Data Analysis Approach

#### Segmentation Analysis
```sql
-- Identify which restaurant segments are most affected
SELECT 
    cuisine_type,
    price_tier,
    market_tier,
    SUM(revenue_current_period) / SUM(revenue_previous_period) - 1 as revenue_change_pct,
    COUNT(DISTINCT restaurant_id) as restaurant_count
FROM restaurant_performance
GROUP BY cuisine_type, price_tier, market_tier
ORDER BY revenue_change_pct
```

#### Cohort Analysis
- Track restaurant performance by onboarding cohort
- Analyze customer retention by restaurant over time
- Compare new vs existing restaurant performance

#### Funnel Analysis
```
Restaurant Page Views → Add to Cart → Checkout → Payment → Successful Delivery
```

### Step 4: Root Cause Investigation

#### Data Points to Examine
1. **Restaurant-Level Metrics**:
   - Individual restaurant revenue trends
   - Menu item performance changes
   - Rating and review sentiment
   - Operational metrics (prep time, accuracy)

2. **Customer Behavior**:
   - Order frequency changes by customer segment
   - Cart abandonment rates
   - Customer lifetime value trends
   - Search and discovery patterns

3. **Competitive Intelligence**:
   - Market share changes
   - Competitor pricing analysis
   - New market entrants
   - Promotional activity comparison

---

## 3. Visualization Design for Restaurant Performance

### Executive Dashboard

#### Top-Level KPIs (Card Layout)
```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│   Total Revenue │   Active Rest.  │   Avg Order Val │   Completion %  │
│   $2.3M (+5%)   │   1,247 (-2%)   │   $23.50 (+8%) │   94.2% (-1%)   │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

#### Time Series Charts
- **Revenue Trend**: Line chart with YoY comparison
- **Order Volume**: Stacked area chart by restaurant category
- **Performance Funnel**: Conversion rates at each step

### Restaurant Deep Dive Dashboard

#### Multi-Dimensional Analysis
```
Restaurant Performance Matrix:
                 High Revenue              Low Revenue
High Order Vol   ┌─ Star Performers ─┐   ┌─ High Vol, Low AOV ─┐
                 │ Focus: Maintain   │   │ Focus: Pricing     │
                 └───────────────────┘   └───────────────────┘

Low Order Vol    ┌─ Premium Niche ───┐   ┌─ At Risk ─────────┐
                 │ Focus: Scale Up   │   │ Focus: Intervention│
                 └───────────────────┘   └───────────────────┘
```

#### Heatmap Visualizations
- **Geographic Performance**: Map overlay with revenue density
- **Time-based Patterns**: Hour-of-day vs day-of-week performance grid
- **Menu Item Performance**: Revenue contribution by item category

### Operational Dashboard

#### Real-Time Monitoring
- **Live Order Tracking**: Current orders in preparation/delivery
- **Restaurant Status**: Online/offline status with capacity indicators
- **Alert System**: Automated flags for performance issues

#### Predictive Analytics
- **Demand Forecasting**: Expected order volume by restaurant/time
- **Capacity Planning**: Restaurant availability optimization
- **Performance Alerts**: Early warning system for declining metrics

### Interactive Features

#### Filtering & Drill-Down
- Multi-select filters: Cuisine type, price tier, geographic market
- Click-through capability: Dashboard → Restaurant → Individual orders
- Time period selection: Custom date ranges, period comparison

#### Export & Sharing
- Scheduled reports: Weekly/monthly performance summaries
- Custom views: Saved filter combinations for different stakeholders
- Data export: CSV/Excel for detailed analysis

---

## 4. Implementation Considerations

### Data Requirements
- **Real-time data**: Order status, restaurant availability
- **Historical data**: 2+ years for trend analysis and seasonality
- **External data**: Weather, events, competitor information

### Stakeholder Alignment
- **Restaurant Partners**: Focus on actionable insights for improvement
- **Operations Teams**: Emphasize efficiency and troubleshooting
- **Executive Leadership**: High-level trends and strategic insights

### Success Metrics for Visualizations
- **Adoption Rate**: % of stakeholders using dashboards regularly
- **Time to Insight**: How quickly users can identify issues
- **Action Frequency**: Number of decisions driven by dashboard insights
- **Performance Impact**: Measurable improvements in restaurant metrics 