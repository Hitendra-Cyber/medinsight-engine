import pandas as pd
from typing import Dict, Any

from typing import List, Dict, Tuple

def validate_dataset_schema(columns: List[str], dataset_type: str) -> Tuple[bool, List[str]]:
    """
    Validates if the uploaded file's columns match the selected clinical domain.
    Returns (isValid, list_of_missing_expected_keywords)
    """
    # Convert all uploaded columns to lowercase for flexible, case-insensitive matching
    cols_lower = [str(c).lower() for c in columns]
    
    # Define signature keywords that SHOULD exist for each profile selection
    SCHEMA_RULES: Dict[str, List[str]] = {
        "Patient Records": ["patient", "id", "age", "gender"],
        "Diabetes Dataset": ["glucose", "insulin", "bmi", "diabetes"],
        "Heart Disease Dataset": ["cholesterol", "heart", "blood", "pressure", "age"],
        "Hospital Management Dataset": ["doctor", "room", "admission", "cost", "discharge"],
        "Disease Statistics Dataset": ["cases", "population", "rate", "year", "disease"],
        "Medical Survey Dataset": ["satisfaction", "score", "response", "rating", "age"],
        "Generic Healthcare Dataset": ["id", "status"] # Very loose fallback rules
    }
    
    if dataset_type not in SCHEMA_RULES:
        return True, [] # Skip validation if it's a generic type not mapped
        
    required_keywords = SCHEMA_RULES[dataset_type]
    missing_requirements = []
    
    # Check if at least some of the signature core themes are present
    # We look for partial matches (e.g., 'patient_id' contains 'patient')
    for keyword in required_keywords:
        match_found = any(keyword in col for col in cols_lower)
        if not match_found:
            missing_requirements.append(keyword)
            
    # If more than 60% of signature keywords are missing, it's likely the wrong file context
    is_invalid = len(missing_requirements) > (len(required_keywords) * 0.4)
    
    return not is_invalid, required_keywords
def generate_healthcare_insights(df: pd.DataFrame, dataset_type: str) -> Dict[str, Any]:
    """Generates rule-based statistical checks depending on the medical domain."""
    insights = {"metrics": {}, "alerts": []}
    
    # Standardize column mappings case-insensitively for student resilience
    cols = {c.lower(): c for c in df.columns}
    
    if dataset_type == "Diabetes Dataset":
        glucose_col = cols.get("glucose") or cols.get("blood_glucose")
        bmi_col = cols.get("bmi")
        
        if glucose_col:
            avg_g = df[glucose_col].mean()
            insights["metrics"]["Avg Glucose Level"] = f"{avg_g:.1f} mg/dL"
            if avg_g > 140:
                insights["alerts"].append("💡 Average Cohort Glucose is elevated (>140 mg/dL), indicating high pre-diabetic tendencies across observations.")
        if bmi_col:
            avg_bmi = df[bmi_col].mean()
            insights["metrics"]["Avg BMI Value"] = f"{avg_bmi:.1f}"
            obese_pct = (df[bmi_col] >= 30).sum() / len(df) * 100
            insights["metrics"]["Obesity Prevalence"] = f"{obese_pct:.1f}%"

    elif dataset_type == "Heart Disease Dataset":
        chol_col = cols.get("cholesterol") or cols.get("chol")
        bp_col = cols.get("blood_pressure") or cols.get("bps") or cols.get("trestbps")
        
        if chol_col:
            avg_c = df[chol_col].mean()
            insights["metrics"]["Avg Cholesterol"] = f"{avg_c:.1f} mg/dL"
            if avg_c > 200:
                insights["alerts"].append("⚠️ High Risk Warning: The population mean cholesterol is classified borderline high (>200 mg/dL).")
        if bp_col:
            insights["metrics"]["Max Resting BP"] = f"{df[bp_col].max()} mmHg"

    else:
         insights["metrics"]["Total Observations"] = f"{len(df)}"
         insights["alerts"].append("ℹ️ Standard data matrix processed. Use custom templates for targeted disease deep dives.")
         
    return insights