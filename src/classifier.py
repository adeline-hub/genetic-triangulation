import pandas as pd

def classify_match(row):
    """
    Heuristic engine to auto-assign a cluster based on metadata.
    You can expand the 'rules' dictionary to include more regions.
    """
    # 1. Define your heuristic knowledge base
    rules = {
        'Italy': ['IT', 'ITALIA', 'VALLE', 'ROSSI', 'LOMBARDY'],
        'Vietnam-Era': ['VN', 'VIETNAM', 'SAIGON', 'HANOI'],
        'Russia-Eurasia': ['RU', 'RUSSIA', 'BORANENKOV', 'KURSK'],
        'UK-General': ['UK', 'UNITED KINGDOM', 'LONDON', 'ENGLAND', 'WADSWORTH', 'DRAKE']
    }
    
    # 2. Check the columns for matches
    location_str = str(row['LOCATION']).upper()
    country_str = str(row['ORIGIN COUNTRY']).upper()
    surname_str = str(row['SURNAME']).upper()
    
    # 3. Logic: If keyword exists in any of these fields, assign cluster
    for cluster, keywords in rules.items():
        if any(key in location_str or key in country_str or key in surname_str for key in keywords):
            return cluster
            
    return "Unassigned"

def apply_classification(df):
    """
    Apply the classifier to the whole dataframe and fill the 'CLUSTER' column 
    only if it is currently empty.
    """
    df['CLUSTER'] = df.apply(
        lambda row: classify_match(row) if pd.isna(row['CLUSTER']) or row['CLUSTER'] == '' else row['CLUSTER'], 
        axis=1
    )
    return df