import streamlit as st
import os

from src.pdf_loader import load_pdf
from src.text_splitter import split_documents
from src.embeddings import create_vector_store
from src.chatbot import get_llm


st.title("🤖 Multi PDF RAG Chatbot")


# Chat memory initialize
if "messages" not in st.session_state:
    st.session_state.messages = []


# Upload PDFs
uploaded_files = st.file_uploader(
    "Upload Multiple PDFs",
    type="pdf",
    accept_multiple_files=True
)


if uploaded_files:

    all_documents = []


    for uploaded_file in uploaded_files:

        file_path = f"data/{uploaded_file.name}"


        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())


        documents = load_pdf(file_path)

        all_documents.extend(documents)



    st.success(
        f"{len(uploaded_files)} PDFs uploaded successfully!"
    )


    chunks = split_documents(all_documents)


    vector_store = create_vector_store(chunks)



    # Display old messages
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.write(message["content"])



    # Chat input
    question = st.chat_input(
        "Ask a question from your PDFs"
    )


    if question:


        # Show user message
        with st.chat_message("user"):

            st.write(question)



        # Save user message
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
            [doc.page_content for doc in docs]
        )



        # Previous conversation
        history = "\n".join(
            [
                f"{msg['role']}: {msg['content']}"
                for msg in st.session_state.messages
            ]
        )



        llm = get_llm()



        response = llm.invoke(
            f"""
            You are an AI assistant.

            Answer using the PDF context.

            Conversation history:
            {history}


            PDF Context:
            {context}


            Question:
            {question}
            """
        )



        answer = response.content



        # Show AI response
        with st.chat_message("assistant"):

            st.write(answer)



        # Save AI response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )



        # Sources
        st.subheader("Sources")


        sources = set()


        for doc in docs:

            source = doc.metadata.get("source")

            page = doc.metadata.get("page")

            file_name = os.path.basename(source)


            sources.add(
                f"📄 {file_name} | Page: {page + 1}"
            )


        for source in sources:

            st.write(source)