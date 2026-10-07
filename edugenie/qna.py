from gemini_client import generate_text

from config import MAX_INPUT_CHARS


SYSTEM_INSTRUCTION = """
You are EduGenie, an educational AI assistant.

Your job is to answer student questions accurately,
clearly and in simple language.

Rules:

1. Give the direct answer first.
2. Explain the answer clearly.
3. Use examples when useful.
4. Avoid unnecessary technical jargon.
5. If the question is ambiguous, mention the assumption.
6. Never invent citations.
7. If you are uncertain, clearly say so.
"""


def answer_question(question: str) -> str:

    question = question[
        :MAX_INPUT_CHARS
    ]


    prompt = f"""
A student has asked the following question:

{question}

Answer the question in a clear educational manner.

Include a short example if it helps understanding.
"""


    answer, _ = generate_text(

        prompt,

        system_instruction=SYSTEM_INSTRUCTION,

        temperature=0.2,

        max_output_tokens=1000,
    )


    return answer