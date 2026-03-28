import pandas as pd

file_path = 'data/raw/my_genealogy_table.xlsx'

def clean_genetic_data(file_path):
    # Load the data
    df = pd.read_excel(file_path)
    
    # 1. Clean IDs: Force as strings to avoid scientific notation
    df['KIT'] = df['KIT'].astype(str)
    
    # 2. Extract "Triangulation Segments" only
    # We only want rows where Chromosome (CHR) data is actually filled
    segments_df = df.dropna(subset=['CHR', 'B37 START POS\'N', 'B37 END POS\'N'])
    
    # 3. Ensure numeric types for the triangulation math
    numeric_cols = ['CHR', 'B37 START POS\'N', 'B37 END POS\'N', 'CENTIMORGANS (CM)']
    for col in numeric_cols:
        segments_df[col] = pd.to_numeric(segments_df[col], errors='coerce')
    
    # 4. Standardize column names for the analyzer.py to read easily
    segments_df = segments_df.rename(columns={
        'KIT': 'ID',
        'CHR': 'Chromosome',
        'B37 START POS\'N': 'Start',
        'B37 END POS\'N': 'End',
        'CENTIMORGANS (CM)': 'cM'
    })
    
    return segments_df

# To use this in your workflow:
# segments = clean_genetic_data('data/raw/my_genealogy_table.xlsx')