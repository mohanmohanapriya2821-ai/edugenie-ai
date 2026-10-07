from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations
from gemini_client import GeminiConfigurationError

from schemas import (
    TextRequest,
    QuizResponse,
    LearningPathResponse,
)


# --------------------------------------------------
# BASE DIRECTORY
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent


# --------------------------------------------------
# FASTAPI APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="EduGenie - AI Learning Assistant",
    description=(
        "AI-powered educational assistant for "
        "questions, explanations, quizzes, summaries "
        "and personalized learning paths."
    ),
    version="1.0.0",
)


@app.exception_handler(GeminiConfigurationError)
async def gemini_config_error_handler(request: Request, exc: GeminiConfigurationError):
    return JSONResponse(
        status_code=503,
        content={"detail": str(exc)},
    )


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# STATIC FILES
# --------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "templates" / "static"),
    name="static",
)


# --------------------------------------------------
# TEMPLATES
# --------------------------------------------------

templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request
        }
    )


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "application": "EduGenie",
        "version": "1.0.0"
    }


# --------------------------------------------------
# QUESTION AND ANSWER
# --------------------------------------------------

@app.post("/qa")
async def qa(payload: TextRequest):

    answer = answer_question(payload.text)

    return {
        "answer": answer
    }


# --------------------------------------------------
# EXPLANATION
# --------------------------------------------------

@app.post("/explain")
async def explain(payload: TextRequest):

    explanation = explain_topic(payload.text)

    return {
        "explanation": explanation
    }


# --------------------------------------------------
# QUIZ
# --------------------------------------------------

@app.post(
    "/quiz",
    response_model=QuizResponse
)
async def quiz(payload: TextRequest):

    return generate_quiz(payload.text)


# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

@app.post("/summarize")
async def summarize(payload: TextRequest):

    summary = summarize_text(payload.text)

    return {
        "summary": summary
    }


# --------------------------------------------------
# LEARNING PATH
# --------------------------------------------------

@app.post(
    "/learn/recommendations",
    response_model=LearningPathResponse
)
async def learning_recommendations(
    payload: TextRequest
):

    return get_learning_recommendations(
        payload.text
    )