"""Create Tab - Professional compound creation with autocomplete"""
import streamlit as st
from app.db import get_db
from app.services.compound_crud import create_compound

# Popular perfume ingredients
POPULAR_INGREDIENTS = [
    "Bergamot Oil", "Lemon Oil", "Orange Oil", "Grapefruit Oil", "Lime Oil",
    "Lavender Oil", "Rose Oil", "Jasmine Absolute", "Ylang-Ylang Oil", "Neroli Oil",
    "Geranium Oil", "Iris Absolute", "Violet Leaf Absolute", "Tuberose Absolute",
    "Sandalwood Oil", "Cedarwood Oil", "Patchouli Oil", "Vetiver Oil", "Oakmoss Absolute",
    "Vanilla Absolute", "Tonka Bean Absolute", "Benzoin Resinoid", "Labdanum Absolute",
    "Limonene", "Linalool", "Geraniol", "Citronellol", "Eugenol",
    "Coumarin", "Iso E Super", "Hedione", "Galaxolide", "Ambroxan",
    "Cashmeran", "Ethyl Maltol", "Methyl Anthranilate", "Cinnamic Aldehyde",
    "Musk Ketone", "Indole", "Phenylethyl Alcohol", "Benzyl Salicylate"
]


def render():
    """Render the create tab with professional card design"""

    # Header
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="margin-bottom: 0.5rem;">Create New Compound</h2>
        <p style="color: #475569; font-size: 0.95rem;">Design your perfume formula with precision</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize ingredient list in session state
    if "ingredients" not in st.session_state:
        st.session_state.ingredients = [{"name": "", "percentage": 0.0}]

    # Compound basic info - NO CARD HERE
    st.markdown("### 📋 Basic Information")

    # Name input - full width on mobile
    name = st.text_input(
        "Compound Name *",
        placeholder="e.g., Summer Breeze No. 5",
        help="Give your compound a unique, memorable name"
    )

    # Ingredient count badge
    st.markdown(f"""
    <div style="display: inline-block; background: linear-gradient(135deg, #0A1F44 0%, #1E3A8A 50%, #3B82F6 100%); color: white; padding: 0.5rem 1rem; border-radius: 8px; margin: 1rem 0; font-weight: 600;">
        {len(st.session_state.ingredients)} Ingredient{'s' if len(st.session_state.ingredients) != 1 else ''}
    </div>
    """, unsafe_allow_html=True)

    description = st.text_area(
        "Description (Optional)",
        placeholder="Describe the inspiration, target profile, or special notes...",
        height=100,
        help="Add context about your creation"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Ingredients section
    st.markdown("### 🧪 Formula Composition")

    # Display ingredients - Mobile friendly stacking
    for idx, ing in enumerate(st.session_state.ingredients):
        st.markdown(f'<div class="card-compact">', unsafe_allow_html=True)

        st.markdown(f"**Ingredient {idx+1}**")

        # Ingredient name with autocomplete
        ingredient_name = st.selectbox(
            f"Select or type ingredient {idx+1}",
            [""] + POPULAR_INGREDIENTS + ["+ Add Custom"],
            key=f"select_{idx}",
            label_visibility="collapsed"
        )

        # If user selects "Add Custom" or wants to type, show text input
        if ingredient_name == "+ Add Custom" or (ingredient_name == "" and ing["name"]):
            custom_name = st.text_input(
                f"Custom ingredient {idx+1}",
                value=ing["name"],
                key=f"custom_{idx}",
                placeholder="Enter custom ingredient name",
                label_visibility="collapsed"
            )
            ing["name"] = custom_name
        elif ingredient_name:
            ing["name"] = ingredient_name

        # Percentage input with remove button side by side
        col1, col2 = st.columns([4, 1])
        with col1:
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

        with col2:
            st.markdown("<div style='padding-top: 0.5rem;'></div>", unsafe_allow_html=True)
            if len(st.session_state.ingredients) > 1:
                if st.button("🗑️", key=f"remove_{idx}", help="Remove", use_container_width=True):
                    st.session_state.ingredients.pop(idx)
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # Add ingredient button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("➕ Add Ingredient", use_container_width=True, type="secondary"):
        st.session_state.ingredients.append({"name": "", "percentage": 0.0})
        st.rerun()

    # Validation display - Mobile stacked
    total = sum(i["percentage"] for i in st.session_state.ingredients if i["name"])
    st.markdown("<br>", unsafe_allow_html=True)

    # Validation metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%); padding: 1rem; border-radius: 12px; text-align: center;">
            <div style="font-size: 1.5rem; font-weight: 700; color: #1E3A8A;">{total:.1f}%</div>
            <div style="font-size: 0.75rem; color: #1E3A8A; font-weight: 600;">Total</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        status_color = "#10B981" if abs(total - 100.0) < 0.1 else "#F59E0B"
        status_text = "Valid ✓" if abs(total - 100.0) < 0.1 else "Adjust"
        status_bg = 'linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%)' if abs(total - 100.0) < 0.1 else 'linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%)'
        st.markdown(f"""
        <div style="background: {status_bg}; padding: 1rem; border-radius: 12px; text-align: center;">
            <div style="font-size: 1.5rem; font-weight: 700; color: {status_color};">{status_text}</div>
            <div style="font-size: 0.75rem; color: {status_color}; font-weight: 600;">Status</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        remaining = 100.0 - total
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%); padding: 1rem; border-radius: 12px; text-align: center;">
            <div style="font-size: 1.5rem; font-weight: 700; color: #DC2626;">{remaining:.1f}%</div>
            <div style="font-size: 0.75rem; color: #DC2626; font-weight: 600;">Remaining</div>
        </div>
        """, unsafe_allow_html=True)

    if total > 0 and abs(total - 100.0) >= 0.1:
        st.warning(f"⚠️ Total must equal 100%. Currently at {total:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # Action buttons - Full width on mobile
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
                    st.success(f"✅ Compound '{name}' saved successfully!")
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
        - Use the dropdown to select from 40+ popular ingredients
        - Choose "+ Add Custom" to enter your own ingredients
        - Ensure percentages add up to exactly 100%
        - Include at least 3-5 ingredients for meaningful analysis

        **Ingredient Categories:**
        - **Top notes:** Citrus oils, light florals, aldehydes (5-15%)
        - **Heart notes:** Florals, spices, fruits (30-50%)
        - **Base notes:** Woods, musks, resins, vanilla (40-60%)
        """)
