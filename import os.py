import os
import psycopg2
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env if available
load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Step 1: Connect to the pgEdge database
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("recently-welcomed-mongrel.a1.pgedge.io"),
        dbname=os.getenv("defaultdb"),
        user=os.getenv("app"),
        password=os.getenv("ty6NNb39tI642nC79Q1jep3V"),
        sslmode=os.getenv("require", "require")
    )

# Step 2: Create table for storing PDFs (if it doesn't exist)
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
@app.route("/submit-journal", methods=["POST"])
def submit_journal():
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
