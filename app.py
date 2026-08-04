import streamlit as st
import requests

# ==========================================
# Page Config
# ==========================================

st.set_page_config(
    page_title="Atomcamp AI Assistant",
    page_icon="🤖",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"

# ==========================================
# Session State
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "knowledge_base_created" not in st.session_state:
    st.session_state.knowledge_base_created = False

# ==========================================
# Title
# ==========================================

st.title("🤖 Atomcamp AI Assistant")

st.caption(
    "Chat with PDFs and Websites using FastAPI + LangChain + FAISS + Gemini"
)

# ==========================================
# Sidebar
# ==========================================

with st.sidebar:

    st.header("Knowledge Base")

    uploaded_files = st.file_uploader(
        "Upload PDF Files",
        type=["pdf"],
        accept_multiple_files=True
    )

    st.divider()

    website_url = st.text_input(
        "Website URL",
        placeholder="https://www.atomcamp.com"
    )

    if uploaded_files:

        st.subheader("Uploaded PDFs")

        for pdf in uploaded_files:
            st.write(f"📄 {pdf.name}")

    st.divider()

    if st.button(
        "Create Knowledge Base",
        use_container_width=True
    ):

        # Require at least one source
        if not uploaded_files and website_url.strip() == "":

            st.warning(
                "Please upload at least one PDF or enter a Website URL."
            )

        else:

            files = []

            if uploaded_files:

                for pdf in uploaded_files:

                    files.append(
                        (
                            "files",
                            (
                                pdf.name,
                                pdf.getvalue(),
                                "application/pdf"
                            )
                        )
                    )

            with st.spinner("Creating Knowledge Base..."):

                try:

                    response = requests.post(
                        f"{API_URL}/upload",
                        files=files,
                        data={
                            "website_url": website_url
                        },
                        timeout=120
                    )

                except requests.exceptions.ConnectionError:

                    st.error("FastAPI server is not running.")
                    st.stop()

            if response.status_code == 200:

                st.session_state.knowledge_base_created = True

                st.success(
                    "Knowledge Base Created Successfully!"
                )

            else:

                st.error(response.text)

    st.divider()

    if st.button(
        "🗑 Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []
        st.rerun()

# ==========================================
# Chat Section
# ==========================================

if st.session_state.knowledge_base_created:

    st.subheader("💬 Chat")

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.write(message["content"])

    question = st.chat_input(
        "Ask your question..."
    )

    if question:

        with st.chat_message("user"):

            st.write(question)

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.spinner("Thinking..."):

            try:

                response = requests.post(
                    f"{API_URL}/chat",
                    json={
                        "question": question
                    },
                    timeout=120
                )

            except requests.exceptions.ConnectionError:

                st.error("FastAPI server is not running.")
                st.stop()

        if response.status_code == 200:

            result = response.json()

            answer = result["answer"]

            with st.chat_message("assistant"):

                st.write(answer)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            with st.expander("📚 Sources Used"):

                for source in result["sources"]:

                    if source["file"].startswith("http"):

                        st.write(f"🌐 {source['file']}")

                    else:

                        st.write(
                            f"📄 {source['file']} | Page {source['page']}"
                        )

        else:

            st.error(response.text)

# ==========================================
# Welcome Screen
# ==========================================

else:

    st.info(
        """
### Welcome to Atomcamp AI Assistant

This assistant can answer questions from:

- 📄 Uploaded PDF documents
- 🌐 Public websites

### Steps

1. Upload one or more PDFs (optional)
2. Enter a website URL (optional)
3. Click **Create Knowledge Base**
4. Start chatting

You can use:
- PDFs only
- Website only
- PDFs + Website together

### Backend

- FastAPI
- LangChain
- FAISS
- Gemini
"""
    )

# ==========================================
# Footer
# ==========================================

st.divider()

st.caption(
    "Built with ❤️ using Streamlit + FastAPI + LangChain + FAISS + Gemini"
)