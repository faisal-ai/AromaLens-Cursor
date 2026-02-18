"""Library Tab - Professional compound library with search"""
import streamlit as st
from app.db import get_db
from app.services.compound_crud import get_all_compounds, get_compound, delete_compound


def render():
    """Render the library tab with professional card design"""

    # Header
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h2 style="margin-bottom: 0.5rem;">Compound Library</h2>
        <p style="color: #718096; font-size: 0.95rem;">Browse, search, and manage your perfume formulations</p>
    </div>
    """, unsafe_allow_html=True)

    # Get compounds from database
    db = next(get_db())

    # Search and filter section
    st.markdown('<div class="professional-card">', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        search = st.text_input(
            "🔍 Search",
            "",
            placeholder="Search by compound name...",
            label_visibility="collapsed"
        )
    with col2:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        compounds = get_all_compounds(db, search)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0A1F44 0%, #1E3A8A 50%, #3B82F6 100%); padding: 1rem; border-radius: 12px; text-align: center; color: white;">
            <div style="font-size: 1.5rem; font-weight: 700;">{len(compounds)}</div>
            <div style="font-size: 0.85rem; font-weight: 600; opacity: 0.9;">COMPOUNDS</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    if not compounds:
        st.markdown('<div class="professional-card" style="text-align: center; padding: 3rem;">', unsafe_allow_html=True)
        if search:
            st.markdown(f"""
            <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
            <h3 style="color: #718096;">No compounds found</h3>
            <p style="color: #A0AEC0;">No matches for "{search}". Try a different search term.</p>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="font-size: 3rem; margin-bottom: 1rem;">📚</div>
            <h3 style="color: #718096;">Your library is empty</h3>
            <p style="color: #A0AEC0;">Create your first compound in the Create tab!</p>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # Display compounds in grid
    st.markdown("<br>", unsafe_allow_html=True)

    for compound in compounds:
        st.markdown('<div class="card-compact">', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

        with col1:
            st.markdown(f"""
            <div>
                <h3 style="margin: 0 0 0.5rem 0; font-size: 1.25rem; color: #1A202C;">{compound['name']}</h3>
                <p style="margin: 0 0 0.5rem 0; color: #718096; font-size: 0.9rem;">{compound['description'][:100] + '...' if compound['description'] and len(compound['description']) > 100 else compound['description'] or 'No description'}</p>
                <div style="display: flex; gap: 1rem; font-size: 0.85rem; color: #A0AEC0;">
                    <span>🧪 {compound['ingredient_count']} ingredients</span>
                    <span>📅 {compound['updated_at'].strftime('%b %d, %Y')}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
            if st.button("👁️ View", key=f"view_{compound['id']}", use_container_width=True):
                st.session_state.selected_compound_id = compound['id']
                st.rerun()

        with col3:
            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
            if st.button("🔬 Analyze", key=f"analyze_{compound['id']}", use_container_width=True, type="secondary"):
                st.session_state.library_selected_for_analysis = compound['id']
                st.success(f"✓ Ready to analyze: {compound['name']}")
                st.info("Switch to the Analyze tab to proceed")

        with col4:
            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
            if st.button("🗑️", key=f"delete_{compound['id']}", use_container_width=True, help="Delete compound"):
                # Confirmation
                if st.session_state.get(f"confirm_delete_{compound['id']}", False):
                    delete_compound(db, compound['id'])
                    st.success(f"✓ Deleted: {compound['name']}")
                    if f"confirm_delete_{compound['id']}" in st.session_state:
                        del st.session_state[f"confirm_delete_{compound['id']}"]
                    st.rerun()
                else:
                    st.session_state[f"confirm_delete_{compound['id']}"] = True
                    st.warning("⚠️ Click again to confirm")

        st.markdown("</div>", unsafe_allow_html=True)

    # Show selected compound details if any
    if "selected_compound_id" in st.session_state:
        st.markdown("<br><br>", unsafe_allow_html=True)
        selected_id = st.session_state.selected_compound_id
        compound_data = get_compound(db, selected_id)

        if compound_data:
            st.markdown('<div class="professional-card">', unsafe_allow_html=True)

            # Header with close button
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"""
                <h3 style="margin-bottom: 0.5rem;">📋 {compound_data['name']}</h3>
                <p style="color: #718096; margin-bottom: 1.5rem;">{compound_data['description'] or 'No description provided'}</p>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("✕ Close", key="close_details", use_container_width=True):
                    del st.session_state.selected_compound_id
                    st.rerun()

            st.markdown("---")
            st.markdown("### 🧪 Formula Breakdown")

            # Ingredients in a nice grid
            for ing in compound_data['ingredients']:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #F7FAFC 0%, #EDF2F7 100%); padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 600; color: #2D3748;">{ing['name']}</span>
                    <span style="background: linear-gradient(135deg, #0A1F44 0%, #1E3A8A 50%, #3B82F6 100%); color: white; padding: 0.25rem 0.75rem; border-radius: 6px; font-weight: 700;">{ing['percentage']}%</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
