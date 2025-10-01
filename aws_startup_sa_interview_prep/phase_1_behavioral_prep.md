# Phase 1: Behavioral Preparation Guide

This guide is your central hub for preparing for the behavioral questions in the AWS onsite interview. It has been updated to incorporate your detailed project histories and provides a structured approach to mapping those stories to Amazon's Leadership Principles (LPs), along with a bank of practice questions.

---

## 1. Project Story Bank

This section contains your key career stories, formatted using the STAR method. These are the building blocks for your behavioral answers.

---

### Story 1: Sales & Underwriting AI Automation Tool
- **Situation**: Sales and underwriting teams spent 4-5 hours of manual prep time on ad hoc reporting for each new business opportunity assessment, leading to inefficiency and inconsistent knowledge transfer.
- **Task**: Create an automated, scalable solution to streamline business case analysis and sales preparation.
- **Action**: I architected and built a comprehensive AI-powered Streamlit application. I embedded SQL queries in Python for data retrieval from our Snowflake database and integrated external data sources. The solution was deployed on AWS using ECS for container hosting and ECR for the image repository, and it leveraged the AWS Bedrock API for LLM-powered analysis. It also featured custom Python PDF generation for client-ready reports, automating the insight-generation process.
- **Result**: The tool dramatically increased efficiency, reducing case prep time from over 4 hours to just 30 minutes. It also created a scalable onboarding process and ensured consistent report quality across the entire sales organization.
- **Leadership Principles**: Customer Obsession, Invent and Simplify, Deliver Results, Ownership, Think Big.

---

### Story 2: Claims Gen-AI Eligibility Solution
- **Situation**: Claims adjusters manually reviewed complex PDFs to determine eligibility, a process that took 30 minutes per claim with only 90% accuracy.
- **Task**: I took the initiative to pilot a Gen-AI solution to automate and improve this process, despite not having formal authority to do so.
- **Action**: I dedicated two evenings to building a proof-of-concept (POC) using a Large Language Model (LLM) and then demonstrated it to the Claims team. After getting their buy-in, I ran a pilot with 10 agents, carefully tracking time savings and accuracy improvements.
- **Result**: The solution was a massive success. It reduced eligibility check time from 30 minutes to just 3 minutes (a 90% reduction), increased accuracy from 90% to 95%, and resulted in a projected $150k in annual operational savings. This "show, don't tell" approach turned skeptics into champions.
- **Leadership Principles**: Invent and Simplify, Bias for Action, Learn and Be Curious, Ownership, Deliver Results.

---

### Story 3: Power BI Version Control Implementation
- **Situation**: The dashboard development process lacked version control, leading to data accuracy issues reaching customers, which eroded trust. Changes were difficult to track in the GUI-heavy environment.
- **Task**: Establish an enterprise-grade version control and review process for all Power BI development to ensure quality and reliability.
- **Action**: I engineered a novel solution by converting Power BI dashboards into JSON text files, which allowed us to use Git for version control. I built a full GitHub repository workflow, created a comprehensive review process for data sources and logic, and established a formal dev/test/prod deployment cycle. I also conducted company-wide training to drive adoption.
- **Result**: This initiative transformed our development culture. GitHub activity skyrocketed from 2 commits per week to over 50. Most importantly, we achieved a 50% reduction in customer-reported data complaints and established proper review gates to prevent future issues.
- **Leadership Principles**: Insist on the Highest Standards, Earn Trust, Learn and Be Curious, Dive Deep.

---

### Story 4: Census Data Ingestion Pipeline
- **Situation**: Critical census data ingestion was an unowned process, causing modeling data to be stale by over 7 days. This lack of ownership was a significant bottleneck.
- **Task**: Enable a daily, automated ingestion process and drive its adoption across engineering without any formal authority over the responsible teams.
- **Action**: I built a working POC that mirrored a familiar payroll ETL process, successfully landing a 200k-row file in Snowflake to prove the concept. I then created and presented a compelling ROI deck to engineering leadership, quantifying the upside at over $800k.
- **Result**: My prototype and business case successfully convinced engineering to prioritize the project in their next sprint. The productionized pipeline now refreshes in 10 minutes, has unlocked $1M in premium lift, and is fully automated. This proved that influence can be achieved with a working prototype and a quantified upside.
- **Leadership Principles**: Ownership, Bias for Action, Have Backbone; Disagree & Commit, Think Big.

---

