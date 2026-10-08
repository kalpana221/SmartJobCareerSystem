# Smart Job Career Management System

A full-stack web application designed to help users manage their job applications, interviews, and resumes in one centralized platform.

## 📌 Project Overview

The Smart Job Career Management System provides a centralized dashboard where users can manage their job search activities.

Users can:

* Create an account and securely log in
* Add and manage job applications
* Search and filter applications
* Schedule and manage interviews
* Upload, download, and delete resumes
* View career-related statistics through the dashboard

The system also provides an administrator panel for managing users, applications, interviews, and resumes.

## ✨ Features

### 👤 User Features

* User Registration
* Secure User Login
* Dashboard
* Job Application Management
* Application Search and Status Filtering
* Interview Management
* Resume Upload and Management
* Resume Download
* Secure Resume Deletion
* Application and Interview Editing

### 🛡️ Admin Features

* Admin Login
* Admin Dashboard
* User Management
* Job Application Management
* Interview Management
* Resume Management
* Resume Download

### 🔐 Security Features

* Password hashing using Werkzeug
* Environment variables for sensitive configuration
* Protected user routes
* Admin authentication
* User ownership validation
* File type validation
* Maximum resume upload size of 5 MB
* Unique filenames for uploaded resumes
* Secure POST-based deletion
* Custom 404 and 500 error pages

## 🛠️ Technologies Used

| Technology             | Purpose                       |
| ---------------------- | ----------------------------- |
| Python                 | Backend programming           |
| Flask                  | Web framework                 |
| HTML                   | Web page structure            |
| CSS                    | User interface and styling    |
| JavaScript             | Client-side functionality     |
| MySQL                  | Database                      |
| mysql-connector-python | MySQL connectivity            |
| Werkzeug               | Password hashing and security |
| Chart.js               | Dashboard charts              |

## 🏗️ System Architecture

```text
Browser
   ↓
HTML / CSS / JavaScript
   ↓
Flask Backend
   ↓
db.py
   ↓
MySQL Database
```

## 🗄️ Database

The application uses MySQL with the following main tables:

* `users`
* `job_applications`
* `interviews`
* `resumes`
* `admins`

Relationships between users, job applications, interviews, and resumes help maintain user-specific data.

## 📂 Project Structure

```text
SmartJobCareerSystem/
│
├── app.py
├── db.py
├── requirements.txt
├── .env
├── .gitignore
├── uploads/
│
└── templates/
    ├── register.html
    ├── login.html
    ├── dashboard.html
    ├── add_application.html
    ├── applications.html
    ├── edit_application.html
    ├── add_interview.html
    ├── interviews.html
    ├── edit_interview.html
    ├── upload_resume.html
    ├── resumes.html
    ├── admin_login.html
    ├── admin_dashboard.html
    ├── admin_users.html
    ├── admin_applications.html
    ├── admin_interviews.html
    ├── admin_resumes.html
    └── error.html
```

> Note: `.env`, `venv/`, and uploaded resume files are excluded from Git using `.gitignore`.

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/kalpana221/SmartJobCareerSystem.git
```

### 2. Open the project

```bash
cd SmartJobCareerSystem
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

## 🗄️ MySQL Configuration

Create a MySQL database named:

```text
smart_job_career
```

Configure the database connection using environment variables in a `.env` file.

Example:

```text
FLASK_SECRET_KEY=your-secret-key
MYSQL_HOST=localhost
MYSQL_USER=your-mysql-user
MYSQL_PASSWORD=your-mysql-password
MYSQL_DATABASE=smart_job_career
```

Do not upload the `.env` file to GitHub.

## ▶️ Run the Application

Activate the virtual environment and run:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## 📊 Dashboard

The dashboard provides an overview of:

* Total job applications
* Application status
* Total interviews
* Interview status
* Total uploaded resumes

## 🔒 Privacy and Security

Sensitive configuration files and uploaded resumes are excluded from version control.

The application also validates user ownership before allowing users to edit or delete their records.

## 🚀 Future Enhancements

Possible future improvements include:

* Email notifications for interviews
* Job recommendation system
* Resume analysis
* Application deadline reminders
* Advanced analytics
* Job portal API integration

## 👩‍💻 Author

**Kalpana Chowdary**

GitHub:
https://github.com/kalpana221

## 📄 License

This project was developed as an academic and portfolio project.
