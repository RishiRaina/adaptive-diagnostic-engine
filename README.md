# AI-Driven Adaptive Diagnostic Engine

This project implements a 1-Dimensional Adaptive Testing Prototype that dynamically selects questions based on a student's previous answers. The system estimates a student's proficiency level and adjusts question difficulty accordingly.

The system simulates how modern standardized exams like GRE, GMAT, or CAT adapt question difficulty to better estimate a student's ability.


--------------------------------
OVERVIEW
--------------------------------

Traditional assessments ask every student the same questions. Adaptive testing instead adjusts question difficulty based on performance, allowing faster and more accurate ability estimation.

This project demonstrates a simplified adaptive testing engine using:

• FastAPI backend  
• MongoDB database  
• IRT-inspired adaptive algorithm  
• LLM integration for personalized study recommendations


--------------------------------
SYSTEM ARCHITECTURE
--------------------------------

Student / Client
        |
        v
FastAPI Backend
        |
        v
Adaptive Engine (IRT Logic)
        |
        v
MongoDB Database (Questions + Session Data)
        |
        v
LLM (Ollama)
        |
        v
Personalized Study Plan


--------------------------------
TECH STACK
--------------------------------

Backend Framework: FastAPI (Python)

Database: MongoDB Atlas

Adaptive Algorithm: Item Response Theory Inspired Logic

LLM Integration: Ollama 

API Testing: Swagger UI



--------------------------------
HOW TO RUN THE PROJECT
--------------------------------

1. Install Dependencies

pip install -r requirements.txt


2. Setup Environment Variables

Create a `.env` file in the project root directory.

Example:

MONGO_URI=your_mongodb_connection_string  
DB_NAME=adaptive_test

This connects the backend to your MongoDB database.


3. Seed the Question Database

Insert GRE-style questions into MongoDB:

python -m app.utils.seed_questions

This populates the questions collection.


4. Start the FastAPI Server

uvicorn app.main:app --reload

Server will start at:

http://127.0.0.1:8000


5. Test the APIs

Open Swagger UI:

http://127.0.0.1:8000/docs

Swagger provides an interactive interface for testing all endpoints.


--------------------------------
ADAPTIVE ALGORITHM LOGIC
--------------------------------

Each student session maintains an ability score (θ).

Initial ability:

θ = 0.5


Each question has a difficulty level (d) between:

0.1 → Easy  
1.0 → Hard


After each answer, the ability score is updated using a logistic function inspired by Item Response Theory (IRT).

Probability of Correct Answer:

p = 1 / (1 + e^(-(θ - d)))


Ability Update Rule

If answer is correct:

θ_new = θ + learning_rate * (1 − p)


If answer is incorrect:

θ_new = θ − learning_rate * p


This causes:

correct answers → higher ability → harder questions  
incorrect answers → lower ability → easier questions

Questions already answered are excluded to prevent repetition.


--------------------------------
PERSONALIZED AI STUDY PLAN
--------------------------------

After 10 questions, the system analyzes:

• final ability score  
• topics answered incorrectly

These are sent to an LLM to generate a personalized 3-step learning plan.

Example prompt sent to the LLM:

Student ability score: 0.62  
Weak topics: Algebra, Geometry  

Generate a 3 step study plan.


Example output:

1. Review algebraic equations and variable manipulation  
2. Study triangle and angle properties in geometry  
3. Practice mixed GRE quantitative problem sets


--------------------------------
API DOCUMENTATION
--------------------------------

1. Start Session

POST /start-session

Creates a new testing session.

Response:

{
 "session_id": "uuid"
}


2. Get Next Question

GET /next-question/{session_id}

Returns a question matching the student's ability level.

Response:

{
 "question_id": "...",
 "question": "...",
 "options": [...]
}


3. Submit Answer

POST /submit-answer

Parameters:

session_id  
question_id  
answer  


Response:

{
 "correct": true
}

After the final question:

{
 "test_complete": true,
 "final_ability": 0.63,
 "study_plan": "..."
}


--------------------------------
AI LOG
--------------------------------

AI tools such as ChatGPT and Cursor were used during development.

AI assisted in:

• Designing the FastAPI project architecture  
• Generating the MongoDB schema structure  
• Implementing the adaptive ability update logic  
• Debugging ObjectId conversion issues in MongoDB queries  
• Improving adaptive question selection to prevent repeated questions  
• Generating sample GRE-style questions for seeding the database


Challenges AI Could Not Fully Solve

Some issues required manual debugging and understanding:

• MongoDB ObjectId type mismatches  
• Handling edge cases when no question matched the ability range  
• Ensuring answered questions were excluded from future queries

These problems required analyzing server logs and modifying database queries.


--------------------------------
FUTURE IMPROVEMENTS
--------------------------------

Possible improvements for a production system:

• Implement full 2-Parameter IRT model  
• Use difficulty optimization instead of difficulty ranges  
• Add a frontend dashboard for students  
• Track progress across multiple testing sessions  
• Introduce topic-specific adaptive testing