### Story 5: SalesMart Quoting Dashboard
- **Situation**: Executives were manually stitching together 10 different reports for quoting analysis, a process that took 5 days and was prone to error.
- **Task**: In 12 months, deliver a single, self-serve dashboard and a robust underlying data model to serve as the single source of truth.
- **Action**: I led the project and a team of two analysts. My first step was to run two metric-definition workshops with executives to create a shared data dictionary, ensuring alignment before any code was written. I then architected and built the Snowflake SalesMart using dbt and implemented Great Expectations for data quality testing.
- **Result**: The new dashboard reduced data refresh time from 5 days to just 15 minutes. It's projected to enable a $1.5M premium lift and became a top-3 most used dashboard in the company. The key lesson was that up-front metric alignment prevents months of downstream rework.
- **Leadership Principles**: Are Right, A Lot, Customer Obsession, Deliver Results, Insist on the Highest Standards.

---

### Story 6: Commission RCA (Failure Story)
- **Situation**: A logic bug I introduced into a SQL script resulted in a $15k overpayment in sales commissions. The payroll run was in 48 hours, creating a high-pressure, time-sensitive situation.
- **Task**: I had to immediately fix the bug, reconcile the data, and implement safeguards to prevent the error from ever happening again, all before the payroll deadline.
- **Action**: I took immediate and transparent ownership. I isolated the specific ETL job, patched the SQL logic, and worked with finance to back-fill the correct payout amounts. Critically, I then designed and implemented three new systemic guardrails: expanded unit tests for this specific edge case, a peer-review checklist for commission logic, and a new canary anomaly alert to detect variances.
- **Result**: The issue was fully corrected before the payroll run, and there have been zero similar defects in the 8 months since. This experience taught me that transparently owning a mistake and building systemic guardrails is the fastest way to rebuild trust.
- **Leadership Principles**: Earn Trust, Ownership, Dive Deep, Insist on the Highest Standards.

---

### Story 7: Data Quality Control Framework
- **Situation**: 15-20 daily reports were running without any proactive error detection. Significant data changes (e.g., $10M to $100M overnight) were only discovered manually after they had already reached senior executives.
- **Task**: Build a comprehensive, two-tier data monitoring and alerting system to catch errors proactively.
- **Action**: I architected and implemented a two-tiered automated quality control system. Tier 1 focused on data entry validation, with automatic scanning and email notifications to staff for immediate fixes. Tier 2 focused on processing anomaly detection, using historical data to create baselines and automatically flagging any variance over a 10-15% threshold, alerting the data team before reports were sent to executives.
- **Result**: The framework had a substantial impact on data reliability. It drove a 70% reduction in data entry errors and completely eliminated executive-level surprises from bad data, shifting the team from reactive firefighting to systematic prevention.
- **Leadership Principles**: Dive Deep, Deliver Results, Customer Obsession.

---

### Story 8: Power BI Latency Fix
- **Situation**: A critical executive dashboard was taking over 120 seconds to load, causing a steady decline in usage and engagement.
- **Task**: Reduce the dashboard latency to under 10 seconds without provisioning any additional hardware or incurring extra costs.
- **Action**: I analyzed the performance issues and moved the heavy DAX calculations upstream into the Snowflake data warehouse. I built pre-aggregated summary tables and composite indexes to optimize the query patterns and enabled incremental refresh on the Power BI side.
- **Result**: The optimizations brought the load time down to just 9 seconds. As a direct result, executive usage of the dashboard increased by over 20% week-over-week. This demonstrated that performance is a feature and a key driver of adoption.
- **Leadership Principles**: Frugality, Dive Deep, Customer Obsession.

---

### Story 9: The Misaligned Metrics (Failure Story)
- **Situation**: Early in the SalesMart Dashboard project, I was tasked with building a unified dashboard for multiple executive stakeholders. I made a critical judgment error by assuming everyone had the same definition for core business concepts like 'premium lift' and 'retention.'
- **Task**: After presenting a prototype that was met with confusion and disagreement from sales and finance leaders, I had to salvage the project's credibility and get all stakeholders aligned on the core metrics.
- **Action**: I immediately paused all technical development. I owned the mistake with the project sponsor, explaining that my engineering bias led me to focus on the 'how' before locking down the 'what'. I then designed and led two mandatory 'metric-definition workshops' with all executive stakeholders. We debated every single metric, documented them in a shared data dictionary, and required formal sign-off. This document became our non-negotiable source of truth.
- **Result**: The workshops successfully realigned the project. Though it caused a short-term delay, it prevented what would have been months of rework. The final dashboard was a huge success precisely because all stakeholders trusted the data. More importantly, this process became a standard for all future analytics projects, making a data dictionary sign-off the first and most critical gate. This failure taught me that for business-facing tools, semantic alignment is even more important than the technical architecture.
- **Leadership Principles**: Earn Trust, Are Right A Lot, Dive Deep.

