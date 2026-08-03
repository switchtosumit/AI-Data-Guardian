from agents.severity_agent import classify_severity

def test_critical():

    alerts = ["Schema change detected"]

    assert classify_severity(alerts) == "Critical"

def test_warning():

    alerts = ["Null spike detected"]

    assert classify_severity(alerts) == "High"

def test_info():

    alerts = []

    assert classify_severity(alerts) == "Medium"