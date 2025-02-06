import pandas as pd
import numpy as np

def balanced_risk_set_matching(df, treatment_col, time_col, covariate_cols, caliper=None):
    """
    Perform balanced risk set matching.
    
    For each treated subject (treatment_col==1) in the dataset, the function 
    finds a control subject (treatment_col==0) in the risk set (i.e., subjects
    with event time >= treated subject's event time) that minimizes the Euclidean
    distance based on the specified covariate columns.
    
    Optionally, a caliper can be provided to only allow matches whose distance is 
    below the caliper threshold.
    
    Parameters:
    -----------
    df : pd.DataFrame
        The dataset containing treatment, time, and covariate information.
    treatment_col : str
        Column name indicating treatment (1 for treated, 0 for control).
    time_col : str
        Column name for the time-to-event (or time of treatment) variable.
    covariate_cols : list of str
        List of column names for covariates to use in matching.
    caliper : float, optional
        Maximum allowed Euclidean distance for a valid match. If None, no caliper is applied.
        
    Returns:
    --------
    matched_pairs : list of tuples
        Each tuple is (treated_index, control_index) corresponding to a matched pair.
    """
    df_matched = df.copy()
    df_matched.sort_values(time_col, inplace=True)
    
    matched_control_indices = set()
    matched_pairs = []
    
    treated_indices = df_matched.index[df_matched[treatment_col] == 1].tolist()
    for treated_idx in treated_indices:
        treated_row = df_matched.loc[treated_idx]
        treated_time = treated_row[time_col]
        
        risk_set = df_matched.loc[
            (df_matched[time_col] >= treated_time) &
            (df_matched[treatment_col] == 0) &
            (~df_matched.index.isin(matched_control_indices))
        ]
        
        if risk_set.empty:
            continue
        
        treated_cov = treated_row[covariate_cols].values.astype(float)
        controls_cov = risk_set[covariate_cols].values.astype(float)
        distances = np.linalg.norm(controls_cov - treated_cov, axis=1)
        
        if caliper is not None:
            valid = distances <= caliper
            if not np.any(valid):
                continue
            distances = distances[valid]
            risk_set = risk_set.iloc[np.where(valid)[0]]
        
        best_match_idx = risk_set.index[np.argmin(distances)]
        matched_pairs.append((treated_idx, best_match_idx))
        matched_control_indices.add(best_match_idx)
        
    return matched_pairs

def analyze_matching_results(matches, df):
    """
    Analyze the matching results by computing basic statistics on matched pairs.
    
    Parameters:
    -----------
    matches : list of tuples
        Matched pairs of treated and control indices.
    df : pd.DataFrame
        The original dataset used for matching.
    
    Returns:
    --------
    summary : dict
        A dictionary containing statistics about the matching results.
    """
    treated_times = [df.loc[t_idx, 'time'] for t_idx, _ in matches]
    control_times = [df.loc[c_idx, 'time'] for _, c_idx in matches]
    time_differences = np.array(treated_times) - np.array(control_times)
    
    summary = {
        'Total Matched Pairs': len(matches),
        'Mean Time Difference': np.mean(time_differences),
        'Std Dev Time Difference': np.std(time_differences),
        'Min Time Difference': np.min(time_differences),
        'Max Time Difference': np.max(time_differences)
    }
    
    return summary

if __name__ == "__main__":
    np.random.seed(0)
    sample_data = {
        'time': np.random.uniform(0, 100, 10),
        'treatment': np.random.binomial(1, 0.4, 10),
        'covariate1': np.random.normal(0, 1, 10),
        'covariate2': np.random.normal(5, 2, 10)
    }
    df = pd.DataFrame(sample_data)
    print("Sample Data:")
    print(df)
    
    treatment_col = 'treatment'
    time_col = 'time'
    covariate_cols = ['covariate1', 'covariate2']
    caliper = 3.0
    
    matches = balanced_risk_set_matching(df, treatment_col, time_col, covariate_cols, caliper)
    
    print("\nMatched Pairs (treated_index, control_index):")
    for pair in matches:
        print(pair)
    
    summary = analyze_matching_results(matches, df)
    print("\nMatching Summary:")
    for key, value in summary.items():
        print(f"{key}: {value}")
