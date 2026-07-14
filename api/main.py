from fastapi import FastAPI
from agents.root_cause_agent import analyze_root_cause
from agents.fix_agent import generate_fix
from monitoring.profiler import profile_dataset
from monitoring.drift import detect_drift
from agents.severity_agent import classify_severity
from db.incidents import save_incident
from db.database import get_connection
from utils.logger import api_logger

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to the AI Data Guardian API!"}

@app.post("/analyze")
def analyze():

    api_logger.info("Analysis request received")

    try:

        profile = profile_dataset("data/gold.csv")

        api_logger.info("Dataset profiling completed")

        drift_detected,alerts = detect_drift(profile)

        api_logger.info(f"Drift detection completed. Drift={drift_detected}, Alerts={alerts}")
        
        # No anomalies
        if not drift_detected:

            api_logger.info("No drift detected")

            return {
                "success": True,
                "drift_detected": False,
                "message": alerts[0] if alerts else "No drift detected",               
                "alerts": []
            }

        # AI analysis
        severity = classify_severity(alerts)
        api_logger.info(f"Incident severity classified as {severity}")
       
        root_cause = analyze_root_cause(alerts)
        api_logger.info("Root cause generated successfully")
        
        fix = generate_fix(alerts)
        api_logger.info("Fix recommendation generated successfully")

        save_incident(
            incident_type="Data Drift",
            severity=severity,
            alert="\n".join(alerts),
            root_cause=root_cause,
            recommended_fix=fix
        )
        api_logger.info("Incident saved to PostgreSQL")

        api_logger.info("Analysis completed successfully")

        return {
           "success": True,
           "drift_detected": True,
           "alerts": alerts,
           "root_cause": root_cause,
           "fix": fix
        }

    except Exception as e:
        api_logger.exception(
            f"Analysis failed: {e}")
        
        return {
            "success": False,
            "error": str(e)
        }
@app.get("/incidents")
def get_incidents():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM incidents ORDER BY created_at DESC")
    incidents = cur.fetchall()

    cur.close()
    conn.close()

    return {"incidents": incidents}