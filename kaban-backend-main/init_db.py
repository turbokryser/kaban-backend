"""
Database initialization script.
Run this to create all tables if they don't exist.
"""
from app.database import engine, Base
from app.models import User, Team, Desk, Project, Section, Ticket, UserToTeam

if __name__ == "__main__":
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")




