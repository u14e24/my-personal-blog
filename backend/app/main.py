from fastapi import FastAPI
from sqlmodel import SQLModel
from app.database import engine
from app.routes import post_routes
from app.routes import user_routes  # Import the router from routes

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
app.include_router(user_routes.users_router)
app.include_router(user_routes.auth_router)