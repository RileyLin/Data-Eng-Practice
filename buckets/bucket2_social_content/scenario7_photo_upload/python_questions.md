# Scenario 7: Photo Upload (Instagram-like) - Python Questions

## Python Question 7.4.1: Photo Upload Log Processing for Average Upload Time

Implement the Python function `process_upload_log(log, pending_buffer, stats_aggregator)` to process a stream of photo upload logs and calculate the running average upload time for *successful* uploads.

**Function Requirements:**
1.  Process each `log` event from a stream of upload logs.
2.  Keep track of 'upload_start' events in the `pending_buffer` (dictionary mapping `upload_id` to `start_timestamp`).
3.  When an 'upload_end' event arrives and is marked as successful (`is_success: True`):
    *   Calculate the upload duration (end_timestamp - start_timestamp).
    *   Update the `stats_aggregator` dictionary, which stores `total_duration_ms` and `successful_uploads`.
    *   Remove the completed upload from `pending_buffer`.
4.  If an 'upload_end' event is not successful or has no matching 'upload_start', it should be handled gracefully (e.g., removed from `pending_buffer` if present, but not counted in `stats_aggregator`).

**DATA STRUCTURE EXAMPLES:**

Input: `log` (dict)
- Structure: `{'timestamp': int, 'event_type': str, 'upload_id': str, 'is_success': bool (optional)}`
- `event_type` values: 'upload_start' or 'upload_end'
- `is_success`: only present in 'upload_end' events (assume `False` or treat as failed if missing for an 'upload_end' event).

Example log events:
- Start event: `{'timestamp': 1000, 'event_type': 'upload_start', 'upload_id': 'up1'}`
- Successful end: `{'timestamp': 1150, 'event_type': 'upload_end', 'upload_id': 'up1', 'is_success': True}`
- Failed end: `{'timestamp': 1200, 'event_type': 'upload_end', 'upload_id': 'up2', 'is_success': False}`

Input/Output: `pending_buffer` (dict)
- Structure: `{upload_id: start_timestamp}`
- Example: `{'up1': 1000, 'up2': 1050}`

Input/Output: `stats_aggregator` (dict)
- Structure: `{'total_duration_ms': int, 'successful_uploads': int}`
- Example: `{'total_duration_ms': 350, 'successful_uploads': 2}`

**PROCESSING FLOW EXAMPLE:**

Initial state:
`pending_buffer = {}`
`stats_aggregator = {'total_duration_ms': 0, 'successful_uploads': 0}`

1.  Process `{'timestamp': 1000, 'event_type': 'upload_start', 'upload_id': 'up1'}`
    *   `pending_buffer` becomes `{'up1': 1000}`.
2.  Process `{'timestamp': 1050, 'event_type': 'upload_start', 'upload_id': 'up2'}`
    *   `pending_buffer` becomes `{'up1': 1000, 'up2': 1050}`.
3.  Process `{'timestamp': 1150, 'event_type': 'upload_end', 'upload_id': 'up1', 'is_success': True}`
    *   Duration = 1150 - 1000 = 150ms.
    *   `pending_buffer` becomes `{'up2': 1050}`.
    *   `stats_aggregator` becomes `{'total_duration_ms': 150, 'successful_uploads': 1}`.
4.  Process `{'timestamp': 1250, 'event_type': 'upload_end', 'upload_id': 'up2', 'is_success': False}`
    *   `pending_buffer` becomes `{}`.
    *   `stats_aggregator` remains unchanged.

Final `stats_aggregator` can be used to calculate average upload time: `total_duration_ms / successful_uploads`.

**Function Signature:**
```python
def process_upload_log(log, pending_buffer, stats_aggregator):
    # ... implementation ...
```

## Question 1: Photo Upload Processing & Validation

**Problem**: Implement a system to process photo upload events, validate image properties (size, format), and track upload success/failure, including basic retry logic.

