# Problem 1: Product Sense - PYMK Success with Private Accounts
**Time Limit: 8 minutes**

## Scenario
Meta's Social Graph team is revamping the "People You May Know" (PYMK) feature. A key challenge is defining and measuring success, especially when suggestions involve private accounts. The PM asks: "How should we define success for PYMK when suggesting private accounts, and what are the key trade-offs?"

**Current State**: 
- PYMK suggests both public and private accounts.
- For private accounts, users can only send a follow request (no profile preview).
- Current success metric for PYMK is "accepted friend/follow requests per suggestion shown."

## Your Task

### Part A: Defining Success for Private Account Suggestions (4 minutes)
**Question**: How would you define and measure the success of PYMK suggestions specifically for *private accounts*? Propose 2-3 key metrics and explain why they are better than the current metric for this segment.

*Hint: Think about user intent, privacy respect, and long-term connection value.*

### Part B: Trade-offs and Risks (2 minutes)  
**Question**: What are the main trade-offs or risks associated with your proposed success metrics for private account suggestions?

*Hint: Consider potential for unwanted requests, user frustration, or metric gaming.*

### Part C: A/B Testing Strategy (2 minutes)
**Question**: If we want to test a new algorithm that aims to improve suggestions for private accounts, how would you design an A/B test? What is your primary success metric, and what are key guardrail metrics?

*Hint: Focus on a specific algorithmic change, like leveraging mutual friend signals more heavily for private account suggestions.*

## Follow-up Questions
Be prepared to discuss:
- How do your metrics account for the "black box" nature of a private account suggestion (user can't see profile before requesting)?
- How would you segment users to understand if private account suggestions are performing differently for various demographics or user types?
- What if your new success metric for private accounts goes up, but overall PYMK engagement (including public accounts) goes down?
- How do you balance growth (more connections) with user safety and privacy?

## Success Criteria
- **Nuanced metrics** that specifically address the challenges of private accounts.
- **Clear articulation of trade-offs** between growth, user experience, and privacy.
- **Well-designed A/B test** with appropriate success and guardrail metrics.
- **Deep understanding** of social graph dynamics and user privacy considerations.

## Meta Context
- Meta aims to foster "meaningful connections," not just connection volume.
- Privacy is a paramount concern, and features must respect user settings.
- PYMK is a major driver of new connections on Facebook and Instagram.
- Success definitions must align with long-term platform health. 