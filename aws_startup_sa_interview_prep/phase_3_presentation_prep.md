# Phase 3: Technical Communications Presentation

This document is for planning and refining your 20-25 minute technical presentation. The goal is to create a compelling narrative that balances technical depth with business impact for a mixed audience.

---

## 1. Project Selection

**Selected Project:** `Sales & Underwriting AI Automation Tool`

**Reasoning:** This project is the ideal choice for the AWS Startup SA role. It directly showcases your hands-on experience with GenAI (AWS Bedrock) and modern cloud-native deployment (ECS), which are key focus areas for the team. The narrative of automating a highly manual process is compelling and clearly demonstrates high-impact business results and innovation.

---

## 2. Presentation Structure (Slide Deck Outline)

**Instructions:** Use this 5-slide structure as a template for your presentation. Draft the key talking points for each slide. Remember to keep it concise and focused on the narrative.

### **Slide 1: Title**
*   **Title:** Automating Sales Insights: How an AI-Powered App Reduced Case Prep Time by 90%
*   **Subtitle:** A technical walkthrough of a generative AI solution built on AWS.
*   **Your Name & Role**

### **Slide 2: Situation/Task (The Business Problem)**
*   **Key Idea:** Focus on the customer's (the sales team's) pain. Make it tangible.
*   **Communication Strategy:** Start with the "why." Don't jump to technology yet. Explain the manual, frustrating process that existed before your solution. Use visuals if possible (e.g., a diagram showing a person juggling multiple spreadsheets and documents).
*   **Talking Points:**
    *   "Our sales and underwriting teams were spending 4-5 hours of manual, repetitive work on every single new business case."
    *   "This involved ad-hoc reporting, profitability analysis, and manual industry research. It was slow, prone to error, and knowledge wasn't being shared effectively."
    *   "The business impact was clear: slower response times to customers and a painful, unscalable onboarding process for new hires. The core problem was a lack of automation and centralized intelligence."

### **Slide 3: Action (The Solution Architecture)**
*   **Key Idea:** Present a clean, high-level architectural diagram that tells the story of the solution.
*   **Communication Strategy:** Walk through the diagram from left to right, explaining how data flows and is transformed. Address the mixed audience by explaining *what* each component does in simple terms before going deeper.
*   **Diagram Components:**
    1.  **Data Sources** (Snowflake DB, External APIs)
    2.  **Python Backend** (Hosted on **AWS ECS on Fargate**) - Explain this as "the brain of the operation, running in a scalable, serverless container."
    3.  **AWS Bedrock API** - Explain as "the Generative AI service we use to analyze data and generate insights."
    4.  **Streamlit UI** - Explain as "the simple web interface for the sales team to interact with."
    5.  **PDF Generation** - The final output.
*   **Talking Points:**
    *   "To solve this, I designed and built an AI-powered application. Here’s how it works at a high level."
    *   "First, the application, running on AWS ECS, pulls structured data from our Snowflake warehouse."
    *   "It then sends that data along with a prompt to the AWS Bedrock API, asking it to perform a detailed analysis."
    *   "The user interacts with a simple Streamlit front-end, and the final output is a client-ready PDF report, generated in minutes."

### **Slide 4: Action (Key Decisions & Trade-offs)**
*   **Key Idea:** This is the most critical slide for an SA role. Show you think like an architect. Pick 2-3 key decisions.
*   **Communication Strategy:** For each decision, explicitly state the **trade-off** you considered and why you made your choice. Frame it as balancing competing needs (e.g., speed vs. control, cost vs. features).
*   **Talking Point 1 (Why a Custom App vs. a BI Dashboard?):**
    *   "My first big decision was to build a custom Streamlit app instead of using a standard BI tool. The **trade-off** was more development effort upfront. But the **benefit** was a perfectly tailored workflow for the sales team and, crucially, the ability to integrate directly with Python-based AI services like Bedrock, which a BI tool couldn't do."
*   **Talking Point 2 (Why ECS with Fargate for Hosting?):**
    *   "For deployment, I chose AWS ECS with Fargate. The **trade-off** was learning how to containerize the application versus using a simple virtual machine. The **benefit** was immense: we got a serverless, scalable, and cost-effective solution. We don't pay for idle servers, and it can automatically handle more users during busy quoting seasons."
*   **Talking Point 3 (Why AWS Bedrock for AI?):**
    *   "For the AI component, I chose to use a managed service, AWS Bedrock. The **trade-off** was using a managed API versus the flexibility of hosting our own open-source model. The **benefit** was a massive reduction in operational overhead, built-in security and compliance, and the ability to easily experiment with different foundation models to find the best one for our needs."

### **Slide 5: Result (The Business & Customer Impact)**
*   **Key Idea:** End on a high note with clear, quantified results. Reconnect back to the pain points from Slide 2.
*   **Communication Strategy:** Use large, bold numbers. Start with your most impressive metric.
*   **Talking Points:**
    *   "The impact on the business was immediate and significant. We reduced case preparation time from over **4 hours to under 30 minutes**—a 90% reduction."
    *   "This translated to faster turnaround for customers and allowed each sales rep to handle a larger pipeline."
    *   "We also created a consistent, high-quality reporting standard and a scalable onboarding process for new team members."
    *   "Ultimately, this project proved that by investing in targeted AI automation on the cloud, we could directly improve the productivity and effectiveness of our entire sales organization."

---

## 3. Rehearsal and Delivery

**Instructions:** Practice delivering the presentation out loud. Record yourself or present to a friend who is not a data expert.

**Key things to check:**
*   [ ] **Timing:** Is the presentation between 20-25 minutes?
*   [ ] **Clarity:** Can a non-technical person (like an Account Manager) understand the business problem and the value of your solution?
*   [ ] **Q&A Ready:** Be prepared for deep-dive questions on your architecture. They will interrupt you. Why Fargate vs. EC2? What kind of prompts did you use for Bedrock? How did you ensure data security? Your `phase_2_technical_prep.md` will be crucial here.
