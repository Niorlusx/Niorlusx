# Carrier Aggregator Integration

The following steps outline how to connect a carrier aggregator to the
Niorlusx AI Call Service. Debug statements mirror what you might log while
setting things up.

1. **Choose and Register**
   ```python
   print("[DEBUG] Selected aggregator and started registration.")
   ```
   - Apply with a provider such as mVoice, Red Telecom or Boku.
   - Provide forecasts and compliance documents.
   - Once approved you'll receive a premium-rate `190x` number.
   - Set payout bank details (Australian bank account).

2. **Configuration**
   ```python
   print("[DEBUG] Configuring premium-rate number and SIP trunk.")
   ```
   - Point the issued premium number to your Twilio SIP domain.
   - The aggregator will handle caller billing automatically.
   - You receive monthly or bi-weekly payout reports.

3. **Pricing Announcement**
   ```python
   print("[DEBUG] Pricing announcement setup step.")
   ```
   - Play an upfront disclosure such as `$4.95 per minute` using a TwiML
     `<Say>` verb or a custom audio file.
