from flask import Flask, render_template, request, redirect
from supabase import create_client, Client
import pandas as pd

app = Flask(__name__)

# ---------------------------
# Supabase Configuration
# ---------------------------
SUPABASE_URL = "https://bidqmjsfyjizhttcjkol.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJpZHFtanNmeWppemh0dGNqa29sIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MjcxMzE4NSwiZXhwIjoyMDc4Mjg5MTg1fQ.x12d46OLujL3O3DJ2ccAJFMglxLaU-8ka8hymMZUBjY"
"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------------------
# Routes
# ---------------------------

@app.route("/")
def index():
    # Fetch all student records
    response = supabase.table("students").select("*").execute()
    data = response.data or []
    df = pd.DataFrame(data)
    students = df.to_dict(orient="records") if not df.empty else []
    return render_template("index.html", students=students)

@app.route("/add", methods=["POST"])
def add_student():
    roll_no = request.form.get("roll_no")
    name = request.form.get("name")
    math = int(request.form.get("math", 0))
    english = int(request.form.get("english", 0))
    science = int(request.form.get("science", 0))
    avg = round((math + english + science) / 3, 2)

    data = {
        "roll_no": roll_no,
        "name": name,
        "math": math,
        "english": english,
        "science": science,
        "average_score": avg
    }
    supabase.table("students").insert(data).execute()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
