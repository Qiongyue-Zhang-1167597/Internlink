# InternLink: Internship Application Portal

InternLink is a dynamic web application designed to bridge the gap between students seeking internships and employers looking for talent. It provides a streamlined platform for managing the entire internship application lifecycle, catering to three distinct user roles: Students, Employers, and Administrators.

This project was developed as part of the COMP639 Web Development course.

---

## Features 

The application provides a role-based experience to ensure users only access relevant features.

#### For Students:
*   **Browse & Filter:** Search and filter a comprehensive list of available internships by category, location, and duration.
*   **Apply for Internships:** Submit applications for specific roles with a cover letter and an uploaded resume (PDF format).
*   **Track Applications:** View the real-time status of all submitted applications (Pending, Accepted, or Rejected) and view feedback from employers.

#### For Employers:
*   **View Postings:** Access a dashboard showing only the internship positions posted by their own organization.
*   **Manage Applicants:** Review a detailed list of student applicants for each internship posting.
*   **Update Status:** Accept or Reject applications, with the option to provide valuable feedback to the student.

#### For Administrators:
*   **User Management:** View a list of all registered users and manage their account status (e.g., active/inactive).
*   **Full Oversight:** View all internships and applications across the entire platform for monitoring and support purposes.

#### General Features:
*   **Profile Management:** All users can view and edit their own profile details and change their password securely.

---

## Technology Stack 

*   **Backend:** Python 3.9+ with Flask Framework
*   **Frontend:** HTML5, Bootstrap 5 CSS, JavaScript
*   **Database:** MySQL
*   **Password Hashing:** Flask-Bcrypt
*   **Deployment:** Hosted on PythonAnywhere

---

## Local Setup and Installation 

Follow these steps to get the application running on your local machine.

#### 1. Prerequisites 
*   Python 3.9 or newer
*   Git
*   A running MySQL server instance

#### 2. Clone the Repository 
```bash
git clone https://github.com/Qiongyue-Zhang-1167597/Internlink.git
cd Internlink
```

#### 3. Create and Activate Virtual Environment 
*   For Windows:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
*   For macOS/Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

#### 4. Install Dependencies 
With your virtual environment activated, run the following command:
```bash
pip install -r requirements.txt
```

#### 5. Database Configuration 
You need to create a `connect.py` file to store your local database credentials.

*   Navigate into the `InternLink` package directory: `cd InternLink`
*   Create a new file named `connect.py` with the following content, replacing the placeholder values with your own MySQL details.

    ```python
    
    
    dbuser = 'your_mysql_username'
    dbpass = 'your_mysql_password'
    dbhost = 'localhost'
    dbname = 'internlink_db'
    dbport = 3306
    ```

#### 6. Database Setup 
You will need a MySQL client (like MySQL Workbench or the command-line client) to set up the database.

1.  **Create the Database:** First, create a new database with the same name you specified in `dbname` (e.g., `internlink_db`).
2.  **Create Tables:** Execute the `create_database.sql` script to create all necessary tables.
3.  **Populate Data:** Execute the `populate_database.sql` script to fill the tables with initial test data.

#### 7. Run the Application 
Navigate back to the project root directory (the one containing `run.py`) and run the application:
```bash
python run.py
```
The application will be available at `http://127.0.0.1:5000`.

---

## Deployment on PythonAnywhere 

This application is deployed and hosted on PythonAnywhere. The general steps are outlined below:

1.  **Clone Repository:** Clone the GitHub repository to your PythonAnywhere account via a Bash console.
2.  **Create Virtual Environment & Install Dependencies:** Set up a virtual environment and install all packages from `requirements.txt`.
3.  **Create Web App:** Create a new "Manual configuration" Web App on the PythonAnywhere Web tab.
4.  **Configure Paths:** Set the "Source code", "Working directory", and "Virtualenv" paths to point to your project directory and the `venv` folder within it.
5.  **Configure WSGI:** Edit the WSGI configuration file to import and use the `app` object from the `InternLink` package.
6.  **Setup Database:** Create a new MySQL database on the Databases tab, note the credentials, and create a `connect.py` file on the server with these new credentials. Then, run the `.sql` scripts in a PythonAnywhere MySQL console.
7.  **Configure Static Files:** Map the URL `/static` to the project's static directory (`.../InternLink/InternLink/static`).
8.  **Reload:** Reload the web app from the Web tab.

---

## Testing Accounts 

You can use the following accounts to test the application's different roles.

#### Administrator
*   **Username:** `admin_linda`
*   **Password:** `AdminPass123!`

#### Employer
*   **Username:** `techcorp`
*   **Password:** `TechCorp@ss`

#### Student
*   **Username:** `janesmith`
*   **Password:** `BlueJay@2024`

*(Note: A full list of 20 students and 5 employers with strong passwords is available in the `populate_database.sql` script.)*