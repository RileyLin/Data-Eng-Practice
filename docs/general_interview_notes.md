# General Interview Notes

This document contains general advice and tips for technical interviews.

## Key Points to Remember

- **Speed is Critical**: Questions might be straightforward, but you need to work through them efficiently. Don't get stuck. Aim for max 8 minutes per SQL/Python question in initial screens.

- **Explain Your Thought Process**: Clearly articulate your reasoning, assumptions, and trade-offs, especially in data modeling and product sense questions.

- **Hints are Okay**: Interviewers often provide hints if you're stuck. Listen carefully and show you can incorporate feedback – this demonstrates learning ability, a key hiring signal.

- **Data Scale**: Assume datasets are large (billions of records). Mentioning data partitioning (e.g., by date on fact tables) and optimizing dashboards by reading from pre-aggregated daily/hourly tables instead of raw fact tables can earn bonus points.

- **Follow-up Questions**: Expect "why" and "how" follow-ups. Interviewers probe for depth and specific signals (ownership, impact, technical depth, collaboration). Be prepared to elaborate.

- **Bonus Questions**: If you finish early, you might get an additional question, potentially including ML concepts depending on the role/interviewer.

## Technical Fundamentals

### SQL Fundamentals

Be solid on:
- GROUP BY, HAVING
- Sub-queries
- Window functions (SUM() OVER, ROW_NUMBER(), etc.)
- CASE statements (e.g., SUM(CASE WHEN ...))
- Self-joins

### Python Fundamentals

Master:
- Lists, strings, tuples, dictionaries
- Common operations/methods
- Data manipulation and transformation
- Algorithm efficiency and optimization 