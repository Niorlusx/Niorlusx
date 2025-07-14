from datetime import datetime
from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.post("/voice", response_class=PlainTextResponse)
async def voice_reply(SpeechResult: str = Form(None)):
    print(f"[DEBUG] Received SpeechResult: {SpeechResult}")
    log_entry = f"[{datetime.utcnow()}] Incoming text: {SpeechResult}"
    with open("call_logs.txt", "a") as log_file:
        log_file.write(log_entry + "\n")
    return "OK"

# Future dashboard integration
print("[DEBUG] Metrics dashboard placeholder added.")
