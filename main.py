import streamlit as st
import json
st.set_page_config(
    layout="wide",
    page_title="AromaLens - AI Perfume Analysis",
    page_icon="🌸"
)
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Crimson+Pro:wght@400;600&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True
)

def local_css():
    st.markdown(
        """
        <style>
        /* Modern Professional Theme */
        :root {
            --primary: #2C3E50;
            --secondary: #3498DB;
            --accent: #E74C3C;
            --light: #ECF0F1;
            --dark: #1A252F;
            --success: #27AE60;
            --gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }

        /* Base App Styling */
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Hide Streamlit Branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Modern Card Design */
        .modern-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.18);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .modern-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 48px rgba(0, 0, 0, 0.12);
        }

        /* Header Typography */
        .main-title {
            font-family: 'Crimson Pro', serif;
            font-size: clamp(2rem, 4vw, 3.5rem);
            font-weight: 600;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
            line-height: 1.2;
        }

        .subtitle {
            font-size: clamp(0.9rem, 1.5vw, 1.1rem);
            color: #64748B;
            font-weight: 400;
            margin-bottom: 2rem;
        }

        /* Selectbox Styling */
        div[data-testid="stSelectbox"] label {
            font-weight: 600 !important;
            color: #1E293B !important;
            font-size: 0.95rem !important;
            margin-bottom: 0.5rem !important;
        }

        div[data-testid="stSelectbox"] > div > div {
            background: white !important;
            border: 2px solid #E2E8F0 !important;
            border-radius: 12px !important;
            padding: 0.75rem !important;
            font-size: 0.95rem !important;
            transition: all 0.2s ease !important;
        }

        div[data-testid="stSelectbox"] > div > div:hover {
            border-color: #667eea !important;
        }

        div[data-testid="stSelectbox"] > div > div:focus-within {
            border-color: #667eea !important;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        }

        /* Input Fields */
        .stTextInput label,
        .stTextArea label {
            font-weight: 600 !important;
            color: #1E293B !important;
            font-size: 0.95rem !important;
        }

        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            background: white !important;
            border: 2px solid #E2E8F0 !important;
            border-radius: 12px !important;
            padding: 0.75rem 1rem !important;
            font-size: 0.95rem !important;
            color: #1E293B !important;
            transition: all 0.2s ease !important;
        }

        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #667eea !important;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        }

        .stTextArea > div > div > textarea {
            min-height: 150px !important;
            font-family: 'Inter', monospace !important;
        }

        /* Modern Buttons */
        button[kind="primary"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.85rem 2rem !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            letter-spacing: 0.3px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
        }

        button[kind="primary"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4) !important;
        }

        button[kind="primary"]:active {
            transform: translateY(0) !important;
        }

        button[kind="secondary"] {
            background: white !important;
            color: #667eea !important;
            border: 2px solid #667eea !important;
            border-radius: 12px !important;
            padding: 0.85rem 2rem !important;
            font-weight: 600 !important;
        }

        /* Results Card */
        .results-card {
            background: white;
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
            margin-top: 1.5rem;
            border: 1px solid #E2E8F0;
        }

        .note-section {
            margin-bottom: 2rem;
            padding: 1.5rem;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 16px;
            border-left: 4px solid #667eea;
        }

        .note-section:nth-child(2) {
            border-left-color: #764ba2;
        }

        .note-section:nth-child(3) {
            border-left-color: #f093fb;
        }

        .note-title {
            font-family: 'Crimson Pro', serif;
            font-size: 1.4rem;
            font-weight: 600;
            color: #1E293B;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .note-item {
            background: white;
            padding: 1rem 1.25rem;
            border-radius: 12px;
            margin-bottom: 0.75rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
            transition: all 0.2s ease;
        }

        .note-item:hover {
            transform: translateX(5px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        }

        .note-name {
            font-weight: 600;
            color: #1E293B;
            font-size: 1rem;
            margin-bottom: 0.25rem;
        }

        .note-reason {
            color: #64748B;
            font-size: 0.9rem;
            line-height: 1.6;
        }

        /* Compound List */
        .compound-list {
            background: white;
            border-radius: 16px;
            padding: 1.5rem;
            margin-top: 1rem;
            border: 1px solid #E2E8F0;
        }

        .compound-title {
            font-weight: 600;
            color: #1E293B;
            font-size: 1.1rem;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .compound-item {
            display: flex;
            justify-content: space-between;
            padding: 0.75rem 1rem;
            background: #F8FAFC;
            border-radius: 10px;
            margin-bottom: 0.5rem;
            transition: all 0.2s ease;
        }

        .compound-item:hover {
            background: #F1F5F9;
            transform: scale(1.02);
        }

        .compound-name {
            font-weight: 500;
            color: #334155;
        }

        .compound-percentage {
            font-weight: 600;
            color: #667eea;
            background: rgba(102, 126, 234, 0.1);
            padding: 0.25rem 0.75rem;
            border-radius: 6px;
            font-size: 0.85rem;
        }

        /* Info Messages */
        .stAlert {
            border-radius: 12px !important;
            border: none !important;
            padding: 1rem 1.25rem !important;
        }

        /* Success Message */
        .stSuccess {
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%) !important;
            color: #155724 !important;
        }

        /* Spinner */
        .stSpinner > div {
            border-top-color: #667eea !important;
        }

        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }

        ::-webkit-scrollbar-track {
            background: #F1F5F9;
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .modern-card {
                padding: 1.5rem;
            }

            .main-title {
                font-size: 2rem;
            }

            .note-section {
                padding: 1rem;
            }

            button[kind="primary"] {
                width: 100% !important;
            }
        }

        /* Column Spacing */
        div[data-testid="column"] {
            padding: 0 1rem;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


local_css()

from core.rule_based import get_heuristic_notes
from core.prompt_builder import build_prompt
from core.llm_interface import query_llm
from core.data_loader import load_presets

# Loading presets JSON
PRESETS_FILE = "data/presets.json"
presets = load_presets(PRESETS_FILE)

# Two columns layout: left for inputs, right for output
col1, col2 = st.columns([1.2, 1.5], gap="large")

with col1:
    st.markdown(
        '''
        <div class="modern-card">
            <h1 class="main-title">AromaLens</h1>
            <p class="subtitle">AI-Powered Perfume Composition Analysis</p>
        </div>
        ''',
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Dropdown for selecting a preset or manual entry
    compound_option = st.selectbox(
        "Select Composition",
        ["Add a new compound"] + list(presets.keys()),
        help="Choose an existing composition or create a new one"
    )

    if compound_option != "Add a new compound":
        chemicals = presets[compound_option]
        heuristics = get_heuristic_notes(chemicals)
        prompt = build_prompt(chemicals, heuristics)
        st.session_state["prompt"] = prompt
        st.session_state["chemicals"] = chemicals
    else:
        st.info("📝 Enter fragrance ingredients and percentages manually (one per line: INGREDIENT: %)")
        manual_input = st.text_area(
            "Composition Formula",
            placeholder="Example:\nBERGAMOT OIL: 15\nLIMONENE: 10\nHEDIONE: 25",
            help="Enter each ingredient on a new line with its percentage"
        )
        chemicals = {}
        if manual_input:
            try:
                for line in manual_input.strip().splitlines():
                    name, pct = line.split(":")
                    chemicals[name.strip()] = float(pct.strip())
            except Exception:
                st.error("Invalid format. Please use 'CHEMICAL NAME: %' per line.")

    # Show chemicals if any (both preset or manual)
    if chemicals:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            '''
            <div class="compound-list">
                <div class="compound-title">
                    <span>🧪</span> Current Composition
                </div>
            ''',
            unsafe_allow_html=True
        )

        for name, pct in chemicals.items():
            st.markdown(
                f'''
                <div class="compound-item">
                    <span class="compound-name">{name}</span>
                    <span class="compound-percentage">{pct}%</span>
                </div>
                ''',
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # If adding a new compound, allow naming & saving it
    if compound_option == "Add a new compound":
        st.markdown("<br>", unsafe_allow_html=True)
        new_name = st.text_input("💾 Save Composition As", placeholder="Enter a name for this composition")
        if st.button("Save Composition", type="primary"):
            if new_name.strip() == "":
                st.error("⚠️ Please enter a valid name.")
            else:
                presets[new_name] = chemicals
                with open(PRESETS_FILE, "w") as f:
                    json.dump(presets, f, indent=2)
                st.success(f"✅ Composition '{new_name}' saved successfully!")

    # Build prompt & heuristics for further processing if chemicals exist
    if chemicals:
        heuristics = get_heuristic_notes(chemicals)
        prompt = build_prompt(chemicals, heuristics)
        st.session_state["prompt"] = prompt
        st.session_state["chemicals"] = chemicals
    else:
        st.session_state["prompt"] = None

    # Generate notes button logic
    if st.session_state.get("prompt"):
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔬 Analyze Composition", type="primary", use_container_width=True):
            st.session_state["generate_clicked"] = True
    else:
        st.session_state["generate_clicked"] = False

def build_notes_html(notes, title, emoji, color="#667eea"):
    if not notes:
        return f'''
            <div class="note-section" style="border-left-color: {color};">
                <div class="note-title">{emoji} {title}</div>
                <p style="color: #94A3B8; font-style: italic;">No {title.lower()} detected in this composition.</p>
            </div>
        '''

    html = f'''
        <div class="note-section" style="border-left-color: {color};">
            <div class="note-title">{emoji} {title}</div>
    '''

    for item in notes:
        name = item.get("name", "Unknown")
        reason = item.get("reason", "")
        html += f'''
            <div class="note-item">
                <div class="note-name">{name}</div>
                <div class="note-reason">{reason}</div>
            </div>
        '''

    html += "</div>"
    return html


with col2:
    if st.session_state.get("generate_clicked", False) and st.session_state.get("prompt"):
        with st.spinner("🔬 Analyzing composition with AI..."):
            response = query_llm(st.session_state["prompt"])

        if "error" in response:
            st.error(f"❌ Analysis Error: {response['error']}")
        else:
            st.success("✅ Analysis Complete!")

            top_html = build_notes_html(response.get("top_notes"), "Top Notes", "🍋", "#667eea")
            middle_html = build_notes_html(response.get("middle_notes"), "Heart Notes", "🌸", "#764ba2")
            base_html = build_notes_html(response.get("base_notes"), "Base Notes", "🌲", "#f093fb")

            uncertain = response.get("uncertain")
            uncertain_html = ""
            if uncertain:
                uncertain_html = '''
                    <div class="note-section" style="border-left-color: #f59e0b;">
                        <div class="note-title">⚠️ Uncertain Notes</div>
                '''
                for item in uncertain:
                    uncertain_html += f'''
                        <div class="note-item">
                            <div class="note-name">{item.get('name', 'Unknown')}</div>
                            <div class="note-reason">Further analysis recommended</div>
                        </div>
                    '''
                uncertain_html += "</div>"

            full_html = f'''
            <div class="results-card">
                <h2 style="font-family: 'Crimson Pro', serif; color: #1E293B; margin-bottom: 1.5rem;">
                    Analysis Results
                </h2>
                {top_html}
                {middle_html}
                {base_html}
                {uncertain_html}
            </div>
            '''
            st.markdown(full_html, unsafe_allow_html=True)
    else:
        st.markdown(
            '''
            <div class="modern-card" style="text-align: center; padding: 3rem 2rem;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">🌸</div>
                <h3 style="font-family: 'Crimson Pro', serif; color: #1E293B; margin-bottom: 1rem;">
                    Ready to Analyze
                </h3>
                <p style="color: #64748B; font-size: 1rem;">
                    Select or create a composition on the left, then click "Analyze Composition" to get detailed fragrance notes analysis.
                </p>
            </div>
            ''',
            unsafe_allow_html=True
        )