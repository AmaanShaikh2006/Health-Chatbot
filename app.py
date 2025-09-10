from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from kb import get_disease_info, get_disease_by_symptoms

app = Flask(__name__)
user_states = {}

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    user_number = request.values.get("From")
    incoming_msg = request.values.get("Body", "").strip()
    state = user_states.get(user_number, "main_menu")

    resp = MessagingResponse()
    msg = resp.message()

    if state == "main_menu":
        if incoming_msg == "1":
            msg.body("🔎 Enter a disease name (e.g., Dengue, Malaria, Diabetes).")
            user_states[user_number] = "waiting_for_disease"
        elif incoming_msg == "2":
            msg.body("📝 Enter symptoms separated by commas (e.g., Fever, Cough, Headache).")
            user_states[user_number] = "waiting_for_symptoms"
        else:
            msg.body("👋 Welcome to HealthBot!\n\nType:\n1️⃣ Know about a Disease\n2️⃣ Know Disease from Symptoms")
    
    elif state == "waiting_for_disease":
        msg.body(get_disease_info(incoming_msg))
        user_states[user_number] = "main_menu"

    elif state == "waiting_for_symptoms":
        symptoms = [s.strip() for s in incoming_msg.split(",")]
        msg.body(get_disease_by_symptoms(symptoms))
        user_states[user_number] = "main_menu"

    return str(resp)

if __name__ == "__main__":
    app.run(port=5000)
