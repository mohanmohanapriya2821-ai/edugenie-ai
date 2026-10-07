import json

from gemini_client import generate_text

from schemas import (
    QuizResponse,
)

from config import MAX_INPUT_CHARS


def generate_quiz(
    text: str
) -> QuizResponse:

    text = text[
        :MAX_INPUT_CHARS
    ]


    prompt = f"""
Create exactly 3 multiple-choice questions
from the educational material below.

Requirements:

- Exactly 3 questions.
- Exactly 4 options for every question.
- Only one correct answer.
- correct_answer must exactly match one option.
- Include a short explanation.
- Questions should test understanding.
- Avoid irrelevant questions.

Educational material:

{text}
"""


    _, response = generate_text(

        prompt,

        system_instruction="""
You are an expert educational quiz generator.
Create accurate and useful quizzes for students.
""",

        temperature=0.35,

        max_output_tokens=1800,

        response_schema=QuizResponse,
    )


    # New SDK structured output
    parsed = getattr(
        response,
        "parsed",
        None
    )


    if parsed is not None:

        if isinstance(
            parsed,
            QuizResponse
        ):

            return parsed


        return QuizResponse.model_validate(
            parsed
        )


    # Fallback
    raw = getattr(
        response,
        "text",
        ""
    )


    data = json.loads(raw)


    return QuizResponse.model_validate(
        data
    )