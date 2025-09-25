# AWS Startup SA: Technical Scenario Practice

This document contains a series of practice scenarios designed to simulate the technical portion of the AWS Solutions Architect interview. Each scenario is deliberately vague. The goal is to first practice the "discovery-first" approach by asking clarifying questions, and then to design a solution, justifying your choices and discussing trade-offs.

---

## Practice Scenarios

1.  **AI-Powered Search (Perplexity-like):** A startup is creating an AI-powered search platform for enterprise clients. It needs to browse the real-time internet, ingest a company's internal documents, and provide verifiable, cited answers to complex research questions.
2.  **HIPAA-Compliant Patient Communication (OhMD-like):** A health-tech startup is building a SaaS platform to enable secure, text-based communication between doctors and patients, integrating with Electronic Health Records (EHR).
3.  **Creator E-commerce Platform (Zeepty-like):** A social commerce startup enables creators to launch their own storefronts, curating and selling products. The platform needs to handle high-traffic product discovery, inventory management, and order processing.
4.  **Real-time Gaming Backend:** A gaming startup is launching a new mobile game and needs a backend to handle user authentication, store player data and game state, and manage a real-time global leaderboard.
5.  **AI Personal Assistant (NinjaTech AI-like):** A startup is developing an AI personal assistant that can research topics, schedule meetings, and execute tasks. It needs to process user requests via chat and voice, and orchestrate a series of actions.
6.  **No-Code AI Business Platform (Symphona-like):** A startup is building a no-code platform that allows business users to create and deploy their own AI-powered automations and data integration workflows.
7.  **E-commerce Modernization (Band T-Shirt Scenario):** A startup manages merchandise sales for a touring band. Their current architecture—a React/Node app and self-managed MySQL database on a single EC2 instance—crashes from traffic spikes after concerts. They also can't perform effective sales analytics. How would you re-architect their solution?

---
## Solutions & Walkthroughs

---

### **Scenario 1: AI-Powered Search (Perplexity-like)**

_"A startup is creating an AI-powered search platform for enterprise clients. It needs to browse the real-time internet, ingest a company's internal documents, and provide verifiable, cited answers to complex research questions."_

#### **Part 1: Clarifying Questions**

*   **Business Goal:** Is the primary value proposition the real-time web search, the internal knowledge search, or the combination of both?
*   **Users & Scale:** How many enterprise clients? How many users per client? What's the expected query volume (queries/sec)? How much internal data will a typical client upload (GBs, TBs)?
*   **Functional Requirements:**
    *   How "real-time" does the web search need to be?
    *   What formats are the internal documents (PDF, DOCX, HTML)?
    *   What does "verifiable" mean? Must we provide URLs and document sources for every statement?
    *   Is there a multi-user, role-based access control requirement for the internal documents?
*   **Non-Functional Requirements:** Data privacy and security for enterprise data are paramount. What are the latency requirements for a search query?
*   **Constraints:** What is the team's expertise in GenAI and search technologies?

#### **Part 2: High-Level Architecture**

This is a Retrieval Augmented Generation (RAG) architecture with two distinct data sources.

1.  **Internal Document Ingestion:**
    *   Enterprise customers upload documents to a secure **S3** bucket.
    *   An S3 event triggers a **Lambda** function that uses **Amazon Textract** to parse PDFs/images.
    *   The text is chunked and converted into embeddings by a model hosted on **Amazon SageMaker** or via **Amazon Bedrock**.
    *   These embeddings are stored in **Amazon OpenSearch Serverless** in a client-specific index.
2.  **Real-time Web Search:**
    *   When a user query arrives at the **API Gateway**, a **Lambda** function first uses a traditional search API (like Bing or Google Search API) to get a list of relevant URLs.
    *   Another service (e.g., an **ECS Fargate** task) crawls these pages, extracts the main text content, chunks it, and creates embeddings on the fly.
