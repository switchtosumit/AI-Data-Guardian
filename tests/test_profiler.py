from monitoring.profiler import profile_dataset

def test_profile_dataset():

    profile = profile_dataset("data/gold.csv")

    assert "metadata" in profile

    assert "amount" in profile

    assert "dtype" in profile["amount"]

    assert "mean" in profile["amount"]

    assert "std" in profile["amount"]

    assert "null_pct" in profile["amount"]