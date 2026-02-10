import threading
import time
import stomp
import os
from flask import Flask, jsonify
import pandas as pd
import psycopg2
from flask_cors import CORS
from dotenv import load_dotenv

# Initialize Flask
app = Flask(__name__)
CORS(app)
load_dotenv()

# --- 1. CONFIGURATION ---

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),       
    "database": os.getenv("DB_NAME", "medipay"), 
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "port": os.getenv("DB_PORT", "5432")
}

ACTIVEMQ_HOST = os.getenv("ACTIVEMQ_HOST", "activemq")
ACTIVEMQ_PORT = int(os.getenv("ACTIVEMQ_PORT", 61613)) # STOMP port

class ClaimsListener(stomp.ConnectionListener):
    """Listener class to handle messages received from ActiveMQ."""
    def on_message(self, frame):
        print(f"\n[JMS RECEIVER] Message from Java: {frame.body}")
        # Will add trigger a cache clear or log this to a file

def start_jms_listener():
    """Background function to connect to ActiveMQ and listen for messages."""
    conn = stomp.Connection(host_and_ports=[(ACTIVEMQ_HOST, ACTIVEMQ_PORT)])
    conn.set_listener('', ClaimsListener())
    
    connected = False
    while not connected:
        try:
            conn.connect(wait=True)
            conn.subscribe(destination='claims-queue', id=1, ack='auto')
            print(f"Python Analytics: Connected to ActiveMQ at {ACTIVEMQ_HOST}:{ACTIVEMQ_PORT}")
            connected = True
        except Exception as e:
            print(f"Waiting for ActiveMQ... ({e})")
            time.sleep(5) 

# Start the listener in a background thread so it doesn't block Flask
jms_thread = threading.Thread(target=start_jms_listener, daemon=True)
jms_thread.start()


def get_data_from_db():
    conn = psycopg2.connect(**DB_CONFIG)
    query = "SELECT * FROM medical_claims"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def calculate_summary(df):
    """Main analytics logic using Pandas."""
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
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # host='0.0.0.0' is required for Docker to allow external access
    app.run(host='0.0.0.0', port=5001, debug=True)