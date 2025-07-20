# Running the Call Service in Termux

This guide outlines how to run the Flask-based Niorlusx AI call service directly on an Android device using the Termux app.

## Step 1: Prepare your workspace
```bash
cd ~
mkdir -p niorlusx-call-service
cd niorlusx-call-service
```

## Step 2: Install dependencies
```bash
pkg install python -y
pip install --upgrade pip
pip install flask twilio openai python-dotenv
mkdir -p $HOME/niorlusx_logs
```

## Step 3: Create the `.env` file
```bash
cat > .env <<'EOT'
OPENAI_API_KEY=[KEY REDACTED]
EOT
```
Replace `[KEY REDACTED]` with your actual API key locally.

## Step 4: Write the Flask app
Copy the `app.py` from this repository into your Termux directory. A log file will be written to `$HOME/niorlusx_logs/app.log`.

## Step 5: Run the service
```bash
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=8080
```
Leave the session running and point your Twilio Voice webhook to:
```
http://<YOUR_PUBLIC_IP>:8080/voice
```
Check `$HOME/niorlusx_logs/app.log` for call details and errors.
