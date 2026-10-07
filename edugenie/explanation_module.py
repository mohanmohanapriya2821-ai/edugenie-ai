from functools import lru_cache

from config import (
    USE_LOCAL_EXPLAINER,
    LOCAL_EXPLAINER_MODEL,
    MAX_INPUT_CHARS,
)

from gemini_client import generate_text


# --------------------------------------------------
# GEMINI SYSTEM PROMPT
# --------------------------------------------------

GEMINI_SYSTEM = """
You are EduGenie.

You explain educational concepts to beginners.

Use:

1. Simple definition
2. Easy explanation
3. Step-by-step understanding
4. Example
5. Important point

Avoid unnecessary jargon.
"""


# --------------------------------------------------
# LOAD LOCAL MODEL
# --------------------------------------------------

@lru_cache(maxsize=1)
def load_local_model():

    from transformers import (
        AutoTokenizer,
        AutoModelForSeq2SeqLM,
    )


    tokenizer = AutoTokenizer.from_pretrained(
        LOCAL_EXPLAINER_MODEL
    )


    model = AutoModelForSeq2SeqLM.from_pretrained(
        LOCAL_EXPLAINER_MODEL
    )


    return tokenizer, model


# --------------------------------------------------
# LOCAL EXPLANATION
# --------------------------------------------------

def local_explanation(topic: str) -> str:

    import torch


    tokenizer, model = load_local_model()


    prompt = f"""
Explain the following educational topic
in simple language for a beginner.

Topic:

{topic}

Include a simple example.
"""


    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )


    with torch.no_grad():

        output = model.generate(

            **inputs,

            max_new_tokens=220,

            num_beams=4,

            early_stopping=True,
        )


    return tokenizer.decode(
        output[0],
        skip_special_tokens=True
    ).strip()


# --------------------------------------------------
# MAIN EXPLANATION FUNCTION
# --------------------------------------------------

def explain_topic(topic: str) -> str:

    topic = topic[
        :MAX_INPUT_CHARS
    ]


    # Try local model
    if USE_LOCAL_EXPLAINER:

        try:

            return local_explanation(
                topic
            )

        except Exception:

            # Fall back to Gemini
            pass


    # Gemini explanation
    prompt = f"""
Explain the following topic to a beginner:

{topic}

Use this structure:

1. Simple definition
2. How it works
3. Easy example
4. Important point to remember
"""


    explanation, _ = generate_text(

        prompt,

        system_instruction=GEMINI_SYSTEM,

        temperature=0.25,

        max_output_tokens=1200,
    )


    return explanation