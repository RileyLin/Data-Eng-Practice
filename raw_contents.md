https://www.1point3acres.com/bbs/thread-1089339-1-1.html

vo uber reel netflix

1. uber/doordash + DAU + Photo Upload
2. Dropbox + Newsfeed + Messenger

https://www.1point3acres.com/bbs/thread-1117388-1-1.html

BQ：
对DE的了解，和SDE，DS的区别
如何priority task，如何处理conflict
data driven result 对business process的impact
基本下面这个帖子都包括了，但会有一些followup 如果signal没有收集到。
🔗 [www.1point3acres.com](http://www.1point3acres.com/)
第一轮 ride sharing 
如何track carpool的performance 的metrics，如何slice and dice dimensions
data model需要考虑fact table可以同时有carpool和regular rides
sql 会提供几个表和sample data，计算carpool占比
python是类似meeting room，问是不是所有ride booking [{start time, end time, number_passenger}]都能complete
第二轮 short video
同样什么样的metrics track performance，有问选一个metric画成什么样的图
Data model focus on engagement有追问如何改model可以找到是从哪儿share到，我给的是加一个shared_by 用engagement_id
Sql 同一天有likes但是没有comments的post，用的是not in。基本都是group by case，尽量写一个select，减少用cte
Python 和下面帖子的很类似，需要用buffer，算total engagement 然后print，有一个条件是如果是internal test的话，考虑buffer 但不考虑计算
🔗 [www.1point3acres.com](http://www.1point3acres.com/)
第三轮 streaming platform
问哪些engagement type，和哪些metrics，会追问还有没有其他可以measure的，从platform，user，video分开讨论
design一个data model可以用来写上面所有的metrics。细节问到如何算duration(end time - start time - pause time)，tradeoff是否要加multiple row when consider pause， 如何算is_complete.
sql考的是batch process，如何update cumulative snapshot，先算today的，然后和snapshot表进行full out join，注意coalesce细节
Python 考的是list of dicts 电影，分类，评分，输出分类和平均分，我用的是list然后算平均，followup问题是如果数据量很大如何优化，结论可以用dict存储总分和cnt

Python：
给你一个number，return odd组成的最小number。1234-->13 （edge case：negative（-23），偶数（24，0--》 none））
most frequency comment of book store (注：remove duplicates）dic1 = {'nyc': ['perfect', 'perfect', 'briliant', 'love it!'], 'london':['gorgerous'，'briliant'], 'berlin':['awful']} --- result：briliant
求连续两年最多的class number courses = [
    ('chemistry', 4, 2010, 2014),
    ('math', 2, 2008, 2012)
    ]--》res：12
SQL：
book transaction customer author
total books and unique customer per payment
顾客可以invite其他顾客，找top 5 邀请别的顾客的average payment per book --》不是avg（payment）是sum(payment)/sum(book_count) --> I struggle a bit.
全部author的数量，author的url符合某个pattern的比例，没有卖出去过书的author的比例。
总体简单，但是我的面试官欧洲口音贼重，10个词我就能听懂2，3个，且气质抽象，都是靠着面经过的，所以一定要把面经闭着眼写出来的程度。但是又得有思考的过程。

Python:
Smallest Odd : Create the smallest odd number from an integer
Most Frequent Theme: From a dictionary of book themes, Find the most common theme
Consecutive Year Classes: Given courses. Determine the maximum number of classes held in two consecutive years.
Bookshelf Fit: Given two list books and shelve, check if all books can fit into the shelves.
Friendship Matrix: Calculate how many people see a post after N reposts based on a friendship matrix.
SQL:
What percentage of products are both low-fat and recyclable?
What are the top five single-channel media types based on promotional spending?
For sales with valid promotions, what percentage of transactions occur on the first or last day of the campaign?
Show total units sold for each product family and the ratio of promoted to non-promoted sales, sorted by total units sold.

Rice please :)

- Data Modeling
o Version 01 - Ride Sharing Company (Uber/Lyft)
 15-20 mins product sense discussion:
e.g. 如何扩大市场占有率/How to do mkt expansion
 20-30 mins data modeling discussion – fact table(s) & dimension tables shall be able to relevant to the product sense
 5-10 mins on SQL query – 1-2 queries:
e.g. 计算只用这个app去机场的人
o Version 02 - Cloud File Storage Company (Dropbox/Google Drive)
 15-20 mins product sense discussion:
e.g. How to evaluate whether the product is success (name some classical metrics and start the discussion)
 20-30 mins data modeling discussion – fact table(s) & dimension tables shall be able to relevant to the product sense
• 有的人被追问到如果这个file是share among multiple people的应该如何考虑建表 (我觉得可以建两个fact tables – 一个是专门记录upload/download 另一个是专门记录shared assets)
• 有的人被追问如何记录file ownership transfer – 我觉得问题还是上面的那个关于share activity的问题
 5-10 mins on SQL query – 1-2 queries:
e.g. 找出只上传照片的人|Find one how many files (storage assets) have multiple owners
- Tech 01
o Version 01 – DAU/MAU (这一轮的case study普遍就是围绕DAU/MAU展开的 也没有disclose太多具体的公司背景)
 Product sense 部分普遍被问到的是如果DAU/MAU突然drop了很多 分析一下可能会是什么原因
 SQL – 会提供table 的schema 但是不会给实际的数据 等于说是”忙写” – 意思是写好了也不用run 但是基本上面试官肯定知道什么是对的什么是错的
e.g.:
• 数据包含N天的登录情况 – 要求计算手机登录的用户和所有用户的数量(AU/N by Phone and AU/N)
• Think about how to design a series of ETL process – how to capture new users/ retained users/ churn users
• Calc DAU by different categories (我估计是DAU group by platforms/devices)
o Version 02 – News Feed
 Product sense – how to evaluate whether users have viewed a post – 需要一些讨论 – 怎么判断用户是否有效阅读了一个post的内容 (最后有的会被drive到可以讨论所谓的 占屏比 – 如果一个post 占屏比达到了x% threshold, 那么就是算作有效阅读)
 SQL & Python
• 分别用SQL和Python来算每一个session里面的对应的post的有效阅读的次数
有些细节的东西需要确认 – 如果一个post下面的有log显示同一个session_id多次- 可能表明这个post被多次阅读了 那么可以考虑取第一次的为准 或者可以考虑取平均值
关于schema 有好几个版本 不过可能大差不差
(表大概是session_id, post_id, start_timestamp, end_timestamp, read_percent)
(Table schema – session id, post id, time_stamp, event_type, percentage 其中event type有start time 和 end time) 实际上这两个表是差不多的
[这个而感觉是比较可信的: Sql-求出这个session中的post（每个post都会对应好几条start 和 end time）是不是有效阅读 （threshold 是5秒和80%屏占比都属于有效阅读）- 这题是需要逐条post evaluate，如果其中一条是有效阅读就算是有效阅读。这个sql的重点考察的是怎么把start time 和 end time align到一起，这个写出来了，后面都简单了]
(要把上面的表的timestamp变成start and end timestamp align到一起window function应该是比较直观的解法 如果数据比较大可能只能通过join来解 但是写起来估计会麻烦点 这两天我会看看有没有更合适的解法)
• Python就是伪streaming 上面SQL的内容 然后每个session_id会有个对应的session end signal
o (感觉就是按照session -> post – validate_whther_in_threshold() -> update dictionary)
- Tech 02
o Version 01- Photo Upload (有点像Instagram)
 Product sense 普遍反应是讨论照片上传流程的process time
 SQL & Python:
• SQL – 计算average time taken
• Python coding – 跟SQL是一样的 但是这里是要求实现伪streaming process – 给一个log file – process data line by line – 计算metrics – average time taken
 Dashboard – data visualization – 基本上就是简单介绍一些准备怎么可视化数据 – 说明白横轴纵轴以及需要visualize的metrics即可
o Version 02 – FB Messenger
 product sense – DAU/MAU – 发现DAU/MAU 人数下降了 可能会有哪些因素导致的
 SQL and Python
• SQL: 给一个log表，求每个用户在一天里sign in过几次，发了多少条message，first sign in date，从first sign in date开始一共发过多少条message，今天是不是active
(log好像有user_id,date,send_on_ios,send_on_android)
• Python: 给几个表，用python写出SQL statements每天更新这几个表
(给表A，表B，表C 表C是SELECT col1, col2 FROM A WHERE condition1 UNION ALL SELECT col3, col4 FROM B WHERE condition2 – 感觉是给了table 然后用python form SQL and insert into DB – 注意SQL injection)
(python的表和log差不多，就是log by different metrics，和device，platform，location相关的data)
(所有的python题都不需要用到pandas，简单点说就是给你几个sql表你用python写一个string，string的内容是”insert into table……”)

Overview

1. ETL Interview 1: Real-time stream system (1 hr)
2. Data modeling (1 hr)
3. ETL Interview 2: Batch system
4. Behavioral and ownership
All the technical ETL design, assume big data context
Main qualities Interviewers look for
Code needs to be written but it will not get tested throughout the interview
5. Python
6. SQL (Postgres)
7. Product sense
8. Data modeling
9. ETL
10. Data visualization (more on data presentation --> will appear in stream system ETL question)
Interview 1: ETL in Real time stream system (Photo upload stream process)
Focus on designing important metrics and E2E ETL process
Q1: (a product sense question) What metrics would you use to evaluate if a feature in the photo upload application is effective or not? What data would you collect? --> Photo upload APP?
Q2: On a high level, design the schema/columns for data modeling for both the source data and the target (output) data.
Q3: The schema of the table will be provided. A set of SQL/ python questions will be asked to answer some questions. --> It will be mainly focused on how to build ETL from source to target and transforming the data
11. Given the schema :
session_id Action timestamp
1 login 2021-11-29:00:02:01
1 click on post 2021-11-29:01:03:03
2 upload photos 2021-11-29:01:12:01
3 tag friends 2021-11-29:02:38:15
3 tag friends 2021-11-29:03:02:01
Find the average time taken between each steps/actions above. For duplicate actions (upload photo again, use the first upload photo time)
SELECT * , DATEDIFF(minutes, lag(timestamp) over (PARTITION BY user_id order by timestamp), timestamp) as inactivity_time
FROM events
12. Code question: same as above sql question, but input data like below [session_id, action/step_id, start_ts].
Table for login session_id A：
starttime：10:00 ， upload photo
Start time: 10:04, tag friends on photos
Start time: 10:05, upload photo
Start time: 10:07, add messages
Start time: 10: 09, post photos (完成了）
session_ID B （另外一个人），做类似的actions。平均每个action 多长？
Compute and update the running new average time spent on each step for every new stream of data coming into the system, assuming infinite amount of memory space
Interview 2: Data modeling (Doordash/Uber --> ride share related product)
Key design guidelines:
• Scalability
• Maintainability
• Normalization/Denormalization
• Performance
Q1: (a product sense question related to the product)
Q2: Create your own data mart, the data dimension tables to analyze the product (Star schema is highly preferred)
Q3: Query based on the schema you've created previously to find out some metrics
1. Calculate all the drivers who departed or reached to the airport as the destination
13. Calculate all the customers who only departed or reached to the airport as the destination. The customers who have been to other destinations don't count
14. Discuss the parts in the table design that could have been improved
Interview 3: ETL in Batch system (Related to Meta quarterly results)
Question 1: a product sense question related to DAU, MAU
Question 2: Query to find the status/count/number of different metrics given a table with new users, retention users and timestamps in it
15. Find the daily new user: 🔗 [leetcode.com](http://leetcode.com/)
16. SQL question. Given table: user_id, last_login_time, prev_login_before_last_login a. Find: yesterday's DAU, last 7 days, last 28 days b. Find continuous user, returning user and churned users
17. Users have more than one devices, last 7 days login (1 = login with that device; 0 means didn't login with that device)
details = {'iPhone':[0, 1,0,1,0,1,0] ,'Android':[1, 0,0,0,0,0,1] ,'Web':[0, 0,1,0,0,0,0]}
rollups= {'overall':['iphone', 'Android', 'Web'] ,'Mobile':['iPhone', 'Android']}
Question: find last 7 days for overall , mobile, etc
Return:
{ “overall” : [1,1,1,0,1,1,1] “Mobile”: [1, 0,0,0,0,0,1]
Interview 4: Behavioral (Follow the STAR framework)
18. What draws you to Meta DE?
19. What is DE?
20. Projects you've worked on --> try to relate the experience to the FB products
21. Leadership questions a. Describe a time when you complete a project from end to end b. What have you done in a cross functional, collaborative environment c. What is the impact of your projects? d. What trade offs did you have to make e. What characteristics and attributes do you think is important as a leader
22. Questions about autonomy/ prioritization
23. Describe a situation where you influenced/or being influenced by others using data
24. How do you handle conflict?
25. How do you plan to succeed in FB in the first year

SQL: 书店

1. 销量和数量by payment type
2. 顾客可以invite其他顾客，找top 3 邀请别的顾客的average payment。
3. 全部author的数量，author的url符合某个pattern的比例，没有卖出去过书的author的比例。
Python:
4. 找一个int中可以用奇数组成的最小的int。
5. 给一个书店的dictionary，找到最多的评论。
6. 经典开会题。找到连续两届参加最多的人。
7. 书的厚度和书架厚度的fit

VO
以下内容需要积分高于 188 您已经可以浏览
因为我之前面过一次这个职位了，所以我的题目和常见的不太一样，但是本质都差不多
1st ETL
FB messenger
Product sense: 发现sign in的人数突然下降，问可能有哪些原因
SQL: 给一个log表，求每个用户在一天里sign in过几次，发了多少条message，first sign in date，从first sign in date开始一共发过多少条message，今天是不是active
Python: 给几个表，用python写出SQL statements每天更新这几个表
2nd ETL
FB news feed
Product sense: 怎么判断用户是不是有效阅读了一个post
SQL: 给一个log表，求每个session里的每个post有几个有效阅读
Python: 把SQL的问题用python写一遍
Data Model
FB box (类似于dropbox)
Product sense： 怎么判断产品是否成功
设计schema做分析
SQL只写了一道，选出所有只上传过照片的用户
Ownership
纯BQ，聊天
自己觉得面得不好是因为第二轮ETL的时候信号不好听不清，一直在重复问题，感觉对方有点不耐烦，弄得我也很紧张，product sense答得乱七八糟。而且data model前面说得太多导致最后没时间只做了一道SQL题，设计的schema也没有完全解决问题，一直被追问细节，内心很崩溃。
不过从结果来看似乎也没有我自己想象的那么糟糕。我的经验就是不会不要紧张，要一直说自己的想法，data model那一轮我被问到答不上来的时候就会说虽然我不知道能不能解决这个问题，但我想到的方案有1，2，3，肯定比直接冷场要好一些。

[structured study guide](https://www.notion.so/structured-study-guide-1cfeec220fb58057b3f6f4c1c5e07633?pvs=21)

[HR Interview questions](https://www.notion.so/HR-Interview-questions-1d1eec220fb5805cb680f01d92230052?pvs=21)

[7 day challenge](https://www.notion.so/7-day-challenge-1d3eec220fb58060b008edba6d44528f?pvs=21)

[Playground](https://www.notion.so/Playground-1d3eec220fb5809a8f4ee71b5fd14e85?pvs=21)

---

---

---

---

carpool：

SQL：
percentage
(drivers(distinct) who take carpool more than regularly )/ total drivers

Python:
if more than capacity (default 6) return False

Newsfeed(reels):

PS:
How to track if a user moves from their regular location to a new location?
Compare the likes of original content and the likes of content that is shared from the original.

DM:
Visualization: show how the reels’ launching affects other functions (posts, pictures and long videos)

SQL:
(Content created today, which has type “reaction” but no “comment”)/total content created today

Python：用（deque）
Use buffer store element (default =3), if test then add to buffer but not aggregation and print
left(oldest) out ,right(new) in
aggregation: 1. total engagement, 2. total views ( ms/1000 to s)
post_id use “, ”.join to string

streaming（Netflix）:

SQL：
Use outer join + coalesce to merge today’s snapshot with the current table, aggregating total view time.
(要求：1. 不要scan全表，2.用select syntax）
gourd by， 给了两个表和数据，一个是watch_fact，一个是session_dim,。只用到fact表，group by content_id count(distinct user),sum(total time)

Python:
每个电影的平均rating.

---

---

---

本帖最后由 andy3545 于 2025-2-13 12:23 编辑

Onsite Interviews:

Very similar to this post.

Behavioral Round (Indian Interviewer)
Interviewed by an Indian manager, very friendly.
Be prepared for follow-up questions—they ask follow up questions if your answer does not give signals they're looking for. Check out this blog for different signals.
What does data engineering mean to you?
Using data to make an impact or convince others
Leading projects and their impact
How do you plan to succeed at Meta?
Prioritizing competing tasks—any frameworks/tools?
A time when you were wrong—how did you handle it?

Full Stack 1 (Chinese Interviewer):
Scenario: Video Streaming Platform (like Netflix), focused on user engagement.
SQL (2 Questions): Update a daily aggregate table from a user activity fact table.
Python (2 Questions): Given a list of movies and categories, map movies to categories and return top 3 movies per category.

Full Stack 2 (Mexican Interviewer)
Scenario: Ride-sharing company introducing a carpooling feature.
Discuss value proposition and Meta’s mission alignment.
Data Modeling: Support rides with multiple riders (IMPORTANT!)
SQL (3 Questions): Very easy.
Python (1 Question): Similar to Leetcode’s Meeting Rooms question—determine if all rides can be completed.
Bonus ML Question: Finished early, so I got a machine learning question, which I solved.

Full Stack 3 (Indian Interviewer)
Scenario: Facebook adding short-form videos (Reels).
Data Modeling: Handle posts shared 10,000+ times (Hint: Use an array to store shares).
SQL (2 Questions): Identify posts with zero likes/reacts on the day they were posted.
Python (1 Question): Process a stream of input data (list of dictionaries), checking conditions, buffering output, and handling edge cases.

Key Takeaways

Questions are straightforward, but speed is critical—you can’t afford to get stuck.
Interviewers help you succeed—they give hints if needed, but explain your thought process.
Receiving hints isn’t bad—responding to them well shows learnings abilities, a key hiring signal.
Utilize the information your recruiter provides—they often share valuable information and even similar questions that may appear in the interview.
Data Modeling – Since we're assuming a dataset with billions of records, bonus points for discussing data partitioning strategies and optimizing dashboards by reading from a daily aggregated table instead of the raw fact table.

Best of Luck. 加油!!

补充内容 (2025-02-14 22:25 +08:00):

Data Modeling: Handle posts shared 10,000+ times (Hint: Use an array to store shares).

Standard newsfeed data model, but the follow up question was "How does your data model handle multiple layers of sharing, and efficietly count how many shares each post has and who the original poster and posted time is?"

For example:
user_1 shares, then user_2 sees user_1's post and shares, this is considered 2 layers of sharing.
Imaginge there is 1000+ layers

---

---

—

脸书DATA ENGINEER 面经及总结 [🔗 www.1point3acres.com](https://www.1point3acres.com/bbs/thread-601367-1-1.html)
买它onsite data eng 回报社会  [🔗 www.1point3acres.com](https://www.1point3acres.com/bbs/thread-850462-1-1.html)
Meta DE Phone + Onsite 面经 - Orz  [🔗 www.1point3acres.com](https://www.1point3acres.com/bbs/thread-817312-1-1.html)
FB DE 电面 VO  [🔗 www.1point3acres.com](https://www.1point3acres.com/bbs/thread-629763-1-1.html)

VO还是可以参考上面帖子中的题目，面试时可能会出现不同的Use Case和feature。下面我分享我遇到的题目和场景。

第一轮： Ride Sharing Company。最近加了一个Carpool的功能，如果判断成功与否，需要哪些Metrics， data modeling design，然后 SQL + Python。 SQL 题目已经忘了，只记得一道题目用到了 sub-query。
Python 题目：input 是 a list of bookings（dictionary）。判断是否所有订单可以通过Carpool完成。

第二轮： Video Streaming Company （like Netflix）。 SQL 考了 batch processing。就是如何update， 我最后用的Merge。Python题目忘记了，只记得用了 nested loop + if check conditions。
可能这一轮太顺了，没留下太多印象。面试官也很给力，交流很顺利。

第三轮： Newsfeed。 最近加了一个short Video的功能，判断这个功能对newsfeed的影响。套路一样，还是需要哪些Metrics， data modeling design，还问dashboard 如何设计。
这一轮我面的真是乱七八糟。SQL题目忘记了，只记用到 Count - Count （reverse thinking），就这面试官愣是不明白，花了10分钟解释，最后说你好像做的对的。

Python很有意思，大概是这样的

Write a python function to take an input of stream data (list of dictionaries) and then print it out following some string format.

Inside the function, You need to create a buffer with certain size to take the input before print ,which means the print only gets executed after buffer is full and then repeat the process to print out all the steam data.

最后祝大家面试顺利，Meta给的准备时间我觉得是够的，把面经和基础弄熟，相信自己，冷静专注，你定会手起刀落，力斩Offer。

---

---

从接到recruiter反馈到现在两周，总算整理好心情来一波挂经
先求个米，需要安慰
感谢：
帮助过我的朋友们，特别特别是那位已经顺利拿到offer的大佬，不仅无私的分享经验，还全程陪我走完面试流程，可惜很遗憾没能一起加入meta做战友。
建议：
如果面试官确定是印，能避开就避开，千万别学我头铁，连中3元。
迟到，拖时间。
DM面试时各种问题，也给正反馈，然后hc时给差评
SQL只出一题就跳到python去，反手sql差评。
Python不读完题不让你开始做等
以下面经
题还是老题,有回忆起新的会来添加

carpool：

SQL：
percentage
(drivers(distinct) who take carpool more than regularly )/ total drivers

Python:
if more than capacity (default 6) return False

Newsfeed(reels):

PS:
How to track if a user moves from their regular location to a new location?
Compare the likes of original content and the likes of content that is shared from the original.

DM:
Visualization: show how the reels’ launching affects other functions (posts, pictures and long videos)

SQL:
(Content created today, which has type “reaction” but no “comment”)/total content created today

Python：用（deque）
Use buffer store element (default =3), if test then add to buffer but not aggregation and print
left(oldest) out ,right(new) in
aggregation: 1. total engagement, 2. total views ( ms/1000 to s)
post_id use “, ”.join to string

streaming（Netflix）:

SQL：
Use outer join + coalesce to merge today’s snapshot with the current table, aggregating total view time.
(要求：1. 不要scan全表，2.用select syntax）
gourd by， 给了两个表和数据，一个是watch_fact，一个是session_dim,。只用到fact表，group by content_id count(distinct user),sum(total time)

Python:
每个电影的平均rating.

comp -

E4

16w

15% perf bonus

14w rsu 4 years

---

---

Bay area E4

188000

15% year end bonus

273000 RSU

sign on bonus 30k 

---

|  | **Level NameTag** | **Years of ExperienceTotal / At Company** | **Total Compensation (USD)Base | Stock (yr) | Bonus** |
| --- | --- | --- | --- |
|  | **IC4**Data | **5 yrs**0 yrs | [**+$27K**](https://www.levels.fyi/services/?from=compensation_table)
**$262,100**179K | 51.3K | 31.9K |

[Key concepts](https://www.notion.so/Key-concepts-1e3eec220fb5805c975bf6413202bb19?pvs=21)

[GPT Study Guide](https://www.notion.so/GPT-Study-Guide-1e5eec220fb580f2bd0cef96d97f9594?pvs=21)

[Product Sense, SQL & Behavioral Interview Prep (Reformatted)](https://www.notion.so/Product-Sense-SQL-Behavioral-Interview-Prep-Reformatted-1eaeec220fb58000bc78f997e144c83c?pvs=21)

[Product & SQL Interview Prep Solutions.wav](attachment:8a8ee3ae-ce03-4d25-af39-f01896fff011:Product__SQL_Interview_Prep_Solutions.wav)

[Behavioral Interview 1](https://www.notion.so/Behavioral-Interview-1-1eeeec220fb580d0a941c1c59a143c26?pvs=21)

[Behavioral Interview - Product Minded](https://www.notion.so/Behavioral-Interview-Product-Minded-1eeeec220fb58083b4d0e11b5c3639ed?pvs=21)

based on the latest version of document - generate a challenge document named 5-15-Carpool Challenge for me on the carpool-doordash questions in the same format with all the answers at the end including sql and python scripts - make sure to base your questions and answers on the existing contents of the document and the additional contents that I provided here: carpool：

[Meta Data Engineering Guideline Summary](https://www.notion.so/Meta-Data-Engineering-Guideline-Summary-1f5eec220fb580848907c5224ca166c1?pvs=21)