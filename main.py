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

# Professional Design System
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
<style>
    /* ===== Design System Variables ===== */
    :root {
        --primary-color: #2D3748;
        --secondary-color: #4A5568;
        --accent-color: #667EEA;
        --accent-hover: #5A67D8;
        --success-color: #48BB78;
        --warning-color: #ED8936;
        --danger-color: #F56565;
        --background: #F7FAFC;
        --surface: #FFFFFF;
        --border: #E2E8F0;
        --text-primary: #1A202C;
        --text-secondary: #718096;
        --text-muted: #A0AEC0;
        --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
    }

    /* ===== Hide Streamlit Branding ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* ===== Base Layout ===== */
    .stApp {
        background: var(--background);
    }

    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* ===== Professional Typography ===== */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Playfair Display', serif;
        color: var(--text-primary);
        font-weight: 700;
        line-height: 1.2;
        letter-spacing: -0.02em;
    }

    h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }

    h2 {
        font-size: 1.875rem;
        margin-bottom: 1rem;
    }

    h3 {
        font-size: 1.5rem;
        margin-bottom: 0.75rem;
    }

    p, .stMarkdown {
        color: var(--text-secondary);
        line-height: 1.6;
        font-size: 0.95rem;
    }

    /* ===== Enhanced Tab System ===== */
    .stTabs {
        background: var(--surface);
        border-radius: var(--radius-lg);
        padding: 0.5rem;
        box-shadow: var(--shadow-md);
        margin-bottom: 2rem;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: transparent;
        border-bottom: none;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 2rem;
        background: transparent;
        border-radius: var(--radius-md);
        font-weight: 600;
        font-size: 0.95rem;
        color: var(--text-secondary);
        border: none;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        letter-spacing: 0.01em;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: var(--background);
        color: var(--accent-color);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
        color: white !important;
        box-shadow: var(--shadow-md);
    }

    .stTabs [data-baseweb="tab-panel"] {
        padding: 2rem 0.5rem 0 0.5rem;
    }

    /* ===== Professional Cards ===== */
    .professional-card {
        background: var(--surface);
        border-radius: var(--radius-lg);
        padding: 2rem;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 1.5rem;
    }

    .professional-card:hover {
        box-shadow: var(--shadow-lg);
        transform: translateY(-2px);
    }

    .card-compact {
        background: var(--surface);
        border-radius: var(--radius-md);
        padding: 1.25rem;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border);
        transition: all 0.2s ease;
        margin-bottom: 1rem;
    }

    .card-compact:hover {
        box-shadow: var(--shadow-md);
        border-color: var(--accent-color);
    }

    /* ===== Enhanced Buttons ===== */
    .stButton > button {
        border-radius: var(--radius-md);
        font-weight: 600;
        font-size: 0.95rem;
        padding: 0.75rem 2rem;
        border: none;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        letter-spacing: 0.025em;
        box-shadow: var(--shadow-sm);
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
        color: white;
    }

    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }

    .stButton > button[kind="secondary"] {
        background: var(--surface);
        color: var(--accent-color);
        border: 2px solid var(--accent-color);
    }

    .stButton > button[kind="secondary"]:hover {
        background: var(--accent-color);
        color: white;
    }

    /* ===== Modern Input Fields ===== */
    .stTextInput label,
    .stTextArea label,
    .stSelectbox label,
    .stNumberInput label {
        font-weight: 600 !important;
        color: var(--text-primary) !important;
        font-size: 0.9rem !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: 0.01em !important;
    }

    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div,
    .stNumberInput > div > div > input {
        background: var(--surface) !important;
        border: 2px solid var(--border) !important;
        border-radius: var(--radius-md) !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.95rem !important;
        color: var(--text-primary) !important;
        transition: all 0.2s ease !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div:focus-within,
    .stNumberInput > div > div > input:focus {
        border-color: var(--accent-color) !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        outline: none !important;
    }

    .stTextArea > div > div > textarea {
        min-height: 120px !important;
    }

    /* ===== Enhanced Alerts ===== */
    .stAlert {
        border-radius: var(--radius-md) !important;
        border: none !important;
        padding: 1rem 1.25rem !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }

    .stSuccess {
        background: linear-gradient(135deg, #E6FFFA 0%, #C6F6D5 100%) !important;
        color: #22543D !important;
    }

    .stInfo {
        background: linear-gradient(135deg, #EBF8FF 0%, #BEE3F8 100%) !important;
        color: #2C5282 !important;
    }

    .stWarning {
        background: linear-gradient(135deg, #FFFAF0 0%, #FED7AA 100%) !important;
        color: #7C2D12 !important;
    }

    .stError {
        background: linear-gradient(135deg, #FFF5F5 0%, #FED7D7 100%) !important;
        color: #742A2A !important;
    }

    /* ===== Chat Interface ===== */
    .stChatMessage {
        border-radius: var(--radius-md) !important;
        padding: 1.25rem !important;
        margin-bottom: 1rem !important;
        box-shadow: var(--shadow-sm) !important;
        border: 1px solid var(--border) !important;
    }

    .stChatMessage[data-testid="user-message"] {
        background: linear-gradient(135deg, #EBF4FF 0%, #E9D8FD 100%) !important;
    }

    .stChatMessage[data-testid="assistant-message"] {
        background: var(--surface) !important;
    }

    /* ===== Container Styling ===== */
    .stContainer {
        background: var(--surface);
        border-radius: var(--radius-md);
        padding: 1.5rem;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border);
    }

    /* ===== Column Styling ===== */
    div[data-testid="column"] {
        background: transparent;
        padding: 0 0.75rem;
    }

    /* ===== Divider ===== */
    hr {
        margin: 2rem 0;
        border: none;
        border-top: 1px solid var(--border);
    }

    /* ===== Caption Text ===== */
    .stCaption {
        color: var(--text-muted) !important;
        font-size: 0.85rem !important;
        font-weight: 400 !important;
    }

    /* ===== Spinner ===== */
    .stSpinner > div {
        border-top-color: var(--accent-color) !important;
    }

    /* ===== Scrollbar ===== */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: var(--background);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5A67D8 0%, #6B46C1 100%);
    }

    /* ===== Metric Cards ===== */
    .metric-card {
        background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
        color: white;
        border-radius: var(--radius-md);
        padding: 1.5rem;
        text-align: center;
        box-shadow: var(--shadow-md);
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .metric-label {
        font-size: 0.85rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* ===== Responsive Design ===== */
    @media (max-width: 768px) {
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        h1 {
            font-size: 2rem;
        }

        .stTabs [data-baseweb="tab"] {
            padding: 0 1rem;
            font-size: 0.85rem;
        }

        .professional-card {
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize database
init_db()

# Professional Header
st.markdown("""
<div style="text-align: center; padding: 2rem 0 3rem 0;">
    <h1 style="font-size: 3rem; margin-bottom: 0.5rem; background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
        🧪 AromaLens
    </h1>
    <p style="font-size: 1.1rem; color: #718096; font-weight: 500; margin: 0;">
        Professional Perfume Compound Analysis & Development Platform
    </p>
</div>
""", unsafe_allow_html=True)

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
