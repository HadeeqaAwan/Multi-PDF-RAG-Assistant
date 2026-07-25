# 🤖 Multi PDF RAG Assistant

An AI-powered chatbot that allows users to upload multiple PDFs and ask questions using Retrieval Augmented Generation (RAG).

## Features

- Upload multiple PDFs
- Extract PDF content
- Text chunking
- Gemini embeddings
- FAISS vector search
- AI-generated answers using Gemini
- Source citation with PDF name and page number
- Chat history memory
- Streamlit interface

## Tech Stack

- Python
- Streamlit
- LangChain
- Google Gemini
- FAISS
- PyPDF

## Architecture

PDF Upload

↓

PDF Loader

↓

Text Chunking

↓

Gemini Embeddings

↓

FAISS Vector Database

↓

Similarity Search

↓

Gemini LLM

↓

Answer + Sources


## Run Locally

Clone repository:

```bash
git clone your-repository-url