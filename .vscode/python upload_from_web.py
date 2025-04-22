import psycopg2 as psycopg
import os
from flask import Flask, request

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Step 1: Connect to the pgEdge database
conn = psycopg.connect(
    host="recently-welcomed-mongrel.a1.pgedge.io",
    dbname="defaultdb",
    user="app",
    password="ty6NNb39tI642nC79Q1jep3V",
    sslmode="require"
)
cursor = conn.cursor()

# Step 2: Create table for storing PDFs
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
        return "No file uploaded!", 400
    
    file = request.files["file"]

    if file.filename == "":
        return "Invalid file name!", 400
    
    if file:
        filename = file.filename
        file_data = file.read()

        cursor.execute("INSERT INTO pdf_storage (filename, file_data) VALUES (%s, %s)", (filename, file_data))
        conn.commit()
        
        return f"Upload successful for {filename}!", 200

# Step 4: Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=5000)