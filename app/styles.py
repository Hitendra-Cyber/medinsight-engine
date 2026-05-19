import streamlit as st

def inject_custom_css():
    st.markdown("""
        <style>
            /* Dynamic CSS Theme Adaptation
               Uses Streamlit's native theme properties seamlessly 
            */
            
            /* Clean modern global layout styling */
            .stApp { 
                background-color: var(--background-color); 
            }
            
            h1, h2, h3 { 
                color: var(--text-color) !important; 
                font-family: 'Inter', sans-serif; 
            }
            
            /* Custom Responsive Container Cards */
            .metric-card {
                background-color: var(--secondary-background-color);
                padding: 20px;
                border-radius: 12px;
                border: 1px solid rgba(128, 128, 128, 0.2);
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
                margin-bottom: 15px;
            }
            
            /* High-end Metric Label Customizations */
            div[data-testid="stMetricValue"] { 
                font-size: 26px !important; 
                font-weight: 600 !important; 
                color: var(--text-color); 
            }
            
            div[data-testid="stMetricLabel"] { 
                font-size: 14px !important; 
                color: var(--text-color);
                opacity: 0.7;
            }
            
            /* Give sidebar active elements a distinct subtle clinical hue */
            section[data-testid="stSidebar"] {
                border-right: 1px solid rgba(128, 128, 128, 0.15);
            }
        </style>
    """, unsafe_allow_html=True)