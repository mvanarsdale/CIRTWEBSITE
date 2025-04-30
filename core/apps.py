from django.apps import AppConfig

import os
import psycopg as psycopg2
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

def ready(self):
    import core.signals


# Set environment variables (for local development; use .env override if needed)
os.environ['PGHOST'] = 'nearly-famous-sunfish.a1.pgedge.io'
os.environ['PGUSER'] = 'app'
os.environ['PGDATABASE'] = 'cirtdb'
os.environ['PGSSLMODE'] = 'require'
os.environ['PGPASSWORD'] = 'E7V5i712eEE19DFD6JhSM7k7'

# Load .env if present
load_dotenv()

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests if frontend is served from different port
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Database connection helper
def get_db_connection():
    return psycopg2.connect(
        host=os.environ['PGHOST'],
        dbname=os.environ['PGDATABASE'],
        user=os.environ['PGUSER'],
        password=os.environ['PGPASSWORD'],
        sslmode=os.environ['PGSSLMODE']
    )

# Create necessary tables if they don't exist
with get_db_connection() as conn:
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pdf_storage (
                id SERIAL PRIMARY KEY,
                filename TEXT,
                file_data BYTEA
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pdf_comments (
                id SERIAL PRIMARY KEY,
                pdf_id INTEGER REFERENCES pdf_storage(id) ON DELETE CASCADE,
                comment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

# Route: Upload PDF + Description + Comments (merged into one file)
@app.route("/submit-journal", methods=["POST"])
def submit_journal():
    try:
        if "file" not in request.files:
            print("❌ No file found in request.")
            return jsonify({"error": "No file uploaded!"}), 400

        file = request.files["file"]
        if file.filename == "":
            print("❌ Empty filename received.")
            return jsonify({"error": "Invalid file name!"}), 400

        description = request.form.get("description", "")
        comments = request.form.get("comments", "")

        print("✅ Received submission:")
        print("   - filename:", file.filename)
        print("   - description:", description)
        print("   - comments:", comments)

        filename = os.path.splitext(file.filename)[0] + "_submission.txt"
        merged_content = f"""--- Journal Submission File ---
Original Filename: {file.filename}

--- Description ---
{description}

--- Comments ---
{comments}
"""

        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO pdf_storage (filename, file_data) VALUES (%s, %s)",
                    (filename, merged_content.encode("utf-8"))
                )
                conn.commit()

        print("✅ Upload complete.")
        return jsonify({"message": f"Upload successful for {filename}!"}), 200

    except Exception as e:
        print("❌ Upload failed:", str(e))
        return jsonify({"error": str(e)}), 500

# Optional raw file upload
@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded!"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "Invalid file name!"}), 400

        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO pdf_storage (filename, file_data) VALUES (%s, %s)",
                    (file.filename, file.read())
                )
                conn.commit()

        return jsonify({"message": f"Upload successful for {file.filename}!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add a comment linked to a PDF (by ID)
@app.route('/comment', methods=['POST'])
def add_comment():
    data = request.json
    pdf_id = data.get('pdf_id')
    comment = data.get('comment')

    if not pdf_id or not comment:
        return jsonify({"error": "pdf_id and comment required"}), 400

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO pdf_comments (pdf_id, comment) VALUES (%s, %s)",
                (pdf_id, comment)
            )
            conn.commit()

    return jsonify({"message": "Comment added"}), 200

# Retrieve comments for a specific PDF
@app.route('/comments/<int:pdf_id>', methods=['GET'])
def get_comments(pdf_id):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT comment, created_at FROM pdf_comments WHERE pdf_id = %s ORDER BY created_at DESC",
                (pdf_id,)
            )
            rows = cursor.fetchall()

    return jsonify([
        {"comment": row[0], "created_at": row[1].isoformat()} for row in rows
    ])

# Start the server
if __name__ == '__main__':
    app.run(debug=True, port=5000)




