import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import List
import streamlit as st

def suggest_charts_by_type(types_dict: dict) -> List[str]:
    suggestions = []
    if not types_dict:
        return suggestions
    if len(types_dict.get("datetime", [])) > 0 and len(types_dict.get("numeric", [])) > 0:
        suggestions.append("Temporal Trendline")
    if len(types_dict.get("categorical", [])) > 0 and len(types_dict.get("numeric", [])) > 0:
        suggestions.append("Categorical Feature Aggregation")
    if len(types_dict.get("numeric", [])) >= 2:
        suggestions.append("Multivariate Correlation Heatmap")
    return suggestions

def plot_histogram(df: pd.DataFrame, col: str) -> go.Figure:
    """Generates a premium density layout combining histograms, marginal boxplots, and sleek styling."""
    if df is None or col not in df.columns:
        return go.Figure()
        
    # Create an advanced statistical distribution view with a top marginal box plot
    fig = px.histogram(
        df, 
        x=col, 
        marginal="box", # Adds a matching mini-box plot right above the distribution!
        opacity=0.85,
        color_discrete_sequence=["#2b7fff"],
        template="plotly_dark" if st_is_dark_mode() else "none"
    )
    
    fig.update_traces(marker_line_color='rgba(255,255,255,0.2)', marker_line_width=1)
    
    fig.update_layout(
        autosize=True,
        height=400,
        margin=dict(l=20, r=20, t=10, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.15)', title_font=dict(size=12)),
        yaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.15)', title_font=dict(size=12)),
        bargap=0.05
    )
    return fig

def plot_correlation(df: pd.DataFrame, numeric_cols: List[str]) -> go.Figure:
    """Generates an enterprise-grade interactive correlation matrix."""
    if df is None or not numeric_cols or len(numeric_cols) < 2:
        return go.Figure()
        
    corr = df[numeric_cols].corr()
    
    fig = px.imshow(
        corr, 
        text_auto=".2f", 
        color_continuous_scale=[[0, "#0f172a"], [0.5, "#2b7fff"], [1, "#10b981"]],
        aspect="auto"
    )
    
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=10, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        coloraxis_showscale=False
    )
    return fig

def st_is_dark_mode() -> bool:
    """Helper to detect system rendering state dynamically."""
    try:
        return st.get_option("theme.base") == "dark"
    except:
        return False