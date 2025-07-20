# Task Manager API

A Flask-based REST API for managing user tasks with JWT authentication.

---

## Setup Instructions


1. **Clone the repo:**

   ```
   git clone https://github.com/DinosL/restApp.git
   cd restAPP

2. **Create and activate a virtual environment:**

    ```
    python3 -m venv venv
    source venv/bin/activate
    ```
3. **Install dependencies**

    ```
    pip install -r requirements.txt
    ```
4. **Setup environments variables**
    - ``` DATABASE_URL ```: The database file URL default is ```sqlite:///test.db```
    - ``` JWT_SECRET_KEY ```: secret key for JWT tokens. If not changed it uses a string which is **not safe**.

5. **Run tests**
    ``` PYTHONPATH=. pytest test  ```


6. **Run the app**
    ```python3 run.py ```


# Supported API calls

The API is documented with Swagger UI, accesible at: 
``` http://127.0.0.1:5000/apidocs/ ```

## Endpoints
| Method | Endpoint      | Description                           | Auth Required |
| ------ | ------------- | ------------------------------------- | ------------- |
| POST   | `/register`   | Register a new user                   | No            |
| POST   | `/login`      | Login and get a JWT token             | No            |
| GET    | `/tasks/`     | List all tasks for the logged-in user | Yes           |
| POST   | `/tasks/`     | Create a new task                     | Yes           |
| PUT    | `/tasks/<id>` | Update a task                         | Yes           |
| DELETE | `/tasks/<id>` | Delete a task                         | Yes           |

# Decisions & Assumptions
- JWT Authentication: Secure token-based authentication is used for stateless session management.

- SQLite by default: For simplicity and easy setup, SQLite is the default database; environment variable support allows easy switch to other DBs.

- Blueprints: Tasks routes are modularized using Flask Blueprints for better organization.

- In-memory DB for tests: Tests run against a SQLite in-memory database for speed and isolation.

- Swagger: API docs are automatically generated using Flasgger for interactive exploration and ease of client integration.

- Password Security: Passwords are hashed using Werkzeug’s security utilities, not stored in plaintext.

- Continuous Intgration: Github Actions is used for basic continuous integration. It automatically runs tests and checks code quality on every push and pull request to the main branch to ensure stability.

- Assumptions: Usernames are unique. Only authenticated users can manipulate their own tasks.
