# Phase 3: Technical Communications Presentation

This document is for planning and refining your 20-25 minute technical presentation. The goal is to create a compelling narrative that balances technical depth with business impact for a mixed audience.

---

## 1. Project Selection

**Selected Project:** `SalesMart Quoting Dashboard`

**Reasoning:** This is your designated "flagship" project with the strongest, most quantifiable business impact ($1.5M projected lift), making it the ideal choice to showcase your ability to deliver results.

---

## 2. Presentation Structure (Slide Deck Outline)

**Instructions:** Use this 5-slide structure as a template for your presentation. Draft the key talking points for each slide. Remember to keep it concise and focused on the narrative.

### **Slide 1: Title**
*   **Title:** The SalesMart Quoting Dashboard: Driving $1.5M in Business Impact Through Data
*   **Your Name & Role**

### **Slide 2: Situation/Task (The Business Problem)**
*   **Key Idea:** Focus on the customer's pain point.
*   **Talking Points:**
    *   "Sales executives were flying blind."
    *   "They had to manually stitch together 10 different reports, a process that took up to 5 days."
    *   "By the time they got the data, it was stale. They couldn't answer critical business questions about their sales funnel."
    *   "The business impact was tangible: we were potentially losing millions because we couldn't react to funnel issues in time."

### **Slide 3: Action (The Solution Architecture)**
*   **Key Idea:** Present a clean, high-level architectural diagram.
*   **Diagram Components:** Data Sources → Ingestion → Staging (Snowflake) → Transformation (dbt) → Data Warehouse/SalesMart → BI Layer (Power BI)
*   **Talking Points:**
    *   "To solve this, I designed and led the development of a new, centralized SalesMart."
    *   "Here is the high-level architecture. I'll walk you through the key components..."
    *   *(Briefly explain the data flow from left to right)*

### **Slide 4: Action (Key Decisions & Trade-offs)**
*   **Key Idea:** Show you are a thoughtful architect by explaining *why* you made certain choices. Pick 1-2 important decisions.
*   **Talking Point 1 (ELT vs. ETL):**
    *   "A key decision was choosing a modern ELT approach with dbt over traditional ETL. The **trade-off** was slightly higher compute cost in the warehouse, but the **benefit** was a massive increase in development speed. This bias for action allowed us to deliver the core dashboard in months, not a year."
*   **Talking Point 2 (Metric-Definition Workshops):**
    *   "I made the call to invest time upfront in two workshops to align on metric definitions. While this seemed to slow us down initially, it ensured we were building the right thing and prevented months of downstream rework. This is an example of insisting on the highest standards."

### **Slide 5: Result (The Business & Customer Impact)**
*   **Key Idea:** End with your strongest, most quantifiable results.
*   **Talking Points:**
    *   "We cut the analytics refresh time from **5 days to 15 minutes**."
    *   "We replaced **10 reports with 1 single source of truth** that became a top-3 most-used dashboard in the company."
    *   "Most importantly, by exposing a 6% drop-off in the sales funnel, the fix we enabled is projected to lift annual premium by **$1.5 million**."
    *   "This project demonstrated the power of turning data into a product that drives proactive business decisions."

---

## 3. Rehearsal and Delivery

**Instructions:** Practice delivering the presentation out loud. Record yourself or present to a friend who is not a data expert.

**Key things to check:**
*   [ ] **Timing:** Is the presentation between 20-25 minutes?
*   [ ] **Clarity:** Can a non-technical person understand the business problem and the value of your solution?
*   [ ] **Q&A Ready:** Are you prepared for interviewers to interrupt and ask questions throughout? (e.g., "Why did you choose Snowflake for this?"). Your `phase_2_technical_prep.md` justification library will help here.
