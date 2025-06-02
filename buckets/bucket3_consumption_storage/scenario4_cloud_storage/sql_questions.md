# SQL Questions for Cloud Storage (Dropbox/Google Drive)

Based on the data model defined in `data_modeling.md`, here are SQL questions to analyze cloud storage usage, collaboration, and file management.

1.  **User Storage Quota Utilization**:
    *   Write a query to list users who have used more than 90% of their allocated storage quota. Include their account type, total quota, used storage, and percentage used. Order by percentage used (descending).

2.  **File Type Distribution and Storage**:
    *   Write a query to show the total number of files and total storage consumed (in GB) for each file type (e.g., pdf, docx, jpg, mp4), broken down by user account type. Order by account type and then by total storage consumed (descending).

3.  **Most Active Collaborators**:
    *   Write a query to identify the top 10 users who have performed the most collaboration activities (e.g., comments, adding users to shares) in the last 30 days. Show the user ID, user name, and total number of collaboration events.

4.  **Orphaned Files Identification**:
    *   Assuming an "orphaned file" is a file whose owner's account is inactive (e.g., `last_login_date` is older than 1 year) or the owner `user_id` no longer exists in `dim_users` (if possible due to data integrity issues). Write a query to find all such orphaned files, including their size and last modified date.

5.  **Sharing Activity Analysis**:
    *   Write a query to analyze sharing activity for the past month. Show:
        *   Total number of items (files/folders) shared.
        *   Number of unique users who shared items.
        *   Number of unique users with whom items were shared.
        *   Most common permission level granted.
        *   Breakdown of shares by `link_type` (e.g., 'public_view', 'company_edit').

6.  **Folder Collaboration Intensity**:
    *   Write a query to identify folders with high collaboration intensity. This could be defined as folders with more than 5 unique collaborators (excluding the owner) and at least 10 collaboration events (comments, file additions/modifications within the folder tracked via `fact_file_activity` where `parent_folder_id` is the folder in question) in the last month. List folder name, owner name, number of unique collaborators, and number of collaboration events.

## Source Table Assumptions for Queries:

*   `dim_users`
*   `dim_files`
*   `dim_folders`
*   `dim_permissions`
*   `dim_collaboration_event_types`
*   `dim_dates`
*   `fact_storage_consumption`
*   `fact_file_activity`
*   `fact_sharing_collaboration`

These questions aim to test understanding of joins, aggregations, window functions (potentially), date manipulations, and subqueries in a cloud storage context. 