from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from chatbot_logic import generate_chat_response
from database import get_chat_history, add_chat_message, save_medical_report, get_all_medical_reports
from ocr_service import process_document

# Load environment variables (e.g., GEMINI_API_KEY)
load_dotenv()

app = Flask(__name__)
# Allow CORS for the frontend to communicate with the backend
CORS(app)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    if not data or 'message' not in data:
        return jsonify({"error": "Message is required"}), 400
    
    user_message = data['message']
    patient_report = data.get('report')
    
    report_id = patient_report.get('report_id', 'unknown') if patient_report else 'unknown'
    patient_id = patient_report.get('patient_id', 'P12345') if patient_report else 'P12345'
    
    # Save user message to DB
    add_chat_message(patient_id, report_id, 'user', user_message)
    
    # Retrieve full history
    history = get_chat_history(patient_id, report_id)
    # The history currently includes the user message we just saved,
    # but generate_chat_response expects history prior to the current message.
    # We can pass all but the last one.
    history_prior = history[:-1] if history else []
    
    # Pass the custom report and history
    response_data = generate_chat_response(
        user_message, 
        patient_id=patient_id,
        patient_report=patient_report,
        chat_history=history_prior
    )
    
    # Save AI response to DB
    ai_response_text = response_data.get('response', '')
    if ai_response_text:
        add_chat_message(patient_id, report_id, 'assistant', ai_response_text)
    
    return jsonify(response_data)

@app.route('/api/chat/history', methods=['GET'])
def get_history():
    patient_id = request.args.get('patient_id', 'P12345')
    report_id = request.args.get('report_id')
    if not report_id:
        return jsonify({"error": "report_id is required"}), 400
        
    history = get_chat_history(patient_id, report_id)
    return jsonify({"history": history})

@app.route('/api/upload_report', methods=['POST'])
def upload_report():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    content_type = file.content_type
    if content_type not in ["application/pdf", "image/jpeg", "image/png"]:
        return jsonify({"error": "Unsupported file type. Use PDF, JPG, or PNG."}), 400
        
    try:
        file_bytes = file.read()
        parsed_report = process_document(file_bytes, content_type)
        
        # Save report to DB
        save_medical_report(parsed_report)
        
        # Automatically generate a summary and save it as the first message
        report_id = parsed_report.get('report_id')
        patient_id = parsed_report.get('patient_id', 'P12345')
        
        summary_prompt = "Please provide a brief 2-3 sentence summary of this report. Do NOT ask any follow-up questions at the end."
        
        # We simulate the user asking for a summary (we don't save this user prompt to DB)
        response_data = generate_chat_response(
            user_message=summary_prompt, 
            patient_id=patient_id,
            patient_report=parsed_report,
            chat_history=[]
        )
        
        ai_response_text = response_data.get('response', '')
        if ai_response_text:
            # Message 1: The Summary
            add_chat_message(patient_id, report_id, 'assistant', ai_response_text)
            
            # Message 2: The prompt
            add_chat_message(patient_id, report_id, 'assistant', "What specific details or lab values would you like to know more about?")
            
        return jsonify({"success": True, "report": parsed_report})
        
    except Exception as e:
        print(f"Error processing upload: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/reports', methods=['GET'])
def reports():
    patient_id = request.args.get('patient_id', 'P12345')
    all_reports = get_all_medical_reports(patient_id)
    return jsonify({"reports": all_reports})

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    # Ensure user is aware they need an API key
    if not os.environ.get("GROQ_API_KEY"):
        print("\n" + "="*50)
        print("WARNING: GROQ_API_KEY environment variable is not set.")
        print("The chatbot will return an error message instead of real AI responses.")
        print("Please export GROQ_API_KEY='your_key' or put it in a .env file.")
        print("="*50 + "\n")
        
    app.run(debug=True, port=5000)
