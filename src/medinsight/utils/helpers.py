import pandas as pd
from typing import Dict, List, Tuple

def analyze_column_types(df: pd.DataFrame) -> Dict[str, List[str]]:
    """Categorizes columns by their technical statistical types."""
    analysis = {
        "numeric": [],
        "categorical": [],
        "datetime": [],
        "bool": []
    }
    
    for col in df.columns:
        if pd.api.types.is_bool_dtype(df[col]):
            analysis["bool"].append(col)
        elif pd.api.types.is_numeric_dtype(df[col]):
            # If numeric but very low unique cardinality, treat as categorical profile
            if df[col].nunique() < 5:
                analysis["categorical"].append(col)
            else:
                analysis["numeric"].append(col)
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            analysis["datetime"].append(col)
        else:
            # Fallback check if it can be parsed as date
            try:
                pd.to_datetime(df[col], errors='raise')
                analysis["datetime"].append(col)
            except (ValueError, TypeError):
                analysis["categorical"].append(col)
                
    return analysis

def get_dataset_profile(df: pd.DataFrame) -> Dict:
    """Returns metadata breakdown for KPI cards."""
    return {
        "rows": df.shape[0],
        "cols": df.shape[1],
        "missing_cells": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "memory_mb": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2)
    }