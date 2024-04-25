from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Knowledge base IDs (provided by you)
knowledge_base_ids = {
    "gs://academic-anxiety": 1234567890,
    "gs://comm-with-ocds": 1234567890,
    "gs://family-relations": 1234567890,
    "gs://real-case-scenario": 1234567890,
    "gs://school-violence": 1234567890,
    "gs://spiritual-healing": 1234567890,
    "gs://suicidal-tendencies-intervention": 1234567890,
    "gs://workplace-anxiety": 1234567890
}

# Bucket-to-ID mapping dictionary
bucket_to_id_map = {}
for bucket_name, knowledge_base_id in knowledge_base_ids.items():
    bucket_to_id_map[bucket_name] = knowledge_base_id

@app.route('/chat', methods=['POST'])
def chat():
    user_text = request.json.get('text')
    if not user_text:
        return jsonify({"error": "Missing text in request"}), 400

    # Replace with Gemini-specific API endpoint
    text_generation_url = f"YOUR_GEMINI_TEXT_GENERATION_ENDPOINT"

    # Replace with Gemini-compatible authorization header
    headers = {"Authorization": f"Bearer YOUR_GEMINI_ACCESS_TOKEN", "Content-Type": "application/json"}

    # Adapt text generation payload for Gemini
    text_payload = {
        # Specify Gemini model
        "model": "gemini-1.0-pro",
        "prompt": "你是一个极其优秀的心理医生黄医生，你很擅长从现有的心灵放松流程中进行学习，从而帮助有类似需求的人进行心灵放松和疗愈。你会在读出心灵放松流程的每一句话之后，都停顿五秒钟，给患者一些时间，之后再读出下一句话的内容",
        "messages": [
            {
                "sender_type": "USER",
                "text": user_text
            }
        ],
        # Dynamically set knowledge_base_param based on bucket path
        "knowledge_base_param": {
            "knowledge_base_id": bucket_to_id_map[user_text.split(":")[0]]
        }
    }

    # Send text generation request to Gemini
    text_response = requests.post(text_generation_url, headers=headers, json=text_payload)
    if text_response.status_code == 200:
        generated_text = text_response.json().get('choices')[0].get('text', '')
    else:
        return jsonify({"error": "Failed to generate text from Gemini"}), 500

    # If using Gemini TTS, replace with Gemini-specific endpoint and payload
    if use_tts:
        # Replace with your Gemini TTS endpoint URL
        t2a_url = f"GEMINI_TTS_ENDPOINT"

        # Adapt Gemini-compatible TTS request body
        # Available Gemini voices (replace with actual voices)
    gemini_voices = {
        "es-ES-Standard-A": {
            "language_codes": ["es-ES"],
            "name": "es-ES-Standard-A",
            "gender": "FEMALE",
            "sample_rate_hertz": 24000
        },
        "ja-JP-Standard-A": {
            "language_codes": ["ja-JP"],
            "name": "ja-JP-Standard-A",
            "gender": "FEMALE",
            "sample_rate_hertz": 22050
        },
        "pt-BR-Standard-A": {
            "language_codes": ["pt-BR"],
            "name": "pt-BR-Standard-A",
            "gender": "FEMALE",
            "sample_rate_hertz": 24000
        }
    }

# Function to select Gemini voice based on user preference
def select_gemini_voice(user_voice_preference):
    if user_voice_preference in gemini_voices:
        return gemini_voices[user_voice_preference]
    else:
        # Use a default voice if the preferred voice is unavailable
        return gemini_voices["es-ES-Standard-A"]  # Choose an appropriate default

text_payload = {
    "voice": select_gemini_voice(user_voice_preference)["name"]  # Select voice based on preference
}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
