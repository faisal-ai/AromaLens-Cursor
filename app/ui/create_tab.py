"""Create Tab - Professional compound creation interface"""
import streamlit as st
from app.db import get_db
from app.services.compound_crud import create_compound


def render():
    """Render the create tab with professional card design"""

    # Header
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h2 style="margin-bottom: 0.5rem;">Create New Compound</h2>
        <p style="color: #718096; font-size: 0.95rem;">Design your perfume formula with precision and save it to your library</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize ingredient list in session state
    if "ingredients" not in st.session_state:
        st.session_state.ingredients = [{"name": "", "percentage": 0.0}]

    # Main form card
    st.markdown('<div class="professional-card">', unsafe_allow_html=True)

    # Compound basic info
    st.markdown("### 📋 Basic Information")

    col1, col2 = st.columns([2, 1])
    with col1:
        name = st.text_input(
            "Compound Name *",
            placeholder="e.g., Summer Breeze No. 5",
            help="Give your compound a unique, memorable name"
        )
    with col2:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-card'><div class='metric-value'>{len(st.session_state.ingredients)}</div><div class='metric-label'>Ingredients</div></div>", unsafe_allow_html=True)

    description = st.text_area(
        "Description (Optional)",
        placeholder="Describe the inspiration, target profile, or special notes about this compound...",
        height=100,
        help="Add context about your creation"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # Ingredients section
    st.markdown('<div class="professional-card">', unsafe_allow_html=True)
    st.markdown("### 🧪 Formula Composition")

    # Display ingredients
    for idx, ing in enumerate(st.session_state.ingredients):
        st.markdown(f'<div class="card-compact">', unsafe_allow_html=True)

        col1, col2, col3 = st.columns([4, 2, 1])

        with col1:
            ing["name"] = st.text_input(
                f"Ingredient {idx+1}",
                ing["name"],
                key=f"name_{idx}",
                placeholder="e.g., Bergamot Oil, Limonene, Hedione",
                label_visibility="collapsed"
            )

        with col2:
            ing["percentage"] = st.number_input(
                f"Percentage {idx+1}",
                0.0,
                100.0,
                ing["percentage"],
                0.1,
                key=f"pct_{idx}",
                help="Percentage by weight",
                label_visibility="collapsed"
            )

        with col3:
            if len(st.session_state.ingredients) > 1:
                if st.button("🗑️", key=f"remove_{idx}", help="Remove ingredient"):
                    st.session_state.ingredients.pop(idx)
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # Add ingredient button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("➕ Add Ingredient", use_container_width=True, type="secondary"):
        st.session_state.ingredients.append({"name": "", "percentage": 0.0})
        st.rerun()

    # Validation display
    total = sum(i["percentage"] for i in st.session_state.ingredients if i["name"])
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #EBF8FF 0%, #BEE3F8 100%); padding: 1rem; border-radius: 12px; text-align: center;">
            <div style="font-size: 1.5rem; font-weight: 700; color: #2C5282;">{total:.1f}%</div>
            <div style="font-size: 0.85rem; color: #2C5282; font-weight: 600;">Total</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        status_color = "#48BB78" if abs(total - 100.0) < 0.1 else "#ED8936"
        status_text = "Valid ✓" if abs(total - 100.0) < 0.1 else "Adjust"
        st.markdown(f"""
        <div style="background: {'linear-gradient(135deg, #E6FFFA 0%, #C6F6D5 100%)' if abs(total - 100.0) < 0.1 else 'linear-gradient(135deg, #FFFAF0 0%, #FED7AA 100%)'}; padding: 1rem; border-radius: 12px; text-align: center;">
            <div style="font-size: 1.5rem; font-weight: 700; color: {status_color};">{status_text}</div>
            <div style="font-size: 0.85rem; color: {status_color}; font-weight: 600;">Status</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        remaining = 100.0 - total
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FFF5F7 0%, #FED7E2 100%); padding: 1rem; border-radius: 12px; text-align: center;">
            <div style="font-size: 1.5rem; font-weight: 700; color: #C53030;">{remaining:.1f}%</div>
            <div style="font-size: 0.85rem; color: #C53030; font-weight: 600;">Remaining</div>
        </div>
        """, unsafe_allow_html=True)

    if total > 0 and abs(total - 100.0) >= 0.1:
        st.warning(f"⚠️ Total must equal 100%. Currently at {total:.1f}%")

    st.markdown("</div>", unsafe_allow_html=True)

    # Action buttons
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        if st.button("💾 Save Compound", type="primary", use_container_width=True):
            # Filter out empty ingredients
            valid_ingredients = [i for i in st.session_state.ingredients if i["name"]]

            if not name:
                st.error("❌ Please enter a compound name")
            elif abs(total - 100.0) > 0.1:
                st.error(f"❌ Percentages must sum to 100% (currently {total:.1f}%)")
            elif len(valid_ingredients) < 2:
                st.error("❌ Please add at least 2 ingredients")
            else:
                try:
                    db = next(get_db())
                    compound_id = create_compound(db, name, description, valid_ingredients)
                    st.success(f"✅ Compound '{name}' saved successfully! (ID: {compound_id})")
                    st.session_state.ingredients = [{"name": "", "percentage": 0.0}]
                    st.session_state.saved_compound_id = compound_id
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Error saving compound: {str(e)}")

    with col2:
        if st.button("🗑️ Clear Form", use_container_width=True):
            st.session_state.ingredients = [{"name": "", "percentage": 0.0}]
            st.rerun()

    # Help section
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("💡 Tips for Creating Compounds"):
        st.markdown("""
        **Best Practices:**
        - Use precise ingredient names for better analysis
        - Ensure percentages add up to exactly 100%
        - Include at least 3-5 ingredients for meaningful analysis
        - Add a descriptive name and notes for future reference

        **Common Ingredient Categories:**
        - Top notes: Citrus oils, light florals, aldehydes
        - Heart notes: Florals, spices, fruits
        - Base notes: Woods, musks, resins, vanilla
        """)
