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
    /* ===== Design System Variables - Navy Blue Theme ===== */
    :root {
        --primary-color: #0A1F44;
        --secondary-color: #1E3A5F;
        --accent-color: #1E3A8A;
        --accent-hover: #1E40AF;
        --accent-light: #3B82F6;
        --navy-dark: #0C1E3A;
        --navy-medium: #1E3A8A;
        --navy-light: #3B82F6;
        --navy-gradient: linear-gradient(135deg, #0A1F44 0%, #1E3A8A 50%, #3B82F6 100%);
        --success-color: #10B981;
        --warning-color: #F59E0B;
        --danger-color: #EF4444;
        --background: #F8FAFC;
        --surface: #FFFFFF;
        --border: #E2E8F0;
        --text-primary: #0F172A;
        --text-secondary: #475569;
        --text-muted: #94A3B8;
        --shadow-sm: 0 1px 3px 0 rgba(10, 31, 68, 0.1);
        --shadow-md: 0 4px 6px -1px rgba(10, 31, 68, 0.15);
        --shadow-lg: 0 10px 15px -3px rgba(10, 31, 68, 0.2);
        --shadow-xl: 0 20px 25px -5px rgba(10, 31, 68, 0.25);
        --shadow-navy: 0 8px 20px rgba(30, 58, 138, 0.3);
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
    }

    /* ===== Hide Streamlit Branding ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* ===== Base Layout - Mobile Optimized ===== */
    .stApp {
        background: linear-gradient(to bottom, #F8FAFC 0%, #EFF6FF 100%);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 100%;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    @media (min-width: 768px) {
        .block-container {
            max-width: 900px;
            margin: 0 auto;
            padding-left: 2rem;
            padding-right: 2rem;
        }
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

    /* ===== Enhanced Tab System - Mobile First ===== */
    .stTabs {
        background: var(--surface);
        border-radius: var(--radius-lg);
        padding: 0.75rem 0.5rem;
        box-shadow: var(--shadow-navy);
        margin-bottom: 2rem;
        border: 1px solid rgba(30, 58, 138, 0.1);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: transparent;
        border-bottom: none;
        display: flex;
        justify-content: space-between;
    }

    .stTabs [data-baseweb="tab"] {
        height: auto;
        min-height: 60px;
        padding: 1rem 0.75rem;
        background: transparent;
        border-radius: var(--radius-md);
        font-weight: 700;
        font-size: 0.95rem;
        color: var(--text-secondary);
        border: 2px solid transparent;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        letter-spacing: 0.02em;
        flex: 1;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 0.25rem;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(30, 58, 138, 0.05);
        color: var(--navy-medium);
        border-color: rgba(30, 58, 138, 0.2);
    }

    .stTabs [aria-selected="true"] {
        background: var(--navy-gradient);
        color: #FFFFFF !important;
        box-shadow: var(--shadow-navy);
        border-color: transparent;
    }

    /* Fix emoji and text visibility in active tabs */
    .stTabs [aria-selected="true"] span {
        color: #FFFFFF !important;
    }

    .stTabs [data-baseweb="tab-panel"] {
        padding: 1.5rem 0 0 0;
    }

    @media (min-width: 768px) {
        .stTabs [data-baseweb="tab"] {
            padding: 1rem 1.5rem;
            font-size: 1.05rem;
        }
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
        background: var(--navy-gradient);
        color: white;
        box-shadow: var(--shadow-navy);
    }

    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 28px rgba(30, 58, 138, 0.4);
    }

    .stButton > button[kind="secondary"] {
        background: var(--surface);
        color: var(--navy-medium);
        border: 2px solid var(--navy-medium);
    }

    .stButton > button[kind="secondary"]:hover {
        background: var(--navy-medium);
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
        border-color: var(--navy-medium) !important;
        box-shadow: 0 0 0 3px rgba(30, 58, 138, 0.15) !important;
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
        background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%) !important;
        border-left: 4px solid var(--navy-medium);
    }

    .stChatMessage[data-testid="assistant-message"] {
        background: var(--surface) !important;
        border-left: 4px solid var(--navy-light);
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
        border-top-color: var(--navy-medium) !important;
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
        background: var(--navy-gradient);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
    }

    /* ===== Metric Cards ===== */
    .metric-card {
        background: var(--navy-gradient);
        color: white;
        border-radius: var(--radius-md);
        padding: 1.5rem;
        text-align: center;
        box-shadow: var(--shadow-navy);
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

# Professional Header with Attractive Title
st.markdown("""
<div style="text-align: center; padding: 1rem 0 1.5rem 0; background: linear-gradient(135deg, rgba(10,31,68,0.03) 0%, rgba(30,58,138,0.05) 100%); border-radius: 16px; margin-bottom: 1.5rem;">
    <h1 style="font-size: clamp(1.75rem, 7vw, 2.5rem); margin-bottom: 0.5rem; background: linear-gradient(135deg, #0A1F44 0%, #1E3A8A 50%, #3B82F6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-weight: 800; letter-spacing: -0.02em;">
        AromaLens
    </h1>
    <p style="font-size: clamp(0.85rem, 2.5vw, 1rem); color: #475569; font-weight: 600; margin: 0;">
        Craft Perfect Fragrances with AI
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
