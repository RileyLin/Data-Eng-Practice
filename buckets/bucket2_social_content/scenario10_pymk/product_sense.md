# Scenario 10: PYMK (People You May Know) - Social Graph Optimization

## Question 10.1.1: PYMK Algorithm Strategy

**Interviewer:** "You're designing the 'People You May Know' feature for a social platform. How would you approach building a recommendation system that balances accuracy, user privacy, and engagement while avoiding awkward or unwanted suggestions?"

**Candidate Answer (Structured Bullet Points):**

"Building an effective PYMK system requires balancing multiple competing objectives: recommendation accuracy, user privacy, engagement optimization, and trust/safety. Here's my comprehensive approach:

*   **I. Core Recommendation Signals & Data Sources:**

    *   **Primary Signals:**
        *   **Mutual Connections:** Friends of friends with weighted scoring by relationship strength
        *   **Contact Book Matching:** Phone/email imports with explicit user consent
        *   **Location Proximity:** Frequent co-location patterns (with privacy controls)
        *   **Interaction History:** Profile views, message exchanges, group memberships

    *   **Secondary Signals:**
        *   **Educational/Professional Networks:** School, workplace, industry connections
        *   **Interest Similarity:** Shared interests, pages liked, content engagement
        *   **Platform Behavior:** Similar usage patterns, timing, feature adoption
        *   **Demographic Similarity:** Age, location, language (used carefully)

*   **II. Algorithm Design Framework:**

    *   **Multi-Stage Recommendation Pipeline:**
        1. **Candidate Generation:** Broad signal-based user filtering (mutual friends, contacts, location)
        2. **Feature Engineering:** Compute similarity scores across multiple dimensions
        3. **Ranking Model:** ML-based scoring considering engagement probability and user preferences
        4. **Safety Filtering:** Remove inappropriate suggestions (exes, professional conflicts, etc.)
        5. **Diversity & Freshness:** Ensure variety in recommendations over time

    *   **Scoring Algorithm Components:**
        *   **Connection Strength Score:** Weight mutual friends by relationship quality
        *   **Interaction Probability:** Likelihood user will engage based on historical patterns
        *   **Network Value:** How much this connection enhances user's overall network
        *   **Privacy Comfort Score:** Confidence the suggestion won't feel invasive

*   **III. Privacy & Trust Considerations:**

    *   **Transparency & Control:**
        *   **Explanation Interface:** Clear reasoning for why someone was suggested
        *   **Opt-out Mechanisms:** Easy ways to hide/remove suggestions and prevent future ones
        *   **Granular Privacy Settings:** Control which signals contribute to recommendations
        *   **Mutual Suggestion Control:** Option to appear/not appear in others' PYMK

    *   **Sensitive Situation Handling:**
        *   **Ex-Relationship Detection:** Avoid suggesting former romantic partners
        *   **Professional Boundaries:** Careful handling of work relationships in personal contexts
        *   **Therapy/Medical Connections:** Special handling for healthcare professional relationships
        *   **Geographic Overlap Sensitivity:** Avoid suggestions based on sensitive locations

*   **IV. Engagement Optimization Strategy:**

    *   **Personalization Dimensions:**
        *   **User Lifecycle Stage:** Different strategies for new vs. established users
        *   **Network Density:** More aggressive suggestions for users with few connections
        *   **Platform Usage Patterns:** Adapt to user's typical engagement style
        *   **Social Comfort Level:** Respect introvert/extrovert tendencies

    *   **Timing & Presentation:**
        *   **Contextual Placement:** Show suggestions when users are in "social discovery" mode
        *   **Batch Size Optimization:** Right number of suggestions to avoid overwhelming
        *   **Visual Design:** Clear, non-pushy interface that respects user agency
        *   **Notification Strategy:** When to proactively surface vs. wait for user exploration

*   **V. Quality & Safety Measures:**

    *   **Fake Account Detection:**
        *   Filter out bots, spam accounts, and fake profiles from suggestions
        *   Account verification signals and behavioral pattern analysis
        *   Community reports and trust score integration

    *   **Harassment Prevention:**
        *   **Block List Integration:** Never suggest users who've been blocked
        *   **Stalking Pattern Detection:** Identify and prevent excessive profile viewing
        *   **Mutual Interest Validation:** Ensure suggestions are likely to be welcomed
        *   **Geographic Sensitivity:** Avoid enabling real-world stalking through location data

*   **VI. Success Metrics & Optimization:**

    *   **Core KPIs:**
        *   **Connection Rate:** Percentage of suggestions that result in friend requests
        *   **Acceptance Rate:** Percentage of requests that are accepted
        *   **Mutual Request Rate:** Both users send/accept requests (strongest signal)
        *   **Long-term Relationship Quality:** Ongoing interaction between connected users

    *   **User Experience Metrics:**
        *   **Suggestion Relevance Rating:** User feedback on recommendation quality
        *   **Feature Adoption:** How often users engage with PYMK vs. ignore
        *   **Negative Feedback Rate:** Complaints, blocks, or opt-outs from suggestions
        *   **Privacy Comfort Score:** User surveys on comfort with recommendation transparency

