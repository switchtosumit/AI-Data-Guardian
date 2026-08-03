import copy
import json

from monitoring.drift import detect_drift


def create_baseline():
    return {
        "metadata": {
            "row_count": 21,
            "duplicate_pct": 0.0,
            "null_pct": 0.0
        },
        "amount": {
            "dtype": "float64",
            "null_pct": 0.0,
            "mean": 100.0,
            "std": 10.0,
            "min": 70.0,
            "max": 150.0
        }
    }


def save_baseline(profile, baseline_file):
    with open(baseline_file, "w") as f:
        json.dump([profile], f, indent=4)


def test_schema_drift(tmp_path):

    baseline = create_baseline()

    current = copy.deepcopy(baseline)

    current["amount"]["dtype"] = "object"

    baseline_file = tmp_path / "profile_history.json"

    save_baseline(baseline, baseline_file)

    drift, alerts = detect_drift(
        current,
        profile_path=str(baseline_file)
    )

    assert drift is True
    assert any("Schema change" in alert for alert in alerts)


def test_statistical_drift(tmp_path):

    baseline = create_baseline()

    current = copy.deepcopy(baseline)

    current["amount"]["mean"] = 10

    baseline_file = tmp_path / "profile_history.json"

    save_baseline(baseline, baseline_file)

    drift, alerts = detect_drift(
        current,
        profile_path=str(baseline_file)
    )

    assert drift is True
    assert any("Drift detected" in alert for alert in alerts)


def test_null_spike(tmp_path):

    baseline = create_baseline()

    current = copy.deepcopy(baseline)

    current["amount"]["null_pct"] = 90

    baseline_file = tmp_path / "profile_history.json"

    save_baseline(baseline, baseline_file)

    drift, alerts = detect_drift(
        current,
        profile_path=str(baseline_file)
    )

    assert drift is True
    assert any("null percentage" in alert for alert in alerts)


def test_volume_anomaly(tmp_path):

    baseline = create_baseline()

    current = copy.deepcopy(baseline)

    current["metadata"]["row_count"] = 100

    baseline_file = tmp_path / "profile_history.json"

    save_baseline(baseline, baseline_file)

    drift, alerts = detect_drift(
        current,
        profile_path=str(baseline_file)
    )

    assert drift is True
    assert any("Volume anomaly" in alert for alert in alerts)