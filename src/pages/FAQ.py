import streamlit as st
from utils import load_company_data, get_translation
from config.languages import TRANSLATIONS

# Get current language
if "language" not in st.session_state:
    st.session_state.language = "English"
t = TRANSLATIONS[st.session_state.language]

# Page config
st.set_page_config(
    page_title=f"{t['nav_faq']} - TechSolutions",
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
    
    /* FAQ container */
    .block-container {
        padding: 2rem;
        max-width: 1200px !important;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #1e3a8a;
        font-weight: 600;
    }
    
    /* Search box */
    .stTextInput input {
        border-radius: 0.5rem;
        border: 1px solid #e2e8f0;
        padding: 0.75rem 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Category tabs */
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
    
    /* FAQ items */
    .streamlit-expanderHeader {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 0.75rem;
        padding: 1.25rem;
        margin-bottom: 1rem;
        transition: all 0.2s;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: #2563eb;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .streamlit-expanderContent {
        background: white;
        border: 1px solid #e2e8f0;
        border-top: none;
        border-radius: 0 0 0.75rem 0.75rem;
        padding: 1.5rem;
    }
    
    /* Resource buttons */
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
    
    /* Feedback section */
    .feedback-buttons {
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

# Categories for FAQs with lowercase keys
categories = {
    t['faq_categories']['general'].lower(): ["setup", "basics", "getting started"],
    t['faq_categories']['technical'].lower(): ["api", "integration", "rate limits"],
    t['faq_categories']['billing'].lower(): ["price", "cost", "enterprise"],
    t['faq_categories']['security'].lower(): ["security", "compliance", "encryption"],
    t['faq_categories']['api'].lower(): ["webhooks", "events", "integration"],
    t['faq_categories']['account'].lower(): ["team", "permissions", "access"]
}

# Update the category mapping to ensure exact matches
CATEGORY_MAPPING = {
    'general': 'general',
    'technical': 'technical',
    'billing': 'billing',
    'security': 'security',
    'api': 'api',
    'account': 'account'
}

# Page header with search
st.title("📚 " + t['nav_faq'])
st.markdown("""
<div style='background-color: #f8f9fa; padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 2rem;'>
    <h4>Find answers to common questions about TechSolutions</h4>
    <p>Browse by category or search across all topics. Can't find what you're looking for? Contact our support team.</p>
</div>
""", unsafe_allow_html=True)

# Search box with icon
col1, col2 = st.columns([3, 1])
with col1:
    search = st.text_input(
        label=t['search_label'],
        placeholder="🔍 " + t['search_placeholder'],
        help="Search across all FAQ categories"
    )

with col2:
    st.link_button("📞 Contact Support", "pages/Support.py", use_container_width=True)

# Category tabs - show original capitalized names
tab_labels = [
    t['faq_categories']['general'],
    t['faq_categories']['technical'],
    t['faq_categories']['billing'],
    t['faq_categories']['security'],
    t['faq_categories']['api'],
    t['faq_categories']['account']
]
tabs = st.tabs(tab_labels)

try:
    # Load FAQs with error handling
    company_data = load_company_data()
    faqs = company_data.get('faqs', [])
    print(f"Loaded {len(faqs)} FAQs")  # Debug print
    
    # Add this debug print to see what categories we're working with
    print("Available categories:", [faq.get('category', '').lower() for faq in faqs])
    
    # Add default FAQ if none exists
    if not faqs:
        print("No FAQs found, adding sample")
        faqs = [{
            "id": "sample",
            "category": "general",
            "keywords": ["sample"],
            "question": "Sample FAQ Question",
            "answer": "This is a sample answer. Please add real FAQs to company_data.json"
        }]
    
    # Display FAQs by category
    for tab, (category, keywords) in zip(tabs, categories.items()):
        with tab:
            found_items = False
            # Convert both to lowercase for comparison and handle translations
            current_category = category.lower().strip()
            
            # Debug prints
            print(f"\nProcessing category: {current_category}")
            print(f"Available categories: {[faq.get('category', '').lower() for faq in faqs]}")
            
            # Filter FAQs for current category
            category_faqs = [
                faq for faq in faqs 
                if faq.get('category', '').lower().strip() == current_category
            ]
            
            print(f"Found {len(category_faqs)} FAQs for category {current_category}")
            
            if not category_faqs:
                # Add a sample FAQ for empty categories
                category_faqs = [{
                    "id": f"sample_{current_category}",
                    "category": current_category,
                    "question": f"Sample {current_category.title()} Question",
                    "answer": f"This is a sample answer for the {current_category} category. More content will be added soon."
                }]
            
            # Display FAQs
            for faq in category_faqs:
                try:
                    # Get translated question/answer or fallback to direct content
                    faq_id = faq.get('id', '')
                    if not faq_id:
                        continue
                        
                    question = t.get(f"faq_{faq_id}_question", faq.get('question', ''))
                    answer = t.get(f"faq_{faq_id}_answer", faq.get('answer', ''))
                    
                    if not question or not answer:
                        continue
                    
                    if (not search or 
                        search.lower() in question.lower() or 
                        search.lower() in answer.lower()):
                        
                        found_items = True
                        with st.expander(question):
                            # Answer content
                            st.markdown(answer)
                            
                            # Show related resources based on category
                            st.divider()
                            
                            # Resource buttons based on category
                            if faq['category'] == 'billing':
                                st.markdown("**🔗 Related Resources**")
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.link_button("💰 Pricing Calculator", "/pricing", use_container_width=True)
                                with col2:
                                    st.link_button("📋 Compare Plans", "/packages", use_container_width=True)
                                with col3:
                                    st.link_button("💳 Billing Portal", "/billing", use_container_width=True)
                            
                            elif faq['category'] == 'security':
                                st.markdown("**🔗 Security Resources**")
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.link_button("🔒 Security Center", "/security", use_container_width=True)
                                with col2:
                                    st.link_button("📜 Compliance", "/compliance", use_container_width=True)
                                with col3:
                                    st.link_button("🛡️ Best Practices", "/security/best-practices", use_container_width=True)
                            
                            elif faq['category'] in ['technical', 'api']:
                                st.markdown("**🔗 Developer Resources**")
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.link_button("📚 API Docs", "/docs/api", use_container_width=True)
                                with col2:
                                    st.link_button("💻 Code Examples", "/docs/examples", use_container_width=True)
                                with col3:
                                    st.link_button("🧪 API Explorer", "/api/explorer", use_container_width=True)
                            
                            elif faq['category'] == 'account':
                                st.markdown("**🔗 Account Management**")
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.link_button("👥 Team Settings", "/settings/team", use_container_width=True)
                                with col2:
                                    st.link_button("🔑 API Keys", "/settings/api-keys", use_container_width=True)
                                with col3:
                                    st.link_button("📊 Usage Dashboard", "/dashboard", use_container_width=True)
                            
                            # Feedback buttons
                            st.divider()
                            st.markdown("##### Was this helpful?")
                            col1, col2, _ = st.columns([1, 1, 4])
                            with col1:
                                st.button("👍 Yes", key=f"yes_{faq_id}", use_container_width=True)
                            with col2:
                                st.button("👎 No", key=f"no_{faq_id}", use_container_width=True)
                            
                except Exception as e:
                    st.error(f"Error displaying FAQ: {str(e)}")
                    continue
            
            if not found_items and search:
                st.warning("🔍 " + t.get('no_results_found', 'No matching questions found in this category.'))

except Exception as e:
    st.error(f"Error loading FAQs: {str(e)}")

# Contact options footer
st.divider()
st.markdown("### 👋 Still Need Help?")

# Contact options in columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.link_button(
        "💬 Live Chat",
        "main.py",
        help="Chat with our AI assistant",
        use_container_width=True
    )

with col2:
    st.link_button(
        "📞 Schedule Call",
        "https://calendly.com/techsolutions",
        help="Book a call with our support team",
        use_container_width=True
    )

with col3:
    st.link_button(
        "📧 Email Support",
        "pages/Support.py",
        help="Send us an email",
        use_container_width=True
    )

with col4:
    st.link_button(
        "📚 Documentation",
        "pages/Documentation.py",
        help="Browse our documentation",
        use_container_width=True
    ) 