# Interview Preparation Repository

This repository is structured to help you systematically prepare for technical interviews in data science, data engineering, and product analytics roles. It contains a comprehensive set of challenges organized by scenario with reference documentation and a structured approach for solving each problem.

## Repository Structure

```
├─ README.md                 ← Overview + study cadence
├─ docs/                     ← Reference content (read-only)
│   ├─ general_interview_notes.md
│   ├─ behavioral_questions.md
│   ├─ product_sense.md
│   ├─ data_modeling.md
│   ├─ sql_questions.md
│   └─ python_questions.md
├─ notebooks/                ← Quick scratch space (optional, Jupyter)
├─ src/                      ← Your answers & code
│   ├─ python/               ← Python challenges
│   │   ├─ q001_ride_overlapping.py
│   │   ├─ q002_carpool_capacity.py
│   │   └─ ...                ← 1 file per question
│   ├─ sql/                  ← SQL challenges
│   │   ├─ q001_carpool_segment_percentage.sql
│   │   └─ ...
│   └─ data_models/          ← Data modeling challenges
│       ├─ q001_rideshare_schema.mmd  ← Mermaid ERD
│       └─ ...
└─ tests/                    ← Tests for your implementations
    ├─ python/
    └─ sql/
```

## Scenarios

The challenges are organized by the following scenarios, each representing a realistic product domain:

1. **Ride Sharing (Uber/Lyft)** - Carpooling Feature
2. **Short Video (TikTok/Reels)** - Sharing Focus
3. **Streaming Platform (Netflix/Hulu)**
4. **Cloud File Storage (Dropbox/Google Drive)**
5. **DAU/MAU Analysis**
6. **News Feed**
7. **Photo Upload (Instagram-like)**
8. **FB Messenger**
9. **Food Delivery (DoorDash)** - Order Batching

## Question Types

Each scenario includes a mix of:
- **Product Sense Questions**: Metrics definition, success measurement, dashboard design
- **Data Modeling Challenges**: Schema design, efficiency considerations, trade-offs
- **SQL Problems**: Data analysis, aggregation, window functions, complex joins
- **Python Challenges**: Algorithmic problems, data processing, stream handling

## Study Plan

### Step 1: Review the General Guidelines
- Review the general interview notes in `docs/general_interview_notes.md`
- Study the example behavioral question responses in `docs/behavioral_questions.md`

### Step 2: Practice by Scenario
For each scenario:
1. Read the product sense questions and formulate answers (practice articulating them verbally)
2. Attempt the data modeling challenge, drawing out your solution using Mermaid syntax
3. Solve the SQL problems, testing them with sample data when possible
4. Implement the Python challenges and run the provided tests

### Step 3: Timed Practice
- Once comfortable with individual problems, practice solving them under time pressure
- Aim to complete SQL/Python questions in under 8 minutes for initial screening level
- Practice explaining your thought process as you work through solutions

### Step 4: Mock Interviews
- Use these problems for mock interviews with peers or mentors
- Focus on clear communication of your thought process

## Working with This Repository

### Python Challenges
Each Python challenge is in its own file in `src/python/` with:
- A clear problem description
- Function signature to implement
- Examples with expected inputs and outputs
- Test cases to validate your solution

Run a challenge file directly to test your implementation:
```bash
python src/python/q001_ride_overlapping.py
```

### SQL Challenges
SQL challenges are in the `src/sql/` directory:
- Each file contains a problem description and schema details
- Write your SQL solution in the file
- Test with a database when possible (SQLite is recommended for quick testing)

### Data Modeling
Data modeling challenges use Mermaid syntax for Entity-Relationship Diagrams:
- Create your solutions in the `src/data_models/` directory
- Use the `.mmd` extension for Mermaid diagrams
- Visualize diagrams using the Mermaid Live Editor or compatible IDE plugins

## Getting Started

1. Clone this repository
2. Set up a Python virtual environment:
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start with the first scenario in each category and work your way through systematically

## Utility Scripts

The repository includes several utility scripts to help you manage and test your solutions:

### Run Tests

The `run_tests.py` script discovers and runs all the Python tests in the repository:

```bash
# Run all tests
python run_tests.py

# Run a specific test file
python run_tests.py tests/python/test_ride_overlapping.py
```

### Create New Challenges

The `create_challenge.py` script helps create template files for new challenges:

```bash
# Create a new Python challenge
python create_challenge.py python 12 --function calculate_metric --args "data, threshold=0.5"

# Create a new SQL challenge
python create_challenge.py sql 5 --description "Calculate User Growth Rate"

# Create a new data model
python create_challenge.py datamodel 4 --model-name messaging_system
```

## Focus Areas

- **Product Sense**: Practice framing metrics, explaining trade-offs, and designing dashboard visualizations
- **Data Modeling**: Focus on understanding entity relationships, normalization, and performance considerations
- **SQL**: Master GROUP BY, HAVING, window functions, subqueries, and CASE statements
- **Python**: Practice working with dictionaries, lists, string manipulation, and stream processing

Good luck with your interview preparation! 