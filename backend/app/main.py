from fastapi import FastAPI
from sqlmodel import SQLModel
from database import engine
from routes import post_routes  # Import the router from routes

# Create FastAPI app
app = FastAPI(
    title="Minimal Blog API",
    description="A simple blog backend with FastAPI",
    version="1.0.0"
)

# Create database tables
SQLModel.metadata.create_all(engine)

# Include routes
app.include_router(post_routes.router)
