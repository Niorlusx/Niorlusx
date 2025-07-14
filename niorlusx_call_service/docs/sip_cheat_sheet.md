# SIP Setup Cheat Sheet

Use this short guide to configure a Twilio SIP domain and route calls to the
AI backend. Debug print statements illustrate key stages.

1. **Setup Twilio SIP Domain**
   ```python
   print("[DEBUG] Starting SIP domain setup in Twilio.")
   ```
   - Create a domain named `niorlusx-voice-service`.
   - SIP URI: `niorlusx-voice-service.sip.twilio.com`.

   ```python
   print("[DEBUG] SIP domain configured with authentication.")
   ```

2. **Authentication**
   - Use an IP ACL or create credentials such as `niorlusx_sip` and a password.

3. **Configure Voice URL**
   - Point to your backend endpoint:
     `https://your-server-domain/voice`

4. **Call Handling**
   - Inbound calls → SIP → AI backend → TwiML response.

