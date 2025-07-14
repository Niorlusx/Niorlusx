import os
from datetime import datetime
from flask import Flask, request, send_file
from twilio.twiml.voice_response import VoiceResponse
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

conversation_history = {}

def get_history(call_sid):
    if call_sid not in conversation_history:
        conversation_history[call_sid] = [
            {
                "role": "system",
                "content": (
                    "You are Niorlusx AI, an emotionally adaptive voice agent."
                ),
            }
        ]
    return conversation_history[call_sid]

@app.route("/incoming_call", methods=["POST"])
def incoming_call():
    call_sid = request.values.get("CallSid")
    get_history(call_sid)
    resp = VoiceResponse()
    resp.say("Welcome to Niorlusx AI Call Service. Please speak after the beep.")
    resp.record(
        timeout=5,
        transcribe=True,
        transcribeCallback="/handle_speech",
        playBeep=True,
    )
    resp.redirect("/handle_speech")
    return str(resp)

@app.route("/handle_speech", methods=["POST"])
def handle_speech():
    call_sid = request.values.get("CallSid")
    text = request.values.get("TranscriptionText")
    resp = VoiceResponse()
    if not call_sid:
        resp.say("Missing call info.")
        return str(resp)
    if text:
        history = get_history(call_sid)
        history.append({"role": "user", "content": text})
        chat = openai_client.chat.completions.create(
            model="gpt-4o", messages=history
        )
        ai_text = chat.choices[0].message.content
        history.append({"role": "assistant", "content": ai_text})
        audio_path = f"/tmp/resp_{call_sid}.mp3"
        with openai_client.audio.speech.with_streaming_response.create(
            model="tts-1", voice="nova", input=ai_text
        ) as stream:
            stream.stream_to_file(audio_path)
        with open("call_logs.txt", "a") as log:
            log.write(f"[{datetime.utcnow()}] {call_sid}: {text}\n")
        resp.play(url=request.url_root + f"play_audio?sid={call_sid}")
        resp.record(
            timeout=5, transcribe=True, transcribeCallback="/handle_speech", playBeep=True
        )
    else:
        resp.say("I didn't catch that. Please repeat.")
        resp.record(
            timeout=5, transcribe=True, transcribeCallback="/handle_speech", playBeep=True
        )
    return str(resp)

@app.route("/play_audio")
def play_audio():
    sid = request.args.get("sid")
    path = f"/tmp/resp_{sid}.mp3"
    return send_file(path, mimetype="audio/mpeg")

@app.route("/")
def index():
    return "Niorlusx AI Call Service running"

if __name__ == "__main__":
    if not os.path.exists("/tmp"):
        os.makedirs("/tmp")
    app.run(host="0.0.0.0", port=8000)
