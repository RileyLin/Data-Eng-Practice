# Scenario 9: Order Batching (DoorDash) - Delivery Optimization

## Question 9.1.1: Order Batching Strategy

**Interviewer:** "You're designing an order batching system for DoorDash to improve delivery efficiency. How would you approach optimizing the batching algorithm to balance customer satisfaction with operational efficiency?"

**Candidate Answer (Structured Bullet Points):**

"Designing an effective order batching system requires balancing multiple objectives: reducing delivery times for customers, maximizing driver efficiency, and optimizing overall platform economics. Here's my comprehensive approach:

*   **I. Core Batching Objectives & Trade-offs:**

    *   **Primary Goals:**
        *   **Customer Experience:** Minimize total delivery time per order
        *   **Driver Efficiency:** Maximize orders delivered per hour/mile
        *   **Platform Economics:** Reduce operational costs while maintaining service quality
        *   **Restaurant Operations:** Optimize pickup timing to minimize wait times

    *   **Key Trade-offs to Balance:**
        *   **Batch Size vs. Delivery Speed:** Larger batches improve efficiency but may increase individual delivery times
        *   **Geographic Proximity vs. Time Constraints:** Perfect routes vs. acceptable delivery windows
        *   **Order Value vs. Delivery Priority:** High-value orders may warrant dedicated delivery

*   **II. Batching Algorithm Design Principles:**

    *   **Spatial Clustering:**
        *   Group orders by delivery location proximity (e.g., within 0.5-mile radius)
        *   Consider restaurant pickup locations to minimize total travel distance
        *   Account for traffic patterns and road network topology

    *   **Temporal Constraints:**
        *   **Order Age Limits:** Maximum wait time before an order must be dispatched (e.g., 15 minutes)
        *   **Restaurant Pickup Windows:** Coordinate with estimated preparation times
        *   **Customer Delivery Promises:** Respect estimated delivery time commitments

    *   **Dynamic Batching Windows:**
        *   **Peak Hours:** Shorter batching windows (3-5 minutes) due to high order volume
        *   **Off-Peak Hours:** Longer windows (10-15 minutes) to accumulate sufficient orders
        *   **Real-time Adjustment:** Adapt based on driver availability and order density

*   **III. Algorithmic Approach & Optimization:**

    *   **Multi-Objective Optimization Framework:**
        *   **Objective Function:** Minimize (weighted sum of delivery time + operational cost)
        *   **Constraints:** Maximum batch size, delivery time limits, driver capacity
        *   **Dynamic Weights:** Adjust based on business priorities and current conditions

    *   **Batch Creation Process:**
        1. **Eligible Order Pool:** Collect orders ready for batching (restaurant confirmed, within time limits)
        2. **Initial Clustering:** Group by geographic proximity and restaurant locations
        3. **Route Optimization:** Calculate optimal pickup and delivery sequences
        4. **Feasibility Check:** Ensure all constraints (time, capacity) are met
        5. **Driver Assignment:** Match batch to available drivers based on location and capacity

    *   **Advanced Techniques:**
        *   **Predictive Batching:** Use ML to predict optimal batch composition based on historical patterns
        *   **Lookahead Optimization:** Consider orders likely to arrive in next few minutes
        *   **Dynamic Re-batching:** Adjust existing batches when high-priority orders arrive

*   **IV. Key Metrics for Optimization:**

    *   **Customer Experience Metrics:**
        *   **Average Delivery Time:** From order placement to delivery
        *   **Delivery Time Variance:** Consistency of delivery experience
        *   **On-Time Delivery Rate:** Percentage meeting promised delivery times
        *   **Customer Satisfaction (CSAT):** Direct feedback on delivery experience

    *   **Operational Efficiency Metrics:**
        *   **Orders per Hour per Driver:** Driver productivity measure
        *   **Miles per Order:** Efficiency of routing
        *   **Batch Utilization Rate:** Average orders per batch vs. maximum capacity
        *   **Driver Idle Time:** Time between completed delivery and next pickup

    *   **Economic Metrics:**
        *   **Cost per Delivery:** Total operational cost divided by deliveries
        *   **Revenue per Hour per Driver:** Driver earning potential
        *   **Batching Success Rate:** Percentage of orders successfully batched vs. single deliveries

*   **V. Implementation Strategy & A/B Testing:**

    *   **Phased Rollout:**
        *   **Phase 1:** Test in low-complexity markets (suburban, predictable demand)
        *   **Phase 2:** Expand to medium-density urban areas
        *   **Phase 3:** Deploy in high-complexity markets (dense cities, complex traffic)

    *   **A/B Testing Framework:**
        *   **Control Group:** Current single-delivery system
        *   **Test Groups:** Different batching algorithms and parameters
        *   **Success Metrics:** Balanced scorecard of customer, driver, and business metrics
        *   **Statistical Significance:** Ensure sufficient sample size and test duration

    *   **Real-time Monitoring & Adjustment:**
        *   **Dynamic Parameter Tuning:** Adjust batching windows, proximity thresholds based on performance
        *   **Alert Systems:** Flag degrading metrics for immediate investigation
        *   **Feedback Loops:** Incorporate driver and customer feedback into algorithm improvements

*   **VI. Risk Mitigation & Edge Cases:**

    *   **Peak Demand Management:**
        *   **Surge Batching:** Temporarily relax constraints during extreme demand
        *   **Priority Queue:** Fast-track high-value or time-sensitive orders
        *   **Capacity Scaling:** Dynamic driver recruitment during peak periods

    *   **Service Quality Protection:**
        *   **Delivery Time Caps:** Hard limits on maximum acceptable delivery times
        *   **Customer Communication:** Proactive updates on delivery status
        *   **Driver Support:** Tools and training for efficient batch execution

