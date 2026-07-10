from flask import Flask, render_template, request, redirect, session
from datetime import datetime, timedelta
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "library_secret_key"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "library.db")


# ==========================
# DATABASE CONNECTION
# ==========================

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ==========================
# CREATE TABLES
# ==========================

def create_tables():

    conn = get_db()
    cur = conn.cursor()

    # Users Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    # Books Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS books(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        isbn TEXT,
        category TEXT,
        quantity INTEGER
    )
    """)

    # Issued Books Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS issued_books(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT,
        role TEXT,
        book_title TEXT,
        issue_date TEXT,
        due_date TEXT,
        return_date TEXT,
        fine INTEGER DEFAULT 0,
        status TEXT
    )
    """)

    # Fine Payments Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS fine_payments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        issue_id INTEGER,
        amount INTEGER,
        payment_method TEXT,
        payment_date TEXT,
        status TEXT
    )
    """)

    # Default Users
    users = [
        ("admin", "admin123", "librarian"),
        ("student", "student123", "student"),
        ("faculty", "faculty123", "faculty")
    ]

    for user in users:

        cur.execute("""
        INSERT OR IGNORE INTO users(username,password,role)
        VALUES(?,?,?)
        """, user)

    conn.commit()
    conn.close()


# ==========================
# LOGIN
# ==========================

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
        SELECT * FROM users
        WHERE username=? AND password=? AND role=?
        """, (username, password, role))

        user = cur.fetchone()

        conn.close()

        if user:

            session["username"] = user["username"]
            session["role"] = user["role"]

            if role == "librarian":
                return redirect("/librarian")

            elif role == "student":
                return redirect("/student")

            elif role == "faculty":
                return redirect("/faculty")

        else:
            return "Invalid Username or Password"

    return render_template("login.html")


# ==========================
# DASHBOARDS
# ==========================

@app.route("/librarian")
def librarian():
    return render_template("librarian_dashboard.html")


@app.route("/student")
def student():
    return render_template("student_dashboard.html")


@app.route("/faculty")
def faculty():
    return render_template("faculty_dashboard.html")

# ==========================
# BOOKS
# ==========================

@app.route("/books", methods=["GET", "POST"])
def books():

    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":

        title = request.form["title"]
        author = request.form["author"]
        isbn = request.form["isbn"]
        category = request.form["category"]
        quantity = request.form["quantity"]

        cur.execute("""
        INSERT INTO books
        (title,author,isbn,category,quantity)
        VALUES(?,?,?,?,?)
        """,
        (
            title,
            author,
            isbn,
            category,
            quantity
        ))

        conn.commit()

    cur.execute("""
    SELECT *
    FROM books
    ORDER BY id DESC
    """)

    books = cur.fetchall()

    conn.close()

    return render_template(
        "books.html",
        books=books
    )


# ==========================
# DELETE BOOK
# ==========================

