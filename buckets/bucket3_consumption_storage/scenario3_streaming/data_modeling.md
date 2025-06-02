# Scenario 3: Streaming (Netflix/YouTube) - Data Model

## Overview
This data model supports a video streaming service, focusing on users, content catalog (movies, series, episodes), user interactions (viewing history, ratings, watchlists), and elements to support personalized recommendations.

## Core Design Principles
1.  **Content Hierarchy**: Clearly define relationships between series, seasons, and episodes.
2.  **User Interaction Tracking**: Capture detailed viewing patterns, ratings, and list management.
3.  **Recommendation Support**: Include entities and attributes that can feed into recommendation algorithms (e.g., genres, tags, user behavior).
4.  **Scalability**: Design for a large catalog and extensive user interaction data.
5.  **Flexibility**: Allow for diverse content types and metadata.

## Entity Relationship Diagram

```mermaid
erDiagram
    dim_users {
        int user_key PK
        varchar user_id UK
        varchar user_name
        timestamp registration_date
        varchar region
        varchar subscription_tier "e.g., basic, standard, premium"
        json user_preferences "e.g., preferred_genres, parental_control_settings"
        timestamp last_login_timestamp
    }

    dim_content {
        int content_key PK
        varchar content_id UK
        varchar title
        text description
        varchar content_type "movie, series, episode, short_clip, trailer"
        int series_key FK "Null if not an episode or part of a series"
        int season_number "For episodes"
        int episode_number "For episodes"
        int duration_seconds
        date release_date
        varchar maturity_rating "e.g., PG-13, TV-MA"
        varchar primary_language
        json production_details "e.g., {director: 'X', studio: 'Y'}"
        varchar thumbnail_url
        varchar streaming_url
    }

    dim_genres {
        int genre_key PK
        varchar genre_name UK
    }

    dim_tags {
        int tag_key PK
        varchar tag_name UK "e.g., suspense, feel-good, critically-acclaimed"
    }
    
    dim_cast_crew {
        int person_key PK
        varchar person_name UK
        varchar person_role "actor, director, writer" -- Could be a separate dim_roles if complex
    }

    dim_date {
        int date_key PK
        date full_date
        int year
        int month
        int day_of_week
        boolean is_weekend
    }

    fact_content_genres {
        int content_key FK
        int genre_key FK
        PRIMARY KEY (content_key, genre_key)
    }

    fact_content_tags {
        int content_key FK
        int tag_key FK
        PRIMARY KEY (content_key, tag_key)
    }
    
    fact_content_cast_crew {
        int content_key FK
        int person_key FK
        varchar specific_role "e.g., Lead Actor, Supporting Actor, Episode Director"
        PRIMARY KEY (content_key, person_key, specific_role)
    }

    fact_viewing_history {
        int view_key PK
        int user_key FK
        int content_key FK "Specifically the episode or movie viewed"
        int device_key FK "FK to a dim_devices (not shown for brevity, but important)"
        int date_key FK
        timestamp view_start_timestamp
        timestamp view_end_timestamp
        int watch_duration_seconds
        float completion_percentage "watch_duration / content_duration"
        boolean was_completed
        varchar exit_reason "e.g., natural_end, user_quit, error"
        json playback_events "e.g., [{'event': 'pause', 'ts': T1}, {'event':'resume', 'ts':T2}]"
    }

    fact_user_ratings {
        int user_key FK
        int content_key FK
        int rating_value "e.g., 1-5 stars, or thumbs_up (1)/thumbs_down (-1)"
        timestamp rating_timestamp
        PRIMARY KEY (user_key, content_key)
    }

    fact_user_watchlist {
        int user_key FK
        int content_key FK
        timestamp added_timestamp
        PRIMARY KEY (user_key, content_key)
    }

    dim_users ||--o{ fact_viewing_history : "views"
    dim_content ||--o{ fact_viewing_history : "is_viewed"
    dim_date ||--o{ fact_viewing_history : "on_date"
    dim_users ||--o{ fact_user_ratings : "rates"
    dim_content ||--o{ fact_user_ratings : "is_rated"
    dim_users ||--o{ fact_user_watchlist : "adds_to_watchlist"
    dim_content ||--o{ fact_user_watchlist : "is_added_to_watchlist"

    dim_content ||--o{ fact_content_genres : "has_genre"
    dim_genres ||--o{ fact_content_genres : "categorizes"
    dim_content ||--o{ fact_content_tags : "has_tag"
    dim_tags ||--o{ fact_content_tags : "describes"
    dim_content ||--o{ fact_content_cast_crew : "features_person"
    dim_cast_crew ||--o{ fact_content_cast_crew : "is_in_content"
    
    dim_content }o--o{ dim_content : "is_episode_of_series" (via series_key)

```

