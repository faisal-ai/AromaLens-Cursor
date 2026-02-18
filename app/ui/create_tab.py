"""Create Tab - Add new compounds with ingredients"""
import streamlit as st
from app.db import get_db
from app.services.compound_crud import create_compound


def render():
    """Render the create compound tab"""
    st.subheader("Create Compound")

    # Initialize ingredient list in session state
    if "ingredients" not in st.session_state:
        st.session_state.ingredients = [{"name": "", "percentage": 0.0}]

    # Compound info
    name = st.text_input("Compound Name", placeholder="e.g., Citrus Fresh")
    description = st.text_area("Description (optional)", height=100, placeholder="Describe your compound...")

    st.markdown("---")
    st.markdown("**Ingredients**")

    # Display ingredients
    for idx, ing in enumerate(st.session_state.ingredients):
        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            ing["name"] = st.text_input(
                f"Ingredient {idx+1}",
                ing["name"],
                key=f"name_{idx}",
                placeholder="e.g., Bergamot Oil"
            )

        with col2:
            ing["percentage"] = st.number_input(
                f"% {idx+1}",
                0.0,
                100.0,
                ing["percentage"],
                key=f"pct_{idx}",
                step=0.1
            )

        with col3:
            if len(st.session_state.ingredients) > 1:
                if st.button("Remove", key=f"remove_{idx}"):
                    st.session_state.ingredients.pop(idx)
                    st.rerun()

    # Add ingredient button
    if st.button("➕ Add Ingredient"):
        st.session_state.ingredients.append({"name": "", "percentage": 0.0})
        st.rerun()

    # Validation - calculate total percentage
    total = sum(i["percentage"] for i in st.session_state.ingredients if i["name"])
    if total > 0:
        if abs(total - 100.0) < 0.1:
            st.success(f"✓ Total: {total:.1f}%")
        else:
            st.warning(f"⚠️ Total: {total:.1f}% (must equal 100%)")

    st.markdown("---")

    # Action buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.button("💾 Save Compound", type="primary", use_container_width=True):
            # Validation
            if not name:
                st.error("Please enter a compound name")
            elif abs(total - 100.0) > 0.1:
                st.error(f"Percentages must sum to 100% (currently {total:.1f}%)")
            elif not any(i["name"] for i in st.session_state.ingredients):
                st.error("Please add at least one ingredient")
            else:
                # Filter out empty ingredients
                valid_ingredients = [i for i in st.session_state.ingredients if i["name"]]

                if len(valid_ingredients) < 2:
                    st.error("Please add at least 2 ingredients")
                else:
                    try:
                        db = next(get_db())
                        compound_id = create_compound(db, name, description, valid_ingredients)
                        st.success(f"✓ Saved! Compound ID: {compound_id}")
                        # Clear form
                        st.session_state.ingredients = [{"name": "", "percentage": 0.0}]
                        st.session_state.saved_compound_id = compound_id
                    except Exception as e:
                        st.error(f"Error saving compound: {e}")

    with col2:
        if st.button("🗑️ Clear Form", use_container_width=True):
            st.session_state.ingredients = [{"name": "", "percentage": 0.0}]
            st.rerun()
