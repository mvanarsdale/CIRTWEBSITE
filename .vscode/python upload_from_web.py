import psycopg
import csv
import requests
from io import StringIO

# Step 1: Download file from website
url = "https://example.com/data.csv"  # Replace with your actual URL
response = requests.get(url)
response.raise_for_status()  # Raise error if download failed

# Step 2: Read CSV from downloaded content
csv_file = StringIO(response.text)
reader = csv.reader(csv_file)
header = next(reader)  # Skip header row

# Step 3: Connect to the pgEdge database
conn = psycopg.connect(
    host="recently-welcomed-mongrel.a1.pgedge.io",
    dbname="defaultdb",
    user="app",
    password="ty6NNb39tI642nC79Q1jep3V",
    sslmode="require"
)
cursor = conn.cursor()

# Step 4: Create table (modify as per your data structure)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS website_data (
        name TEXT,
        age INT
    )
""")

# Step 5: Insert rows
for row in reader:
    cursor.execute("INSERT INTO website_data (name, age) VALUES (%s, %s)", row)

# Step 6: Commit and close
conn.commit()
cursor.close()
conn.close()
print("Upload complete!")
