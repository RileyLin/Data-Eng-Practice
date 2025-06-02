# Scenario 7: Photo Upload (Instagram/Snapchat) - Data Model

## Overview
This data model supports analytics for a photo upload feature, focusing on the upload pipeline, image characteristics, editing steps, user experience, and success/failure rates.

## Core Design Principles
1.  **Upload Event Tracking**: Detailed logging of each step in the upload process.
2.  **Image Metadata**: Capture attributes of the uploaded images (format, size, resolution, EXIF).
3.  **Editing Analytics**: Track usage of filters and editing tools.
4.  **Performance & Reliability**: Monitor upload times, success rates, and error types.
5.  **User Segmentation**: Analyze upload behavior across different user segments and device types.

## Entity Relationship Diagram

```mermaid
erDiagram
    dim_users {
        int user_key PK
        varchar user_id UK
        timestamp registration_date
        varchar user_segment "e.g., new_user, casual_uploader, power_creator"
        varchar region
    }

    dim_devices {
        int device_key PK
        varchar device_id UK "Can be a more persistent device identifier"
        varchar device_model
        varchar os_version
        varchar app_version
        varchar network_type "e.g., wifi, 4g, 5g, unknown"
    }

    dim_image_attributes {
        int image_attributes_key PK
        int original_width_px
        int original_height_px
        bigint original_size_bytes
        varchar original_format "e.g., JPEG, PNG, HEIC"
        int uploaded_width_px
        int uploaded_height_px
        bigint uploaded_size_bytes
        varchar uploaded_format
        boolean has_hdr
        varchar color_profile
        json exif_data "Key EXIF tags like camera model, ISO, shutter speed"
    }

    dim_edit_actions {
        int edit_action_key PK
        varchar action_name UK "e.g., filter_apply, crop, rotate, brightness_adj, contrast_adj, ai_enhance"
        varchar action_category "e.g., filter, adjustment, transform, ai_tool"
    }
    
    dim_upload_status {
        int upload_status_key PK
        varchar status_code UK
        varchar status_description
        boolean is_successful
        boolean is_terminal_failure
        varchar failure_category "e.g., network, server, client_validation, user_cancelled"
    }

    dim_date {
        int date_key PK
        date full_date
        int hour
        int minute
    }

    fact_photo_uploads {
        int upload_attempt_key PK
        varchar upload_session_id UK "Groups all events for one upload attempt"
        int user_key FK
        int device_key FK
        int image_attributes_key FK
        int date_key FK
        timestamp upload_start_timestamp
        timestamp upload_end_timestamp
        int duration_ms
        int final_upload_status_key FK
        int retry_count
        boolean used_background_upload
        varchar source_application "e.g., in-app_camera, gallery, external_share"
    }

    fact_upload_editing_steps {
        int upload_attempt_key FK
        int edit_action_key FK
        int sequence_order
        timestamp action_timestamp
        json action_parameters "e.g., {'filter_name': 'Clarendon', 'intensity': 0.8}, {'brightness': 15}"
        PRIMARY KEY (upload_attempt_key, edit_action_key, sequence_order)
    }
    
    fact_upload_progress_events {
        int event_key PK
        int upload_attempt_key FK
        timestamp event_timestamp
        varchar event_name "e.g., upload_initiated, chunk_uploaded, transcoding_started, transcoding_completed, server_processing_started, post_created"
        int bytes_transferred
        int current_progress_pct
        varchar event_metadata
    }

    dim_users ||--o{ fact_photo_uploads : "initiates"
    dim_devices ||--o{ fact_photo_uploads : "on_device"
    dim_image_attributes ||--o{ fact_photo_uploads : "describes_image"
    dim_upload_status ||--o{ fact_photo_uploads : "results_in_status"
    dim_date ||--o{ fact_photo_uploads : "occurs_on_date"
    
    fact_photo_uploads ||--o{ fact_upload_editing_steps : "has_editing_steps"
    dim_edit_actions ||--o{ fact_upload_editing_steps : "type_of_edit"

    fact_photo_uploads ||--o{ fact_upload_progress_events : "has_progress_events"

```

## Table Specifications

### Dimension Tables

#### `dim_users`
-   **Purpose**: User information relevant to upload behavior.
-   **Key Fields**:
    -   `user_segment`: Categorizes users based on their typical upload activity.

