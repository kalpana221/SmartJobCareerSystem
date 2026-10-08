from flask import Flask, render_template, request, session, redirect, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from db import get_connection
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("FLASK_SECRET_KEY")

@app.route("/")
def home():
    return "Smart Job Application & Career Management System"

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # Check if email already exists
        cursor.execute(
            "SELECT user_id FROM users WHERE email = %s",
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            connection.close()
            return "Email already registered. Please use a different email."

        # Hash password
        hashed_password = generate_password_hash(password)

        # Insert new user
        cursor.execute(
            """
            INSERT INTO users (name, email, password)
            VALUES (%s, %s, %s)
            """,
            (
                name,
                email,
                hashed_password
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE email = %s",
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user and check_password_hash(user["password"], password):

            session["user_id"] = user["user_id"]
            session["name"] = user["name"]

            return redirect("/dashboard")

        return "Invalid email or password!"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM job_applications
        WHERE user_id = %s
        """,
        (session["user_id"],)
    )

    total = cursor.fetchone()["total"]

    cursor.execute(
        """
        SELECT COUNT(*) AS applied
        FROM job_applications
        WHERE user_id = %s
        AND status = 'Applied'
        """,
        (session["user_id"],)
    )

    applied = cursor.fetchone()["applied"]

    cursor.execute(
        """
        SELECT COUNT(*) AS interview
        FROM job_applications
        WHERE user_id = %s
        AND status = 'Interview'
        """,
        (session["user_id"],)
    )

    interview = cursor.fetchone()["interview"]

    cursor.execute(
        """
        SELECT COUNT(*) AS selected
        FROM job_applications
        WHERE user_id = %s
        AND status = 'Selected'
        """,
        (session["user_id"],)
    )

    selected = cursor.fetchone()["selected"]

    cursor.execute(
        """
        SELECT COUNT(*) AS rejected
        FROM job_applications
        WHERE user_id = %s
        AND status = 'Rejected'
        """,
        (session["user_id"],)
    )
    rejected = cursor.fetchone()["rejected"]

    cursor.execute(
    """
    SELECT COUNT(*) AS total_interviews
    FROM interviews
    WHERE user_id = %s
    """,
    (session["user_id"],)
    )

    total_interviews = cursor.fetchone()["total_interviews"]


    cursor.execute(
    """
    SELECT COUNT(*) AS scheduled
    FROM interviews
    WHERE user_id = %s
    AND status = 'Scheduled'
    """,
    (session["user_id"],)
    )

    scheduled = cursor.fetchone()["scheduled"]


    cursor.execute(
    """
    SELECT COUNT(*) AS completed
    FROM interviews
    WHERE user_id = %s
    AND status = 'Completed'
    """,
    (session["user_id"],)
    )

    completed = cursor.fetchone()["completed"]


    cursor.execute(
    """
    SELECT COUNT(*) AS cancelled
    FROM interviews
    WHERE user_id = %s
    AND status = 'Cancelled'
    """,
    (session["user_id"],)
    )

    cancelled = cursor.fetchone()["cancelled"]

    cursor.execute(
    """
    SELECT COUNT(*) AS total_resumes
    FROM resumes
    WHERE user_id = %s
    """,
    (session["user_id"],)
    )

    total_resumes = cursor.fetchone()["total_resumes"]

    cursor.close()
    connection.close()

    return render_template(
        "dashboard.html",
        total=total,
        applied=applied,
        interview=interview,
        selected=selected,
        rejected=rejected,
        total_interviews=total_interviews,
        scheduled=scheduled,
        completed=completed,
        cancelled=cancelled,
        total_resumes=total_resumes
    )

@app.route("/add-application", methods=["GET", "POST"])
def add_application():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        company_name = request.form["company_name"]
        job_role = request.form["job_role"]
        location = request.form["location"]
        status = request.form["status"]
        applied_date = request.form["applied_date"]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO job_applications
            (user_id, company_name, job_role, location, status, applied_date)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                session["user_id"],
                company_name,
                job_role,
                location,
                status,
                applied_date
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        return "Job Application Added Successfully!"

    return render_template("add_application.html")

@app.route("/applications")
def applications():

    if "user_id" not in session:
        return redirect("/login")

    search = request.args.get("search", "")
    status = request.args.get("status", "")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT *
        FROM job_applications
        WHERE user_id = %s
    """

    params = [session["user_id"]]

    # Search by company or job role
    if search:
        query += """
            AND (
                company_name LIKE %s
                OR job_role LIKE %s
            )
        """

        search_value = "%" + search + "%"

        params.append(search_value)
        params.append(search_value)

    # Filter by status
    if status:
        query += " AND status = %s"
        params.append(status)

    query += " ORDER BY application_id DESC"

    cursor.execute(query, tuple(params))

    applications = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "applications.html",
        applications=applications,
        search=search,
        status=status
    )

@app.route("/interviews")
def interviews():

    if "user_id" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            i.interview_id,
            j.company_name,
            j.job_role,
            i.interview_date,
            i.interview_time,
            i.interview_type,
            i.status,
            i.notes
        FROM interviews i
        JOIN job_applications j
            ON i.application_id = j.application_id
        WHERE i.user_id = %s
        ORDER BY i.interview_date ASC
        """,
        (session["user_id"],)
    )

    interviews = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "interviews.html",
        interviews=interviews
    )

@app.route("/add-interview", methods=["GET", "POST"])
def add_interview():

    if "user_id" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        application_id = request.form["application_id"]
        interview_date = request.form["interview_date"]
        interview_time = request.form["interview_time"]
        interview_type = request.form["interview_type"]
        status = request.form["status"]
        notes = request.form["notes"]

        # Check whether the application belongs to the logged-in user
        cursor.execute(
            """
            SELECT application_id
            FROM job_applications
            WHERE application_id = %s AND user_id = %s
            """,
            (application_id, session["user_id"])
        )

        application = cursor.fetchone()

        if not application:
            cursor.close()
            connection.close()
            return "Invalid job application"

        # Add interview
        cursor.execute(
            """
            INSERT INTO interviews
            (
                user_id,
                application_id,
                interview_date,
                interview_time,
                interview_type,
                status,
                notes
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                session["user_id"],
                application_id,
                interview_date,
                interview_time,
                interview_type,
                status,
                notes
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/interviews")

    # Get only this user's job applications
    cursor.execute(
        """
        SELECT application_id, company_name, job_role
        FROM job_applications
        WHERE user_id = %s
        ORDER BY application_id DESC
        """,
        (session["user_id"],)
    )

    applications = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "add_interview.html",
        applications=applications
    )

@app.route("/delete-interview/<int:interview_id>", methods=["POST"])
def delete_interview(interview_id):

    if "user_id" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM interviews
        WHERE interview_id = %s AND user_id = %s
        """,
        (interview_id, session["user_id"])
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/interviews")


@app.route("/delete-application/<int:application_id>", methods=["POST"])
def delete_application(application_id):

    if "user_id" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        # Check whether the application belongs to this user
        cursor.execute(
            """
            SELECT application_id
            FROM job_applications
            WHERE application_id = %s AND user_id = %s
            """,
            (application_id, session["user_id"])
        )

        application = cursor.fetchone()

        if not application:
            return "Application not found"

        # Delete related interviews first
        cursor.execute(
            """
            DELETE FROM interviews
            WHERE application_id = %s AND user_id = %s
            """,
            (application_id, session["user_id"])
        )

        # Delete the job application
        cursor.execute(
            """
            DELETE FROM job_applications
            WHERE application_id = %s AND user_id = %s
            """,
            (application_id, session["user_id"])
        )

        connection.commit()

        return redirect("/applications")

    except Exception:
        connection.rollback()
        return "Unable to delete application. Please try again."

    finally:
        cursor.close()
        connection.close()

@app.route("/edit-application/<int:application_id>", methods=["GET", "POST"])
def edit_application(application_id):

    if "user_id" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    # Check that this application belongs to the logged-in user
    cursor.execute(
        """
        SELECT *
        FROM job_applications
        WHERE application_id = %s AND user_id = %s
        """,
        (application_id, session["user_id"])
    )

    application = cursor.fetchone()

    if not application:
        cursor.close()
        connection.close()
        return "Application not found"

    if request.method == "POST":

        company_name = request.form["company_name"]
        job_role = request.form["job_role"]
        location = request.form["location"]
        status = request.form["status"]
        applied_date = request.form["applied_date"]

        cursor.execute(
            """
            UPDATE job_applications
            SET company_name = %s,
                job_role = %s,
                location = %s,
                status = %s,
                applied_date = %s
            WHERE application_id = %s AND user_id = %s
            """,
            (
                company_name,
                job_role,
                location,
                status,
                applied_date,
                application_id,
                session["user_id"]
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/applications")

    cursor.close()
    connection.close()

    return render_template(
        "edit_application.html",
        application=application
    )

@app.route("/logout")
def logout():

    session.clear()

    return "Logout Successful!"

@app.route("/edit-interview/<int:interview_id>", methods=["GET", "POST"])
def edit_interview(interview_id):

    if "user_id" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    # Check that this interview belongs to the logged-in user
    cursor.execute(
        """
        SELECT *
        FROM interviews
        WHERE interview_id = %s AND user_id = %s
        """,
        (interview_id, session["user_id"])
    )

    interview = cursor.fetchone()

    if not interview:
        cursor.close()
        connection.close()
        return "Interview not found"

    if request.method == "POST":

        interview_date = request.form["interview_date"]
        interview_time = request.form["interview_time"]
        interview_type = request.form["interview_type"]
        status = request.form["status"]
        notes = request.form["notes"]

        cursor.execute(
            """
            UPDATE interviews
            SET interview_date = %s,
                interview_time = %s,
                interview_type = %s,
                status = %s,
                notes = %s
            WHERE interview_id = %s AND user_id = %s
            """,
            (
                interview_date,
                interview_time,
                interview_type,
                status,
                notes,
                interview_id,
                session["user_id"]
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/interviews")

    cursor.close()
    connection.close()

    return render_template(
        "edit_interview.html",
        interview=interview
    )

@app.route("/upload-resume", methods=["GET", "POST"])
def upload_resume():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        file = request.files["resume"]

        if file.filename == "":
            return "Please select a resume"

        original_filename = secure_filename(file.filename)

        # Check file size (maximum 5 MB)
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)

        max_size = 5 * 1024 * 1024

        if file_size > max_size:
            return "File too large. Maximum file size is 5 MB."

        # Check file type
        allowed_extensions = {"pdf", "doc", "docx"}

        if (
            "." not in original_filename
            or original_filename.rsplit(".", 1)[1].lower()
            not in allowed_extensions
        ):
            return "Invalid file type. Only PDF, DOC and DOCX files are allowed."

        # Create uploads folder
        upload_folder = "uploads"

        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        # Create unique filename
        import uuid

        extension = original_filename.rsplit(".", 1)[1].lower()

        unique_filename = str(uuid.uuid4()) + "." + extension

        file_path = os.path.join(upload_folder, unique_filename)

        # Save file
        file.save(file_path)

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO resumes
            (user_id, resume_name, resume_path)
            VALUES (%s, %s, %s)
            """,
            (
                session["user_id"],
                original_filename,
                file_path
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        return "Resume Uploaded Successfully!"

    return render_template("upload_resume.html")

@app.route("/resumes")
def resumes():

    if "user_id" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT resume_id, resume_name, uploaded_at
        FROM resumes
        WHERE user_id = %s
        ORDER BY resume_id DESC
        """,
        (session["user_id"],)
    )

    resumes = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "resumes.html",
        resumes=resumes
    )

@app.route("/download-resume/<int:resume_id>")
def download_resume(resume_id):

    if "user_id" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT resume_name, resume_path
        FROM resumes
        WHERE resume_id = %s AND user_id = %s
        """,
        (resume_id, session["user_id"])
    )

    resume = cursor.fetchone()

    cursor.close()
    connection.close()

    if not resume:
        return "Resume not found"

    return send_file(
        resume["resume_path"],
        as_attachment=True,
        download_name=resume["resume_name"]
    )

@app.route("/delete-resume/<int:resume_id>", methods=["POST"])
def delete_resume(resume_id):

    if "user_id" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT resume_path
        FROM resumes
        WHERE resume_id = %s AND user_id = %s
        """,
        (resume_id, session["user_id"])
    )

    resume = cursor.fetchone()

    if not resume:
        cursor.close()
        connection.close()
        return "Resume not found"

    # Delete the physical file
    if os.path.exists(resume["resume_path"]):
        os.remove(resume["resume_path"])

    # Delete database record
    cursor.execute(
        """
        DELETE FROM resumes
        WHERE resume_id = %s AND user_id = %s
        """,
        (resume_id, session["user_id"])
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/resumes")

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM admins
            WHERE email = %s
            """,
            (email,)
        )

        admin = cursor.fetchone()

        cursor.close()
        connection.close()

        if admin and check_password_hash(admin["password"], password):

            session["admin_id"] = admin["admin_id"]
            session["admin_name"] = admin["name"]

            return redirect("/admin-dashboard")

        return "Invalid admin email or password!"

    return render_template("admin_login.html")

@app.route("/admin-dashboard")
def admin_dashboard():

    if "admin_id" not in session:
        return redirect("/admin-login")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT COUNT(*) AS total_users
        FROM users
        """
    )

    total_users = cursor.fetchone()["total_users"]

    cursor.execute(
        """
        SELECT COUNT(*) AS total_applications
        FROM job_applications
        """
    )

    total_applications = cursor.fetchone()["total_applications"]

    cursor.execute(
        """
        SELECT COUNT(*) AS total_interviews
        FROM interviews
        """
    )

    total_interviews = cursor.fetchone()["total_interviews"]

    cursor.execute(
        """
        SELECT COUNT(*) AS total_resumes
        FROM resumes
        """
    )

    total_resumes = cursor.fetchone()["total_resumes"]

    cursor.close()
    connection.close()

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_applications=total_applications,
        total_interviews=total_interviews,
        total_resumes=total_resumes
    )

@app.route("/admin-users")
def admin_users():

    if "admin_id" not in session:
        return redirect("/admin-login")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT user_id, name, email, created_at
        FROM users
        ORDER BY user_id DESC
        """
    )

    users = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "admin_users.html",
        users=users
    )

