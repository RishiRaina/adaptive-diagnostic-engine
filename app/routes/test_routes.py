from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.database import questions_collection, sessions_collection
from app.services.adaptive_engine import update_ability
from app.services.llm_service import generate_study_plan
import uuid

router = APIRouter()

TOTAL_QUESTIONS = 10


# -------------------------
# START SESSION
# -------------------------
@router.post("/start-session")
def start_session():

    session_id = str(uuid.uuid4())

    session = {
        "session_id": session_id,
        "ability": 0.5,
        "answered_questions": [],
        "topics_wrong": []
    }

    sessions_collection.insert_one(session)

    return {"session_id": session_id}


# -------------------------
# GET NEXT QUESTION
# -------------------------
@router.get("/next-question/{session_id}")
def next_question(session_id: str):

    session = sessions_collection.find_one({"session_id": session_id})

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    ability = session["ability"]
    answered = session["answered_questions"]

    question = questions_collection.find_one({
        "difficulty": {"$gte": ability - 0.1, "$lte": ability + 0.1},
        "_id": {"$nin": answered}
    })

    if not question:
        raise HTTPException(status_code=404, detail="No more questions available")

    return {
        "question_id": str(question["_id"]),
        "question": question["question"],
        "options": question["options"]
    }


# -------------------------
# SUBMIT ANSWER
# -------------------------
@router.post("/submit-answer")
def submit_answer(session_id: str, question_id: str, answer: str):

    session = sessions_collection.find_one({"session_id": session_id})

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    question = questions_collection.find_one({"_id": ObjectId(question_id)})

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    correct = answer == question["correct_answer"]

    # Update ability using IRT logic
    new_ability = update_ability(
        session["ability"],
        question["difficulty"],
        correct
    )

    update_data = {
        "$set": {"ability": new_ability},
        "$push": {"answered_questions": ObjectId(question_id)}
    }

    # Track weak topics
    if not correct:
        update_data["$push"] = {
            "answered_questions": ObjectId(question_id),
            "topics_wrong": question["topic"]
        }

    sessions_collection.update_one(
        {"session_id": session_id},
        update_data
    )

    # Check if test finished
    updated_session = sessions_collection.find_one({"session_id": session_id})

    if len(updated_session["answered_questions"]) >= TOTAL_QUESTIONS:

        study_plan = generate_study_plan(
            updated_session["topics_wrong"],
            updated_session["ability"]
        )

        return {
            "test_complete": True,
            "final_ability": updated_session["ability"],
            "study_plan": study_plan
        }

    return {"correct": correct}