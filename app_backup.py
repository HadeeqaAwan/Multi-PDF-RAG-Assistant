import streamlit as st
import os

from src.pdf_loader import load_pdf
from src.text_splitter import split_documents
from src.embeddings import create_vector_store
from src.chatbot import get_llm


st.title("🤖 Multi PDF RAG Chatbot")


# Upload multiple PDFs
uploaded_files = st.file_uploader(
    "Upload Multiple PDFs",
    type="pdf",
    accept_multiple_files=True
)


if uploaded_files:

    all_documents = []


    # Load all PDFs
    for uploaded_file in uploaded_files:

        file_path = f"data/{uploaded_file.name}"


        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())


        documents = load_pdf(file_path)


        all_documents.extend(documents)



    st.success(
        f"{len(uploaded_files)} PDFs uploaded successfully!"
    )


    # Split documents into chunks
    chunks = split_documents(all_documents)


    # Create FAISS vector database
    vector_store = create_vector_store(chunks)



    question = st.text_input(
        "Ask a question from your PDFs"
    )



    if question:


        # Retrieve relevant documents
        docs = vector_store.similarity_search(
            question,
            k=3
        )


        # Prepare context
        context = "\n\n".join(
            [doc.page_content for doc in docs]
        )



        # Gemini LLM
        llm = get_llm()



        response = llm.invoke(
            f"""
            You are an AI assistant.

            Answer only using the provided context.
            If the answer is not present in the context,
            say:
            "I could not find this information in the uploaded PDFs."

            Context:
            {context}

            Question:
            {question}
            """
        )



        # Answer section
        st.subheader("Answer")

        st.write(response.content)



        # Source section
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