The key to success is continuous optimization based on real-world performance data, maintaining flexibility to adapt to changing market conditions while never compromising core service quality standards."

## Question 9.1.2: Metrics Framework for Batching Success

**Interviewer:** "How would you design a comprehensive metrics framework to measure the success of your order batching system across different stakeholders?"

**Candidate Answer (Structured Bullet Points):**

"A successful order batching system affects multiple stakeholders, so the metrics framework must capture impacts across customers, drivers, restaurants, and the business. Here's my comprehensive approach:

*   **I. Stakeholder-Specific Metric Categories:**

    *   **Customer Experience Metrics:**
        *   **Primary KPIs:**
            *   **Total Delivery Time:** From order placement to delivery completion
            *   **Delivery Time Variance:** Standard deviation to measure consistency
            *   **On-Time Delivery Rate:** Percentage meeting estimated delivery times
            *   **Order Accuracy Rate:** Correct orders delivered (batching shouldn't impact accuracy)

        *   **Secondary KPIs:**
            *   **Customer Satisfaction Score (CSAT):** Post-delivery survey ratings
            *   **Net Promoter Score (NPS):** Customer willingness to recommend
            *   **Complaint Rate:** Delivery-related customer service contacts
            *   **Re-order Rate:** Customer retention and repeat business

    *   **Driver Experience & Efficiency Metrics:**
        *   **Productivity Metrics:**
            *   **Orders per Hour:** Driver throughput during active time
            *   **Earnings per Hour:** Driver income efficiency
            *   **Miles per Order:** Route efficiency measure
            *   **Batch Completion Rate:** Successfully completed batched deliveries

        *   **Experience Metrics:**
            *   **Driver Satisfaction (DSAT):** Feedback on batching experience
            *   **Navigation Complexity:** Average stops per batch, routing difficulty
            *   **Wait Time at Restaurants:** Impact of batching on pickup delays
            *   **Customer Interaction Quality:** Feedback on delivery experience

    *   **Restaurant Partner Metrics:**
        *   **Operational Impact:**
            *   **Order Pickup Time:** Time from ready to driver pickup
            *   **Batch Pickup Efficiency:** Multiple orders picked up per visit
            *   **Kitchen Workflow Disruption:** Impact on restaurant operations
            *   **Order Accuracy:** Maintaining quality with batched pickups

*   **II. Business Performance Metrics:**

    *   **Operational Efficiency:**
        *   **Cost per Delivery:** Total delivery cost including driver pay, gas, platform costs
        *   **Fleet Utilization Rate:** Percentage of time drivers are actively delivering
        *   **Batching Success Rate:** Orders successfully batched vs. requiring individual delivery
        *   **Market Coverage:** Delivery capacity across service areas

    *   **Financial Impact:**
        *   **Contribution Margin per Order:** Revenue minus variable costs
        *   **Driver Cost per Mile:** Efficiency of driver utilization
        *   **Peak Hour Capacity:** Orders handled during high-demand periods
        *   **Service Level Achievement:** Meeting delivery promises while optimizing costs

*   **III. Comparative Analysis Framework:**

    *   **Batched vs. Individual Delivery Comparison:**
        *   **Delivery Time Impact:** How batching affects average delivery times
        *   **Cost Efficiency Gains:** Cost savings from batching
        *   **Customer Satisfaction Delta:** Impact on customer experience
        *   **Driver Productivity Improvement:** Efficiency gains per driver

    *   **Segmented Analysis:**
        *   **By Market Type:** Urban dense vs. suburban vs. rural performance
        *   **By Time Period:** Peak vs. off-peak batching effectiveness
        *   **By Order Value:** Premium vs. standard order handling
        *   **By Distance:** Short vs. long delivery distances

*   **IV. Real-Time Monitoring Dashboard:**

    *   **Executive Dashboard (High-Level KPIs):**
        *   Daily delivery performance vs. targets
        *   Customer satisfaction trends
        *   Cost efficiency metrics
        *   Driver utilization rates

    *   **Operations Dashboard (Tactical Metrics):**
        *   Current batching performance by market
        *   Real-time delivery time tracking
        *   Driver productivity monitoring
        *   Alert system for metric degradation

    *   **Algorithm Performance Dashboard (Technical Metrics):**
        *   Batch creation success rates
        *   Route optimization effectiveness
        *   Prediction accuracy for batch timing
        *   System response times and reliability

*   **V. Success Criteria & Target Setting:**

    *   **Baseline Establishment:**
        *   Measure current performance without batching
        *   Establish statistical significance requirements
        *   Define minimum acceptable performance thresholds

    *   **Target Definition:**
        *   **Customer Metrics:** No degradation in delivery time; improve consistency
        *   **Driver Metrics:** 15-25% improvement in orders per hour
        *   **Cost Metrics:** 10-20% reduction in cost per delivery
        *   **Overall:** Positive impact across all stakeholder groups

*   **VI. Continuous Improvement Framework:**

    *   **Weekly Performance Reviews:**
        *   Stakeholder metric assessment
        *   Identification of underperforming segments
        *   Algorithm parameter adjustment recommendations

    *   **Monthly Strategic Analysis:**
        *   Trend analysis across all metrics
        *   Market-specific optimization opportunities
        *   Driver and customer feedback integration

    *   **Quarterly Business Impact Assessment:**
        *   Financial impact quantification
        *   Strategic initiative alignment
        *   Expansion planning based on success metrics

The framework ensures that batching optimization doesn't come at the expense of any stakeholder group and provides clear visibility into the system's overall health and effectiveness." 