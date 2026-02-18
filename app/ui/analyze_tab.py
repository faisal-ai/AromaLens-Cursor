"""Analyze Tab - Professional LLM-powered compound analysis"""
import streamlit as st
from app.db import get_db
from app.services.compound_crud import get_all_compounds, get_compound
from app.services.analysis import analyze_formula


def render():
    """Render the analyze tab with professional card design"""

    # Header
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h2 style="margin-bottom: 0.5rem;">AI-Powered Analysis</h2>
        <p style="color: #718096; font-size: 0.95rem;">Get comprehensive insights about your perfume compounds using advanced LLM analysis</p>
    </div>
    """, unsafe_allow_html=True)

    # Get compounds
    db = next(get_db())
    compounds = get_all_compounds(db)

    if not compounds:
        st.markdown('<div class="professional-card" style="text-align: center; padding: 3rem;">', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size: 3rem; margin-bottom: 1rem;">📚</div>
        <h3 style="color: #718096;">No compounds available</h3>
        <p style="color: #A0AEC0;">Create your first compound in the Create tab to begin analysis</p>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # Compound selection card
    st.markdown('<div class="professional-card">', unsafe_allow_html=True)
    st.markdown("### 🎯 Select Compound")

    compound_names = [c["name"] for c in compounds]
    selected_name = st.selectbox(
        "Choose a compound to analyze",
        compound_names,
        help="Select from your saved compounds",
        label_visibility="collapsed"
    )

    selected_compound = next(c for c in compounds if c["name"] == selected_name)
    compound_data = get_compound(db, selected_compound["id"])

    # Formula preview
    if compound_data:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Formula Preview:**")
        for ing in compound_data["ingredients"]:
            st.markdown(f"""
            <div style="background: #F7FAFC; padding: 0.5rem 1rem; border-radius: 6px; margin-bottom: 0.5rem; display: flex; justify-content: space-between;">
                <span style="color: #2D3748;">{ing['name']}</span>
                <span style="color: #667EEA; font-weight: 600;">{ing['percentage']}%</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔬 Analyze Composition", type="primary", use_container_width=True):
        with st.spinner("🧠 AI is analyzing your compound..."):
            # Prepare formula as list of tuples
            formula = [(ing["name"], ing["percentage"]) for ing in compound_data["ingredients"]]

            # Run analysis
            prompt, json_str, result = analyze_formula(formula)

            # Store in session state
            st.session_state.analysis_result = result
            st.session_state.analyzed_compound = compound_data

        st.success("✅ Analysis Complete!")
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # Display results if available
    if "analysis_result" in st.session_state and st.session_state.get("analyzed_compound", {}).get("id") == compound_data.get("id"):
        result = st.session_state.analysis_result

        # Summary card
        st.markdown('<div class="professional-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Analysis Summary")
        st.markdown(f"<p style='color: #2D3748; font-size: 1rem; line-height: 1.6;'>{result.get('summary', 'N/A')}</p>", unsafe_allow_html=True)

        # Key metrics
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)

        with col1:
            families = result.get('olfactive_family', [])
            family_text = ', '.join(families) if families else 'Not specified'
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #EBF4FF 0%, #E9D8FD 100%); padding: 1.25rem; border-radius: 12px; text-align: center;">
                <div style="font-size: 0.85rem; color: #5A67D8; font-weight: 600; margin-bottom: 0.5rem;">OLFACTIVE FAMILY</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: #434190;">{family_text}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            projection = result.get('projection', 'N/A')
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #E6FFFA 0%, #C6F6D5 100%); padding: 1.25rem; border-radius: 12px; text-align: center;">
                <div style="font-size: 0.85rem; color: #38A169; font-weight: 600; margin-bottom: 0.5rem;">PROJECTION</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: #22543D;">{projection}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            longevity = result.get('longevity_hours', 0)
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #FFF5F7 0%, #FED7E2 100%); padding: 1.25rem; border-radius: 12px; text-align: center;">
                <div style="font-size: 0.85rem; color: #E53E3E; font-weight: 600; margin-bottom: 0.5rem;">LONGEVITY</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: #742A2A;">{longevity} hours</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Notes pyramid
        st.markdown('<div class="professional-card">', unsafe_allow_html=True)
        st.markdown("### 🎭 Fragrance Pyramid")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("#### 🍋 Top Notes")
            top_notes = result.get('top_notes', [])
            if top_notes:
                for note in top_notes:
                    if isinstance(note, dict):
                        name = note.get('name', 'Unknown')
                        reason = note.get('reason', '')
                        st.markdown(f"""
                        <div style="background: #FFFBEB; padding: 0.75rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 3px solid #F59E0B;">
                            <div style="font-weight: 600; color: #78350F; margin-bottom: 0.25rem;">{name}</div>
                            <div style="font-size: 0.85rem; color: #92400E;">{reason}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"• {note}")
            else:
                st.caption("_No top notes detected_")

        with col2:
            st.markdown("#### 🌸 Heart Notes")
            heart_notes = result.get('heart_notes', [])
            if heart_notes:
                for note in heart_notes:
                    if isinstance(note, dict):
                        name = note.get('name', 'Unknown')
                        reason = note.get('reason', '')
                        st.markdown(f"""
                        <div style="background: #FCE7F3; padding: 0.75rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 3px solid #EC4899;">
                            <div style="font-weight: 600; color: #831843; margin-bottom: 0.25rem;">{name}</div>
                            <div style="font-size: 0.85rem; color: #9F1239;">{reason}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"• {note}")
            else:
                st.caption("_No heart notes detected_")

        with col3:
            st.markdown("#### 🌲 Base Notes")
            base_notes = result.get('base_notes', [])
            if base_notes:
                for note in base_notes:
                    if isinstance(note, dict):
                        name = note.get('name', 'Unknown')
                        reason = note.get('reason', '')
                        st.markdown(f"""
                        <div style="background: #ECFDF5; padding: 0.75rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 3px solid #10B981;">
                            <div style="font-weight: 600; color: #064E3B; margin-bottom: 0.25rem;">{name}</div>
                            <div style="font-size: 0.85rem; color: #065F46;">{reason}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"• {note}")
            else:
                st.caption("_No base notes detected_")

        st.markdown("</div>", unsafe_allow_html=True)

        # Accords
        if result.get('accords'):
            st.markdown('<div class="professional-card">', unsafe_allow_html=True)
            st.markdown("### 🎨 Accords")
            for accord in result['accords']:
                if isinstance(accord, dict):
                    st.markdown(f"""
                    <div style="background: #F7FAFC; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem;">
                        <span style="font-weight: 600; color: #2D3748;">{accord.get('name', 'Unknown')}</span>
                        <span style="color: #718096;">: {accord.get('description', '')}</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"• {accord}")
            st.markdown("</div>", unsafe_allow_html=True)

        # Improvement suggestions
        if result.get('improvement_suggestions'):
            st.markdown('<div class="professional-card">', unsafe_allow_html=True)
            st.markdown("### 💡 Improvement Suggestions")
            for suggestion in result['improvement_suggestions']:
                if isinstance(suggestion, dict):
                    st.markdown(f"✨ {suggestion.get('suggestion', suggestion)}")
                else:
                    st.markdown(f"✨ {suggestion}")
            st.markdown("</div>", unsafe_allow_html=True)

        # Similar scents and risks in columns
        col1, col2 = st.columns(2)

        with col1:
            if result.get('similar_popular_scents'):
                st.markdown('<div class="professional-card">', unsafe_allow_html=True)
                st.markdown("### 👃 Similar Scents")
                scents = result['similar_popular_scents']
                scent_list = scents if isinstance(scents, list) else [scents]
                for scent in scent_list:
                    st.markdown(f"• {scent}")
                st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            if result.get('risks'):
                st.markdown('<div class="professional-card">', unsafe_allow_html=True)
                st.markdown("### ⚠️ Safety Notes")
                for risk in result['risks']:
                    if isinstance(risk, dict):
                        st.warning(f"{risk.get('risk', risk)}")
                    else:
                        st.warning(f"{risk}")
                st.markdown("</div>", unsafe_allow_html=True)

        # Confidence
        confidence = result.get('confidence')
        if confidence is not None:
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; color: #A0AEC0; font-size: 0.9rem;">
                Analysis Confidence: <span style="font-weight: 700; color: #667EEA;">{confidence * 100:.0f}%</span>
            </div>
            """, unsafe_allow_html=True)
