from gemini_client import generate_text

from config import MAX_INPUT_CHARS


SYSTEM_INSTRUCTION = """
You are EduGenie's educational summarization assistant.

Summarize educational content accurately.

Keep:

- Important facts
- Definitions
- Main ideas
- Relationships
- Conclusions

Do not introduce information
that does not exist in the original text.
"""


def summarize_text(
    text: str
) -> str:

    text = text[
        :MAX_INPUT_CHARS
    ]


    prompt = f"""
Summarize the following educational passage.

Return:

1. Short overview
2. Key points
3. Important terms or formulas

Educational passage:

{text}
"""


    summary, _ = generate_text(

        prompt,

        system_instruction=SYSTEM_INSTRUCTION,

        temperature=0.2,

        max_output_tokens=1200,
    )


    return summary