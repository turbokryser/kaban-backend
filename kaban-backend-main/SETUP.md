# Setup Guide for Kaban X Backend

This guide will help you set up the Kaban X backend API on a new computer.

## Prerequisites

- Python 3.11 or higher
- MySQL 8.0 or higher (or use Docker)
- pip (Python package manager)

## Option 1: Using Docker (Recommended - Easiest)

### Step 1: Install Docker
- Download and install Docker Desktop from https://www.docker.com/products/docker-desktop
- Make sure Docker is running

### Step 2: Configure Environment Variables
1. Copy the `.env.example` file and create a `.env` file:
   ```bash
   # On Windows PowerShell:
   Copy-Item .env.example .env
   
   # On Linux/Mac:
   cp .env.example .env
   ```

2. Edit the `.env` file and update the following values:
   ```
   DATABASE_URL=mysql+pymysql://kaban_user:kaban_password@db:3306/kaban_db
   SECRET_KEY=your-secret-key-here-change-in-production-use-a-random-string
   ```

### Step 3: Run with Docker Compose
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## Option 2: Manual Setup (Without Docker)

### Step 1: Install MySQL
- Install MySQL 8.0+ from https://dev.mysql.com/downloads/mysql/
- Create a database:
  ```sql
  CREATE DATABASE kaban_db;
  CREATE USER 'kaban_user'@'localhost' IDENTIFIED BY 'kaban_password';
  GRANT ALL PRIVILEGES ON kaban_db.* TO 'kaban_user'@'localhost';
  FLUSH PRIVILEGES;
  ```

### Step 2: Import Database Schema
```bash
mysql -u kaban_user -p kaban_db < "drawSQL-mysql-export-2025-12-09 (1).sql"
```

### Step 3: Create Virtual Environment
```bash
# On Windows:
python -m venv venv
venv\Scripts\activate

# On Linux/Mac:
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Configure Environment Variables
1. Create a `.env` file:
   ```bash
   # On Windows PowerShell:
   Copy-Item .env.example .env
   
   # On Linux/Mac:
   cp .env.example .env
   ```

2. Edit `.env` and set:
   ```
   DATABASE_URL=mysql+pymysql://kaban_user:kaban_password@localhost:3306/kaban_db
   SECRET_KEY=your-secret-key-here-change-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   REFRESH_TOKEN_EXPIRE_DAYS=7
   ```

### Step 6: Run the Application
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

Once running, you can access:
- **API Documentation (Swagger)**: http://localhost:8000/docs
- **Alternative Documentation**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Available Endpoints:

#### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get tokens
- `POST /auth/refresh` - Refresh access token

#### User
- `GET /user/me` - Get current user info (requires authentication)

#### Projects
- `POST /projects` - Create a new project
- `GET /projects` - List all projects user has access to
- `GET /projects/{id}` - Get project details
- `POST /projects/{id}/invite` - Invite user to project
- `GET /projects/{id}/board` - Get project board with sections and tasks

#### Sections (Columns)
- `POST /projects/{id}/sections` - Create a new section
- `PATCH /projects/{id}/sections/{section_id}` - Update a section

#### Tasks
- `POST /projects/{id}/tasks` - Create a new task
- `PATCH /projects/{id}/tasks/{task_id}` - Update a task

## Testing the API

### 1. Register a User
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpassword123"
  }'
```

### 2. Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123"
  }'
```

### 3. Use the Token
Copy the `access_token` from the response and use it in subsequent requests:
```bash
curl -X GET "http://localhost:8000/user/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

## Troubleshooting

### Database Connection Issues
- Make sure MySQL is running
- Check that the database credentials in `.env` are correct
- Verify the database exists

### Port Already in Use
- Change the port in `.env` file or docker-compose.yml
- Or stop the service using port 8000

### Import Errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.11+)

### Docker Issues
- Make sure Docker Desktop is running
- Try: `docker-compose down` then `docker-compose up --build`
- Check logs: `docker-compose logs`

## Project Structure

```
kaban-backend-main/
├── app/
│   ├── __init__.py
│   ├── config.py          # Configuration settings
│   ├── database.py        # Database connection
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas
│   ├── auth.py            # Authentication utilities
│   └── routers/
│       ├── __init__.py
│       ├── auth.py        # Authentication endpoints
│       ├── user.py        # User endpoints
│       ├── projects.py    # Project endpoints
│       ├── sections.py    # Section endpoints
│       └── tasks.py       # Task endpoints
├── main.py                # FastAPI application entry point
├── requirements.txt       # Python dependencies
├── docker-compose.yml     # Docker configuration
├── Dockerfile             # Docker image definition
├── .env.example           # Environment variables template
├── .gitignore            # Git ignore rules
└── SETUP.md              # This file
```

## Notes

- The database schema is automatically created when the application starts (via SQLAlchemy)
- All passwords are hashed using bcrypt
- JWT tokens are used for authentication
- CORS is enabled for all origins (change in production)




