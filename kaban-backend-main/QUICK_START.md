# Quick Start Guide

## 🚀 Fastest Way to Get Started

### 1. Copy environment file
```bash
# Windows PowerShell
Copy-Item env.example .env

# Linux/Mac
cp env.example .env
```

### 2. Edit `.env` file
Set a strong `SECRET_KEY` (any random string)

### 3. Start with Docker
```bash
docker-compose up --build
```

That's it! The API is now running at http://localhost:8000

## 📝 First Steps

### 1. Register a user
```bash
POST http://localhost:8000/auth/register
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}
```

### 2. Create a team
```bash
POST http://localhost:8000/teams
Authorization: Bearer YOUR_ACCESS_TOKEN
{
  "name": "My Team"
}
```

### 3. Create a project
```bash
POST http://localhost:8000/projects
Authorization: Bearer YOUR_ACCESS_TOKEN
{
  "name": "My Project",
  "description": "Project description",
  "team_id": 1
}
```

### 4. View the board
```bash
GET http://localhost:8000/projects/1/board
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## 🔍 Explore the API

Visit http://localhost:8000/docs for interactive API documentation where you can test all endpoints directly!




