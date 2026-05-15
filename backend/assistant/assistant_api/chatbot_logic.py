import os
import json
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize the Groq client. It will automatically pick up GROQ_API_KEY from the environment.
# We will initialize this lazily in case the key isn't set immediately upon import.
client = None

def get_groq_client():
    global client
    if client is None:
        client = Groq()
    return client

def generate_chat_response(user_message, patient_id="P12345", patient_report=None, chat_history=None):
    """
    Takes a user message, injects the patient's parsed context, and gets a response from the AI.
    """
    if not patient_report:
        return {"error": "patient_report is required now"}
    report = patient_report
    
    # Generate alerts based on the report
    alerts = []
    if report.get('test_results'):
        for test in report['test_results']:
            if test.get('status', '').lower() in ['high', 'low', 'abnormal']:
                alerts.append(f"{test.get('test_name')} is {test.get('status')} ({test.get('value')} {test.get('unit')})")
    
    # Construct a system prompt to give the AI context about the patient
    system_instruction = (
        "You are an AI healthcare assistant. Your primary goal is to help explain the patient's lab results.\n\n"
        "STRICT CONSTRAINTS:\n"
        "1. CONCISENESS: Keep your responses extremely concise, clear, and straight to the point. Do not ramble. Use bullet points if helpful.\n"
        "2. DISCLAIMER: Whenever discussing medical conditions, symptoms, or treatments, you MUST append a brief disclaimer that you are an AI and the patient should consult a doctor.\n"
        "3. NO DIAGNOSIS: Do not diagnose the patient. Only explain the data provided.\n\n"
        f"PATIENT REPORT CONTEXT:\n{json.dumps(report, indent=2)}\n\n"
        f"ACTIVE ALERTS (Abnormal values):\n{json.dumps(alerts, indent=2)}"
    )

    try:
        groq_client = get_groq_client()
        
        # Build the messages array
        messages = [
            {
                "role": "system",
                "content": system_instruction,
            }
        ]
        
        # Inject previous chat history
        if chat_history:
            for msg in chat_history:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
                
        # Append the new user message
        messages.append({
            "role": "user",
            "content": user_message,
        })
        
        response = groq_client.chat.completions.create(
            messages=messages,
            model="llama-3.1-8b-instant",
            temperature=0.4,
        )
        ai_message = response.choices[0].message.content
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        ai_message = "I'm sorry, I'm having trouble connecting to my AI brain right now. Please make sure your GROQ_API_KEY is configured correctly."

    return {
        "response": ai_message,
        "alerts": alerts
    }
