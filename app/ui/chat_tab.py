"""Chat Tab - Professional AI-powered Q&A about compounds"""
import streamlit as st
from app.services.chat_service import chat_about_compound


def render():
    """Render the chat tab with professional card design"""

    # Header
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h2 style="margin-bottom: 0.5rem;">AI Assistant</h2>
        <p style="color: #718096; font-size: 0.95rem;">Have a conversation about your analyzed compounds with our AI expert</p>
    </div>
    """, unsafe_allow_html=True)

    # Check if compound and analysis exist
    if "analyzed_compound" not in st.session_state or "analysis_result" not in st.session_state:
        st.markdown('<div class="professional-card" style="text-align: center; padding: 3rem;">', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size: 3rem; margin-bottom: 1rem;">🔬</div>
        <h3 style="color: #718096;">No Compound Analyzed Yet</h3>
        <p style="color: #A0AEC0;">Analyze a compound first in the Analyze tab to start chatting with the AI assistant</p>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        return

    compound = st.session_state.analyzed_compound
    analysis = st.session_state.analysis_result

    # Context card
    st.markdown('<div class="professional-card">', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
        <div>
            <h3 style="margin: 0 0 0.5rem 0; font-size: 1.25rem; color: #1A202C;">💬 Discussing: {compound['name']}</h3>
            <p style="margin: 0; color: #A0AEC0; font-size: 0.9rem;">
                {', '.join([ing['name'] for ing in compound['ingredients'][:3]])}{'...' if len(compound['ingredients']) > 3 else ''}
            </p>
        </div>
        <div style="background: linear-gradient(135deg, #0A1F44 0%, #1E3A8A 50%, #3B82F6 100%); color: white; padding: 0.5rem 1rem; border-radius: 8px; font-weight: 600;">
            {len(compound['ingredients'])} ingredients
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Initialize chat history
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # Chat container
    st.markdown("<br>", unsafe_allow_html=True)

    # Display chat history
    if not st.session_state.chat_messages:
        st.markdown('<div class="professional-card" style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #F7FAFC 0%, #EDF2F7 100%);">', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">👋</div>
        <p style="color: #718096; margin: 0;">Ask me anything about this compound!</p>
        <p style="color: #A0AEC0; font-size: 0.85rem; margin-top: 0.5rem;">
            Try asking: "What's the dominant note?", "How can I improve longevity?", or "What makes this unique?"
        </p>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    for msg in st.session_state.chat_messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%); padding: 1rem 1.25rem; border-radius: 12px; margin-bottom: 1rem; border-left: 4px solid #1E3A8A;">
                <div style="font-size: 0.75rem; color: #1E40AF; font-weight: 600; margin-bottom: 0.25rem;">YOU</div>
                <div style="color: #2D3748; line-height: 1.6;">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: #FFFFFF; padding: 1rem 1.25rem; border-radius: 12px; margin-bottom: 1rem; border: 1px solid #E2E8F0; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                <div style="font-size: 0.75rem; color: #1E3A8A; font-weight: 600; margin-bottom: 0.25rem;">🤖 AI ASSISTANT</div>
                <div style="color: #2D3748; line-height: 1.6;">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)

    # Chat input
    if prompt := st.chat_input("💬 Ask about this compound..."):
        # Add user message
        st.session_state.chat_messages.append({"role": "user", "content": prompt})

        # Get response
        with st.spinner("🧠 AI is thinking..."):
            response = chat_about_compound(compound, analysis, prompt)

        # Add assistant message
        st.session_state.chat_messages.append({"role": "assistant", "content": response})
        st.rerun()

    # Clear chat button
    if st.session_state.chat_messages:
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🗑️ Clear Chat History", use_container_width=True):
                st.session_state.chat_messages = []
                st.rerun()
