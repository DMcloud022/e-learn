import streamlit as st
from utils import get_translation
import json
from config.languages import TRANSLATIONS

# Get current language
if "language" not in st.session_state:
    st.session_state.language = "English"
t = TRANSLATIONS[st.session_state.language]

# Page config
st.set_page_config(
    page_title=f"{t['nav_api_reference']} - TechSolutions",
    page_icon=None,
    layout="wide"
)

# Page header
st.title(t['nav_api_reference'])
st.markdown("Complete reference documentation for the TechSolutions API")

# Sidebar navigation
with st.sidebar:
    st.title(t['nav_api_reference'])
    endpoint_section = st.radio(
        label="Select API Section",
        options=list(t['api_sections'].values()),
        label_visibility="collapsed"
    )

# Main content
if endpoint_section == t['api_sections']['authentication']:
    st.header(t['api_sections']['authentication'])
    st.markdown("""
    The TechSolutions API uses API keys for authentication. You can manage your API keys in the 
    [Dashboard Settings](https://dashboard.techsolutions.com/settings/api).
    """)
    
    # Authentication examples
    with st.expander("API Key Authentication"):
        st.code("""
        # Include in HTTP header
        Authorization: Bearer your_api_key

        # Python example
        import requests
        
        headers = {
            'Authorization': 'Bearer your_api_key',
            'Content-Type': 'application/json'
        }
        
        response = requests.get('https://api.techsolutions.com/v1/projects', headers=headers)
        """)
    
    with st.expander("OAuth 2.0"):
        st.code("""
        POST /oauth/token
        
        {
            "grant_type": "client_credentials",
            "client_id": "your_client_id",
            "client_secret": "your_client_secret"
        }
        """)

elif endpoint_section == t['api_sections']['projects']:
    st.header(t['api_sections']['projects'])
    
    endpoints = {
        "List Projects": {
            "method": "GET",
            "path": "/v1/projects",
            "description": "Returns a list of projects",
            "parameters": [
                {"name": "limit", "type": "integer", "description": "Maximum number of records"},
                {"name": "offset", "type": "integer", "description": "Number of records to skip"}
            ],
            "response": {
                "projects": [
                    {"id": "proj_123", "name": "Example Project", "created_at": "2024-03-20T10:00:00Z"}
                ]
            }
        },
        "Create Project": {
            "method": "POST",
            "path": "/v1/projects",
            "description": "Creates a new project",
            "parameters": [
                {"name": "name", "type": "string", "required": True, "description": "Project name"},
                {"name": "description", "type": "string", "description": "Project description"}
            ],
            "response": {
                "id": "proj_123",
                "name": "New Project",
                "created_at": "2024-03-20T10:00:00Z"
            }
        }
    }
    
    for name, details in endpoints.items():
        with st.expander(f"{details['method']} {name}"):
            st.markdown(f"**{details['description']}**")
            st.markdown(f"`{details['method']} {details['path']}`")
            
            if details.get('parameters'):
                st.markdown("#### Parameters")
                for param in details['parameters']:
                    required = "required" if param.get('required') else "optional"
                    st.markdown(f"- `{param['name']}` ({param['type']}, {required}): {param['description']}")
            
            st.markdown("#### Response")
            st.json(details['response'])
            
            # Example request
            st.markdown("#### Example Request")
            if details['method'] == 'GET':
                st.code(f"""
                curl -X GET \\
                  https://api.techsolutions.com{details['path']} \\
                  -H 'Authorization: Bearer your_api_key'
                """)
            else:
                st.code(f"""
                curl -X {details['method']} \\
                  https://api.techsolutions.com{details['path']} \\
                  -H 'Authorization: Bearer your_api_key' \\
                  -H 'Content-Type: application/json' \\
                  -d '{json.dumps({"name": "Example", "description": "Test project"}, indent=2)}'
                """)

# API Status
st.divider()
st.markdown("### API Status")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Uptime", "99.99%", "0.01%")

with col2:
    st.metric("Avg Response Time", "45ms", "-5ms")

with col3:
    st.metric("Requests/sec", "1.2K", "8%")

# Resources
st.divider()
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Tools")
    st.markdown("""
    - [API Explorer](/explorer)
    - [Status Dashboard](/status)
    - [Rate Limit Calculator](/rate-limits)
    """)

with col2:
    st.markdown("### SDKs")
    st.markdown("""
    - [Python SDK](https://github.com/techsolutions/python-sdk)
    - [JavaScript SDK](https://github.com/techsolutions/js-sdk)
    - [Java SDK](https://github.com/techsolutions/java-sdk)
    - [Go SDK](https://github.com/techsolutions/go-sdk)
    """)

# Download OpenAPI Spec
st.divider()
col1, col2 = st.columns(2)

with col1:
    st.download_button(
        "Download OpenAPI Specification",
        "OpenAPI spec content",
        file_name="openapi.yaml",
        mime="application/yaml",
        use_container_width=True
    )

with col2:
    st.download_button(
        "Download Postman Collection",
        "Postman collection content",
        file_name="techsolutions.postman_collection.json",
        mime="application/json",
        use_container_width=True
    )
