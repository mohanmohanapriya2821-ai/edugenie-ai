from fastapi.testclient import TestClient

import main


client = TestClient(
    main.app
)


# ============================================
# HEALTH
# ============================================

def test_health():

    response =client.get("/health")

    assert response.status_code == 200

    assert response.json()["status"] == "ok"


# ============================================
# HOME PAGE
# ============================================

def test_home():

    response = client.get("/")

    assert response.status_code == 200

    assert "EduGenie" in response.text


# ============================================
# VALIDATION
# ============================================

def test_validation():

    response = client.post(
        "/qa",
        json={
            "text": ""
        }
    )

    assert response.status_code == 422


# ============================================
# Q&A
# ============================================

def test_qa(
    monkeypatch
):

    monkeypatch.setattr(
        main,
        "answer_question",
        lambda text:
            "Mock answer"
    )


    response = client.post(

        "/qa",

        json={
            "text":
                "What is Python?"
        }

    )


    assert response.status_code == 200

    assert (
        response.json()["answer"]
        ==
        "Mock answer"
    )


# ============================================
# EXPLANATION
# ============================================

def test_explain(
    monkeypatch
):

    monkeypatch.setattr(

        main,

        "explain_topic",

        lambda text:
            "Mock explanation"

    )


    response = client.post(

        "/explain",

        json={
            "text":
                "Python"
        }

    )


    assert response.status_code == 200

    assert (
        response.json()["explanation"]
        ==
        "Mock explanation"
    )


# ============================================
# SUMMARY
# ============================================

def test_summary(
    monkeypatch
):

    monkeypatch.setattr(

        main,

        "summarize_text",

        lambda text:
            "Mock summary"

    )


    response = client.post(

        "/summarize",

        json={
            "text":
                "Long educational text"
        }

    )


    assert response.status_code == 200

    assert (
        response.json()["summary"]
        ==
        "Mock summary"
    )


# ============================================
# QUIZ
# ============================================

def test_quiz(
    monkeypatch
):

    from schemas import (
        QuizResponse,
        QuizQuestion
    )


    quiz = QuizResponse(

        questions=[

            QuizQuestion(

                question="Question 1",

                options=[
                    "A",
                    "B",
                    "C",
                    "D"
                ],

                correct_answer="A",

                explanation=
                    "Explanation 1"

            ),

            QuizQuestion(

                question="Question 2",

                options=[
                    "A",
                    "B",
                    "C",
                    "D"
                ],

                correct_answer="B",

                explanation=
                    "Explanation 2"

            ),

            QuizQuestion(

                question="Question 3",

                options=[
                    "A",
                    "B",
                    "C",
                    "D"
                ],

                correct_answer="C",

                explanation=
                    "Explanation 3"

            )

        ]

    )


    monkeypatch.setattr(

        main,

        "generate_quiz",

        lambda text:
            quiz

    )


    response = client.post(

        "/quiz",

        json={
            "text":
                "Educational lesson"
        }

    )


    assert response.status_code == 200

    assert (
        len(
            response.json()["questions"]
        )
        ==
        3
    )


# ============================================
# LEARNING PATH
# ============================================

def test_learning_path(
    monkeypatch
):

    from schemas import (
        LearningPathResponse,
        LearningStep
    )


    path = LearningPathResponse(

        topic="SQL",

        overview=
            "Mock learning path",

        steps=[

            LearningStep(

                level="Beginner",

                topic="SELECT",

                duration="1 week",

                goals=[
                    "Understand queries"
                ],

                resources=[
                    "Official documentation"
                ]

            )

        ]

    )


    monkeypatch.setattr(

        main,

        "get_learning_recommendations",

        lambda text:
            path

    )


    response = client.post(

        "/learn/recommendations",

        json={
            "text":
                "SQL"
        }

    )


    assert response.status_code == 200

    assert (
        response.json()["topic"]
        ==
        "SQL"
    )