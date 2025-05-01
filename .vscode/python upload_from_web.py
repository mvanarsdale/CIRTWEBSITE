from Flask import Flask, request, jsonify, send_file
import psycopg2 as psycopg
import os
import io


app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Database connection parameters
DB_CONFIG = {
    "host": "recently-welcomed-mongrel.a1.pgedge.io",
    "dbname": "defaultdb",
    "user": "app",
    "password": "ty6NNb39tI642nC79Q1jep3V",
    "sslmode": "require"
}

# Step 1: Initialize the database table (run once at startup)
def initialize_db():
    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pdf_storage (
                    id SERIAL PRIMARY KEY,
                    filename TEXT,
                    file_data BYTEA
                )
            """)
            conn.commit()

initialize_db()

# Step 2: Define upload route
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
        with psycopg.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO pdf_storage (filename, file_data) VALUES (%s, %s)",
                    (filename, file_data)
                )
                conn.commit()
        return jsonify({"message": f"Upload successful for {filename}!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/files", methods=["GET"])
def list_files():
    try:
        with psycopg.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, filename FROM pdf_storage ORDER BY id DESC")
                files = cursor.fetchall()
        return jsonify([{"id": row[0], "filename": row[1]} for row in files]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/download/<int:file_id>", methods=["GET"])
def download_file(file_id):
    try:
        with psycopg.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT filename, file_data FROM pdf_storage WHERE id = %s", (file_id,))
                result = cursor.fetchone()
        if result:
            filename, file_data = result
            return send_file(
                io.BytesIO(file_data),
                as_attachment=True,
                download_name=filename,
                mimetype='application/pdf'
            )
        else:
            return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Step 3: Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=5000)
