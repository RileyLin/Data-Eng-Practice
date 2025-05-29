# Meta Interview Final Sprint - Complete Structure

## 📁 Directory Structure

```
final_sprint/
├── README.md                    # Overview and practice instructions
├── STRUCTURE.md                 # This file - complete structure guide
├── practice/                    # Practice problems (your workspace)
│   ├── scenario_1/             # DAU/MAU Engagement Funnel ✅ COMPLETE
│   │   ├── 01_product_sense.md ✅
│   │   ├── 02_data_modeling.md ✅
│   │   ├── 03_sql_analytics.md ✅
│   │   └── 04_python_processing.py ✅
│   ├── scenario_2/             # Reels Session Analytics ✅ COMPLETE
│   │   ├── 01_product_sense.md ✅
│   │   ├── 02_data_modeling.md ✅
│   │   ├── 03_sql_analytics.md ✅
│   │   └── 04_python_processing.py ✅
│   ├── scenario_3/             # Ads Attribution & ROI ✅ COMPLETE
│   │   ├── 01_product_sense.md ✅
│   │   ├── 02_data_modeling.md ✅
│   │   ├── 03_sql_analytics.md ✅
│   │   └── 04_python_processing.py ✅
│   ├── scenario_4/             # Messaging Share Lineage [TODO: Create]
│   └── scenario_5/             # Data Quality & ETL [TODO: Create]
└── solutions/                  # Complete solutions with explanations
    └── README.md               # All solutions with Meta-level depth ✅
```

## 🎯 Scenario Coverage

### ✅ **Completed Scenarios**

#### **Scenario 1: DAU/MAU Engagement Funnel** ✅ COMPLETE
- **Theme**: News Feed retention and user stickiness analysis
- **Business Context**: DAU/MAU ratio declined from 0.65 to 0.58
- **All 4 parts complete**: Product sense, data modeling, SQL, Python
- **Python File**: Runnable with test cases for DAU/MAU calculation, churn analysis, cohort retention

#### **Scenario 2: Reels Session Analytics** ✅ COMPLETE
- **Theme**: Short-form video engagement and creator performance
- **Business Context**: Session duration dropped 15%, need analytics infrastructure
- **All 4 parts complete**: Product sense, data modeling, SQL, Python
- **Python File**: Runnable with test cases for event parsing, metrics tracking, viral detection

#### **Scenario 3: Ads Attribution & ROI** ✅ COMPLETE
- **Theme**: Ad performance measurement and attribution analysis
- **Business Context**: 30% attribution gaps affecting advertiser confidence
- **All 4 parts complete**: Product sense, data modeling, SQL, Python
- **Python File**: Runnable with test cases for attribution models, cross-device linking, ROAS calculation

### 🚧 **TODO: Complete Remaining Scenarios**

Need to create:
- Scenario 4: Complete messaging/share lineage scenario (viral content tracking)
- Scenario 5: Complete data quality/ETL scenario (pipeline optimization)

## 🚀 How to Use This Practice Set

### **For Interview Prep:**

1. **Pick a scenario** based on what Meta trend you want to practice
2. **Set 32-minute timer** (8 min per section)
3. **Work through all 4 parts** under time pressure
4. **Compare to solutions** in `solutions/README.md`
5. **Focus on weak areas** and retry

### **For Python Testing:**

```bash
# Test your implementations
python3 final_sprint/practice/scenario_1/04_python_processing.py
python3 final_sprint/practice/scenario_2/04_python_processing.py
python3 final_sprint/practice/scenario_3/04_python_processing.py
```

Each Python file:
- ✅ Has runnable test framework
- ✅ Shows template with TODO sections
- ✅ Includes sample data and test cases
- ✅ Provides guidance on implementation focus

### **Meta Interview Alignment:**

| Scenario | Meta Theme | Interview Frequency | Key Skills Tested | Status |
|----------|------------|-------------------|------------------|---------|
| 1: DAU/MAU | Engagement funnel | ⭐⭐⭐⭐⭐ | Window functions, retention analysis | ✅ COMPLETE |
| 2: Reels | Short-form video | ⭐⭐⭐⭐⭐ | Time-based modeling, streaming | ✅ COMPLETE |
| 3: Ads | Monetization | ⭐⭐⭐⭐ | Attribution logic, business impact | ✅ COMPLETE |
| 4: Messaging | Share lineage | ⭐⭐⭐ | Hierarchical modeling, graph analysis | 🚧 TODO |
| 5: ETL | Data quality | ⭐⭐⭐ | Pipeline optimization, incident response | 🚧 TODO |

## 💡 Meta Success Signals

**Technical Depth:**
- Scale-aware thinking (billions of records)
- Performance optimization strategies
- Trade-off discussions

**Product Intuition:**
- Business impact understanding
- User behavior insights
- Competitive awareness

**Collaboration:**
- Clarifying questions
- Stakeholder consideration
- Clear communication

**Ownership:**
- End-to-end thinking
- Operational concerns
- Long-term maintenance

## 🎯 Current Status

✅ **3 Complete Scenarios** covering the highest-frequency Meta interview themes:
- DAU/MAU engagement analysis
- Video/content analytics
- Ads attribution and monetization

🚧 **Remaining Work**: 2 additional scenarios for complete coverage:
- Messaging/share lineage (viral content tracking)
- Data quality/ETL optimization

This gives you **3 comprehensive Meta interview practice scenarios** covering the most critical themes, with all parts complete and runnable Python challenges! Perfect for practicing the core concepts that appear in 80%+ of Meta data engineer interviews. 🚀 