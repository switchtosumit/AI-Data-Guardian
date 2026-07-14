import pandas as pd
import json 
import os

def profile_dataset(path):

    # load dataset
    df = pd.read_csv(path)

    profile = {}

    profile['metadata'] = {
        'row_count': len(df),
        'duplicate_pct': float(df.duplicated().mean() * 100)        
    }

    for col in df.columns:
        profile[col] = {
            'dtype': str(df[col].dtype),
            'null_pct': float(df[col].isnull().mean() * 100)
        }

    # Numeric stats
        if pd.api.types.is_numeric_dtype(df[col]):

            profile[col]["mean"] = float(df[col].mean())
            profile[col]["std"] = float(df[col].std())
            profile[col]["min"] = float(df[col].min())
            profile[col]["max"] = float(df[col].max())

    return profile

def save_profile(profile, filename = "monitoring/profile_history.json"):
    if os.path.exists(filename):
        history = json.load(open(filename))
    else:
        history = []
    history.append(profile)
    
    json.dump(history, open(filename, 'w'), indent=4)