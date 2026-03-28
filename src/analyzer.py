import pandas as pd

def find_triangulation_groups(df, min_cm=15):
    """
    Finds all sets of 3+ people who share the same segment.
    df columns expected: ['ID', 'Chromosome', 'Start', 'End', 'cM']
    """
    # 1. Filter by cM threshold
    df = df[df['cM'] >= min_cm].copy()
    
    # 2. Self-Join to find overlaps between all pairs
    # We join on Chromosome to keep the search space small
    merged = df.merge(df, on='Chromosome', suffixes=('_A', '_B'))
    
    # 3. Filter for valid overlaps (Interval Intersection logic)
    # Start_A < End_B AND End_A > Start_B
    overlaps = merged[
        (merged['ID_A'] < merged['ID_B']) & 
        (merged['Start_A'] < merged['End_B']) & 
        (merged['End_A'] > merged['Start_B'])
    ].copy()
    
    # 4. Calculate the overlap size (the 'sticky' segment length)
    overlaps['Overlap_Start'] = overlaps[['Start_A', 'Start_B']].max(axis=1)
    overlaps['Overlap_End'] = overlaps[['End_A', 'End_B']].min(axis=1)
    overlaps['Overlap_cM'] = overlaps['Overlap_End'] - overlaps['Overlap_Start']
    
    # 5. Filter segments that are actually significant
    return overlaps[overlaps['Overlap_cM'] > min_cm]

def get_clusters_by_chromosome(df):
    """
    Groups segments by Cluster to see which chromosomes are 'hotspots' 
    for specific ancestral lines (e.g., your Italian cluster).
    """
    return df.groupby(['CLUSTER', 'Chromosome']).size().reset_index(name='Segment_Count')