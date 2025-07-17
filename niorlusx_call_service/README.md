# Niorlusx AI Call Service

This example Flask application demonstrates a minimal integration of Twilio voice calls with OpenAI's Whisper, GPT-4o and TTS APIs.

## Setup

1. Copy `.env.example` to `.env` and fill in your credentials.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the service:
   ```bash
   ./start.sh
   ```
4. Configure your Twilio number's voice webhook to `https://<your-url>/incoming_call`.

Call logs are appended to `call_logs.txt`.

## Additional Documentation

- `docs/carrier_aggregator.md` – steps for registering with a carrier aggregator with debug statements.
- `docs/sip_cheat_sheet.md` – Twilio SIP setup instructions including debug prints.
- `docs/metrics_example.py` – example endpoint for real-time call metrics with a dashboard placeholder.
- `docs/twilio_flex_sso.md` – how to configure your IdP for Twilio Flex SSO.
- `docs/duckdns_cron.md` – configure a DuckDNS update script with cron.

Repository layout:

```
app.py
requirements.txt
.env.example
start.sh
README.md
twiml.xml
Dockerfile
.github/workflows/deploy.yml
call_logs.txt (auto-created)
```
