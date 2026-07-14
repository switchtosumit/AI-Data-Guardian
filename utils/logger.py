import logging
import os

os.makedirs("logs", exist_ok=True)

def setup_logger(name, log_file):

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger

api_logger = setup_logger('api_logger', 'logs/api.log')

drift_logger = setup_logger('drift_logger', 'logs/drift.log')

agent_logger = setup_logger('agent_logger', 'logs/agent.log')
