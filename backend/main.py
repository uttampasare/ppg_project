from fastapi import FastAPI, UploadFile, File
import tempfile
from backend.ppg import extract_ppg_from_video
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LLM_ENDPOINT = "http://localhost:11434/api/generate"   # Replace with your LLM API

def call_llm_with_bpm(bpm):
    prompt = f"""Health Indicator:
                 Heart Rate: {bpm} BPM

                 Provide a personalized wellbeing and healthy behaviour
                 interpretation based on this reading.

                 Structure your response as follows:

                 1. HEALTH INTERPRETATION:
                    Explain what the heart-rate reading may indicate.
                    Consider whether it is within the typical adult resting
                    heart-rate range, if it was measured at rest.

                 2. WELLBEING INSIGHT:
                    Explain possible lifestyle factors influencing this reading.

                 3. AYURVEDIC WELLNESS SUGGESTIONS:
                    Provide safe, general Ayurveda-inspired daily wellness
                    recommendations.

                 4. ADAPTIVE BEHAVIOUR CHANGE PLAN:
                    Suggest three small and achievable healthy lifestyle actions.

                 5. DAILY HEALTHY HABITS:
                    Recommend practical improvements in food, movement,
                    sleep and stress management.

                 6. MOTIVATIONAL MESSAGE:
                    End with one encouraging message to support sustainable
                    healthy behaviour.

                 Important:
                 - Do not assume this is a resting heart-rate measurement.
                 - Do not diagnose any disease.
                 - Avoid unsupported medical or Ayurvedic claims.
                 - Mention when medical assessment is appropriate.
                 - Keep the response simple, actionable and personalized.
                 """

    payload = {
        "model": "llama3.1",
        "prompt": prompt,
        "stream": False
    }
    print("Calling LLM :", payload)
    response = requests.post(LLM_ENDPOINT, json=payload)

    # Debug: print raw text if needed
    print("RAW:", response.text)

    return response.json()

@app.post("/extract_pulse")
async def extract_pulse(video: UploadFile = File(...)):
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.write(await video.read())
    temp.close()

    bpm = extract_ppg_from_video(temp.name)
    llm_response = call_llm_with_bpm(bpm)
#     print("--- llm_response -----:", llm_response)
#     print("---- response from llm ----", llm_response.get("response", ""))
    return {
        "bpm": bpm,
        "llm_analysis": llm_response.get("response", "")
    }

    # Send result to LLM
#     llm_payload = {
#         "model": "llama3.1",
#         "messages": [
#             {"role": "user", "content": "Provide a health interpretation."}
#         ],
#         "prompt": f"The user's heart rate is {bpm} bpm. Provide a health interpretation."
#     }

#     llm_payload = {
#         "model": "llama3.1",
#         "prompt": f"The user's heart rate is {bpm} bpm. Provide a health interpretation.",
#         "stream": False
#     }

#     llm_response = requests.post(LLM_ENDPOINT, json=llm_payload).json()
#     llm_response = requests.post(LLM_ENDPOINT, json=llm_payload).json()
#     return {
#         "heart_rate_bpm": bpm,
#         "llm_interpretation": llm_response.get("response", "No LLM response")
#     }
#
#     return {
#         "llm_output": llm_response
#     }