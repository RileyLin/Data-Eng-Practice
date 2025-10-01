# Architectural Trade-offs for Startups: An Evolutionary Guide

This document provides a framework for thinking about how startup architectures evolve. The right answer for a Pre-Seed MVP is often the wrong answer for an enterprise-scale company. A good architect understands the trade-offs at each stage, balancing cost, simplicity, and scalability.

---

## Pattern 1: Video Processing & Analysis Platform

This pattern is common for startups in social media, content creation, or security.

### Architectural Evolution Chart

| Architectural Component | Decision for Pre-Seed (MVP) | Decision for Startup Scale | Evolution at Enterprise Scale |
| :--- | :--- | :--- | :--- |
| **Video Ingestion & Storage** | S3 Standard | S3 Standard | S3 Intelligent-Tiering & CloudFront |
| **Processing Trigger** | S3 Event -> Lambda | S3 Event -> SQS -> Compute | Amazon EventBridge |
| **Video Analysis Compute** | Single EC2 Instance | AWS Lambda | ECS on Fargate / AWS Batch |
| **Recommendation Engine** | Keyword Search (SQL `LIKE`) | Semantic Search (pgvector in RDS) | Dedicated Vector DB (OpenSearch) |
| **Primary Database** | Athena over S3 & DynamoDB Free Tier| Amazon RDS (PostgreSQL) | Polyglot Persistence (Aurora, OpenSearch, DynamoDB) |

### Explanation of Trade-offs

*   **Video Storage:** You start with **S3 Standard** because it's simple, cheap, and reliable. At enterprise scale, you introduce **S3 Intelligent-Tiering** to automatically optimize storage costs for less frequently accessed videos, and **CloudFront** (a CDN) to reduce latency and data transfer costs for users globally.
*   **Processing Trigger:** The MVP starts with a tightly coupled **S3 Event -> Lambda** trigger. It's simple and instant. As you scale, you introduce an **SQS queue** to decouple the system. This adds resilience; if the compute service fails, the processing requests are safely stored in the queue. At enterprise scale, **Amazon EventBridge** is used as a sophisticated event bus, allowing multiple different services to react to a single event (e.g., video upload triggers analysis, notifications, and billing).
*   **Video Analysis Compute:** An MVP can run on a **single EC2 instance** for simplicity. As you scale, you move to **AWS Lambda** to get serverless scalability and pay-per-use pricing. For very long-running or resource-intensive analysis at enterprise scale, you move to **ECS on Fargate** or **AWS Batch**, which are better suited for heavy, stateful workloads than Lambda.
*   **Recommendation Engine:** You begin with a basic **keyword search** using SQL's `LIKE` operator—it's built-in and "free." As you grow, you need smarter recommendations, so you adopt **semantic search** using an extension like `pgvector` in your existing RDS database. At massive scale, you need a dedicated, performance-optimized **Vector Database** like OpenSearch to handle the load.
*   **Primary Database:** The MVP uses **serverless and free-tier options** like Athena and DynamoDB to keep costs near zero. A scaling startup needs the consistency and power of a managed relational database like **Amazon RDS**. An enterprise uses **Polyglot Persistence**, choosing the right database for the right job (e.g., Aurora for transactions, OpenSearch for search, DynamoDB for user metadata), as no single database can solve all problems at scale.

---

## Pattern 2: E-commerce Platform

This pattern is for transactional businesses selling products online.

### Architectural Evolution Chart

| Architectural Component | Decision for Pre-Seed (MVP) | Decision for Startup Scale | Evolution at Enterprise Scale |
| :--- | :--- | :--- | :--- |
| **Product Catalog API** | Lambda + API Gateway | ECS on Fargate + ALB | Microservices on EKS/ECS |
| **Shopping Cart** | DynamoDB | ElastiCache for Redis | ElastiCache for Redis |
| **Order Processing** | Lambda writing to DynamoDB | Decoupled via SQS | Event-driven via EventBridge |
| **Primary Database** | DynamoDB Free Tier | Amazon Aurora (MySQL/Postgres) | Aurora + DynamoDB |

### Explanation of Trade-offs

*   **Product Catalog API:** Start serverless with **Lambda and API Gateway** for low cost and simplicity. As traffic grows, move to **ECS on Fargate** behind an Application Load Balancer (ALB) for better control over networking and sustained performance. At enterprise scale, you would likely break this monolith into **multiple microservices** to allow independent scaling and development.
*   **Shopping Cart:** A shopping cart needs to be fast and handle temporary state. **DynamoDB** works for an MVP, but an in-memory database is the right tool for the job. You quickly evolve to **ElastiCache for Redis** at startup scale for its microsecond latency and it remains the best choice even at enterprise scale.
*   **Order Processing:** An MVP can have a Lambda function **write directly to a database**. This is simple but brittle. You quickly introduce an **SQS queue** to ensure that even if the database is busy, no orders are ever lost. At enterprise scale, placing an order becomes a business event that multiple systems need to react to (inventory, shipping, analytics, notifications), making **EventBridge** the right choice.
*   **Primary Database:** The MVP can start with **DynamoDB's free tier**. As the business grows and requires complex transactional queries (e.g., joining orders with customers and products), a relational database like **Amazon Aurora** becomes necessary. Enterprises will often use both: Aurora for the core transactional order data and DynamoDB for high-traffic, key-value data like user session history or product metadata.

---

## Pattern 3: Multi-Tenant SaaS Application

This pattern is for B2B startups selling software subscriptions.

### Architectural Evolution Chart

| Architectural Component | Decision for Pre-Seed (MVP) | Decision for Startup Scale | Evolution at Enterprise Scale |
| :--- | :--- | :--- | :--- |
| **Authentication** | Amazon Cognito | Amazon Cognito | Cognito + Custom Authorizers / Federation |
| **Application Backend** | Monolith on Elastic Beanstalk | Monolith on Fargate | Microservices on EKS/ECS |
| **Tenant Data Isolation** | Shared DB, Shared Schema | Shared DB, Schema-per-Tenant | Database-per-Tenant ("Silo") |
| **Tenant Onboarding** | Manual Scripts | Automated via Lambda | "Vending Machine" with Step Functions |

### Explanation of Trade-offs

*   **Authentication:** **Amazon Cognito** is the right choice at almost every stage for handling user sign-up, sign-in, and security. It's a managed service that solves a complex problem. At enterprise scale, you may need to add **custom authorizers** for fine-grained permissions or **federate** with a customer's identity provider like Okta or Azure AD.
*   **Application Backend:** The MVP starts as a **monolith on Elastic Beanstalk** because it's the fastest way to get a traditional web app running. You evolve to a **monolith on Fargate** for better cost control and scalability. At enterprise scale, the monolith is broken into **microservices**, allowing different components of your application to be developed and scaled independently.
*   **Tenant Data Isolation:** This is the most critical decision in a SaaS app. The MVP starts with the simplest model: all tenants share a **single database and schema**, with a `tenant_id` column on every table. As you scale and tenants demand more data isolation, you move to a **schema-per-tenant** model. At enterprise scale, for maximum security and to prevent the "noisy neighbor" problem, you move to a **database-per-tenant** model, where each customer gets their own dedicated database.
*   **Tenant Onboarding:** You start by **running manual scripts** to provision a new customer. You quickly **automate this with a Lambda function**. At enterprise scale, you build a "vending machine" using **AWS Step Functions** that orchestrates the entire, complex process of creating a new tenant: provisioning the database, setting up users, configuring permissions, and activating the subscription.
