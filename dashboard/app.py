import streamlit as st
import requests
import time

st.title("AI Data Guardian Dashboard")

API_URL = "http://api:8000/analyze"

def call_api_with_retry(retries=5, delay=3):

    last_error = None

    for attempt in range(retries):

        try:

            response = requests.post(API_URL, timeout=30)

            if response.status_code == 200:
                return response.json()

            last_error = f"HTTP {response.status_code}: {response.text}"

        except Exception as e:
            last_error = str(e)

        time.sleep(delay)

    return {
        "success": False,
        "error": last_error
    }


if st.button("Run Analysis"):

    with st.spinner("Running monitoring and AI analysis..."):

        data = call_api_with_retry()
        

    if data.get("error"):
        st.error(data["error"])
        st.stop()

    if not data.get("drift_detected", False):

        st.success(data.get("message", "No drift detected"))

    else:

        st.error("Drift Detected")

        st.write("### Alerts")
        for alert in data.get("alerts", []):
            st.warning(alert)

        st.markdown("## Root Cause Analysis")
        st.markdown(data.get("root_cause", "N/A"))

        st.markdown("## Recommended SQL Fix")
        st.code(data.get("fix", ""), language="sql")

if st.button("View Incident History"):

    try:

        response = requests.get("http://api:8000/incidents", timeout=30)

        if response.status_code == 200:
            incidents = response.json().get("incidents", [])
            st.write("### Incident History")
            st.table(incidents, height=600,hide_header=False)
        else:
            st.error(f"Failed to fetch incidents: HTTP {response.status_code}")

    except Exception as e:
        st.error(f"Error fetching incidents: {str(e)}")