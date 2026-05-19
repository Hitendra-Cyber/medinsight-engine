import pandas as pd
from typing import List, Union, Dict

class DataCleaner:
    def __init__(self, df: pd.DataFrame):
        if df is None or df.empty:
            raise ValueError("Target DataFrame context cannot be empty or null initialization states.")
        self.df = df.copy()

    def get_cleaning_status(self) -> Dict[str, int]:
        return {
            "total_nulls": int(self.df.isna().sum().sum()),
            "duplicate_count": int(self.df.duplicated().sum())
        }

    def fill_missing(self, column: str, strategy: str, constant_val: Union[int, float, str] = None) -> pd.DataFrame:
        if column not in self.df.columns:
            return self.df
            
        # If there are no null values, escape instantly to save computational resources
        if self.df[column].isna().sum() == 0:
            return self.df

        is_numeric = pd.api.types.is_numeric_dtype(self.df[column])
        
        if strategy == "Mean":
            fill_val = self.df[column].mean() if is_numeric else self.df[column].mode().dropna().set_axis([0]).get(0, "Missing")
        elif strategy == "Median":
            fill_val = self.df[column].median() if is_numeric else self.df[column].mode().dropna().set_axis([0]).get(0, "Missing")
        elif strategy == "Mode":
            mode_series = self.df[column].mode().dropna()
            fill_val = mode_series.iloc[0] if not mode_series.empty else "Missing"
        else:
            fill_val = constant_val if constant_val is not None else "Missing"
            
        self.df[column] = self.df[column].fillna(fill_val)
        return self.df

    def remove_duplicates(self) -> pd.DataFrame:
        if self.df.duplicated().sum() == 0:
            return self.df
        self.df.drop_duplicates(keep='first', inplace=True)
        self.df.reset_index(drop=True, inplace=True) # Protects plotting structures later
        return self.df