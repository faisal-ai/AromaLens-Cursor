"""AromaLens MVP - Perfume Compound Analysis Tool"""
import streamlit as st
from app.db import init_db
from app.ui import create_tab, library_tab, analyze_tab, chat_tab

# Page configuration
st.set_page_config(
    layout="wide",
    page_title="AromaLens - Perfume Analysis",
    page_icon="🧪"
)

# Minimal professional CSS
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Clean container styling */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    /* Professional typography */
    h1, h2, h3 {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
        font-weight: 600;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 1.5rem;
        background-color: transparent;
        border-radius: 8px 8px 0 0;
        font-weight: 500;
    }

    .stTabs [aria-selected="true"] {
        background-color: #f0f2f6;
    }

    /* Button styling */
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }

    /* Input styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div {
        border-radius: 8px;
        border: 1px solid #e0e0e0;
    }

    /* Card-like containers */
    .stContainer {
        background-color: white;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
    }

    /* Info/success/warning messages */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid;
    }

    /* Chat messages */
    .stChatMessage {
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize database
init_db()

# Header
st.title("🧪 AromaLens")
st.caption("Professional Perfume Compound Analysis Tool")
st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📝 Create", "📚 Library", "🔬 Analyze", "💬 Chat"])

with tab1:
    create_tab.render()

with tab2:
    library_tab.render()

with tab3:
    analyze_tab.render()

with tab4:
    chat_tab.render()
