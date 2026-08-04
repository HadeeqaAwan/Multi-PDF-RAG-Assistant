from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Optional
import os
import shutil

from src.data_ingestion import create_knowledge_base
from src.chat_api import ask_question

app = FastAPI(
    title="Atomcamp AI Assistant API",
    description="Backend APIs for Atomcamp AI Assistant",
    version="1.0"
)


# ==========================================
# Request Model
# ==========================================

class ChatRequest(BaseModel):
    question: str


# ==========================================
# Home API
# ==========================================

@app.get("/")
def home():

    return {
        "message": "Atomcamp AI Assistant API is Running"
    }


# ==========================================
# Upload API
# ==========================================

@app.post("/upload")
async def upload_files(

    files: Optional[List[UploadFile]] = File(None),

    website_url: str = Form("")

):

    os.makedirs(
        "uploads",
        exist_ok=True
    )

    pdf_paths = []

    # ------------------------------------
    # Save PDFs (only if uploaded)
    # ------------------------------------

    if files:

        for file in files:

            file_path = os.path.join(
                "uploads",
                file.filename
            )

            with open(file_path, "wb") as buffer:

                shutil.copyfileobj(
                    file.file,
                    buffer
                )

            pdf_paths.append(file_path)

    # ------------------------------------
    # Website URLs
    # ------------------------------------

    website_urls = []

    if website_url.strip():

        website_urls.append(
            website_url.strip()
        )

    # ------------------------------------
    # Validation
    # ------------------------------------

    if not pdf_paths and not website_urls:

        return {
            "status": "error",
            "message": "Please upload at least one PDF or enter a Website URL."
        }

    # ------------------------------------
    # Create Knowledge Base
    # ------------------------------------

    create_knowledge_base(
        pdf_paths=pdf_paths,
        website_urls=website_urls
    )

    return {

        "status": "success",

        "message": "Knowledge Base Created Successfully.",

        "uploaded_files": [
            os.path.basename(path)
            for path in pdf_paths
        ],

        "website_urls": website_urls

    }


# ==========================================
# Chat API
# ==========================================

@app.post("/chat")
async def chat(
    request: ChatRequest
):

    result = ask_question(
        request.question
    )

    return result