3.  **Answer Generation (RAG):**
    *   The user query is converted into an embedding.
    *   The backend queries both the client's OpenSearch index AND the in-memory embeddings from the web crawl to find the most relevant context.
    *   This combined context (from internal docs + web pages) and the original query are passed to a powerful foundation model (e.g., Anthropic's Claude 3 on **Amazon Bedrock**).
    *   Bedrock generates the final, cited answer, which is streamed back to the user.

#### **Part 3: Technology Choices & Justifications**

*   **S3 & Lambda:** A standard, event-driven, and scalable pattern for ingesting and processing customer data. (Pillar: Operational Excellence)
*   **Amazon Textract:** Chosen to handle complex document formats like PDFs that may contain tables and images, ensuring we extract high-quality text for our RAG pipeline. (Pillar: Reliability)
*   **OpenSearch Serverless:** A managed and scalable vector database. It's ideal for storing and searching the embeddings from internal documents, and "serverless" reduces operational overhead for the startup. (Pillar: Performance Efficiency, Operational Excellence)
*   **ECS Fargate (for crawler):** A web crawler can be a long-running or spiky task, making it a better fit for a container service like Fargate than for Lambda with its 15-minute timeout.
*   **Amazon Bedrock:** Provides secure, private access to high-performing foundation models. This is critical for enterprise customers who cannot risk their data being used for training. It simplifies model management significantly. (Pillar: Security, Operational Excellence)

#### **Part 4: Trade-offs & Path to Scale**

*   **Trade-off (Search API):** We are relying on an external search API. This adds a dependency and cost but is far more practical for a startup than trying to build a real-time web indexer from scratch.
*   **Trade-off (Embedding Model):** Using Bedrock for embeddings is easy, but a custom-trained model on SageMaker might yield better results for domain-specific jargon. The startup should start with Bedrock and only invest in a custom model if search quality becomes a competitive differentiator.
*   **Path to Scale:** As the number of clients grows, the system scales naturally. OpenSearch Serverless handles more data, and Bedrock/Lambda/Fargate scale on demand. The main bottleneck could become the real-time crawling. To scale this, they could build a more sophisticated crawling and caching layer, perhaps using a distributed web crawling framework.

---

### **Scenario 2: HIPAA-Compliant Patient Communication (OhMD-like)**

_"A health-tech startup is building a SaaS platform to enable secure, text-based communication between doctors and patients, integrating with Electronic Health Records (EHR)."_

#### **Part 1: Clarifying Questions**
*   **Compliance:** HIPAA is the key constraint. This means all services must be HIPAA-eligible and a Business Associate Addendum (BAA) must be in place with AWS.
*   **Users & Roles:** Who are the personas? Patients, doctors, nurses, clinic admins? What actions can each role perform?
*   **Functional Requirements:**
    *   How does EHR integration work? Is it a read-only sync, or do we write back to the EHR? What integration standards (e.g., HL7, FHIR)?
    *   Is it just 1-to-1 chat, or are there group/care team chats?
    *   Are we supporting just text, or also images and documents?
*   **Non-Functional Requirements:** Security is paramount: end-to-end encryption, detailed audit trails of every message view, strict access control. High availability is crucial for clinical communication.
*   **Constraints:** What is the team's experience with healthcare IT and security?

#### **Part 2: High-Level Architecture**

1.  **Authentication & Web Tier:**
    *   Users authenticate via **Amazon Cognito**. All traffic flows through an **Application Load Balancer (ALB)** to an application running on **ECS with Fargate**. These services are all in private subnets.
2.  **Messaging Service:**
    *   The core messaging logic is handled by a WebSocket API built with **API Gateway**.
    *   When a user connects, the API Gateway invokes a **Lambda** function to handle the connection.
    *   When a user sends a message, it hits a Lambda function that writes the message to a **DynamoDB** table (optimized for chat applications).
    *   The Lambda then queries a "connections" table and uses the API Gateway's post-to-connection endpoint to push the message in real-time to the recipient(s).
3.  **Data Storage & Security:**
    *   All chat messages are stored in **Amazon DynamoDB**, with encryption at rest enabled.
    *   Patient data synced from EHRs is stored in a separate, encrypted **Amazon Aurora (RDS)** database.
    *   Any uploaded files/images are stored in an **S3** bucket with SSE-KMS encryption, versioning, and object lock for retention. Access is via pre-signed URLs only.
4.  **Auditing & Integration:**
    *   **AWS CloudTrail** and VPC Flow Logs are enabled to log all API calls and network traffic.
    *   EHR integration is handled by a dedicated Fargate service that connects to the healthcare provider's network via a secure **VPN** or **AWS Direct Connect**.

#### **Part 3: Technology Choices & Justifications**

*   **All Services HIPAA-Eligible:** This is a foundational, non-negotiable requirement.
*   **API Gateway (WebSockets) & Lambda:** This combination is perfect for building a scalable, real-time, serverless chat application. It removes the need to manage a fleet of stateful servers for WebSocket connections. (Pillar: Operational Excellence, Performance Efficiency)
*   **DynamoDB for Chat:** DynamoDB's key-value model is ideal for chat applications. A common pattern is to use a composite primary key (e.g., `ConversationID` as partition key, `Timestamp` as sort key) to efficiently retrieve messages for a conversation in chronological order. (Pillar: Performance Efficiency)
*   **Aurora for Relational Data:** Patient demographic data from an EHR is highly structured and relational, making Aurora (or RDS) a better fit than DynamoDB for that specific dataset. (Pillar: Reliability)
*   **Strict Security Posture:** The use of private subnets, encryption everywhere (in transit and at rest), KMS for key management, and detailed auditing with CloudTrail are all essential controls for a HIPAA-compliant architecture. (Pillar: Security)

#### **Part 4: Trade-offs & Path to Scale**

*   **Trade-off (EHR Integration):** Integrating with EHRs is notoriously difficult. The architecture isolates this complexity into a dedicated service. The trade-off is that this integration can be slow and costly to build, depending on the EHR system.
*   **Trade-off (Feature Velocity vs. Compliance):** Every new feature must undergo a thorough security and compliance review. This will slow down development compared to a non-healthcare startup, but it's a necessary trade-off to manage risk.
*   **Path to Scale:** The serverless chat backend can scale to millions of users. As the product evolves, they can add more AI-powered features. For example, using **Amazon Comprehend Medical** on chat transcripts to extract entities or using **Amazon Transcribe** for voice-to-text notes, adding significant value for clinicians.

---
### **Scenario 3: Creator E-commerce Platform (Zeepty-like)**

_"A social commerce startup enables creators to launch their own storefronts, curating and selling products. The platform needs to handle high-traffic product discovery, inventory management, and order processing."_

#### **Part 1: Clarifying Questions**
*   **Business Model:** Are creators selling their own products, or drop-shipping? This heavily influences inventory and order management. Let's assume drop-shipping for simplicity.
*   **Users & Scale:** How many creators? How many products per creator? What is the expected traffic pattern (e.g., massive spikes when a popular creator posts a link)?
*   **Functional Requirements:**
    *   Does each creator have a customizable storefront?
    *   What are the search and discovery requirements (search by creator, product, etc.)?
    *   How is inventory tracked with the source merchants?
*   **Non-Functional Requirements:** High availability is critical, especially during traffic spikes. The site must be fast to keep potential buyers engaged.
*   **Constraints:** Small engineering team, need to launch quickly.

#### **Part 2: High-Level Architecture**

This is a microservices architecture.

1.  **Frontend & Discovery:**
    *   The creator storefronts are React applications hosted as static sites on **S3** and distributed globally with **Amazon CloudFront**.
    *   Product data is stored in **Amazon OpenSearch** for powerful search and faceting capabilities. The main application website uses OpenSearch to power its discovery features.
2.  **Core Services (Microservices on ECS with Fargate):**
    *   **Product Service:** Manages the product catalog. Data is stored in **Amazon Aurora (RDS)** as the source of truth. It writes data to OpenSearch for discovery.
    *   **Order Service:** Handles the checkout process, interacting with a payment provider like Stripe. Order data is stored in its own Aurora database.
    *   **Inventory Service:** Periodically polls third-party merchant APIs to get the latest inventory levels, caching the data in **ElastiCache (Redis)** for fast lookups during checkout.
3.  **Asynchronous Communication:**
    *   When an order is placed, the Order Service publishes an `OrderCreated` event to **Amazon EventBridge**.
    *   Other services subscribe to this event. For example, a "Notifications" service (using **Lambda**) sends a confirmation email to the customer, and a "Fulfillment" service sends the order to the merchant's API.
4.  **CDN and Caching:**
    *   **CloudFront** is used extensively to cache not just static assets but also API responses from **API Gateway**, reducing the load on the backend services during traffic spikes.

#### **Part 3: Technology Choices & Justifications**

*   **Microservices on ECS/Fargate:** The business domain (Products, Orders, Inventory) naturally breaks down into separate services. This allows for independent scaling (e.g., the Product service will get more read traffic than the Order service) and development. Fargate is chosen to minimize operational overhead. (Pillar: Performance Efficiency, Operational Excellence)
*   **CloudFront:** A CDN is non-negotiable for an e-commerce site. It ensures a fast experience for users globally and shields the backend from traffic spikes, which is a key requirement. (Pillar: Performance Efficiency, Reliability)
*   **OpenSearch:** A relational database like Aurora is not ideal for complex product search and discovery. OpenSearch provides advanced text search, filtering, and faceting, which is essential for a good e-commerce user experience. (Pillar: Performance Efficiency)
*   **EventBridge:** Using an event bus to communicate between services creates a decoupled and resilient system. If the notification service fails, for example, it doesn't stop orders from being placed. The event can be retried later. This is a much more robust pattern than direct synchronous API calls. (Pillar: Reliability)
*   **ElastiCache for Inventory:** Inventory checks are a high-throughput, low-latency operation. Hitting the database or a third-party API for every check would be too slow. Caching this data in Redis is a classic pattern to ensure a fast checkout process. (Pillar: Performance Efficiency)

#### **Part 4: Trade-offs & Path to Scale**

*   **Trade-off (Consistency):** The inventory data in Redis is cached and might not be perfectly up-to-date, which could lead to overselling. The trade-off is accepting a small risk of overselling in exchange for a much faster and more scalable checkout experience. The business would need to decide on the acceptable level of risk.
*   **Trade-off (Complexity):** A microservices architecture is more complex to develop, deploy, and monitor than a monolith. The trade-off is that it provides better scalability and long-term agility. For a very early-stage MVP, a monolith might be faster to build, but this architecture is designed for growth.
*   **Path to Scale:** The next step is to add personalization. They can use **Amazon Personalize** to create a recommendation engine, feeding it user behavior data (clicks, purchases) to create "Recommended for You" sections on the storefronts, increasing engagement and sales.

*(Solutions for scenarios 4-7 would follow the same detailed format)*