@app.route("/delete_book/<int:id>")
def delete_book(id):

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    DELETE FROM books
    WHERE id=?
    """, (id,))

    conn.commit()
    conn.close()

    return redirect("/books")


# ==========================
# ISSUE BOOK
# ==========================

@app.route("/issue", methods=["GET", "POST"])
def issue():

    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":

        user_name = request.form["user_name"]
        role = request.form["role"]
        book_title = request.form["book_title"]

        issue_date = datetime.today().strftime("%Y-%m-%d")

        # Due after 7 days
        due_date = (
            datetime.today() + timedelta(days=7)
        ).strftime("%Y-%m-%d")

        cur.execute("""
        INSERT INTO issued_books
        (
            user_name,
            role,
            book_title,
            issue_date,
            due_date,
            status
        )
        VALUES(?,?,?,?,?,?)
        """,
        (
            user_name,
            role,
            book_title,
            issue_date,
            due_date,
            "Issued"
        ))

        conn.commit()

    cur.execute("""
    SELECT *
    FROM issued_books
    ORDER BY id DESC
    """)

    issued = cur.fetchall()

    conn.close()

    return render_template(
        "issue_book.html",
        issued=issued
    )


# ==========================
# RETURN BOOK
# ==========================

@app.route("/return", methods=["GET", "POST"])
def return_book():

    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":

        issue_id = request.form["issue_id"]

        cur.execute("""
        SELECT *
        FROM issued_books
        WHERE id=?
        """, (issue_id,))

        book = cur.fetchone()

        if book:

            today = datetime.today()

            due = datetime.strptime(
                book["due_date"],
                "%Y-%m-%d"
            )

            fine = 0

            if today > due:

                days = (today - due).days

                fine = days * 10

            cur.execute("""
            UPDATE issued_books
            SET
                return_date=?,
                fine=?,
                status=?
            WHERE id=?
            """,
            (
                today.strftime("%Y-%m-%d"),
                fine,
                "Returned",
                issue_id
            ))

            conn.commit()

    cur.execute("""
    SELECT *
    FROM issued_books
    ORDER BY id DESC
    """)

    books = cur.fetchall()

    conn.close()

    return render_template(
        "return_book.html",
        books=books
    )


# ==========================
# FINES
# ==========================

@app.route("/fines")
def fines():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT *
    FROM issued_books
    WHERE fine > 0
    ORDER BY id DESC
    """)

    fines = cur.fetchall()

    conn.close()

    return render_template(
        "fines.html",
        fines=fines
    )


# ==========================
# REPORTS
# ==========================

@app.route("/reports")
def reports():

    conn = get_db()
    cur = conn.cursor()

    # ------------------------
    # Summary
    # ------------------------

    cur.execute("SELECT COUNT(*) FROM books")
    total_books = cur.fetchone()[0]

    cur.execute("""
    SELECT COUNT(*)
    FROM issued_books
    WHERE status='Issued'
    """)
    total_issued = cur.fetchone()[0]

    cur.execute("""
    SELECT COUNT(*)
    FROM issued_books
    WHERE status='Returned'
       OR status='Paid'
    """)
    total_returned = cur.fetchone()[0]

    cur.execute("""
    SELECT IFNULL(SUM(fine),0)
    FROM issued_books
    """)
    total_fine = cur.fetchone()[0]

    # ------------------------
    # Books
    # ------------------------

    cur.execute("""
    SELECT *
    FROM books
    ORDER BY id DESC
    """)

    books = cur.fetchall()

    # ------------------------
    # Issued Books
    # ------------------------

    cur.execute("""
    SELECT *
    FROM issued_books
    WHERE status='Issued'
    ORDER BY id DESC
    """)

    issued_books = cur.fetchall()

    # ------------------------
    # Returned Books
    # ------------------------

    cur.execute("""
    SELECT *
    FROM issued_books
    WHERE status='Returned'
       OR status='Paid'
    ORDER BY id DESC
    """)

    returned_books = cur.fetchall()

    # ------------------------
    # Fine Report
    # ------------------------

    cur.execute("""
    SELECT *
    FROM issued_books
    WHERE fine>0
    ORDER BY id DESC
    """)

    fines = cur.fetchall()

    conn.close()

    return render_template(

        "reports.html",

        total_books=total_books,

        total_issued=total_issued,

        total_returned=total_returned,

        total_fine=total_fine,

        books=books,

        issued_books=issued_books,

        returned_books=returned_books,

        fines=fines

    )


# ==========================
# PAY FINE
# ==========================

@app.route("/pay_fine/<int:id>")
def pay_fine(id):

    conn = get_db()
    cur = conn.cursor()

    # Mark fine as paid
    cur.execute("""
    UPDATE issued_books
    SET status='Paid'
    WHERE id=?
    """, (id,))

    conn.commit()
    conn.close()

    return redirect("/fines")


# ==========================
# LOGOUT
# ==========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# ==========================
# MAIN
# ==========================

if __name__ == "__main__":

    create_tables()

    app.run(
        debug=True
    )