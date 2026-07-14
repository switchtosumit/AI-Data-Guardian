from agents.llm import call_llm
from utils.logger import agent_logger

def analyze_root_cause(alerts):

    agent_logger.info(
    f"Analyzing alerts: {alerts}")    

    prompt = f"""You are a senior Data Reliability Engineer.
            Analyze the following production data quality incidents:{alerts}
            Explain:
            1. Probable root cause
            2. Business impact
            3. Recommended investigation steps
            4. Suggested remediation"""
    
    agent_logger.info(
    "Root cause generated successfully")
    
    return call_llm(prompt)

agent_logger.info(
    "no drift detected, no root cause analysis needed")




