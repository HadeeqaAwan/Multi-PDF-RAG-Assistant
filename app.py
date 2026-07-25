import streamlit as st
import os

from src.pdf_loader import load_pdf
from src.text_splitter import split_documents
from src.embeddings import create_vector_store
from src.chatbot import get_llm


# ---------------- Page Configuration ----------------

st.set_page_config(
    page_title="Multi PDF RAG Chatbot",
    page_icon="",
    layout="wide"
)


# ---------------- Title ----------------

st.title("Multi PDF RAG Assistant")

st.caption(
    "Chat with your documents using Gemini, LangChain and FAISS"
)



# ---------------- Session Memory ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []


if "pdf_names" not in st.session_state:
    st.session_state.pdf_names = []



# ---------------- Sidebar ----------------

with st.sidebar:

    st.header(" Document Panel")


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

        st.subheader("Uploaded Files")

        for pdf in st.session_state.pdf_names:

            st.write(
                f" {pdf}"
            )



    st.divider()


    if st.button(" Clear Chat"):

        st.session_state.messages = []

        st.rerun()



# ---------------- Main App ----------------


if uploaded_files:


    with st.spinner(" Reading and processing documents..."):


        all_documents = []


        for uploaded_file in uploaded_files:


            file_path = f"data/{uploaded_file.name}"


            with open(file_path, "wb") as f:

                f.write(
                    uploaded_file.getbuffer()
                )


            documents = load_pdf(file_path)


            all_documents.extend(documents)



        chunks = split_documents(
            all_documents
        )


        vector_store = create_vector_store(
            chunks
        )


    st.success(
        "Documents processed successfully!"
    )



    # Display previous messages

    for message in st.session_state.messages:


        with st.chat_message(
            message["role"]
        ):

            st.write(
                message["content"]
            )



    # Chat Input

    question = st.chat_input(
        "Ask something from your PDFs..."
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



        # Retrieve documents

        docs = vector_store.similarity_search(
            question,
            k=3
        )



        context = "\n\n".join(
            [
                doc.page_content
                for doc in docs
            ]
        )



        history = "\n".join(
            [
                f"{m['role']}: {m['content']}"
                for m in st.session_state.messages
            ]
        )



        llm = get_llm()



        response = llm.invoke(
            f"""
            You are an AI assistant.

            Answer only using the PDF context.

            Conversation:
            {history}

            Context:
            {context}

            Question:
            {question}
            """
        )



        answer = response.content



        with st.chat_message(
            "assistant"
        ):

            st.write(answer)



        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )



        # Sources

        st.subheader(" Sources")


        sources = set()


        for doc in docs:


            source = doc.metadata.get(
                "source"
            )

            page = doc.metadata.get(
                "page"
            )


            file_name = os.path.basename(
                source
            )


            sources.add(
                f" {file_name} | Page {page+1}"
            )


        for source in sources:

            st.write(source)



else:

    st.info(
        " Upload PDFs from the sidebar to start chatting."
    )