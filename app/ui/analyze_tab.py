"""Analyze Tab - Analyze compounds using LLM"""
import streamlit as st
from app.db import get_db
from app.services.compound_crud import get_all_compounds, get_compound
from app.services.analysis import analyze_formula


def render():
    """Render the analyze tab"""
    st.subheader("Analyze Compound")

    # Get compounds
    db = next(get_db())
    compounds = get_all_compounds(db)

    if not compounds:
        st.info("📚 No compounds to analyze. Create one in the Create tab first!")
        return

    # Select compound
    compound_names = [c["name"] for c in compounds]
    selected_name = st.selectbox(
        "Select Compound",
        compound_names,
        help="Choose a compound to analyze"
    )

    selected_compound = next(c for c in compounds if c["name"] == selected_name)

    # Get full compound data
    compound_data = get_compound(db, selected_compound["id"])

    if compound_data:
        st.markdown("---")
        st.markdown("**Formula Preview:**")
        for ing in compound_data["ingredients"]:
            st.caption(f"• {ing['name']}: {ing['percentage']}%")

    # Analyze button
    st.markdown("---")
    if st.button("🔬 Analyze Composition", type="primary", use_container_width=True):
        with st.spinner("🔬 Analyzing composition with AI..."):
            # Prepare formula as list of tuples (name, percentage)
            formula = [(ing["name"], ing["percentage"]) for ing in compound_data["ingredients"]]

            # Run analysis (uses existing service)
            prompt, json_str, result = analyze_formula(formula)

            # Store in session state for chat tab
            st.session_state.analysis_result = result
            st.session_state.analyzed_compound = compound_data

        st.success("✅ Analysis Complete!")
        st.rerun()

    # Display results if available
    if "analysis_result" in st.session_state and st.session_state.get("analyzed_compound", {}).get("id") == compound_data.get("id"):
        result = st.session_state.analysis_result

        st.markdown("---")
        st.markdown("### 📊 Analysis Results")

        # Summary section
        st.markdown(f"**Summary:** {result.get('summary', 'N/A')}")

        # Key characteristics
        col1, col2 = st.columns(2)
        with col1:
            families = result.get('olfactive_family', [])
            if families:
                st.markdown(f"**Olfactive Family:** {', '.join(families)}")
            else:
                st.markdown("**Olfactive Family:** Not specified")

        with col2:
            st.markdown(f"**Projection:** {result.get('projection', 'N/A')}")
            st.markdown(f"**Longevity:** {result.get('longevity_hours', 0)} hours")

        st.markdown("---")

        # Notes pyramid
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("#### 🍋 Top Notes")
            top_notes = result.get('top_notes', [])
            if top_notes:
                for note in top_notes:
                    if isinstance(note, dict):
                        name = note.get('name', 'Unknown')
                        reason = note.get('reason', '')
                        st.markdown(f"**{name}**")
                        if reason:
                            st.caption(reason)
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
                        st.markdown(f"**{name}**")
                        if reason:
                            st.caption(reason)
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
                        st.markdown(f"**{name}**")
                        if reason:
                            st.caption(reason)
                    else:
                        st.markdown(f"• {note}")
            else:
                st.caption("_No base notes detected_")

        # Additional information
        if result.get('accords'):
            st.markdown("---")
            st.markdown("**Accords:**")
            for accord in result['accords']:
                if isinstance(accord, dict):
                    st.markdown(f"• {accord.get('name', 'Unknown')}: {accord.get('description', '')}")
                else:
                    st.markdown(f"• {accord}")

        if result.get('improvement_suggestions'):
            st.markdown("---")
            st.markdown("**💡 Improvement Suggestions:**")
            for suggestion in result['improvement_suggestions']:
                if isinstance(suggestion, dict):
                    st.markdown(f"• {suggestion.get('suggestion', suggestion)}")
                else:
                    st.markdown(f"• {suggestion}")

        if result.get('similar_popular_scents'):
            st.markdown("---")
            st.markdown("**Similar Popular Scents:**")
            scents = result['similar_popular_scents']
            st.markdown(", ".join(scents if isinstance(scents, list) else [scents]))

        if result.get('risks'):
            st.markdown("---")
            st.markdown("**⚠️ Risks & Safety:**")
            for risk in result['risks']:
                if isinstance(risk, dict):
                    st.warning(f"• {risk.get('risk', risk)}")
                else:
                    st.warning(f"• {risk}")

        # Confidence score
        confidence = result.get('confidence')
        if confidence is not None:
            st.markdown("---")
            st.caption(f"_Analysis confidence: {confidence * 100:.0f}%_")
