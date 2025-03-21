import streamlit as st
from utils import get_translation
from config.languages import TRANSLATIONS
import base64

# Get current language
if "language" not in st.session_state:
    st.session_state.language = "English"
t = TRANSLATIONS[st.session_state.language]

# Page config
st.set_page_config(
    page_title=f"{t['nav_documentation']} - TechSolutions",
    page_icon=None,
    layout="wide"
)

# Sidebar navigation
with st.sidebar:
    st.title(t['nav_documentation'])
    section = st.radio(
        label="Select Documentation Section",
        options=list(t['doc_sections'].values()),
        label_visibility="collapsed"
    )

# Main content based on language
if section == t['doc_sections']['getting_started']:
    st.title(t['doc_sections']['getting_started'])
    
    # Quick start guide
    st.markdown("""
    ## Quick Start Guide
    
    Follow these steps to integrate with TechSolutions:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 1. Account Setup
        1. Create account at [dashboard.techsolutions.com](/)
        2. Verify email and complete profile
        3. Generate API keys
        
        ### 2. Installation
        ```bash
        # Using pip
        pip install techsolutions-sdk
        
        # Using Docker
        docker pull techsolutions/sdk
        ```
        """)
    
    with col2:
        st.markdown("""
        ### 3. Basic Usage
        ```python
        from techsolutions import Client
        
        # Initialize client
        client = Client(api_key='your_api_key')
        
        # Create project
        project = client.create_project(
            name="My Project",
            description="Description"
        )
        ```
        """)

elif section == t['doc_sections']['api_reference']:
    st.title(t['doc_sections']['api_reference'])
    
    # API documentation
    st.markdown("""
    ## REST API Endpoints
    
    All API access is over HTTPS and accessed through `https://api.techsolutions.com`.
    All data is sent and received as JSON.
    """)
    
    with st.expander("Authentication"):
        st.code("""
        POST /api/v1/auth/token
        
        {
            "client_id": "your_client_id",
            "client_secret": "your_client_secret"
        }
        """)
    
    with st.expander("Projects API"):
        st.code("""
        # List projects
        GET /api/v1/projects
        
        # Create project
        POST /api/v1/projects
        
        # Get project
        GET /api/v1/projects/{id}
        """)

elif section == t['doc_sections']['sdks']:
    st.title(t['doc_sections']['sdks'])
    
    sdks = {
        "Python": "pip install techsolutions-sdk",
        "JavaScript": "npm install techsolutions-js",
        "Java": "maven install techsolutions-java",
        "Go": "go get github.com/techsolutions/sdk-go"
    }
    
    for lang, install in sdks.items():
        with st.expander(f"{lang} SDK"):
            st.code(install)
            st.markdown(f"[View on GitHub](https://github.com/techsolutions/sdk-{lang.lower()})")

# Download options
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    st.download_button(
        "📥 Download PDF",
        "Documentation PDF content",
        file_name="documentation.pdf",
        mime="application/pdf"
    )

with col2:
    st.download_button(
        "📥 OpenAPI Spec",
        "OpenAPI specification content",
        file_name="openapi.yaml",
        mime="application/yaml"
    )

with col3:
    st.download_button(
        "📥 Postman Collection",
        "Postman collection content",
        file_name="postman_collection.json",
        mime="application/json"
    ) 