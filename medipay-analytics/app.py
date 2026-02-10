import threading
import time
import stomp
import os
import logging 
from flask import Flask, jsonify, send_file  # Added send_file
import pandas as pd
import psycopg2
from flask_cors import CORS
from dotenv import load_dotenv

LOG_FILE = "analytics_events.log"

# Configure logging to write to both the console AND a file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHeader(LOG_FILE),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)
CORS(app)
load_dotenv()


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),       
    "database": os.getenv("DB_NAME", "medipay"), 
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "port": os.getenv("DB_PORT", "5432")
}

ACTIVEMQ_HOST = os.getenv("ACTIVEMQ_HOST", "activemq")
ACTIVEMQ_PORT = int(os.getenv("ACTIVEMQ_PORT", 61613)) 

class ClaimsListener(stomp.ConnectionListener):
    """Listener class to handle messages received from ActiveMQ."""
    def on_message(self, frame):
        logging.info(f"[JMS RECEIVER] Processing Claim from Java: {frame.body}")
        
    def on_error(self, frame):
        logging.error(f"[JMS ERROR] {frame.body}")

def start_jms_listener():
    """Background function to connect to ActiveMQ and listen for messages."""
    conn = stomp.Connection(host_and_ports=[(ACTIVEMQ_HOST, ACTIVEMQ_PORT)])
    conn.set_listener('', ClaimsListener())
    
    connected = False
    while not connected:
        try:
            conn.connect(wait=True)
            conn.subscribe(destination='claims-queue', id=1, ack='auto')
            logging.info(f"Python Analytics: Connected to ActiveMQ at {ACTIVEMQ_HOST}")
            connected = True
        except Exception as e:
            logging.warning(f"Waiting for ActiveMQ... ({e})")
            time.sleep(5) 

# Start listener
jms_thread = threading.Thread(target=start_jms_listener, daemon=True)
jms_thread.start()


def get_data_from_db():
    conn = psycopg2.connect(**DB_CONFIG)
    query = "SELECT * FROM medical_claims"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def calculate_summary(df):
    if df.empty:
        return {"message": "No data available"}
    return {
        "total_claims": int(df.shape[0]),
        "total_value": float(df['claim_amount'].sum()),
        "avg_claim": float(df['claim_amount'].mean()),
        "status_counts": df['status'].value_counts().to_dict(),
        "top_providers": df['provider_name'].value_counts().head(3).to_dict()
    }


@app.route('/summary', methods=['GET'])
def get_summary():
    try:
        df = get_data_from_db()
        summary = calculate_summary(df) 
        return jsonify(summary)
    except Exception as e:
        logging.error(f"Error calculating summary: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/download-logs', methods=['GET'])
def download_logs():
    try:
        if os.path.exists(LOG_FILE):
            return send_file(LOG_FILE, as_attachment=True)
        else:
            return jsonify({"error": "Log file not found yet. Generate some activity first!"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    logging.info("Starting MediPay Python Analytics Service...")
    app.run(host='0.0.0.0', port=5001, debug=False) 