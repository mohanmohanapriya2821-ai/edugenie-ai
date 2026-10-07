import json

from gemini_client import generate_text

from schemas import (
    LearningPathResponse,
)


def get_learning_recommendations(
    topic: str
) -> LearningPathResponse:


    prompt = f"""
Create a complete learning path for:

{topic}

The learning path must progress from
beginner to advanced.

For every learning step provide:

- level
- topic
- realistic duration
- learning goals
- useful learning resources

Make the plan practical for a student.

Do not invent specific URLs.
"""


    _, response = generate_text(

        prompt,

        system_instruction="""
You are EduGenie, an expert learning-path planner.

Organize subjects logically from basic
concepts to advanced concepts.
""",

        temperature=0.35,

        max_output_tokens=2200,

        response_schema=LearningPathResponse,
    )


    parsed = getattr(
        response,
        "parsed",
        None
    )


    if parsed is not None:

        if isinstance(
            parsed,
            LearningPathResponse
        ):

            return parsed


        return LearningPathResponse.model_validate(
            parsed
        )


    raw = getattr(
        response,
        "text",
        ""
    )


    return LearningPathResponse.model_validate(
        json.loads(raw)
    )