---

### Story 10: Unlocking Market Insights with External Data Integration
- **Situation**: Our sales and product teams were operating with a significant blind spot. We had no reliable data on our competitors, and our internal account data was fragmented, making it nearly impossible to identify the right contacts at large companies or to get a single view of our strategic broker relationships. This was directly impacting our ability to price competitively and manage key partnerships.
- **Task**: I took ownership of solving this strategic data gap. My goal was to architect a solution that would enrich our internal data with external market intelligence, create a single source of truth for account and broker data, and drive its adoption across the entire company.
- **Action**: I led this initiative from discovery to delivery. First, I partnered with senior sales leaders to define the key business requirements. After researching and vetting several external data vendors, I selected two that best fit our needs. As the main architect, I translated the business needs into a technical integration plan, designed and built the data pipelines to merge the vendor data with our internal Snowflake warehouse, and worked with the vendors to run a successful POC. A critical part of the project was evangelism; I ran technical workshops to show our engineers how to leverage the new competitor data, and I ran separate business workshops to train our sales, product, and marketing teams on how to use the enriched data in their dashboards and strategic planning.
- **Result**: The project became a core data asset for the company. We achieved over **80% adoption** of the new data source within six months. The sales team reported a **90% reduction in time** spent on researching accounts and competitors. This time savings contributed to a **5% increase in our competitive win rate** in the first year. The unified broker view also allowed us to strengthen key partnerships, unlocking an estimated **$2M in new pipeline opportunities**.
- **Leadership Principles**: Ownership, Think Big, Customer Obsession, Deliver Results, Dive Deep.

---

## 2. Leadership Principle (LP) to Story Matrix

Use this matrix to quickly select the best story for a given LP and to have a backup ready if you've already used your primary one.

| Leadership Principle | Primary Story | Backup Story |
| :--- | :--- | :--- |
| **Customer Obsession** | SalesMart Dashboard | Sales & Underwriting AI Tool |
| **Ownership** | Census Pipeline | Claims Gen-AI Solution |
| **Invent and Simplify**| Claims Gen-AI Solution | Sales & Underwriting AI Tool |
| **Are Right, A Lot** | SalesMart Dashboard | The Misaligned Metrics (Failure)|
| **Learn and Be Curious**| Claims Gen-AI Solution | Power BI Version Control |
| **Hire and Develop** | Salesforce Migration | SalesMart Dashboard |
| **Insist on Highest Standards**| Power BI Version Control | Commission RCA |
| **Think Big** | Sales & Underwriting AI Tool| Unlocking Market Insights |
| **Bias for Action** | Census Pipeline | Claims Gen-AI Solution |
| **Frugality** | Power BI Latency Fix | (Could be improved) |
| **Earn Trust** | Commission RCA (Failure) | The Misaligned Metrics (Failure)|
| **Dive Deep** | Commission RCA (Failure) | Data Quality Framework |
| **Have Backbone** | Census Pipeline | (Could be improved) |
| **Deliver Results** | SalesMart Dashboard | Unlocking Market Insights |
| **Strive to be Earth's Best Employer**| (Mentoring/Team Story) | (Could be improved) |
| **Success and Scale...**| (Security/Compliance Story) | (Could be improved) |

---

## 3. Practice Question Bank

Use these questions to practice delivering your stories. For each question, a suggested Primary and Backup story is provided from the Story Bank.

