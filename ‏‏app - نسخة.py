from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "mosque_secret"


# ================= DATABASE =================
def db():
    conn = sqlite3.connect("mosque.db")
    conn.row_factory = sqlite3.Row
    return conn


# ================= AUTH =================
def auth():
    return "user" in session


# ================= LOGIN =================
@app.route("/", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = db()
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()
        conn.close()

        if user:
            session["user"] = user["username"]
            return redirect("/welcome")
        else:
            error = "خطأ في البيانات"

    return render_template("login.html", error=error)


# ================= WELCOME =================
@app.route("/welcome")
def welcome():
    if not auth():
        return redirect("/")
    return render_template("welcome.html", username=session["user"])


# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    if not auth():
        return redirect("/")
    return render_template("dashboard.html", username=session["user"])


# ================= STUDENTS =================
@app.route("/students")
def students():
    if not auth():
        return redirect("/")

    conn = db()
    data = conn.execute("SELECT * FROM students").fetchall()
    conn.close()

    return render_template("students.html", students=data)


@app.route("/add_student_page")
def add_student_page():
    if not auth():
        return redirect("/")
    return render_template("add_student.html")


@app.route("/add_student", methods=["POST"])
def add_student():
    if not auth():
        return redirect("/")

    name = request.form.get("name")
    age = request.form.get("age")
    phone = request.form.get("phone")
    national_id = request.form.get("national_id")
    sheikh_group = request.form.get("sheikh_group")
    address = request.form.get("address")
    parent_phone = request.form.get("parent_phone")
    image = request.form.get("image")

    conn = db()
    conn.execute("""
        INSERT INTO students
        (name, age, phone, national_id, sheikh_group, address, parent_phone, image)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, age, phone, national_id, sheikh_group, address, parent_phone, image))

    conn.commit()
    conn.close()

    return redirect("/students")


# ================= ✏ EDIT STUDENT =================
@app.route("/edit_student/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    if not auth():
        return redirect("/")

    conn = db()

    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        phone = request.form.get("phone")
        national_id = request.form.get("national_id")
        sheikh_group = request.form.get("sheikh_group")
        address = request.form.get("address")
        parent_phone = request.form.get("parent_phone")
        image = request.form.get("image")

        conn.execute("""
            UPDATE students
            SET name=?, age=?, phone=?, national_id=?, sheikh_group=?, address=?, parent_phone=?, image=?
            WHERE id=?
        """, (name, age, phone, national_id, sheikh_group, address, parent_phone, image, id))

        conn.commit()
        conn.close()
        return redirect("/students")

    student = conn.execute("SELECT * FROM students WHERE id=?", (id,)).fetchone()
    conn.close()

    return render_template("edit_student.html", student=student)


# ================= 🗑 DELETE STUDENT =================
@app.route("/delete_student/<int:id>")
def delete_student(id):
    if not auth():
        return redirect("/")

    conn = db()
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/students")


# ================= 👤 STUDENT PROFILE (NEW) =================
@app.route("/student/<int:id>")
def student_profile(id):
    if not auth():
        return redirect("/")

    conn = db()
    student = conn.execute("SELECT * FROM students WHERE id=?", (id,)).fetchone()
    conn.close()

    return render_template("student_profile.html", student=student)


# ================= USERS =================
@app.route("/users")
def users():
    if not auth():
        return redirect("/")

    conn = db()
    data = conn.execute("SELECT * FROM users").fetchall()
    conn.close()

    return render_template("users.html", users=data)


@app.route("/add_user_page")
def add_user_page():
    if not auth():
        return redirect("/")
    return render_template("add_user.html")


@app.route("/add_user", methods=["POST"])
def add_user():
    if not auth():
        return redirect("/")

    username = request.form.get("username")
    password = request.form.get("password")

    conn = db()
    conn.execute(
        "INSERT INTO users (username,password) VALUES (?,?)",
        (username, password)
    )
    conn.commit()
    conn.close()

    return redirect("/users")


@app.route("/delete_user/<int:id>")
def delete_user(id):
    if not auth():
        return redirect("/")

    conn = db()
    conn.execute("DELETE FROM users WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/users")


# ================= TEACHERS =================
@app.route("/teachers")
def teachers():
    if not auth():
        return redirect("/")

    conn = db()
    data = conn.execute("SELECT * FROM teachers").fetchall()
    conn.close()

    return render_template("teachers.html", teachers=data)


# ================= SESSIONS =================
@app.route("/sessions")
def sessions():
    if not auth():
        return redirect("/")

    conn = db()
    students = conn.execute("SELECT * FROM students").fetchall()
    sessions_list = conn.execute("SELECT * FROM sessions ORDER BY id DESC").fetchall()
    conn.close()

    return render_template("sessions.html", students=students, sessions=sessions_list)


@app.route("/add_session_page")
def add_session_page():
    if not auth():
        return redirect("/")
    return render_template("add_session.html")


@app.route("/add_session", methods=["POST"])
def add_session():
    if not auth():
        return redirect("/")

    name = request.form.get("name")
    time = request.form.get("time")
    supervisor = request.form.get("supervisor")

    conn = db()
    conn.execute("""
        INSERT INTO sessions (name, session_time, supervisor)
        VALUES (?, ?, ?)
    """, (name, time, supervisor))

    conn.commit()
    conn.close()

    return redirect("/sessions")


@app.route("/delete_session/<int:id>")
def delete_session(id):
    if not auth():
        return redirect("/")

    conn = db()
    conn.execute("DELETE FROM sessions WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/sessions")


@app.route("/edit_session/<int:id>", methods=["GET", "POST"])
def edit_session(id):
    if not auth():
        return redirect("/")

    conn = db()

    if request.method == "POST":
        name = request.form.get("name")
        time = request.form.get("time")
        supervisor = request.form.get("supervisor")

        conn.execute("""
            UPDATE sessions
            SET name=?, session_time=?, supervisor=?
            WHERE id=?
        """, (name, time, supervisor, id))

        conn.commit()
        conn.close()
        return redirect("/sessions")

    data = conn.execute("SELECT * FROM sessions WHERE id=?", (id,)).fetchone()
    conn.close()

    return render_template("edit_session.html", session=data)


# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)