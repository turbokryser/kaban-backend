from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, user, teams, projects, sections, tasks
from app.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Kaban X API",
    description="Backend API for Kaban X project management system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(teams.router)
app.include_router(projects.router)
app.include_router(sections.router)
app.include_router(tasks.router)


@app.get("/")
async def root():
    return {
        "message": "Kaban X API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    return {"status": "ok"}