#### `dim_devices`
-   **Purpose**: Device and network context at the time of upload.
-   **Key Fields**:
    -   `device_id`: A unique identifier for the device, if available and privacy-compliant.
    -   `network_type`: Crucial for diagnosing network-related failures.

#### `dim_image_attributes`
-   **Purpose**: Stores detailed characteristics of the original and uploaded image.
-   **Key Fields**:
    -   `original_size_bytes`, `uploaded_size_bytes`: To track compression impact.
    -   `exif_data`: For advanced analysis (e.g., common camera models, settings associated with good/bad uploads).

#### `dim_edit_actions`
-   **Purpose**: Catalog of all available editing actions.
-   **Key Fields**:
    -   `action_name`: Specific edit performed.
    -   `action_category`: Grouping of edit actions.

#### `dim_upload_status`
-   **Purpose**: Lookup table for final status codes and descriptions of an upload attempt.
-   **Key Fields**:
    -   `is_successful`: Boolean flag for easy filtering.
    -   `failure_category`: Broad categorization for error analysis.

#### `dim_date`
-   **Purpose**: Standard date dimension, possibly with hour/minute for detailed time-of-day analysis.

### Fact Tables

#### `fact_photo_uploads`
-   **Purpose**: Core table logging each photo upload attempt.
-   **Granularity**: One record per unique upload attempt (identified by `upload_session_id`).
-   **Key Fields**:
    -   `upload_session_id`: Links all related events for a single attempt (progress, edits).
    -   `duration_ms`: Total time taken for the upload attempt.
    -   `final_upload_status_key`: Foreign key to `dim_upload_status`.
    -   `retry_count`: Number of retries for this attempt.
    -   `source_application`: Where the upload originated from.

#### `fact_upload_editing_steps`
-   **Purpose**: Records each editing action applied to a photo during an upload session.
-   **Granularity**: One record per edit action per upload attempt.
-   **Key Fields**:
    -   `upload_attempt_key`, `edit_action_key`: Composite primary key with `sequence_order`.
    -   `sequence_order`: Order in which edits were applied.
    -   `action_parameters`: JSON field to store specific parameters of the edit (e.g., filter name, adjustment value).

#### `fact_upload_progress_events`
-   **Purpose**: Logs key milestones or events during the lifecycle of an upload attempt.
-   **Granularity**: One record per progress event within an upload attempt.
-   **Key Fields**:
    -   `event_name`: Specific milestone (e.g., `chunk_uploaded`, `transcoding_completed`).
    -   `bytes_transferred`, `current_progress_pct`: For detailed progress tracking.

## Key Business Rules & Considerations

1.  **Upload Session**: An `upload_session_id` in `fact_photo_uploads` ties together all events, edits, and final status for a single attempt to upload one or more photos (if part of a batch/carousel, though this model focuses on single photo for simplicity, can be extended).
2.  **Retry Logic**: `retry_count` helps analyze resilience.
3.  **Editing Granularity**: `fact_upload_editing_steps` allows analysis of popular tools, common sequences, and time spent on editing.
4.  **Failure Analysis**: `dim_upload_status.failure_category` combined with `dim_devices.network_type` and `dim_image_attributes` helps pinpoint causes of failures.

## Analytics Use Cases
-   **Upload Success Rate Analysis**: By device, OS, app version, network type, region, image size/format.
-   **Upload Funnel Analysis**: Identify drop-off points using `fact_upload_progress_events` (e.g., from selection to editing to final upload).
-   **Editing Tool Popularity**: Which filters or adjustments are most used? Which lead to higher engagement post-upload?
-   **Impact of Image Characteristics**: Do large images or specific formats have higher failure rates?
-   **Performance Monitoring**: Track average upload times, time spent in editing vs. actual upload.
-   **Error Diagnostics**: Correlate error types with device/network conditions.
-   **A/B Testing**: Measure impact of new upload features (e.g., new compression algorithm, UI changes in editing flow) on success rates and times.

## Implementation Notes
-   `fact_upload_progress_events` can be very high volume; consider sampling or TTL policies if full logging is too expensive.
-   `exif_data` and `action_parameters` in JSON format provide flexibility but require appropriate query capabilities.
-   Client-side logging needs to be robust to capture these detailed events accurately. 