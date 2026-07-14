from agents.llm import call_llm
from utils.logger import agent_logger


def generate_fix(alerts):
    
    agent_logger.info(
    f"Generating fix for alerts: {alerts}")
    
    prompt = f"""
            Generate a SQL fix for: {alerts} 

            Output only the SQL code:"""
    
    agent_logger.info(
    "Remediation generated successfully")
    
    return call_llm(prompt)

agent_logger.info(
    "No drift detected, no remediation needed")