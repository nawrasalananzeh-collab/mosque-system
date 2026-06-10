from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "mosque_secret"


# ================= DATABASE =================
def db():
    conn = sqlite3.connect("mosque.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = db()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS umrah_memories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        umrah_year TEXT,
        umrah_date TEXT,
        description TEXT,
        file_name TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()
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

@app.route("/test_db")
def test_db():
    conn = db()

    tables = conn.execute("""
        SELECT name FROM sqlite_master WHERE type='table'
    """).fetchall()

    conn.close()

    return str([t["name"] for t in tables])
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

    # 🔥 الأرقام (تصحيح نهائي)
    juz_count = request.form.get("juz_count")
    umrah_count = request.form.get("umrah_count")
    umrah_dates = request.form.get("umrah_dates") or ""

    # تحويل آمن للأرقام
    juz_count = int(juz_count) if juz_count and juz_count.strip() != "" else 0
    umrah_count = int(umrah_count) if umrah_count and umrah_count.strip() != "" else 0

    conn = db()

    conn.execute("""
        INSERT INTO students (
            name,
            age,
            phone,
            national_id,
            sheikh_group,
            address,
            parent_phone,
            image,
            juz_count,
            umrah_count,
            umrah_dates
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        age,
        phone,
        national_id,
        sheikh_group,
        address,
        parent_phone,
        image,
        juz_count,
        umrah_count,
        umrah_dates
    ))

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

        # 🔥 الجديد
        juz_count = request.form.get("juz_count") or 0
        umrah_count = request.form.get("umrah_count") or 0
        umrah_dates = request.form.get("umrah_dates") or ""

        conn.execute("""
            UPDATE students
            SET name=?,
                age=?,
                phone=?,
                national_id=?,
                sheikh_group=?,
                address=?,
                parent_phone=?,
                image=?,
                juz_count=?,
                umrah_count=?,
                umrah_dates=?
            WHERE id=?
        """, (
            name,
            age,
            phone,
            national_id,
            sheikh_group,
            address,
            parent_phone,
            image,
            juz_count,
            umrah_count,
            umrah_dates,
            id
        ))

        conn.commit()
        conn.close()
        return redirect("/students")

    # GET request (عرض البيانات)
    student = conn.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    ).fetchone()

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

USERS_PIN = "123456789987654321"

@app.route("/users_pin", methods=["GET", "POST"])
def users_pin():
    if not auth():
        return redirect("/")

    error = None

    if request.method == "POST":
        pin = request.form.get("pin")

        if pin == USERS_PIN:
            session["users_pin_ok"] = True
            return redirect("/users")
        else:
            error = "PIN خطأ"

    return render_template("users_pin.html", error=error)
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

# ================= ✏ EDIT USER =================
@app.route("/edit_user/<int:id>", methods=["GET", "POST"])
def edit_user(id):
    if not auth():
        return redirect("/")

    conn = db()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn.execute("""
            UPDATE users
            SET username=?,
                password=?
            WHERE id=?
        """, (
            username,
            password,
            id
        ))

        conn.commit()
        conn.close()

        return redirect("/users")

    user = conn.execute(
        "SELECT * FROM users WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template("edit_user.html", user=user)

# ================= TEACHERS =================
# ================= TEACHERS LIST =================
@app.route("/teachers")
def teachers():
    if not auth():
        return redirect("/")

    conn = db()
    data = conn.execute("SELECT * FROM teachers").fetchall()
    conn.close()

    return render_template("teachers.html", teachers=data)
# ================= 👨‍🏫 TEACHER PROFILE =================
@app.route("/teacher/<int:id>")
def teacher_profile(id):
    if not auth():
        return redirect("/")

    conn = db()
    teacher = conn.execute(
        "SELECT * FROM teachers WHERE id=?",
        (id,)
    ).fetchone()
    conn.close()

    return render_template("teacher_profile.html", teacher=teacher)

# ================= ADD TEACHER =================
@app.route("/add_teacher_page")
def add_teacher_page():
    if not auth():
        return redirect("/")

    return render_template("add_teacher.html")


@app.route("/add_teacher", methods=["POST"])
def add_teacher():
    if not auth():
        return redirect("/")

    name = request.form.get("name")
    phone = request.form.get("phone")
    age = request.form.get("age")
    address = request.form.get("address")
    specialization = request.form.get("specialization")
    join_date = request.form.get("join_date")
    students_count = request.form.get("students_count")
    status = request.form.get("status")

    conn = db()

    conn.execute("""
        INSERT INTO teachers
        (name, phone, age, address, specialization, join_date, students_count, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        phone,
        age,
        address,
        specialization,
        join_date,
        students_count,
        status
    ))

    conn.commit()
    conn.close()

    return redirect("/teachers")


# ================= EDIT TEACHER =================
# ================= ✏ EDIT TEACHER =================
@app.route("/edit_teacher/<int:id>", methods=["GET", "POST"])
def edit_teacher(id):
    if not auth():
        return redirect("/")

    conn = db()

    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        age = request.form.get("age")
        address = request.form.get("address")
        specialization = request.form.get("specialization")
        join_date = request.form.get("join_date")
        students_count = request.form.get("students_count")
        status = request.form.get("status")

        conn.execute("""
            UPDATE teachers
            SET name=?,
                phone=?,
                age=?,
                address=?,
                specialization=?,
                join_date=?,
                students_count=?,
                status=?
            WHERE id=?
        """, (
            name,
            phone,
            age,
            address,
            specialization,
            join_date,
            students_count,
            status,
            id
        ))

        conn.commit()
        conn.close()

        return redirect("/teachers")

    teacher = conn.execute(
        "SELECT * FROM teachers WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template("edit_teacher.html", teacher=teacher)

# ================= DELETE TEACHER =================
@app.route("/delete_teacher/<int:id>")
def delete_teacher(id):
    if not auth():
        return redirect("/")

    conn = db()

    conn.execute(
        "DELETE FROM teachers WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/teachers")
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
    
@app.route("/hafaz")
def hafaz():
    if not auth():
        return redirect("/")

    conn = db()
    data = conn.execute("SELECT * FROM hafaz").fetchall()
    conn.close()

    return render_template("hafaz.html", hafaz=data)


# ================= ADD HAFZ =================
@app.route("/add_hafaz", methods=["GET", "POST"])
def add_hafaz():
    if not auth():
        return redirect("/")

    if request.method == "POST":
        full_name = request.form.get("full_name")
        juz_count = request.form.get("juz_count")
        sheikh = request.form.get("sheikh")
        khatma_date = request.form.get("khatma_date")
        khatma_place = request.form.get("khatma_place")

        conn = db()
        conn.execute("""
            INSERT INTO hafaz (full_name, juz_count, sheikh, khatma_date, khatma_place)
            VALUES (?, ?, ?, ?, ?)
        """, (full_name, juz_count, sheikh, khatma_date, khatma_place))

        conn.commit()
        conn.close()

        return redirect("/hafaz")

    return render_template("add_hafaz.html")

@app.route("/hafaz/<int:id>")
def hafaz_view(id):
    if not auth():
        return redirect("/")

    conn = db()
    data = conn.execute("SELECT * FROM hafaz WHERE id=?", (id,)).fetchone()
    conn.close()

    return render_template("hafaz_view.html", hafaz=data)
@app.route("/edit_hafaz/<int:id>", methods=["GET", "POST"])
def edit_hafaz(id):
    if not auth():
        return redirect("/")

    conn = db()

    if request.method == "POST":
        full_name = request.form.get("full_name")
        juz_count = request.form.get("juz_count")
        sheikh = request.form.get("sheikh")
        khatma_date = request.form.get("khatma_date")
        khatma_place = request.form.get("khatma_place")

        conn.execute("""
            UPDATE hafaz
            SET full_name=?, juz_count=?, sheikh=?, khatma_date=?, khatma_place=?
            WHERE id=?
        """, (full_name, juz_count, sheikh, khatma_date, khatma_place, id))

        conn.commit()
        conn.close()
        return redirect("/hafaz")

    data = conn.execute("SELECT * FROM hafaz WHERE id=?", (id,)).fetchone()
    conn.close()

    return render_template("edit_hafaz.html", hafaz=data)
@app.route("/delete_hafaz/<int:id>")
def delete_hafaz(id):
    if not auth():
        return redirect("/")

    conn = db()
    conn.execute("DELETE FROM hafaz WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/hafaz")
import os
from werkzeug.utils import secure_filename

import os

UPLOAD_FOLDER = os.path.join("static", "uploads")

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ================= TESTS =================
# ================= TESTS =================
from flask import send_from_directory

UPLOAD_FOLDER = os.path.join("static", "uploads")

@app.route("/tests")
def tests():
    if not auth():
        return redirect("/")

    try:
        conn = db()
        data = conn.execute("SELECT * FROM tests ORDER BY id DESC").fetchall()
        conn.close()
        return render_template("tests.html", tests=data)

    except Exception as e:
        return f"ERROR: {e}"


@app.route("/add_test_page")
def add_test_page():
    if not auth():
        return redirect("/")
    return render_template("add_test.html")


@app.route("/add_test", methods=["POST"])
def add_test():
    if not auth():
        return redirect("/")

    student_name = request.form.get("student_name")
    test_type = request.form.get("test_type")
    score = request.form.get("score")
    date = request.form.get("date")
    notes = request.form.get("notes")

    pdf_file = ""

    file = request.files.get("pdf_file")
    if file and file.filename != "":
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        pdf_file = filename

    conn = db()
    conn.execute("""
        INSERT INTO tests (student_name, test_type, score, date, notes, pdf_file)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (student_name, test_type, score, date, notes, pdf_file))

    conn.commit()
    conn.close()

    return redirect("/tests")


@app.route("/view_test_file/<filename>")
def view_test_file(filename):
    if not auth():
        return redirect("/")

    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route("/test/<int:id>")
def test_profile(id):
    if not auth():
        return redirect("/")

    conn = db()
    test = conn.execute("SELECT * FROM tests WHERE id=?", (id,)).fetchone()
    conn.close()

    return render_template("test_profile.html", test=test)


@app.route("/edit_test/<int:id>", methods=["GET", "POST"])
def edit_test(id):
    if not auth():
        return redirect("/")

    conn = db()

    test = conn.execute(
        "SELECT * FROM tests WHERE id=?",
        (id,)
    ).fetchone()

    if request.method == "POST":

        student_name = request.form.get("student_name")
        test_type = request.form.get("test_type")
        score = request.form.get("score")
        date = request.form.get("date")
        notes = request.form.get("notes")

        file = request.files.get("pdf_file")

        pdf_file = test["pdf_file"]  # الافتراضي = القديم

        # لو رفع ملف جديد
        if file and file.filename != "":
            filename = secure_filename(file.filename)

            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            pdf_file = filename  # تحديث الاسم الجديد

        # 🔥 تحديث كامل في قاعدة البيانات
        conn.execute("""
            UPDATE tests
            SET student_name=?,
                test_type=?,
                score=?,
                date=?,
                notes=?,
                pdf_file=?
            WHERE id=?
        """, (
            student_name,
            test_type,
            score,
            date,
            notes,
            pdf_file,
            id
        ))

        conn.commit()
        conn.close()

        return redirect("/tests")

    conn.close()
    return render_template("edit_test.html", test=test)

@app.route("/delete_test/<int:id>")
def delete_test(id):
    if not auth():
        return redirect("/")

    conn = db()
    conn.execute("DELETE FROM tests WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/tests")
# ================= UMRAH =================
@app.route("/umrah")
def umrah():
    if not auth():
        return redirect("/")

    conn = db()

    years = conn.execute("""
        SELECT DISTINCT umrah_year 
        FROM umrah_memories 
        ORDER BY umrah_year DESC
    """).fetchall()

    data = conn.execute("""
        SELECT * FROM umrah_memories 
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template("umrah.html", data=data, years=years)


# ================= ADD UMRAH (NEW SIMPLE FORM) =================
@app.route("/add_umrah", methods=["GET", "POST"])
def add_umrah():
    if not auth():
        return redirect("/")

    if request.method == "POST":
        name = request.form.get("name")
        year = request.form.get("year")
        date = request.form.get("date")
        description = request.form.get("description")

        conn = db()
        conn.execute("""
            INSERT INTO umrah_memories 
            (student_id, umrah_year, umrah_date, description, file_name)
            VALUES (?, ?, ?, ?, ?)
        """, (None, year, date, description, ""))

        conn.commit()
        conn.close()

        return redirect("/umrah")

    return render_template("add_umrah.html")
@app.route("/umrah_file/<filename>")
def umrah_file(filename):
    if not auth():
        return redirect("/")

    return send_from_directory(UPLOAD_FOLDER, filename)


# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ================= KHATMAT LIST =================
@app.route("/khatmat")
def khatmat():
    if not auth():
        return redirect("/")

    conn = db()
    data = conn.execute("SELECT * FROM khatmat ORDER BY id DESC").fetchall()
    conn.close()

    return render_template("khatmat.html", khatmat=data)


# ================= ADD KHATMA =================
@app.route("/add_khatma", methods=["GET", "POST"])
def add_khatma():
    if not auth():
        return redirect("/")

    if request.method == "POST":

        student_name = request.form.get("student_name")
        khatma_date = request.form.get("khatma_date")
        khatma_place = request.form.get("khatma_place")

        sheikh_name = request.form.get("sheikh_name")
        mosque_name = request.form.get("mosque_name")

        city = request.form.get("city")
        country = request.form.get("country")

        age = request.form.get("age")
        grade = request.form.get("grade")
        khatma_type = request.form.get("khatma_type")
        attendance_count = request.form.get("attendance_count")

        conn = db()
        conn.execute("""
            INSERT INTO khatmat (
                student_name,
                khatma_date,
                khatma_place,
                sheikh_name,
                mosque_name,
                city,
                country,
                age,
                grade,
                khatma_type,
                attendance_count,
                certificate_image,
                student_image,
                video_file,
                pdf_file
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '', '', '', '')
        """, (
            student_name,
            khatma_date,
            khatma_place,
            sheikh_name,
            mosque_name,
            city,
            country,
            age,
            grade,
            khatma_type,
            attendance_count
        ))

        conn.commit()
        conn.close()

        return redirect("/khatmat")

    return render_template("add_khatma.html")


# ================= KHATMA PROFILE =================
@app.route("/khatma/<int:id>")
def khatma_profile(id):
    if not auth():
        return redirect("/")

    conn = db()
    data = conn.execute("SELECT * FROM khatmat WHERE id=?", (id,)).fetchone()
    conn.close()

    return render_template("khatma_profile.html", khatma=data)


# ================= DELETE KHATMA =================
@app.route("/delete_khatma/<int:id>")
def delete_khatma(id):
    if not auth():
        return redirect("/")

    conn = db()
    conn.execute("DELETE FROM khatmat WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/khatmat")


# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)