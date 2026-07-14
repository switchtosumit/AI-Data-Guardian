CREATE TABLE IF NOT EXISTS incidents (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    incident_type VARCHAR(100),
    severity VARCHAR(20),
    alert TEXT,
    root_cause TEXT,
    recommended_fix TEXT,
    status VARCHAR(20) DEFAULT 'OPEN'
);