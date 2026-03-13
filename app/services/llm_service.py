import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL = "phi3"   # or llama3


def generate_study_plan(topics, ability):

    prompt = f"""
A student completed an adaptive GRE test.

Ability Score: {ability}

Weak Topics: {topics}

Create a 3-step study plan to improve these topics.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    return data["response"]