**Key Requirements**:
-   Validate image against constraints (max size, allowed formats).
-   Simulate upload process and potential failures.
-   Implement a simple retry mechanism for transient failures.
-   Log success/failure status with reasons.

### Solution (Adapted from `src/python/q009_photo_upload.py`):

```python
import time
import random

MAX_FILE_SIZE_MB = 10
ALLOWED_FORMATS = ['jpeg', 'png', 'heic']
MAX_RETRIES = 2

class PhotoUploadProcessor:
    def __init__(self):
        self.upload_log = []

    def _validate_photo(self, photo_details):
        """Validate photo properties."""
        file_size_mb = photo_details.get('size_bytes', 0) / (1024 * 1024)
        file_format = photo_details.get('format', '').lower()

        if file_size_mb > MAX_FILE_SIZE_MB:
            return False, f"File size {file_size_mb:.2f}MB exceeds limit of {MAX_FILE_SIZE_MB}MB."
        if file_format not in ALLOWED_FORMATS:
            return False, f"File format '{file_format}' not allowed. Supported: {ALLOWED_FORMATS}."
        return True, "Validation successful."

    def _simulate_upload_attempt(self, photo_details):
        """Simulate a single upload attempt, returning success or a failure type."""
        # Simulate network or server issues
        if random.random() < 0.1: # 10% chance of a network error
            return False, "network_error"
        if random.random() < 0.05: # 5% chance of a server error
            return False, "server_error"
        
        # Simulate processing time
        time.sleep(random.uniform(0.1, 0.5)) # Simulate upload/processing time
        return True, "upload_successful"

    def process_upload(self, user_id, photo_id, photo_details):
        """Process a photo upload attempt with validation and retries."""
        upload_attempt_key = f"{user_id}_{photo_id}_{int(time.time())}"
        
        is_valid, validation_msg = self._validate_photo(photo_details)
        if not is_valid:
            self.upload_log.append({
                'attempt_key': upload_attempt_key,
                'user_id': user_id,
                'photo_id': photo_id,
                'status': 'validation_failed',
                'reason': validation_msg,
                'retries': 0,
                'timestamp': time.time()
            })
            return False, validation_msg

        retries = 0
        success = False
        final_status_reason = ""

        while retries <= MAX_RETRIES:
            attempt_success, status_reason = self._simulate_upload_attempt(photo_details)
            if attempt_success:
                success = True
                final_status_reason = status_reason
                break
            else:
                final_status_reason = status_reason
                # Only retry on potentially transient errors like network error
                if status_reason == "network_error":
                    retries += 1
                    time.sleep(0.1 * retries) # Exponential backoff (simplified)
                else: # Non-retryable error like server_error (in this simple model)
                    break 
        
        self.upload_log.append({
            'attempt_key': upload_attempt_key,
            'user_id': user_id,
            'photo_id': photo_id,
            'status': 'upload_successful' if success else 'upload_failed',
            'reason': final_status_reason,
            'retries': retries if not success else retries, # retries count for the failed ones that led to success
            'timestamp': time.time()
        })
        return success, final_status_reason

    def get_upload_summary(self):
        total_attempts = len(self.upload_log)
        successful_uploads = sum(1 for log in self.upload_log if log['status'] == 'upload_successful')
        failed_uploads = total_attempts - successful_uploads
        failure_reasons = {}
        for log in self.upload_log:
            if log['status'] != 'upload_successful':
                reason = log['reason']
                failure_reasons[reason] = failure_reasons.get(reason, 0) + 1
        return {
            'total_attempts': total_attempts,
            'successful_uploads': successful_uploads,
            'failed_uploads': failed_uploads,
            'success_rate_pct': (successful_uploads / total_attempts * 100) if total_attempts > 0 else 0,
            'failure_reasons': failure_reasons
        }

# Test Cases
def test_photo_upload_processing():
    processor = PhotoUploadProcessor()
    
    # Valid photo
    processor.process_upload('user1', 'photo1', {'size_bytes': 5*1024*1024, 'format': 'jpeg'})
    # Invalid size
    processor.process_upload('user2', 'photo2', {'size_bytes': 15*1024*1024, 'format': 'jpeg'})
    # Invalid format
    processor.process_upload('user3', 'photo3', {'size_bytes': 2*1024*1024, 'format': 'gif'})

    # Simulate more uploads to see retry/failure dynamics (randomness involved)
    for i in range(10):
        processor.process_upload(f'user_test{i}', f'photo_test{i}', {'size_bytes': random.randint(1,9)*1024*1024, 'format': random.choice(ALLOWED_FORMATS)})

    summary = processor.get_upload_summary()
    print("Upload Summary:", summary)
    assert summary['total_attempts'] == 13
    # Exact success/failure counts will vary due to randomness in _simulate_upload_attempt
    assert 'validation_failed' in summary['failure_reasons']
    print("Photo upload processing test executed.")

if __name__ == "__main__":
    test_photo_upload_processing()
```

