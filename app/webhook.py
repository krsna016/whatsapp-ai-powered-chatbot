import os
import requests
from flask import Blueprint, request, jsonify
from .utils import ollama_generate

# Create a Flask blueprint for the webhook
webhook_blueprint = Blueprint('webhook', __name__)

# Route to handle incoming WhatsApp messages from Twilio
@webhook_blueprint.route("/webhook", methods=["POST"])
def webhook():
    # Twilio sends data as form-url-encoded, not JSON
    incoming_message = request.form.get("Body")
    sender = request.form.get("From")

    if not incoming_message or not sender:
        return jsonify({"error": "Invalid request"}), 400

    # Remove the 'whatsapp:' prefix from sender number
    sender = sender.replace("whatsapp:", "")

    # Get a response from the Ollama API
    response = ollama_generate(incoming_message)

    # Send the response back to WhatsApp using the Twilio API
    send_whatsapp_reply(sender, response)

    return jsonify({"status": "ok"})

# Function to send a message back to WhatsApp via Twilio API
def send_whatsapp_reply(to, message):
    url = f'https://api.twilio.com/2010-04-01/Accounts/{os.getenv("TWILIO_ACCOUNT_SID")}/Messages.json'
    data = {
        'To': f'whatsapp:{to}',
        'From': f'whatsapp:{os.getenv("TWILIO_PHONE_NUMBER")}',
        'Body': message
    }
    auth = (os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
    response = requests.post(url, data=data, auth=auth)
    return response