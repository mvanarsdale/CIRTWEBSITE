from django.apps import AppConfig
import psycopg2
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

# Load environment variables
os.environ['PGHOST'] = 'nearly-famous-sunfish.a1.pgedge.io'
os.environ['PGUSER'] = 'app'
os.environ['PGDATABASE'] = 'cirtdb'
os.environ['PGSSLMODE'] = 'require'
os.environ['PGPASSWORD'] = 'E7V5i712eEE19DFD6JhSM7k7'
load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Connect to the pgEdge database
def get_db_connection():
    return psycopg2.connect(
        host=os.environ["PGHOST"],
        dbname=os.environ["PGDATABASE"],
        user=os.environ["PGUSER"],
        password=os.environ["PGPASSWORD"],
        sslmode="require"
    )

# Load and run schema from external .sql file
def initialize_db():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            with open("Project.session.sql", "r") as sql_file:
                cursor.execute(sql_file.read())
        conn.commit()

# Initialize tables
initialize_db()

# Add a comment
@app.route('/comment', methods=['POST'])
def add_comment():
    data = request.json
    pdf_id = data['pdf_id']
    comment = data['comment']

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO pdf_comments (pdf_id, comment) VALUES (%s, %s)",
                (pdf_id, comment)
            )
            conn.commit()

    return jsonify({"message": "Comment added"})

# Get comments
@app.route('/comments/<int:pdf_id>', methods=['GET'])
def get_comments(pdf_id):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT comment, created_at FROM pdf_comments WHERE pdf_id = %s ORDER BY created_at DESC",
                (pdf_id,)
            )
            comments = cursor.fetchall()

    return jsonify([
        {"comment": row[0], "created_at": row[1].isoformat()} for row in comments
    ])

# Upload a PDF
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded!"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Invalid file name!"}), 400

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

# Start Flask app
if __name__ == "__main__":
    app.run(debug=True, port=5000)