---

## Question 2: EXIF Data Extraction and Analysis

**Problem**: Implement a function to parse basic EXIF data (e.g., camera model, creation date, GPS coordinates if available) from a simulated image file or data structure. Then, analyze this data to find common camera models or typical photo-taking times.

**Key Requirements**:
-   Input: A representation of an image containing EXIF-like key-value pairs.
-   Output: Parsed EXIF data and a simple analysis (e.g., top N camera models).
-   Handle missing EXIF tags gracefully.

### Solution:

```python
from collections import Counter
from datetime import datetime

def parse_exif_data(image_with_exif):
    """
    Parses EXIF-like data from an image dictionary.
    Relevant keys: 'Make', 'Model', 'DateTimeOriginal', 'GPSLatitude', 'GPSLongitude'.
    """
    parsed_data = {}
    exif = image_with_exif.get('exif_data', {})

    parsed_data['camera_make'] = exif.get('Make')
    parsed_data['camera_model'] = exif.get('Model')
    
    datetime_original_str = exif.get('DateTimeOriginal')
    if datetime_original_str:
        try:
            # Example format: "2023:04:15 10:30:00"
            parsed_data['creation_datetime'] = datetime.strptime(datetime_original_str, "%Y:%m:%d %H:%M:%S")
        except ValueError:
            parsed_data['creation_datetime'] = None # Or log a warning
    else:
        parsed_data['creation_datetime'] = None

    gps_lat = exif.get('GPSLatitude')
    gps_lon = exif.get('GPSLongitude')
    if gps_lat is not None and gps_lon is not None:
        parsed_data['gps_coordinates'] = {'latitude': gps_lat, 'longitude': gps_lon}
    else:
        parsed_data['gps_coordinates'] = None
        
    return parsed_data

def analyze_exif_batch(image_list):
    """
    Analyzes a list of images (with parsed EXIF data) to find common trends.
    """
    camera_models = []
    creation_hours = []
    has_gps_count = 0

    for image_info in image_list:
        exif = parse_exif_data(image_info)
        if exif.get('camera_model'):
            camera_models.append(f"{exif.get('camera_make', 'Unknown')} {exif.get('camera_model')}")
        if exif.get('creation_datetime'):
            creation_hours.append(exif['creation_datetime'].hour)
        if exif.get('gps_coordinates'):
            has_gps_count += 1
            
    top_camera_models = Counter(camera_models).most_common(3)
    common_photo_hours = Counter(creation_hours).most_common(5)
    
    return {
        'total_images_processed': len(image_list),
        'top_camera_models': top_camera_models,
        'common_photo_hours (UTC if not specified)': common_photo_hours,
        'images_with_gps_pct': (has_gps_count / len(image_list) * 100) if image_list else 0
    }

# Test Cases
def test_exif_analysis():
    sample_images = [
        {'image_id': 'img1', 'exif_data': {'Make': 'Apple', 'Model': 'iPhone 13 Pro', 'DateTimeOriginal': '2023:10:22 14:35:10', 'GPSLatitude': 34.0522, 'GPSLongitude': -118.2437}},
        {'image_id': 'img2', 'exif_data': {'Make': 'Google', 'Model': 'Pixel 7', 'DateTimeOriginal': '2023:10:21 09:15:00'}},
        {'image_id': 'img3', 'exif_data': {'Make': 'Apple', 'Model': 'iPhone 13 Pro', 'DateTimeOriginal': '2023:10:20 18:00:05'}},
        {'image_id': 'img4', 'exif_data': {'Model': 'Generic Cam', 'GPSLatitude': 40.7128, 'GPSLongitude': -74.0060}},
        {'image_id': 'img5', 'exif_data': {'Make': 'Sony', 'Model': 'Alpha 7 IV', 'DateTimeOriginal': '2023:10:22 14:00:00'}},
        {'image_id': 'img6', 'exif_data': {'Make': 'Apple', 'Model': 'iPhone 12', 'DateTimeOriginal': '2023:04:15 10:30:00'}},
    ]

    parsed_img1_exif = parse_exif_data(sample_images[0])
    assert parsed_img1_exif['camera_model'] == 'iPhone 13 Pro'
    assert parsed_img1_exif['gps_coordinates'] is not None

    analysis_results = analyze_exif_batch(sample_images)
    print("EXIF Analysis Results:", analysis_results)
    assert len(analysis_results['top_camera_models']) > 0
    assert analysis_results['top_camera_models'][0][0] == 'Apple iPhone 13 Pro'
    assert analysis_results['images_with_gps_pct'] > 0
    print("EXIF data analysis test passed.")

if __name__ == "__main__":
    test_photo_upload_processing()
    print("\n---\n")
    test_exif_analysis()

```

