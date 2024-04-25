from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

app = Flask(__name__)
CORS(app)  # 启用CORS

def get_access_token():
    credentials = service_account.Credentials.from_service_account_file(
        '/service-account-file.json',  # 替换为实际路径
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )

    # 请求一个访问令牌
    credentials.refresh(Request())
    return credentials.token

def convert_text_to_speech(text):
    url = "https://texttospeech.googleapis.com/v1/text:synthesize"
    token = get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8"
    }
    data = {
        "input": {"text": text},
        "voice": {
            "languageCode": "en-US",
            "name": "en-US-Standard-C",
            "ssmlGender": "FEMALE"
        },
        "audioConfig": {
            "audioEncoding": "MP3"
        }
    }

    # 发送POST请求
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        audio_content = response.json()['audioContent']
        # 返回Base64编码的音频内容
        return f"data:audio/mp3;base64,{audio_content}"
    else:
        return "Failed to generate audio"

@app.route('/tts', methods=['POST'])
def tts():
    if not request.json or 'text' not in request.json:
        return jsonify({"error": "Missing 'text' in request"}), 400

    text = request.json['text']
    audio_data = convert_text_to_speech(text)

    if audio_data.startswith("data:"):
        return jsonify({"audioContent": audio_data})
    else:
        return jsonify({"error": audio_data}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