#### Customer Obsession
*   **Question:** "Tell me about a time you worked backwards from a customer's needs to deliver a solution."
    *   **Primary:** `SalesMart Dashboard` (Started with exec pain points)
    *   **Backup:** `Sales & Underwriting AI Tool` (Focused on sales team's manual workflow)

#### Ownership
*   **Question:** "Describe a situation where you saw a problem that was outside of your direct responsibility and you took the initiative to solve it."
    *   **Primary:** `Census Pipeline` (No team owned it, so I built the POC)
    *   **Backup:** `Claims Gen-AI Solution` (No one asked for it, but I saw the opportunity)

#### Invent and Simplify
*   **Question:** "Walk me through a time you simplified a complex process or built an innovative solution."
    *   **Primary:** `Claims Gen-AI Solution` (Simplified manual PDF reading with AI)
    *   **Backup:** `Power BI Version Control` (Created a simple text-based workflow for a complex GUI tool)

#### Are Right, A Lot
*   **Question:** "Tell me about a time you had to make a decision with incomplete data. How did you make that judgment call and what was the outcome?"
    *   **Primary:** `SalesMart Dashboard` (My judgment to hold metric workshops prevented months of rework)
    *   **Backup:** `The Misaligned Metrics` (My initial judgment was wrong, but the correction process showed better judgment)

#### Learn and Be Curious
*   **Question:** "Describe a time you had to quickly learn a new technology or domain to deliver on a project."
    *   **Primary:** `Claims Gen-AI Solution` (Taught myself LLMs and prompt engineering in my own time)
    *   **Backup:** `Sales & Underwriting AI Tool` (Had to learn AWS Bedrock and ECS deployment)

#### Insist on the Highest Standards
*   **Question:** "Tell me about a time you refused to let a project ship because it didn't meet your quality bar. What was the situation and outcome?"
    *   **Primary:** `Power BI Version Control` (Established gates to stop bad data from reaching customers)
    *   **Backup:** `Commission RCA` (Implemented new QA standards after a failure)

#### Think Big
*   **Question:** "Describe a solution you built that was not just a one-off fix, but a scalable pattern that could be used by the rest of the company."
    *   **Primary:** `Sales & Underwriting AI Tool` (Framed the tool not just for one team but as a pattern for AI-powered apps)
    *   **Backup:** `Unlocking Market Insights` (Created a core data asset for the whole company)

#### Bias for Action
*   **Question:** "Tell me about a time you favored swift, calculated action over waiting for perfect information or consensus."
    *   **Primary:** `Census Pipeline` (Broke a deadlock by building a POC instead of waiting for engineering)
    *   **Backup:** `Claims Gen-AI Solution` (Built it in my evenings to show what was possible)

#### Frugality
*   **Question:** "Describe a time you were able to achieve a significant result with limited resources or budget."
    *   **Primary:** `Power BI Latency Fix` (Solved a major performance issue with no extra hardware or cost)

#### Earn Trust (Negative Style)
*   **Question:** "Tell me about a time you made a mistake or a bad judgment call. What was it, and how did you handle it?"
    *   **Primary:** `Commission RCA` (My logic bug, how I owned it, fixed it, and implemented safeguards)
    *   **Backup:** `The Misaligned Metrics` (My judgment error in assuming metric alignment)

#### Dive Deep
*   **Question:** "Walk me through a complex problem that required a deep root cause analysis from you. How did you diagnose the issue?"
    *   **Primary:** `Commission RCA` (Performed deep RCA under pressure to find the specific logic bug)
    *   **Backup:** `Power BI Latency Fix` (Had to analyze the entire data pipeline to find the bottleneck)

#### Have Backbone; Disagree & Commit
*   **Question:** "Tell me about a time you had a professional disagreement with a stakeholder or your manager. How did you handle it?"
    *   **Primary:** `Census Pipeline` (Disagreed with Engineering on priorities and used data/ROI deck to convince them)

#### Deliver Results
*   **Question:** "Tell me about your proudest professional achievement." or "Describe the project where you had the most significant, quantifiable impact."
    *   **Primary:** `SalesMart Dashboard` ($1.5M lift, top-3 dashboard)
    *   **Backup:** `Unlocking Market Insights` ($2M pipeline, 5% win rate increase)

---

## 4. Frameworks for Answering

#### The STAR Method
For every behavioral question, structure your answer this way:
-   **S/T (Situation/Task):** 20-30 seconds. Briefly provide the business context and what was required.
-   **A (Action):** 60-90 seconds. This is the most important part. Detail the specific actions *you* took. Use "I" not "we". Go into technical detail where appropriate.
-   **R (Result):** 30 seconds. Conclude with the outcome. Quantify the results using one of the three impact angles below.

#### "Negative Style" Question Framework
When asked about a failure, mistake, or weakness, use this three-part structure:
1.  **Humility (Own the mistake):** State clearly and without excuses what the mistake was and that you were responsible. *"I made a mistake in the logic that caused a $15k overpayment."*
2.  **Vocal Self-Criticism (Analyze what went wrong):** Explain the root cause. This shows you have the self-awareness to diagnose your own gaps. *"The root cause was my misinterpretation of a nuanced rule and an inadequate test case for that specific scenario."*
3.  **Course Correction (Prevent repeat mistakes):** Describe the specific, systemic changes you made to prevent this class of error from ever happening again. *"To prevent it, I implemented three new safeguards: expanded unit tests, automated reconciliation checks, and a new peer-review checklist."*

#### Quantify All Results (Checklist)
For every story you tell, ensure you include at least one of these, in order of preference:
-   [ ] **Customer Impact (Strongest):** A clear, quantitative metric showing how it helped the customer (e.g., saved 4 hours per case, reduced data complaints by 50%, increased accuracy by 5%).
-   [ ] **Business Impact:** How it benefited the company beyond the immediate customer (e.g., unlocked $1M in premium, created a new development standard, influenced engineering roadmap).
-   [ ] **Lessons Learned (Required for failure stories):** Clearly articulate what you learned and how you have applied that lesson since.

---

## 5. Universal Story Framework: How to Frame Any Story

Use this chart to adapt any of your stories to a specific Leadership Principle by emphasizing the right details.

| Leadership Principle | What to Focus On in Your Story |
| :--- | :--- |
| **Customer Obsession** | How you worked backwards from a specific customer's pain point or request. |
| **Ownership** | The moment you took initiative on a problem that wasn't your direct responsibility. |
| **Invent and Simplify** | The novelty of your solution and how it made a complex process fundamentally easier. |
| **Are Right, A Lot** | A difficult judgment call you made with incomplete data by seeking diverse perspectives. |
| **Learn and Be Curious**| A time you had to quickly learn a new technology, domain, or skill to succeed. |
| **Hire and Develop the Best** | How you mentored a teammate, raised the performance bar, or made a great hiring decision. |
| **Insist on the Highest Standards**| A time you prevented a defect, established a new quality bar, or refused to accept "good enough." |
| **Think Big** | How your solution was not just a one-off fix, but a scalable pattern for the entire company. |
| **Bias for Action** | A time you took a calculated risk to make progress instead of waiting for perfect consensus. |
| **Frugality** | How you achieved significant results by optimizing existing resources instead of asking for more. |
| **Earn Trust** | A time you made a mistake, owned it transparently, and described the specific steps you took to fix it. |
| **Dive Deep** | The specific data, metrics, or logs you personally used to diagnose a root cause. |
| **Have Backbone; Disagree & Commit** | How you respectfully challenged a decision with data, and then fully supported the final outcome. |
| **Deliver Results** | The most significant, quantifiable business or customer metric that you personally moved. |
| **Strive to be Earth's Best Employer** | How you helped create a safer, more productive, or more inclusive team environment. |
| **Success and Scale Bring Broad Responsibility** | The long-term, secondary consequences of your work (e.g., security, privacy) and how you anticipated them. |

---

## 6. Quick-Reference Story Bank

Use this list during your interview as a quick reminder of the stories you have prepared.

*   **AI Sales Tool:** (Invent & Simplify, Customer Obsession, Deliver Results) - *GenAI, Streamlit, ECS, Bedrock, Snowflake, 90% time reduction.*
*   **AI Claims Tool:** (Bias for Action, Invent & Simplify) - *POC in evenings, 90% time reduction, 95% accuracy.*
*   **Power BI Version Control:** (Insist on Highest Standards, Earn Trust) - *Git for BI, JSON conversion, 50% fewer complaints.*
*   **Census Data Pipeline:** (Ownership, Have Backbone) - *Unowned process, built POC, $800k ROI deck to influence eng.*
*   **SalesMart Dashboard:** (Are Right, A Lot, Deliver Results) - *Metric alignment workshops, $1.5M lift, top-3 dashboard.*
*   **Commission RCA (Failure):** (Earn Trust, Ownership, Dive Deep) - *$15k overpayment bug, took ownership, built 3 new guardrails.*
*   **Data Quality Framework:** (Dive Deep, Deliver Results) - *Proactive monitoring, 70% error reduction, no more exec surprises.*
*   **Power BI Latency Fix:** (Frugality, Dive Deep) - *120s to 9s load time, no new hardware, 20% usage increase.*
*   **Misaligned Metrics (Failure):** (Earn Trust, Are Right A Lot) - *Paused development, owned mistake, ran metric workshops, became new standard.*
*   **Market Insights Integration:** (Think Big, Ownership) - *Solved strategic data gap, 80% adoption, 5% win rate increase, $2M pipeline.*
