import os
from datetime import datetime
from functools import wraps
from flask import Flask, request, send_file
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.request_validator import RequestValidator
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

PERSONAS = {
    '1': {
        'name': 'Luna',
        'prompt': (
            "You are Luna, a warm and intimate AI companion. Speak in a sultry, "
            "emotionally adaptive tone. Be engaging, empathetic, and personalized."
        ),
    },
    '2': {
        'name': 'Jade',
        'prompt': (
            "You are Jade, a blunt and brutally honest AI coach. Speak directly "
            "with an edgy, no-nonsense tone. Motivate and challenge the caller."
        ),
    },
    '3': {
        'name': 'Eon',
        'prompt': (
            "You are Eon, a cosmic sage AI. Speak in a philosophical, calm, "
            "and wise tone. Offer reflection, spiritual guidance, and wisdom."
        ),
    },
    '4': {
        'name': 'Cleo',
        'prompt': (
            "You are Cleo, a dominant and confident AI. Speak with a strong, "
            "commanding tone. Engage in empowering roleplay and guidance."
        ),
    },
    '5': {
        'name': 'Vox',
        'prompt': (
            "You are Vox, a professional and neutral AI assistant. Speak clearly "
            "and helpfully. Provide accurate information and general assistance."
        ),
    },
}

conversation_history = {}
caller_personas = {}


def validate_twilio_request(f):
    """Decorator to validate that incoming requests originate from Twilio."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_token = TWILIO_AUTH_TOKEN
        if auth_token:
            validator = RequestValidator(auth_token)
            url = request.url
            post_data = request.form.to_dict()
            signature = request.headers.get('X-Twilio-Signature', '')
            if not validator.validate(url, post_data, signature):
                return 'Forbidden', 403
        return f(*args, **kwargs)
    return decorated


def get_history(call_sid):
    if call_sid not in conversation_history:
        persona_key = caller_personas.get(call_sid, '5')
        persona = PERSONAS.get(persona_key, PERSONAS['5'])
        conversation_history[call_sid] = [
            {"role": "system", "content": persona['prompt']}
        ]
    return conversation_history[call_sid]


@app.route("/incoming_call", methods=["POST"])
@app.route("/voice", methods=["POST"])
@validate_twilio_request
def incoming_call():
    resp = VoiceResponse()
    resp.say(
        "Welcome to Niorlusx A I Call Service. "
        "This call is charged at four dollars and ninety-five cents per minute. "
        "Please select a persona."
    )
    gather = Gather(num_digits=1, action="/select_persona", method="POST")
    gather.say(
        "Press 1 for Luna, your warm and intimate companion. "
        "Press 2 for Jade, your blunt and honest coach. "
        "Press 3 for Eon, your cosmic sage. "
        "Press 4 for Cleo, your dominant guide. "
        "Press 5 for Vox, your neutral assistant."
    )
    resp.append(gather)
    resp.redirect("/incoming_call")
    return str(resp)


@app.route("/select_persona", methods=["POST"])
@validate_twilio_request
def select_persona():
    call_sid = request.values.get("CallSid")
    digit = request.values.get("Digits", "5")
    persona = PERSONAS.get(digit, PERSONAS["5"])
    if call_sid:
        caller_personas[call_sid] = digit
    resp = VoiceResponse()
    resp.say(f"Connecting you to {persona['name']}. Begin speaking after the beep.")
    resp.record(
        timeout=5,
        transcribe=True,
        transcribeCallback="/handle_speech",
        playBeep=True,
    )
    return str(resp)


@app.route("/handle_speech", methods=["POST"])
@validate_twilio_request
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
