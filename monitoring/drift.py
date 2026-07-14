import json
import os
import numpy as np
from utils.logger import drift_logger

def detect_drift(current_profile, threshold = 2.0):
    path = "monitoring/profile_history.json"

    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump([current_profile], f, indent=4)
        return False, ["First Run No Drift, Baseline profile created"]
    
    with open(path, "r") as f:
        history = json.load(f)
    
    if len(history) < 1:
        return False, ["No baseline profile available"]
        
    baseline = history[-1]
    
    alerts = []
    

   
    #Volumne Detection
    baseline_row_count = baseline['metadata']['row_count']
    current_row_count = current_profile['metadata']['row_count']
    row_diff_pct = abs(current_row_count - baseline_row_count) / baseline_row_count * 100

    if row_diff_pct > 30:
        alerts.append( f"Volume anomaly detected: "
        f"{baseline_row_count} rows -> "
        f"{current_row_count} rows")

    #Duplicate Detection
    baseline_duplicate = baseline['metadata']['duplicate_pct']
    current_duplicate = current_profile['metadata']['duplicate_pct']
    duplicate_diff = abs(current_duplicate - baseline_duplicate)

    if duplicate_diff > 10:
        alerts.append( f"Duplicate anomaly detected: "
        f"{baseline_duplicate:.2f}% -> "
        f"{current_duplicate:.2f}%")

    for col in current_profile:

        if col == 'metadata':
            continue

        if 'mean' in current_profile[col]:
            if col in baseline:
                diff = abs(current_profile[col]['mean'] - baseline[col]['mean'])

                if diff > threshold*baseline[col]['std']:
                    alerts.append(f"Drift detected in {col}: mean changed from {baseline[col]['mean']} to {current_profile[col]['mean']} diff: {diff:.2f}")
        if current_profile[col]['dtype'] != baseline[col]['dtype']:
            alerts.append(f"Schema change detected in {col}: type changed from {baseline[col]['dtype']} to {current_profile[col]['dtype']}")

        null_threshold = 5.0
        if col in baseline:
            diff = abs(current_profile[col]['null_pct'] - baseline[col]['null_pct'])
            if diff > null_threshold:
                alerts.append(f"Drift detected in {col}: null percentage changed from {baseline[col]['null_pct']}% to {current_profile[col]['null_pct']}% diff: {diff:.2f}%")   

    drift_logger.info(
    f"Current profile generated")

    if alerts:
        drift_logger.warning(f"Drift detected: {alerts}")
    else:
        drift_logger.info("No drift detected")

    return len(alerts) > 0, alerts


    