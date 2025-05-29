# Problem 2: Data Modeling - Ads Attribution Schema Design
**Time Limit: 8 minutes**

## Scenario
Design a data warehouse schema to track ad impressions, clicks, and conversions for attribution analysis. The system must handle complex customer journeys across multiple devices and platforms while supporting real-time attribution calculations.

## Requirements
- **Scale**: 100B+ ad events per day globally
- **Attribution**: Support multiple attribution models (last-click, first-click, linear, data-driven)
- **Cross-device**: Track user journeys across mobile, desktop, apps
- **Real-time**: Enable real-time conversion attribution for campaign optimization
- **Privacy**: Comply with iOS 14.5+, GDPR, and other privacy regulations

## Your Task

### Part A: Core Schema Design (4 minutes)
**Design the main fact and dimension tables for:**

1. **Ad Events**: Track impressions, clicks, and post-click behavior
2. **Conversion Events**: Capture purchases, sign-ups, and other conversion actions
3. **Attribution Logic**: Support multiple attribution models and windows

**Required Events to Model:**
- `ad_impression`, `ad_click`, `ad_view_through`
- `landing_page_visit`, `product_page_view`, `add_to_cart`
- `purchase`, `signup`, `download`, `form_submit`
- `cross_device_match`, `identity_resolution`

**Key Attribution Features:**
- Attribution windows (1, 7, 28 days)
- Multiple touchpoint tracking
- Campaign/ad group hierarchy
- Device and platform tracking
- Revenue and conversion value

### Part B: Cross-Device Identity Resolution (2 minutes)
**Question**: How would you model user identity linking across devices while respecting privacy constraints?

*Consider: Probabilistic matching, deterministic linking, privacy-safe hashing, confidence scores*

### Part C: Attribution Model Flexibility (2 minutes)
**Question**: How would you design the schema to support different attribution models without reprocessing all historical data?

*Consider: Touchpoint storage, attribution calculation flexibility, model comparison capabilities*

## Follow-up Questions
Be prepared to discuss:
- How would you handle iOS ATT (App Tracking Transparency) limitations?
- What approach would you take for modeling view-through attribution?
- How would you design for incrementality measurement vs last-touch attribution?
- What schema optimizations would support real-time bidding decisions?

## Technical Constraints
- **Query Performance**: Attribution queries must complete in <5 seconds for campaign dashboards
- **Data Retention**: Support 2+ years of attribution analysis
- **Privacy Compliance**: Enable efficient data deletion and anonymization
- **Real-time Processing**: Support streaming attribution calculations
- **Cross-platform**: Work across Facebook, Instagram, Audience Network

## Success Criteria
- **Scalable design** for Meta's advertising volume (millions of advertisers)
- **Flexible attribution** supporting multiple models and windows
- **Privacy-compliant** identity resolution approach
- **Performance-optimized** for real-time and batch workloads

## Meta Context
- Attribution accuracy directly impacts advertiser spend and Meta revenue
- Cross-device attribution is critical for mobile-first advertisers
- Privacy changes require sophisticated modeling approaches
- Real-time attribution enables dynamic campaign optimization
- Schema must support ML-based attribution models 