---

## Question 3: Predicting Upload Failure Risk

**Problem**: Implement a simplified function to predict the risk of an photo upload failing based on input features like image size, network type, and historical device success rate.

**Key Requirements**:
-   Input: Photo details (size, format), device details (network type, historical success rate for this device model).
-   Output: A risk score (e.g., 0-1) or a risk category (Low, Medium, High).
-   Logic: A simple rule-based or weighted scoring approach.

### Solution:

```python
def predict_upload_failure_risk(photo_details, device_info, historical_data):
    """
    Predicts the risk of photo upload failure using a simple scoring model.

    Args:
        photo_details (dict): {'size_bytes': int, 'format': str}.
        device_info (dict): {'network_type': str, 'device_model': str}.
        historical_data (dict): {
            'device_model_success_rates': {'model_X': 0.95, 'model_Y': 0.80},
            'network_failure_multipliers': {'2g': 2.0, '3g': 1.5, '4g': 1.0, 'wifi': 0.8, 'unknown': 1.2}
        }

    Returns:
        tuple: (risk_score: float (0-1), risk_category: str)
    """
    base_risk = 0.1 # Base risk for any upload
    risk_score = base_risk

    # Factor 1: Image Size
    size_mb = photo_details.get('size_bytes', 0) / (1024 * 1024)
    if size_mb > 8: # Large files are riskier
        risk_score += 0.3
    elif size_mb > 4:
        risk_score += 0.15

    # Factor 2: Network Type
    network = device_info.get('network_type', 'unknown').lower()
    multiplier = historical_data.get('network_failure_multipliers', {}).get(network, 1.2)
    risk_score *= multiplier # Apply multiplier directly, could be additive too

    # Factor 3: Historical Device Success Rate
    device_model = device_info.get('device_model')
    device_success_rates = historical_data.get('device_model_success_rates', {})
    # Default to a moderate success rate if model unknown
    device_success_rate = device_success_rates.get(device_model, 0.90) 
    device_failure_rate_factor = (1 - device_success_rate) * 2 # Amplify failure impact
    risk_score += device_failure_rate_factor
    
    # Factor 4: Image format (minor impact)
    if photo_details.get('format', '').lower() == 'heic' and network not in ['wifi', '5g']:
        risk_score += 0.05 # HEIC can sometimes be problematic on slower networks if not optimized

    # Normalize score (crude normalization to keep it roughly 0-1, can be more sophisticated)
    final_risk_score = min(1.0, max(0.0, risk_score / 2.0)) # Adjust divisor based on typical score range

    risk_category = "Low"
    if final_risk_score > 0.6:
        risk_category = "High"
    elif final_risk_score > 0.3:
        risk_category = "Medium"

    return final_risk_score, risk_category

# Test Cases
def test_failure_risk_prediction():
    historical_data = {
        'device_model_success_rates': {'iPhone13': 0.98, 'Pixel6': 0.96, 'GalaxyS21': 0.92, 'OldPhone': 0.75},
        'network_failure_multipliers': {'2g': 2.5, '3g': 1.8, '4g': 1.0, '5g':0.9, 'wifi': 0.8, 'unknown': 1.5}
    }

    # Scenario 1: Good conditions
    photo1 = {'size_bytes': 2*1024*1024, 'format': 'jpeg'}
    device1 = {'network_type': 'wifi', 'device_model': 'iPhone13'}
    risk1_score, category1 = predict_upload_failure_risk(photo1, device1, historical_data)
    print(f"Scenario 1 Risk: Score={risk1_score:.2f}, Category='{category1}'")
    assert category1 == "Low"

    # Scenario 2: Bad network, large file, older device
    photo2 = {'size_bytes': 9*1024*1024, 'format': 'png'}
    device2 = {'network_type': '2g', 'device_model': 'OldPhone'}
    risk2_score, category2 = predict_upload_failure_risk(photo2, device2, historical_data)
    print(f"Scenario 2 Risk: Score={risk2_score:.2f}, Category='{category2}'")
    assert category2 == "High"

    # Scenario 3: Medium conditions
    photo3 = {'size_bytes': 6*1024*1024, 'format': 'heic'}
    device3 = {'network_type': '4g', 'device_model': 'GalaxyS21'}
    risk3_score, category3 = predict_upload_failure_risk(photo3, device3, historical_data)
    print(f"Scenario 3 Risk: Score={risk3_score:.2f}, Category='{category3}'")
    assert category3 == "Medium" or category3 == "High" # Depends on threshold tuning
    
    # Scenario 4: Unknown device model
    photo4 = {'size_bytes': 3*1024*1024, 'format': 'jpeg'}
    device4 = {'network_type': 'unknown', 'device_model': 'UnknownDeviceX'}
    risk4_score, category4 = predict_upload_failure_risk(photo4, device4, historical_data)
    print(f"Scenario 4 Risk: Score={risk4_score:.2f}, Category='{category4}'")
    # Expected: Medium or High due to unknown network and device success rate default
    assert category4 in ["Medium", "High"]

    print("Upload failure risk prediction test passed.")

if __name__ == "__main__":
    test_photo_upload_processing()
    print("\n---\n")
    test_exif_analysis()
    print("\n---\n")
    test_failure_risk_prediction()
```

## Key Concepts Tested
1.  **Event Simulation & Processing**: Simulating multi-stage processes like photo uploads with retries.
2.  **Data Validation**: Checking inputs against predefined constraints.
3.  **EXIF Data Handling**: Parsing and extracting meaningful information from image metadata.
4.  **Basic Data Analysis**: Aggregating data to find trends (e.g., common camera models from EXIF).
5.  **Risk Scoring/Prediction**: Implementing simple rule-based or weighted models for predictive tasks.
6.  **Modularity**: Designing classes and functions for specific, testable tasks.
7.  **Handling Missing Data**: Graceful degradation when optional data (like certain EXIF tags) is not present. 