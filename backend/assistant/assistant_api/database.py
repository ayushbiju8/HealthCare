import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'chat_history.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT NOT NULL,
            report_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS medical_reports (
            report_id TEXT PRIMARY KEY,
            patient_id TEXT NOT NULL,
            date_of_report TEXT NOT NULL,
            report_json TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    conn.close()

def add_chat_message(patient_id, report_id, role, content):
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO chat_messages (patient_id, report_id, role, content) VALUES (?, ?, ?, ?)',
        (patient_id, report_id, role, content)
    )
    conn.commit()
    conn.close()

def get_chat_history(patient_id, report_id):
    conn = get_db_connection()
    messages = conn.execute(
        'SELECT role, content FROM chat_messages WHERE patient_id = ? AND report_id = ? ORDER BY id ASC',
        (patient_id, report_id)
    ).fetchall()
    conn.close()
    
    return [{"role": msg["role"], "content": msg["content"]} for msg in messages]

import json

def save_medical_report(report_dict):
    conn = get_db_connection()
    conn.execute(
        'INSERT OR REPLACE INTO medical_reports (report_id, patient_id, date_of_report, report_json) VALUES (?, ?, ?, ?)',
        (report_dict.get('report_id'), report_dict.get('patient_id'), report_dict.get('date_of_report'), json.dumps(report_dict))
    )
    conn.commit()
    conn.close()

def get_all_medical_reports(patient_id=None):
    conn = get_db_connection()
    rows = conn.execute(
        'SELECT report_json FROM medical_reports ORDER BY date_of_report DESC'
    ).fetchall()
    conn.close()
    
    return [json.loads(row['report_json']) for row in rows]

# Initialize the database when the module is imported
init_db()
