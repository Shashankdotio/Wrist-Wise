# Wrist-Wise

A Flask-based backend server for health data management.

---

## 🛠️ Setup Instructions

This guide will help you set up and run Wrist-Wise locally (using VS Code and launch.json) and with Docker Compose. All steps are beginner-friendly and explained in detail.

---

### 1. Clone the Repository

Open your terminal and run:

```sh
git clone <repo-url>
cd Wrist-Wise
```

---

### 2. Configure Environment Variables

#### For Local Development

Create a file named `.env` in the `env/` folder (not the project root). Add the following line:

```
DATABASE_URL=postgresql://appleuser:applepass@localhost:5432/appledb
```

#### For Docker Compose

The required environment variables are already set in `env/service.env` and used by Docker Compose.

---

### 3. Install Poetry & Python Dependencies

Wrist-Wise uses [Poetry](https://python-poetry.org/) for dependency management.

1. Make sure Poetry is installed. If not, install it:
   ```sh
   pipx install poetry==1.8.5
   ```
2. Install dependencies:
   ```sh
   poetry install
   ```
3. (Optional) Activate the Poetry shell for local development:
   ```sh
   poetry shell
   ```
4. Get the Python path for VS Code launch config:
   ```sh
   which python
   ```

---

### 4. Set Up the Database

Wrist-Wise uses PostgreSQL. You can set it up manually or let Docker Compose handle it for you.

#### Option A: Manual Setup (Local Development)

1. Make sure PostgreSQL is installed and running on your machine.
2. Open a terminal and run:
   ```sh
   psql -U postgres
   ```
3. In the PostgreSQL prompt, run:
   ```sql
   CREATE USER appleuser WITH PASSWORD 'applepass';
   CREATE DATABASE appledb OWNER appleuser;
   GRANT ALL PRIVILEGES ON DATABASE appledb TO appleuser;
   ```

#### Option B: Automatic Setup (Docker Compose)

1. In your project directory, run:
   ```sh
   docker compose up -d db
   ```
2. Check if the DB is running:
   ```sh
   docker ps -a
   ```
3. Docker Compose will automatically create the database, user, and set the password as specified in `docker-compose.yml`.

---

### 4. Install Python Dependencies (Local Development)

Wrist-Wise uses [Poetry](https://python-poetry.org/) for dependency management.

1. Make sure Poetry is installed. If not, install it:
   ````sh
   pipx install poetry==1.8.5
   ```jsonc
   {
     "version": "0.2.0",
     "configurations": [
       {
         "name": "Python: Flask (backend_server.py)",
         "type": "python",
         "request": "launch",
         "program": "${workspaceFolder}/backend_server.py",
         "envFile": "${workspaceFolder}/env/.env",
         "env": {
           "FLASK_ENV": "development"
         },
         "pythonPath": "<your-poetry-python-path>",
         "console": "integratedTerminal"
       }
     ]
   }
   ````
   ```sh
   poetry install
   ```

---

Wrist-Wise uses [Poetry](https://python-poetry.org/) for dependency management.

1. Run This in root directory:
   ```sh
   poetry shell
   ```
2. get the python path:
   ```sh
   which python
   ```
   ```sh
   docker-compose up --build
   ```

### 6. Run Database on your local

Wrist-Wise uses Postgres as DB:

1. Run This in root directory:
   ```sh
   docker compose up -d db
   ```
2. Re-check if DB is running with:
   ```sh
   docker ps -a
   ```

---

### 7. Run the Server Locally (VS Code Launch Configuration)

You can run the server using VS Code's built-in debugger for a smooth development experience.

#### Steps:

1. Open the project in VS Code.
2. If the folder `.vscode` or the file `.vscode/launch.json` does not exist, create them:
   - Right-click in the Explorer panel, choose "New Folder" and name it `.vscode`.
   - Inside `.vscode`, create a new file named `launch.json`.
3. Copy and paste the following configuration into `.vscode/launch.json`:
   ```jsonc
   {
     "version": "0.2.0",
     "configurations": [
       {
         "name": "Python: Flask (backend_server.py)",
         "type": "python",
         "request": "launch",
         "program": "${workspaceFolder}/backend_server.py",
         "envFile": "${workspaceFolder}/env/.env",
         "env": {
           "FLASK_ENV": "development"
         },
         "pythonPath": "<your-poetry-python-path>",
         "console": "integratedTerminal"
       }
     ]
   }
   ```
4. Replace `<your-poetry-python-path>` with the path you got from the `which python` command in step 5 above (e.g., `/Users/dheeraj/Library/Caches/pypoetry/virtualenvs/wrist-wise-xxxxxx/bin/python`).
5. Save the file.
6. Press `F5` or click the green "Run" button in VS Code to start the server.
7. The server will run on [http://localhost:8000/](http://localhost:8000/).
8. If you see errors about missing dependencies, make sure you ran `poetry install` and activated the Poetry shell.

---

### 8. Run the Server with Docker Compose

Docker Compose makes it easy to run both the backend and the database in containers.

#### Steps:

1. Make sure Docker is installed and running on your machine.
   - On macOS, install [Docker Desktop](https://www.docker.com/products/docker-desktop/).
   - After installation, open Docker Desktop and ensure it is running.
2. If you are inside a Poetry shell, exit it first by typing `exit` in the terminal.
3. In your project directory, run:
   ```sh
   docker-compose up --build
   ```
4. This will build the backend image, start the backend and PostgreSQL containers, and set up the database automatically.
5. The backend will be available at [http://localhost:8000/](http://localhost:8000/).
6. To stop the containers, use:
   ```sh
   docker-compose down
   ```
7. If you need to restart containers:
   ```sh
   docker-compose restart
   ```
8. If you get a port conflict error, make sure no other process is using port 8000 or 5432.

---

### 9. Health Check

To verify the backend is running, open your browser and visit:

[http://localhost:8000/](http://localhost:8000/)

You should see a response from the server (such as a health check message).

---

## 🗂️ Project Structure

- `models/` - Database models
- `routes/` - API routes
- `backend_server.py` - Entry point
- `requirements.txt` - Pip requirements
- `pyproject.toml` - Poetry configuration
- `Dockerfile` and `docker-compose.yml` - Containerization
- `env/` - Environment variable files

---

## 💡 Troubleshooting & Tips

- If you get a database connection error, make sure PostgreSQL is running and the credentials match those in your `.env` or `service.env` file.
- For Docker Compose, containers can be restarted with `docker-compose restart`.
- To stop containers, use `docker-compose down`.
- For local development, ensure your Python version matches the one specified in `pyproject.toml`.
- If you change dependencies, re-run `poetry install`.
- If Docker Compose fails to start, check Docker Desktop is running and try restarting it.
- If you see `ModuleNotFoundError` in VS Code, check your launch.json `pythonPath` and that Poetry dependencies are installed.
- If you get a port conflict, stop any other services using port 8000 or 5432.

---

## 📚 Useful Resources

- [Poetry Documentation](https://python-poetry.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [VS Code Python Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

---
