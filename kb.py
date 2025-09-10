import json

# Load knowledge base JSON
with open("knowledge_base.json", "r", encoding="utf-8") as f:
    kb = json.load(f)

def get_disease_info(disease_name: str) -> str:
    disease_name = disease_name.lower()
    for option in kb["options"]:
        if option["id"] == 1:  # "Know about a Disease"
            for d in option["data"]:
                if d["name"].lower() == disease_name:
                    return (
                        f"🦠 *{d['name']}*\n\n"
                        f"📖 {d['description']}\n\n"
                        f"🔎 Symptoms: {', '.join(d['symptoms'])}\n"
                        f"🛡 Prevention: {', '.join(d['prevention'])}\n"
                        f"💊 Medication: {', '.join(d['medication'])}\n"
                        f"💉 Vaccine: {d['vaccine']}"
                    )
    return "❌ Sorry, I don’t have information about that disease."

def get_disease_by_symptoms(symptom_list: list[str]) -> str:
    for option in kb["options"]:
        if option["id"] == 2:  # "Know Disease from Symptoms"
            for entry in option["data"]:
                if all(sym.lower() in [s.lower() for s in entry["symptoms"]] for sym in symptom_list):
                    return (
                        f"🤒 Based on your symptoms, possible disease: *{entry['disease']}*\n\n"
                        f"📖 {entry['description']}\n"
                        f"🛡 Prevention: {', '.join(entry['prevention'])}\n"
                        f"💊 Medication: {', '.join(entry['medication'])}\n"
                        f"💉 Vaccine: {entry['vaccine']}\n"
                        f"⚠️ {entry['consult_doctor']}"
                    )
    return "⚠️ No exact match found. Please consult a doctor for accurate diagnosis."
