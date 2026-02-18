"""Chat Tab - Ask questions about analyzed compounds"""
import streamlit as st
from app.services.chat_service import chat_about_compound


def render():
    """Render the chat tab"""
    st.subheader("💬 Chat")

    # Check if compound and analysis exist
    if "analyzed_compound" not in st.session_state or "analysis_result" not in st.session_state:
        st.info("🔬 Please analyze a compound first in the Analyze tab to start chatting!")
        return

    compound = st.session_state.analyzed_compound
    analysis = st.session_state.analysis_result

    # Display current compound context
    st.markdown(f"**Discussing:** {compound['name']}")
    st.caption(f"Ingredients: {', '.join([ing['name'] for ing in compound['ingredients'][:3]])}{'...' if len(compound['ingredients']) > 3 else ''}")
    st.markdown("---")

    # Initialize chat history
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # Display chat history
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("Ask about this compound..."):
        # Add user message
        st.session_state.chat_messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_about_compound(compound, analysis, prompt)
            st.markdown(response)

        # Add assistant message
        st.session_state.chat_messages.append({"role": "assistant", "content": response})
        st.rerun()

    # Clear chat button
    if st.session_state.chat_messages:
        st.markdown("---")
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.chat_messages = []
            st.rerun()
