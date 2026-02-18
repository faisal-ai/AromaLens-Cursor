"""Library Tab - View and manage all compounds"""
import streamlit as st
from app.db import get_db
from app.services.compound_crud import get_all_compounds, delete_compound


def render():
    """Render the library tab"""
    st.subheader("Compound Library")

    # Search bar
    search = st.text_input("🔍 Search compounds", "", placeholder="Type to search...")

    # Get compounds from database
    db = next(get_db())
    compounds = get_all_compounds(db, search)

    if not compounds:
        if search:
            st.info(f"No compounds found matching '{search}'")
        else:
            st.info("📚 No compounds yet. Create one in the Create tab!")
        return

    # Display count
    st.caption(f"Found {len(compounds)} compound(s)")
    st.markdown("---")

    # Display compounds
    for compound in compounds:
        with st.container():
            col1, col2, col3 = st.columns([4, 1, 1])

            with col1:
                st.markdown(f"### {compound['name']}")
                if compound['description']:
                    st.caption(compound['description'])
                st.caption(
                    f"🧪 {compound['ingredient_count']} ingredients • "
                    f"📅 {compound['updated_at'].strftime('%Y-%m-%d %H:%M')}"
                )

            with col2:
                if st.button("View", key=f"view_{compound['id']}", use_container_width=True):
                    st.session_state.selected_compound_id = compound['id']
                    st.success(f"Selected: {compound['name']}")

            with col3:
                if st.button("🗑️", key=f"delete_{compound['id']}", use_container_width=True, help="Delete compound"):
                    # Confirmation
                    if st.session_state.get(f"confirm_delete_{compound['id']}", False):
                        delete_compound(db, compound['id'])
                        st.success("Deleted!")
                        if f"confirm_delete_{compound['id']}" in st.session_state:
                            del st.session_state[f"confirm_delete_{compound['id']}"]
                        st.rerun()
                    else:
                        st.session_state[f"confirm_delete_{compound['id']}"] = True
                        st.warning("Click again to confirm delete")

            st.markdown("---")

    # Show selected compound details if any
    if "selected_compound_id" in st.session_state:
        from app.services.compound_crud import get_compound

        selected_id = st.session_state.selected_compound_id
        compound_data = get_compound(db, selected_id)

        if compound_data:
            st.markdown("### Selected Compound Details")

            st.markdown(f"**{compound_data['name']}**")
            if compound_data['description']:
                st.markdown(f"_{compound_data['description']}_")

            st.markdown("**Ingredients:**")
            for ing in compound_data['ingredients']:
                st.markdown(f"- {ing['name']}: {ing['percentage']}%")

            if st.button("Clear Selection"):
                del st.session_state.selected_compound_id
                st.rerun()
