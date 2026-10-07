from pydantic import BaseModel, Field, field_validator


# --------------------------------------------------
# GENERAL TEXT REQUEST
# --------------------------------------------------

class TextRequest(BaseModel):

    text: str = Field(
        ...,
        min_length=1,
        max_length=20000
    )

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("text must not be empty")

        return value


# --------------------------------------------------
# QUIZ QUESTION
# --------------------------------------------------

class QuizQuestion(BaseModel):

    question: str

    options: list[str] = Field(
        ...,
        min_length=4,
        max_length=4
    )

    correct_answer: str

    explanation: str

    @field_validator("correct_answer")
    @classmethod
    def validate_correct_answer(cls, value: str, info):
        options = info.data.get("options")

        if options is not None and value not in options:
            raise ValueError("correct_answer must match one of the provided options")

        return value


# --------------------------------------------------
# QUIZ RESPONSE
# --------------------------------------------------

class QuizResponse(BaseModel):

    questions: list[QuizQuestion] = Field(
        ...,
        min_length=3,
        max_length=3
    )


# --------------------------------------------------
# LEARNING STEP
# --------------------------------------------------

class LearningStep(BaseModel):

    level: str

    topic: str

    duration: str

    goals: list[str]

    resources: list[str]


# --------------------------------------------------
# LEARNING PATH RESPONSE
# --------------------------------------------------

class LearningPathResponse(BaseModel):

    topic: str

    overview: str

    steps: list[LearningStep]