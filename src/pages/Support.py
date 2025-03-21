import streamlit as st
from datetime import datetime, timedelta
import pytz
from config.languages import TRANSLATIONS

# Get current language
if "language" not in st.session_state:
    st.session_state.language = "English"
t = TRANSLATIONS[st.session_state.language]

# Page config
st.set_page_config(
    page_title=f"{t['nav_support']} - TechSolutions",
    page_icon=None,
    layout="wide"
)

# Add enterprise styling
st.markdown("""
    <style>
    /* Global styles */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Page container */
    .block-container {
        padding: 2rem;
        max-width: 1200px !important;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #1e3a8a;
        font-weight: 600;
    }
    
    /* Cards */
    .support-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background-color: white;
        padding: 1rem;
        border-radius: 0.75rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        color: #64748b;
        font-weight: 500;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
        color: white;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .stButton button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 0.5rem;
    }
    
    .status-operational {
        background: #059669;
    }
    
    .status-degraded {
        background: #eab308;
    }
    
    /* Forms */
    .stForm {
        background: white;
        padding: 2rem;
        border-radius: 0.75rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        border-radius: 0.5rem;
        border: 1px solid #e2e8f0;
        padding: 0.75rem;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 0.5rem;
        padding: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Support header
st.title(t['support_title'])

# Support options tabs
tabs = st.tabs([
    t['support_tabs']['self_service'],
    t['support_tabs']['contact'],
    t['support_tabs']['status']
])

with tabs[0]:
    st.markdown(f"### {t['quick_solutions_title']}")
    
    # Common issues with translations
    with st.expander(t['auth_issues_title']):
        st.markdown(t['auth_issues_content'])
    
    with st.expander(t['connection_issues_title']):
        st.markdown(t['connection_issues_content'])
    
    # Troubleshooting tools
    st.markdown(f"### {t['diagnostic_tools_title']}")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Connection Test", use_container_width=True):
            with st.spinner(t['thinking']):
                st.success("Connection successful!")
        
        if st.button("📊 View Logs", use_container_width=True):
            st.info("Log viewer opening...")

    with col2:
        if st.button("⚡ Speed Test", use_container_width=True):
            with st.spinner(t['thinking']):
                st.success("Latency: 120ms")
        
        if st.button("🔄 Clear Cache", use_container_width=True):
            st.success("Cache cleared successfully")

with tabs[1]:
    st.markdown(f"### {t['contact_form_title']}")
    
    # Support ticket form
    with st.form("support_ticket"):
        cols = st.columns([2, 1])
        with cols[0]:
            email = st.text_input(t['email_label'])
        with cols[1]:
            priority = st.selectbox(
                t['priority_label'],
                ["Low", "Medium", "High", "Critical"]
            )
        
        issue_type = st.selectbox(
            "Issue Type",
            ["Technical Problem", "Account Issue", "Billing Question", 
             "Feature Request", "Security Concern", "Other"]
        )
        
        description = st.text_area(t['message_label'])
        
        cols = st.columns(2)
        with cols[0]:
            st.file_uploader(t['attachment_label'], accept_multiple_files=True)
        with cols[1]:
            st.selectbox(t['contact_method'], ["Email", "Phone", "Video Call"])
        
        if st.form_submit_button(t['send_button'], use_container_width=True):
            st.success(t['success_message'])

with tabs[2]:
    st.markdown(f"### {t['system_status_title']}")
    
    # Current status
    services = {
        "API Service": {"status": "Operational", "uptime": "99.99%"},
        "Dashboard": {"status": "Operational", "uptime": "99.95%"},
        "Database": {"status": "Operational", "uptime": "99.99%"},
        "Auth Service": {"status": "Operational", "uptime": "100%"},
        "Storage": {"status": "Degraded", "uptime": "98.5%"},
    }
    
    # Display status
    for service, details in services.items():
        cols = st.columns([2, 1, 1])
        with cols[0]:
            status_color = "🟢" if details["status"] == "Operational" else "🟡"
            st.markdown(f"{status_color} **{service}**")
        with cols[1]:
            st.markdown(details["status"])
        with cols[2]:
            st.markdown(details["uptime"])
    
    # Incident history
    st.markdown("### Recent Incidents")
    with st.expander("View History"):
        st.markdown("""
        **March 18, 2024 - API Latency**  
        *Resolved* - Increased latency due to database optimization
        
        **March 15, 2024 - Storage Service**  
        *Resolved* - Intermittent access issues during maintenance
        """)
    
    # Maintenance schedule
    st.info("""
    **Scheduled Maintenance**  
    Next window: March 25, 2024 (02:00-04:00 UTC)  
    Impact: Minor API disruption expected
    """) 