import streamlit as st
import os

from src.data_ingestion import create_knowledge_base
from src.chatbot import get_llm


# ---------------- Page Configuration ----------------

st.set_page_config(
    page_title="Atomcamp AI Assistant",
    page_icon="🤖",
    layout="wide"
)


# ---------------- Title ----------------

st.title("🤖 Atomcamp AI Assistant")

st.caption(
    "Chat with PDFs and Public Websites using Gemini + FAISS"
)


# ---------------- Session State ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "knowledge_base_created" not in st.session_state:
    st.session_state.knowledge_base_created = False

if "pdf_names" not in st.session_state:
    st.session_state.pdf_names = []


# ---------------- Sidebar ----------------

with st.sidebar:

    st.header(" Knowledge Base")

    uploaded_files = st.file_uploader(
        "Upload PDFs",
        type="pdf",
        accept_multiple_files=True
    )

    if uploaded_files:

        st.session_state.pdf_names = [
            file.name for file in uploaded_files
        ]

    if st.session_state.pdf_names:

        st.subheader("Uploaded PDFs")

        for pdf in st.session_state.pdf_names:

            st.write(f"📄 {pdf}")

    st.divider()

    website_url = st.text_input(
        "🌐 Website URL",
        placeholder="https://www.atomcamp.com"
    )

    st.divider()

    create_button = st.button(
        "Create Knowledge Base",
        use_container_width=True
    )

    st.divider()

    if st.button(
        "🗑 Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()

        # ---------------- Create Knowledge Base ----------------

if create_button:

    # User must provide at least one source
    if not uploaded_files and website_url.strip() == "":

        st.error(
            "Please upload at least one PDF or enter a website URL."
        )

    else:

        os.makedirs("data", exist_ok=True)

        pdf_paths = []

        # Save PDFs (only if uploaded)
        if uploaded_files:

            for uploaded_file in uploaded_files:

                file_path = os.path.join(
                    "data",
                    uploaded_file.name
                )

                with open(file_path, "wb") as f:

                    f.write(
                        uploaded_file.getbuffer()
                    )

                pdf_paths.append(file_path)

        # Website list
        website_urls = []

        if website_url.strip():

            website_urls.append(
                website_url.strip()
            )

        with st.spinner("Creating Knowledge Base..."):

            st.session_state.vector_store = create_knowledge_base(
                pdf_paths,
                website_urls
            )

            st.session_state.knowledge_base_created = True

        st.success("Knowledge Base Created Successfully!")



# ---------------- Chat Interface ----------------

if st.session_state.knowledge_base_created:

    st.divider()

    st.subheader("💬 Chat")

    # Display Previous Messages

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.write(
                message["content"]
            )


    question = st.chat_input(
        "Ask anything..."
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


        docs = st.session_state.vector_store.similarity_search(
            question,
            k=4
        )


        context = "\n\n".join(

            [
                doc.page_content
                for doc in docs
            ]

        )


        history = "\n".join(

            [

                f"{msg['role']}: {msg['content']}"

                for msg in st.session_state.messages

            ]

        )


        llm = get_llm()


        prompt = f"""

You are an AI Assistant.

Answer ONLY using the provided context.

If the answer is not available in the context, simply say:

"I couldn't find that information in the uploaded PDFs or website."

------------------------

Conversation:

{history}

------------------------

Context:

{context}

------------------------

Question:

{question}

"""

        with st.spinner("Thinking..."):

            response = llm.invoke(
                prompt
            )

            answer = response.content


        with st.chat_message("assistant"):

            st.write(answer)


        st.session_state.messages.append(

            {
                "role": "assistant",
                "content": answer
            }

        )

                # ---------------- Sources ----------------

        with st.expander("Sources Used"):

            sources = []

            for doc in docs:

                source = doc.metadata.get(
                    "source",
                    "Unknown Source"
                )

                page = doc.metadata.get(
                    "page",
                    None
                )

                if source.startswith("http"):

                    text = f"{source}"

                else:

                    file_name = os.path.basename(source)

                    if page is not None:

                        text = f" {file_name} | Page {page + 1}"

                    else:

                        text = f"{file_name}"

                if text not in sources:

                    sources.append(text)

            for source in sources:

                st.write(source)

# ---------------- Welcome Screen ----------------

else:

    st.info(
        """
### Welcome to Atomcamp AI Assistant

This assistant can answer questions from:

-  Uploaded PDF documents
-  Public website pages

### How to use

1. Upload one or more PDFs.
2. Enter a public website URL.
3. Click **Create Knowledge Base**.
4. Start chatting!

Your knowledge base will be saved locally using **FAISS**, so it loads much faster the next time.
"""
    )


# ---------------- Footer ----------------

st.divider()

st.caption(
    "Built with using Streamlit, LangChain, FAISS, HuggingFace Embeddings and Gemini"
)