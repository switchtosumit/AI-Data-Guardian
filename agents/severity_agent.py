def classify_severity(alerts):

    severity = 0

    for alert in alerts:
        
        alert_lower = alert.lower()

        if "volumne anomaly" in alert_lower:
            severity += 3
        elif "duplicate spike" in alert_lower:
            severity += 2
        elif "drift detected" in alert_lower:
            severity += 1
        elif "schema" in alert_lower:
            severity += 5
        elif "null spike" in alert_lower:
            severity += 3

    if severity >= 5:
        return "Critical"
    if severity >= 3:
        return "High"
    return "Medium"
    
   
       
