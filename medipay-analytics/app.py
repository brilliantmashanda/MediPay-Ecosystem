from flask import Flask, jsonify
import pandas as pd
import psycopg2
from flask_cors import CORS
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app) # Allows the Angular dashboard to talk to this service

load_dotenv()
# Database connection settings (Match your Java settings)
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),       
    "database": os.getenv("DB_NAME", "postgres"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
    "port": os.getenv("DB_PORT", "5432")
}

def get_data_from_db():
    conn = psycopg2.connect(**DB_CONFIG)
    query = "SELECT * FROM medical_claims"
    # Load SQL results directly into a Pandas DataFrame
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
def calculate_summary(df):
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
        
        # Performance analytics using Pandas
        summary = calculate_summary(df) 
        
        return jsonify(summary)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run on port 5001 to avoid conflict with Java (8080)
    # app.run(debug=True, port=5001)
    app.run(host='0.0.0.0', port=5001, debug=True)