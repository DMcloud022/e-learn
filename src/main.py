import streamlit as st
from chatbot import Chatbot
from utils import load_company_data, get_translation
from config.languages import TRANSLATIONS
import smtplib
from email.mime.text import MIMEText
import time
from datetime import datetime
import pytz
import base64
import os

# Page configuration
st.set_page_config(
    page_title="TechSolutions Assistant",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
def load_custom_css():
    css_path = os.path.join(os.path.dirname(__file__), 'static', 'style.css')
    try:
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading CSS: {str(e)}")

def load_local_css():
    with open('src/static/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def load_local_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return f"data:image/png;base64,{encoded_string}"

def send_email(recipient_email, subject, message):
    """Send email to company representative"""
    try:
        company_data = load_company_data()
        company_email = company_data['contact']['email']
        
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = recipient_email
        msg['To'] = company_email
        
        # Configure your SMTP settings here
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(company_email, st.secrets["EMAIL_PASSWORD"])
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Error sending email: {str(e)}")
        return False

def main():
    load_custom_css()

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "language" not in st.session_state:
        st.session_state.language = "English"
    if "chat_started" not in st.session_state:
        st.session_state.chat_started = False
    if "selected_language" not in st.session_state:
        st.session_state.selected_language = "English"
    if "max_messages" not in st.session_state:
        st.session_state.max_messages = 20
    if "company_data" not in st.session_state:
        st.session_state.company_data = load_company_data()
    if "needs_rerun" not in st.session_state:
        st.session_state.needs_rerun = False

    # Sidebar navigation
    with st.sidebar:
        # Custom CSS for sidebar
        st.markdown("""
            <style>
            [data-testid="stSidebar"] {
                background-color: #ffffff;
                border-right: 1px solid #e2e8f0;
            }
            .sidebar-header {
                padding: 2rem 1.5rem;
                margin: -1rem -1rem 0 -1rem;
                background: linear-gradient(to right, #1e3a8a, #2563eb);
                color: white;
            }
            .sidebar-section {
                padding: 1.5rem;
                border-bottom: 1px solid #e2e8f0;
                margin: 0;
            }
            .sidebar-title {
                font-size: 0.75rem;
                font-weight: 600;
                color: #64748b;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                margin-bottom: 1rem;
            }
            /* Radio button improvements */
            .stRadio > div {
                display: flex !important;
                flex-direction: column !important;
                gap: 0.5rem !important;
            }
            .stRadio > div > label {
                padding: 0.75rem !important;
                background-color: #f8fafc !important;
                border: 1px solid #e2e8f0 !important;
                border-radius: 0.375rem !important;
                color: #475569 !important;
                font-size: 0.875rem !important;
                transition: all 0.2s !important;
            }
            .stRadio > div > label:hover {
                background-color: #f1f5f9 !important;
                border-color: #cbd5e1 !important;
            }
            .stRadio > div > label[data-checked="true"] {
                background-color: #e0f2fe !important;
                border-color: #2563eb !important;
                color: #1e40af !important;
            }
            /* Select box improvements */
            .stSelectbox > div > div {
                padding: 0.75rem !important;
                border-radius: 0.375rem !important;
                border-color: #e2e8f0 !important;
                font-size: 0.875rem !important;
            }
            /* Navigation buttons */
            .nav-button {
                display: block;
                width: 100%;
                padding: 0.75rem 1rem !important;
                margin-bottom: 0.25rem !important;
                text-align: left !important;
                background: white !important;
                border: 1px solid #e2e8f0 !important;
                border-radius: 0.375rem !important;
                color: #1a202c !important;  /* Dark text for white background */
                font-size: 0.875rem !important;
                transition: all 0.2s !important;
                text-decoration: none !important;
            }
            .nav-button:hover {
                background-color: #f8fafc !important;
                border-color: #2563eb !important;
                color: #2563eb !important;
            }
            .nav-button.active {
                background-color: #2563eb !important;
                border-color: #2563eb !important;
                color: white !important;  /* White text for blue background */
                font-weight: 500 !important;
            }
            </style>
        """, unsafe_allow_html=True)

        # Company logo/header
        st.markdown("""
            <div class="sidebar-header">
                <h1 style='font-size: 1.5rem; font-weight: 600; margin: 0;'>
                    Coral System
                </h1>
                <p style='font-size: 0.875rem; opacity: 0.9; margin: 0.5rem 0 0 0;'>
                    AI Support Portal
                </p>
            </div>
        """, unsafe_allow_html=True)

        # Navigation section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)

        nav_items = {
            "/": "Chat",
            "/API_Reference": "API Reference",
            "/Documentation": "Documentation",
            "/FAQ": "FAQ",
            "/Support": "Support"
        }

        # Get current page from URL
        current_path = st.query_params.get("page", "/")

        # Navigation links
        for path, label in nav_items.items():
            st.markdown(
                f"""<a href="{path}" 
                    class="nav-button {'active' if current_path == path.replace('/', '') else ''}"
                    target="_self">
                    {label}
                </a>""",
                unsafe_allow_html=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

        # Language section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">Language</div>', unsafe_allow_html=True)
        selected_lang = st.selectbox(
            "Select Language",
            ["English", "日本語", "Filipino"],
            format_func=lambda x: x,
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # Chat Mode section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">Chat Mode</div>', unsafe_allow_html=True)
        chat_mode = st.radio(
            "Select AI Mode",
            ["Company Assistant", "General AI"],
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # Support Type section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">Support Type</div>', unsafe_allow_html=True)
        interaction_mode = st.radio(
            "How can we help?",
            ["AI Assistant", "Contact Form"],
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # Version info at bottom
        st.markdown("""
            <div style='position: fixed; bottom: 0; left: 0; right: 0; 
                        padding: 1rem; text-align: center; font-size: 0.75rem; 
                        color: #64748b; background: linear-gradient(to top, white 80%, transparent);
                        border-top: 1px solid #e2e8f0;'>
                <div style='font-weight: 500;'>Coral System Technologies Inc.</div>
                <div style='margin-top: 0.25rem; opacity: 0.8;'>Version 1.0.0</div>
            </div>
        """, unsafe_allow_html=True)

    # Main Content Area
    if "AI Assistant" in interaction_mode:
        # Chat container with custom styling
        st.markdown("""
            <style>
            /* Global styles */
            .stApp {
                background-color: #f8fafc;
            }
            
            /* Chat container */
            .chat-container {
                max-width: 1000px;
                margin: 0 auto;
                padding: 1.5rem;
                height: calc(100vh - 80px);
                display: flex;
                flex-direction: column;
                background: white;
                border-radius: 1rem;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }
            
            /* Chat header */
            .chat-header {
                background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
                color: white;
                padding: 2rem;
                border-radius: 0.75rem 0.75rem 0 0;
                margin: -1.5rem -1.5rem 1.5rem -1.5rem;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }
            
            /* Messages container */
            .messages-container {
                flex: 1;
                overflow-y: auto;
                padding: 1rem;
                display: flex;
                flex-direction: column;
                gap: 1.5rem;
                scroll-behavior: smooth;
                height: calc(100vh - 200px);
            }
            
            /* Message bubbles */
            .message-container {
                display: flex;
                gap: 1.5rem;
                margin: 2rem 0;
                padding: 0.75rem;
                align-items: flex-start;
                animation: slideIn 0.3s ease-out;
            }
            
            /* User message specific */
            .user-message {
                flex-direction: row-reverse;  /* Reverse direction for user messages */
                margin-left: auto;  /* Push to right side */
            }
            
            /* Message content */
            .message-content {
                padding: 1.25rem 1.75rem;
                border-radius: 1.25rem;
                max-width: 80%;
                line-height: 1.7;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                transition: all 0.2s ease;
            }
            
            .user-message .message-content {
                margin-right: 0;  /* Align to avatar */
                margin-left: 0;   /* Reset auto margin */
                background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%);
                color: white;
                border-bottom-right-radius: 0.5rem;
            }
            
            .assistant-message .message-content {
                margin-left: 0;  /* Align to avatar */
                background: white;
                border: 1px solid #e2e8f0;
                border-bottom-left-radius: 0.5rem;
            }
            
            /* Avatar positioning */
            .user-message .avatar {
                margin-left: 0;  /* Reset margin for user avatar */
            }
            
            .assistant-message .avatar {
                margin-right: 0;  /* Reset margin for assistant avatar */
            }
            
            /* Avatar */
            .avatar {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                flex-shrink: 0;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 500;
                background-size: cover;
                background-position: center;
            }
            
            .user-avatar {
                background-image: url('https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y');
                color: transparent;
            }
            
            .assistant-avatar {
                background-image: url('https://cdn-icons-png.flaticon.com/512/4712/4712009.png');
                color: transparent;
            }
            
            /* Input area */
            .input-area {
                position: sticky;
                bottom: 0;
                background: white;
                padding: 1rem;
                border-top: 1px solid #e2e8f0;
                margin-top: auto;
            }
            
            .input-container {
                position: fixed;
                bottom: 0;
                left: 0;
                right: 0;
                background: rgba(255, 255, 255, 0.98);
                padding: 1.5rem 2rem;
                border-top: 2px solid #cbd5e1;
                box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.1);
                backdrop-filter: blur(10px);
                z-index: 100;
            }
            
            .input-container .stTextInput {
                margin-bottom: 0;
            }
            
            /* Welcome message */
            .welcome-message {
                text-align: center;
                padding: 4rem 2rem;
                color: #64748b;
                background: white;
                border-radius: 1rem;
                border: 1px solid #e2e8f0;
                margin: 2rem 0;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            }
            
            /* Animations */
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            /* Markdown content */
            .markdown-content h1 {
                font-size: 1.5rem;
                font-weight: 600;
                margin: 1.5rem 0 1rem 0;
                color: #111827;
            }
            
            .markdown-content h2 {
                font-size: 1.25rem;
                font-weight: 600;
                margin: 1.25rem 0 0.75rem 0;
                color: #1f2937;
            }
            
            .markdown-content ul {
                margin: 0.75rem 0;
                padding-left: 1.5rem;
            }
            
            .markdown-content li {
                margin: 0.5rem 0;
                line-height: 1.6;
            }
            
            .markdown-content p {
                margin: 0.75rem 0;
                line-height: 1.6;
            }
            
            .markdown-content pre {
                margin: 1rem 0;
                background-color: #1e293b;
                padding: 1.25rem;
                border-radius: 0.75rem;
                overflow-x: auto;
            }
            
            .markdown-content pre code {
                color: #e2e8f0;
                background-color: transparent;
            }
            
            /* Input styling */
            .stTextInput input {
                border: 2px solid #94a3b8 !important;  /* Darker border */
                border-radius: 1.5rem !important;
                padding: 1rem 1.5rem !important;
                font-size: 1rem !important;
                background: white !important;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
                transition: all 0.2s ease !important;
                color: #1e293b !important;  /* Darker text */
            }
            
            .stTextInput input:hover {
                border-color: #64748b !important;  /* Darker hover border */
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
            }
            
            .stTextInput input:focus {
                border-color: #2563eb !important;
                box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.15) !important;
                outline: none !important;
            }
            
            .stButton button {
                border-radius: 1.5rem !important;
                padding: 0.75rem 2rem !important;
                background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%) !important;
                color: white !important;
                font-weight: 600 !important;
                transition: all 0.2s ease !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                gap: 0.5rem !important;
                height: 100% !important;
                box-shadow: 0 2px 8px rgba(37, 99, 235, 0.2) !important;
            }
            
            .stButton button:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 4px 15px rgba(37, 99, 235, 0.25) !important;
            }
            
            /* Adjust message container to prevent overlap */
            .messages-container {
                height: calc(100vh - 220px);
                padding-bottom: 100px;
                margin-bottom: 2rem;
            }
            
            /* Input placeholder */
            .stTextInput input::placeholder {
                color: #64748b !important;  /* Darker placeholder */
                font-weight: 500 !important;
            }
            </style>
        """, unsafe_allow_html=True)

        # Chat header with subtle description
        st.markdown("""
            <div style='text-align: center; margin-bottom: 2rem;'>
                <h1 style='color: #1e3a8a; font-size: 2rem; margin-bottom: 0.5rem;'>Coral System AI Assistant</h1>
                <p style='color: #64748b; font-size: 1rem;'>Ask me anything about our services or any other topic!</p>
            </div>
        """, unsafe_allow_html=True)

        # Message handler
        def handle_message(message):
            if message.strip():
                # Add user message
                st.session_state.messages.append({"role": "user", "content": message})
                
                # Get AI response
                try:
                    chatbot = Chatbot(st.session_state.company_data, mode=chat_mode)
                    with st.spinner(""):
                        response = chatbot.get_response(message, st.session_state.messages[-3:])
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                
                # Clear input and set rerun flag
                st.session_state.user_input = ""
                st.session_state.needs_rerun = True

        # Input handler
        def on_input_change():
            if st.session_state.user_input.strip():
                handle_message(st.session_state.user_input)

        # Chat interface
        chat_container = st.container()
        
        with chat_container:
            # Messages area
            for message in st.session_state.messages:
                role = message["role"]
                content = message["content"]
                
                st.markdown(f"""
                    <div class='message-container {'user-message' if role == 'user' else 'assistant-message'}'>
                        <div class='avatar {'user-avatar' if role == 'user' else 'assistant-avatar'}'></div>
                        <div class='message-content markdown-content'>
                            {content}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            # Welcome message with subtle suggestions
            if not st.session_state.messages:
                st.markdown("""
                    <div class='welcome-message'>
                        <h3>👋 Welcome to Coral System AI</h3>
                        <p>I can help you with:</p>
                        <div class='suggestion-chips'>
                            <span>💻 Technical Support</span>
                            <span>🔧 System Integration</span>
                            <span>📱 Product Information</span>
                            <span>❓ General Inquiries</span>
                        </div>
                        <p class='hint-text'>Type your question below to get started!</p>
                    </div>
                """, unsafe_allow_html=True)

            # Input area
            with st.container():
                cols = st.columns([6, 1])
                with cols[0]:
                    st.text_input(
                        "Message Coral System AI...",
                        key="user_input",
                        label_visibility="collapsed",
                        on_change=on_input_change
                    )
                with cols[1]:
                    st.button("Send", on_click=on_input_change, use_container_width=True)

        # Add subtle styling improvements
        st.markdown("""
            <style>
            /* Welcome message styling */
            .welcome-message {
                text-align: center;
                padding: 2rem 1rem;
                color: #64748b;
                animation: fadeIn 0.5s ease-out;
            }

            .suggestion-chips {
                display: flex;
                gap: 0.75rem;
                justify-content: center;
                flex-wrap: wrap;
                margin: 1.5rem 0;
            }

            .suggestion-chips span {
                background: #f1f5f9;
                padding: 0.5rem 1rem;
                border-radius: 1rem;
                font-size: 0.875rem;
                color: #1e3a8a;
                transition: all 0.2s ease;
                cursor: pointer;
            }

            .suggestion-chips span:hover {
                background: #e2e8f0;
                transform: translateY(-1px);
            }

            .hint-text {
                font-size: 0.875rem;
                color: #94a3b8;
                margin-top: 1.5rem;
            }

            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            </style>
        """, unsafe_allow_html=True)

        # Check if rerun is needed
        if st.session_state.needs_rerun:
            st.session_state.needs_rerun = False
            st.rerun()

    else:
        # Contact form
        st.markdown("""
            <div style='max-width: 800px; margin: 0 auto; padding: 2rem;'>
                <h1>Contact Support</h1>
                <p>Get in touch with our team for personalized assistance.</p>
            </div>
        """, unsafe_allow_html=True)
        
        contact_col1, contact_col2 = st.columns([2, 1])
        
        with contact_col1:
            with st.form("contact_form"):
                email = st.text_input("Email Address")
                subject = st.text_input("Subject")
                message = st.text_area("Message")
                priority = st.selectbox("Priority", ["Normal", "High", "Urgent"])
                
                if st.form_submit_button("Send Message", use_container_width=True):
                    if email and subject and message:
                        with st.spinner("Sending..."):
                            if send_email(email, subject, message):
                                st.success("Message sent successfully.")
                                time.sleep(2)
                                st.rerun()
                    else:
                        st.error("Please fill in all required fields.")
        
        with contact_col2:
            st.markdown("### Business Hours")
            st.markdown("""
            Monday-Friday: 9:00 AM - 6:00 PM PST  
            24/7 Support for Enterprise clients
            
            **Response Times**
            - Urgent: 1-2 hours
            - High: 4-8 hours
            - Normal: 24 hours
            """)

if __name__ == "__main__":
    main() 