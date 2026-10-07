from functools import lru_cache
from types import SimpleNamespace

from google import genai
from google.genai import types

from config import (
    ALLOW_OFFLINE_FALLBACK,
    GEMINI_API_KEY,
    GEMINI_MODEL,
)

from schemas import QuizResponse, LearningPathResponse


# --------------------------------------------------
# CUSTOM ERROR
# --------------------------------------------------

class GeminiConfigurationError(RuntimeError):
    pass


# --------------------------------------------------
# GEMINI CLIENT
# --------------------------------------------------

@lru_cache(maxsize=1)
def get_client():

    if not GEMINI_API_KEY:

        raise GeminiConfigurationError(
            "GEMINI_API_KEY is not configured. "
            "Please create a .env file and add your "
            "Gemini API key or enable offline fallback."
        )

    return genai.Client(
        api_key=GEMINI_API_KEY
    )


# --------------------------------------------------
# OFFLINE FALLBACK
# --------------------------------------------------

def _fallback_quiz_response(topic: str):
    topic = (topic or "the topic").strip() or "the topic"

    data = {
        "questions": [
            {
                "question": f"What is the main idea of {topic}?",
                "options": [
                    "A basic summary of the key concept",
                    "A random unrelated fact",
                    "An exact copy of the source text",
                    "A complete textbook chapter",
                ],
                "correct_answer": "A basic summary of the key concept",
                "explanation": "The main idea focuses on the key concept being explained rather than unrelated or excessive detail.",
            },
            {
                "question": f"Which statement best helps someone understand {topic}?",
                "options": [
                    "Use a simple definition and a clear example",
                    "Ignore examples and focus only on terminology",
                    "Skip the topic and move to advanced content",
                    "Rewrite the topic in a different language",
                ],
                "correct_answer": "Use a simple definition and a clear example",
                "explanation": "Good explanations begin with a simple definition and make the concept easier to grasp with an example.",
            },
            {
                "question": f"Why is reviewing {topic} important?",
                "options": [
                    "It reinforces understanding and helps recall key ideas",
                    "It makes the topic longer without adding meaning",
                    "It guarantees mastery without practice",
                    "It removes the need to study anything else",
                ],
                "correct_answer": "It reinforces understanding and helps recall key ideas",
                "explanation": "Reviewing a topic strengthens understanding and helps link ideas to memory.",
            },
        ]
    }

    parsed = QuizResponse.model_validate(data)
    return parsed


def _fallback_learning_path_response(topic: str):
    topic = (topic or "the topic").strip() or "the topic"

    data = {
        "topic": topic,
        "overview": f"A beginner-friendly learning path for {topic} that moves from core concepts to practical understanding.",
        "steps": [
            {
                "level": "Beginner",
                "topic": f"Fundamentals of {topic}",
                "duration": "1 week",
                "goals": [
                    "Understand the core idea",
                    "Learn the key vocabulary",
                    "Recognize one simple example",
                ],
                "resources": [
                    "Class notes",
                    "Introductory textbook section",
                    "Short explanatory video",
                ],
            },
            {
                "level": "Intermediate",
                "topic": f"Applying {topic}",
                "duration": "2 weeks",
                "goals": [
                    "Practice with real examples",
                    "Compare common patterns",
                    "Explain the concept in your own words",
                ],
                "resources": [
                    "Practice exercises",
                    "Worked examples",
                    "Review articles",
                ],
            },
            {
                "level": "Advanced",
                "topic": f"Mastering {topic}",
                "duration": "3 weeks",
                "goals": [
                    "Solve more complex problems",
                    "Connect ideas across topics",
                    "Apply the concept in new situations",
                ],
                "resources": [
                    "Advanced reading material",
                    "Case studies",
                    "Project-based exercises",
                ],
            },
        ],
    }

    parsed = LearningPathResponse.model_validate(data)
    return parsed


def _offline_fallback(prompt: str, *, system_instruction: str | None = None, response_schema=None):
    topic_hint = (prompt or "").strip().splitlines()
    topic = "the requested topic"

    if topic_hint:
        topic = topic_hint[0].strip() or topic

    if response_schema is QuizResponse:
        parsed = _fallback_quiz_response(topic)
        return (
            "Offline fallback response generated because no Gemini API key is configured.",
            SimpleNamespace(text='{"questions": []}', parsed=parsed),
        )

    if response_schema is LearningPathResponse:
        parsed = _fallback_learning_path_response(topic)
        return (
            "Offline fallback response generated because no Gemini API key is configured.",
            SimpleNamespace(text='{"topic": ""}', parsed=parsed),
        )

    fallback_text = (
        "Offline fallback mode is active because GEMINI_API_KEY is not configured. "
        "Add the API key to your .env file to enable live Gemini responses."
    )
    return fallback_text, SimpleNamespace(text=fallback_text, parsed=None)


# --------------------------------------------------
# GENERATE TEXT
# --------------------------------------------------

def generate_text(
    prompt: str,
    *,
    system_instruction: str | None = None,
    temperature: float = 0.3,
    max_output_tokens: int = 1200,
    response_schema=None,
):

    if not GEMINI_API_KEY and ALLOW_OFFLINE_FALLBACK:
        return _offline_fallback(
            prompt,
            system_instruction=system_instruction,
            response_schema=response_schema,
        )

    client = get_client()


    config_options = {
        "temperature": temperature,
        "max_output_tokens": max_output_tokens,
    }


    if system_instruction:

        config_options[
            "system_instruction"
        ] = system_instruction


    # Structured JSON response
    if response_schema is not None:

        config_options[
            "response_mime_type"
        ] = "application/json"

        config_options[
            "response_schema"
        ] = response_schema


    response = client.models.generate_content(

        model=GEMINI_MODEL,

        contents=prompt,

        config=types.GenerateContentConfig(
            **config_options
        ),
    )


    text = getattr(
        response,
        "text",
        None
    )


    if not text:

        raise RuntimeError(
            "Gemini returned an empty response."
        )


    return text.strip(), response