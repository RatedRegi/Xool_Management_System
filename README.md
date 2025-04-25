# 🏫 Xool - Django School Management System

**Xool** is a simple yet powerful school management system built with Django. It features user registration, authentication, and role-based access (students, teachers, and admins). The system is designed to be modular and easy to extend for more functionalities like grades, attendance, subjects, and reports.

---

## 🚀 Features

- ✅ Custom user model with roles (`student`, `teacher`, `admin`)
- ✅ Student registration with extended fields (first name, last name, email, grade level, and school)
- ✅ Role-based redirection after login
- ✅ Bootstrap 5 frontend styling for clean UI
- ✅ Login/logout with Django's built-in auth system
- ✅ Future-proof structure for adding teacher and admin dashboards

---

## 🖼️ Screenshots

> 🧑‍🎓 Student Registration Page  
![Student Registration Screenshot](screenshots/student-register.png)

> 🔐 Login Page  
![Login Page Screenshot](screenshots/login.png)

---

## 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, Bootstrap 5
- **Database:** SQLite (can switch to PostgreSQL)
- **Environment:** Virtualenv / venv

---

## 🧑‍💻 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/xool.git
cd xool

### 2. Create and activate a virtual environmet

python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Run migrations

python manage.py makemigrations
python manage.py migrate

### 5. Create a superuser

python manage.py createsuperuser

### 6. Start the development server

python manage.py runserver
Then go to: http://127.0.0.1:8000/

📁 Project Structure
bash
Copy
Edit
xool/
│
├── users/                 # Handles custom user model and registration
├── templates/             # HTML templates (login, register)
├── static/                # Static files (CSS, JS, images)
├── db.sqlite3             # Default database
├── manage.py              # Django command-line utility
├── README.md              # This file
✨ Coming Soon
Teacher registration and dashboard

Class and subject management

Attendance tracking

Report generation

Email notifications

📜 License
This project is open-source and available under the MIT License.

🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change or add.

📬 Contact
Author: Reginald Chikuni
Email: reginaldchikun2@gmail.com
GitHub: @RatedRegi