@app.route("/admin-applications")
def admin_applications():

    if "admin_id" not in session:
        return redirect("/admin-login")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            j.application_id,
            u.name AS user_name,
            u.email AS user_email,
            j.company_name,
            j.job_role,
            j.location,
            j.status,
            j.applied_date
        FROM job_applications j
        JOIN users u
            ON j.user_id = u.user_id
        ORDER BY j.application_id DESC
        """
    )

    applications = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "admin_applications.html",
        applications=applications
    )

@app.route("/admin-interviews")
def admin_interviews():

    if "admin_id" not in session:
        return redirect("/admin-login")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            i.interview_id,
            u.name AS user_name,
            u.email AS user_email,
            j.company_name,
            j.job_role,
            i.interview_date,
            i.interview_time,
            i.interview_type,
            i.status,
            i.notes
        FROM interviews i
        JOIN users u
            ON i.user_id = u.user_id
        JOIN job_applications j
            ON i.application_id = j.application_id
        ORDER BY i.interview_date ASC
        """
    )

    interviews = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "admin_interviews.html",
        interviews=interviews
    )

@app.route("/admin-resumes")
def admin_resumes():

    if "admin_id" not in session:
        return redirect("/admin-login")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            r.resume_id,
            u.name AS user_name,
            u.email AS user_email,
            r.resume_name,
            r.uploaded_at
        FROM resumes r
        JOIN users u
            ON r.user_id = u.user_id
        ORDER BY r.resume_id DESC
        """
    )

    resumes = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "admin_resumes.html",
        resumes=resumes
    )

@app.route("/admin-logout")
def admin_logout():

    session.pop("admin_id", None)
    session.pop("admin_name", None)

    return redirect("/admin-login")


if __name__ == "__main__":
    app.run(debug=True)