The key is building a system that feels helpful rather than creepy, respects user privacy and consent, and creates genuine value by facilitating meaningful connections while preventing misuse."

## Question 10.1.2: PYMK Success Metrics Framework

**Interviewer:** "How would you design a comprehensive metrics framework to measure the success of your PYMK feature across user acquisition, engagement, and long-term platform health?"

**Candidate Answer (Structured Bullet Points):**

"A successful PYMK system impacts multiple aspects of platform health, so the metrics framework must capture both immediate user behavior and long-term network effects. Here's my comprehensive approach:

*   **I. User Acquisition & Network Growth Metrics:**

    *   **Connection Formation KPIs:**
        *   **Daily/Monthly New Connections:** Total friendships formed via PYMK suggestions
        *   **Connection Velocity:** Time from suggestion to friend request to acceptance
        *   **Suggestion-to-Connection Rate:** Overall conversion funnel performance
        *   **Mutual Connection Rate:** Bidirectional friend requests (strongest success signal)

    *   **Network Expansion Impact:**
        *   **Network Size Growth:** Average friend count increase for PYMK users
        *   **Network Quality Score:** Engagement levels between PYMK-introduced connections
        *   **First-Degree Network Density:** How PYMK affects user's immediate network richness
        *   **Second-Degree Network Reach:** Access to broader social graph through new connections

*   **II. User Engagement & Platform Activity:**

    *   **Direct Feature Engagement:**
        *   **PYMK Section Visit Rate:** How often users check suggestions
        *   **Suggestion Interaction Rate:** Clicks, profile views, message sends from PYMK
        *   **Session Depth:** How PYMK affects overall platform session duration
        *   **Return Engagement:** Users coming back specifically for social discovery

    *   **Downstream Platform Activity:**
        *   **Content Engagement Boost:** Increased likes, comments, shares after new connections
        *   **Messaging Activity:** New conversation threads started with PYMK connections
        *   **Event/Group Participation:** Social activities enabled by PYMK connections
        *   **Platform Stickiness:** Overall DAU/MAU improvement attributable to PYMK

*   **III. User Experience & Satisfaction Metrics:**

    *   **Suggestion Quality Indicators:**
        *   **Relevance Rating:** User feedback on suggestion appropriateness (1-5 scale)
        *   **Surprise vs. Expected Ratio:** Balance of obvious vs. serendipitous suggestions
        *   **Suggestion Freshness:** How often new, non-repetitive suggestions appear
        *   **Geographic/Interest Relevance:** Match quality across different user attributes

    *   **User Control & Comfort:**
        *   **Privacy Comfort Score:** User surveys on comfort with recommendation transparency
        *   **Control Usage Rate:** How often users adjust PYMK privacy settings
        *   **Negative Feedback Rate:** Hide/block suggestions, opt-out requests
        *   **Feature Satisfaction NPS:** Net Promoter Score specifically for PYMK

*   **IV. Trust & Safety Performance:**

    *   **Safety Incident Prevention:**
        *   **Inappropriate Suggestion Rate:** Suggestions leading to harassment reports
        *   **Ex-Partner Suggestion Errors:** False positives in sensitive relationship detection
        *   **Stalking Enablement:** Incidents where PYMK facilitated unwanted contact
        *   **Fake Account Filter Effectiveness:** Spam/bot accounts prevented from suggestions

    *   **Privacy Protection Metrics:**
        *   **Contact Leak Prevention:** Zero unauthorized contact book disclosures
        *   **Location Privacy Compliance:** Adherence to location-based suggestion preferences
        *   **Professional/Personal Boundary Respect:** Work vs. personal context separation
        *   **User Data Minimization:** Only using necessary data for recommendations

*   **V. Business Impact & Platform Health:**

    *   **User Retention & Growth:**
        *   **New User Onboarding Success:** PYMK impact on user activation and retention
        *   **Churned User Reactivation:** Bringing back inactive users through social re-engagement
        *   **Organic Growth Rate:** New user acquisition through strengthened social networks
        *   **User Lifetime Value:** Long-term platform value increase from PYMK connections

    *   **Network Effect Amplification:**
        *   **Platform Network Density:** Overall connectedness improvement across user base
        *   **Content Virality:** How PYMK connections affect content spread
        *   **Community Formation:** New groups/communities formed via PYMK connections
        *   **Cross-Product Engagement:** PYMK impact on other platform features

*   **VI. Comparative & Experimental Analysis:**

    *   **A/B Testing Framework:**
        *   **Algorithm Performance:** Different recommendation approaches and their outcomes
        *   **UI/UX Variations:** Presentation format impact on user engagement
        *   **Frequency Optimization:** Optimal timing and volume of suggestions
        *   **Personalization Effectiveness:** Customized vs. generic recommendation strategies

    *   **Benchmarking & Industry Comparison:**
        *   **Peer Platform Performance:** Connection rates compared to industry standards
        *   **Feature Adoption Curves:** PYMK uptake vs. other social discovery features
        *   **User Segment Analysis:** Performance across demographics, usage patterns, network sizes
        *   **Regional/Cultural Effectiveness:** How PYMK performs across different markets

The framework ensures PYMK creates genuine value for users while supporting broader platform objectives and maintaining the trust and safety that's essential for long-term social platform success." 