## Table Specifications

### Dimension Tables

#### `dim_users`
-   **Purpose**: Stores information about registered users.
-   **Key Fields**:
    -   `subscription_tier`: For segmenting users by service level.
    -   `user_preferences`: JSON for storing explicit preferences.

#### `dim_content`
-   **Purpose**: Central catalog for all streamable content.
-   **Key Fields**:
    -   `content_type`: Distinguishes movies, series, episodes, etc.
    -   `series_key`: Foreign key to link episodes/seasons to their parent series (references `content_key` of the series entry).
    -   `season_number`, `episode_number`: For episodic content organization.
    -   `production_details`: JSON for flexible storage of director, studio, etc.

#### `dim_genres`
-   **Purpose**: Lookup table for content genres.

#### `dim_tags`
-   **Purpose**: Lookup table for descriptive tags (moods, themes, keywords).

#### `dim_cast_crew`
-   **Purpose**: Information about actors, directors, and other personnel.

#### `dim_date`
-   **Purpose**: Standard date dimension for time-based analysis.

### Fact Tables & Associative Entities

#### `fact_content_genres`
-   **Purpose**: Links content to its genres (many-to-many).

#### `fact_content_tags`
-   **Purpose**: Links content to its descriptive tags (many-to-many).

#### `fact_content_cast_crew`
-   **Purpose**: Links content to cast and crew members and their specific roles in that content (many-to-many).

#### `fact_viewing_history`
-   **Purpose**: Records detailed user viewing sessions.
-   **Granularity**: One record per viewing session of a piece of content by a user.
-   **Key Fields**:
    -   `content_key`: Refers to the specific movie or episode watched.
    -   `watch_duration_seconds`, `completion_percentage`: Key engagement metrics.
    -   `playback_events`: JSON array to store fine-grained interaction data like pauses, skips.

#### `fact_user_ratings`
-   **Purpose**: Stores explicit user ratings for content.
-   **Granularity**: One record per user per rated piece of content.

#### `fact_user_watchlist`
-   **Purpose**: Tracks items users have added to their watchlist or 'My List'.

## Key Business Rules & Considerations

1.  **Series Hierarchy**: A `dim_content` entry with `content_type = 'series'` acts as a parent. Episodes have `content_type = 'episode'` and link to the series via `series_key`.
2.  **Content Uniqueness**: `content_id` should be unique across all content types.
3.  **Viewing Session Definition**: A viewing session in `fact_viewing_history` might be defined by a user starting content and then stopping or a significant interruption.
4.  **Recommendation Inputs**: `fact_viewing_history`, `fact_user_ratings`, `fact_user_watchlist`, along with content genres, tags, and cast/crew, are primary inputs for recommendation algorithms.

## Analytics Use Cases
-   **Content Popularity Analysis**: Most viewed, highest rated, most watchlisted content.
-   **User Engagement Patterns**: Watch duration, completion rates, binge-watching behavior (multiple episodes of a series in sequence).
-   **Recommendation Algorithm Performance**: A/B testing different recommendation strategies based on predicted vs. actual engagement.
-   **Content Catalog Analysis**: Genre/tag distribution, identifying underperforming content.
-   **Subscription Tier Analysis**: Do users on different tiers exhibit different viewing patterns or preferences?
-   **Personalized Dashboards**: Showing users their recently watched, new episodes for their series, and personalized recommendations.

## Implementation Notes
-   `playback_events` in `fact_viewing_history` can generate a large volume of data; consider if full detail is always needed or if aggregation/sampling is appropriate.
-   Consider a separate `dim_devices` table to join with `fact_viewing_history` for device-specific analysis.
-   For YouTube-like platforms with user-generated content, `dim_users` might also act as content creators, adding complexity to `dim_content` (e.g., uploader_user_key). 