import json
from monitoring.drift import detect_drift

def test_no_drift(tmp_path):

    baseline = {
        "metadata": {
            "row_count": 21,
            "duplicate_pct": 0.0
        },
        "amount": {
            "dtype": "float64",
            "null_pct": 0.0,
            "mean": 100,
            "std": 10,
            "min": 70,
            "max": 150
        }
    }

    current = {
        "metadata": {
            "row_count": 21,
            "duplicate_pct": 0.0
        },
        "amount": {
            "dtype": "float64",
            "null_pct": 0.0,
            "mean": 100,
            "std": 10,
            "min": 70,
            "max": 150
        }
    }

    baseline_file = tmp_path / "profile_history.json"

    with open(baseline_file, "w") as f:
        json.dump([baseline], f)

    drift, alerts = detect_drift(
        current,
        profile_path=str(baseline_file)
    )

    assert drift is False
    assert alerts == []