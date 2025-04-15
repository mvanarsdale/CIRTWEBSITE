import psycopg as psycopg2
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
os.environ['PGHOST'] = 'nearly-famous-sunfish.a1.pgedge.io'
os.environ['PGUSER'] = 'app'
os.environ['PGDATABASE'] = 'cirtdb'
os.environ['PGSSLMODE'] = 'require'
os.environ['PGPASSWORD'] = 'E7V5i712eEE19DFD6JhSM7k7'

# Load environment variables
load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Step 1: Connect to the pgEdge database
def get_db_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        sslmode="require"
    )

# Step 2: Create table for storing PDFs
with get_db_connection() as conn:
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pdf_storage (
                id SERIAL PRIMARY KEY,
                filename TEXT,
                file_data BYTEA
            )
        """)
        conn.commit()

# Step 3: Define upload route
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded!"}), 400
    
    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Invalid file name!"}), 400
    
    if file:
        filename = file.filename
        file_data = file.read()

        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO pdf_storage (filename, file_data) VALUES (%s, %s)",
                        (filename, file_data)
                    )
                    conn.commit()
            return jsonify({"message": f"Upload successful for {filename}!"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

# Step 4: Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=5000)
    