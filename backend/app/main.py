from fastapi import FastAPI
from sqlmodel import SQLModel
from app.database import engine
from app.routes import post_routes
from app.routes import user_routes  # Import the router from routes
from app.routes import admin_routes
from datetime import datetime

# TODO: Add CORS middleware for frontend integration (allow_origins=["http://localhost:3000"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
# TODO: Add logging configuration (import logging; logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'); add loggers in routes/services for requests/errors)
# TODO: Add global exception handlers for better error responses (@app.exception_handler(HTTPException) for JSON responses; handle ValidationError, SQLAlchemyError, etc. with custom messages)
# TODO: Consider API versioning (e.g., prefix routes with /v1/ for future breaking changes)

# Create FastAPI app
app = FastAPI(
    title="Minimal Blog API",
    description="A simple blog backend with FastAPI",
    version="1.0.0"
)

# Create database tables
SQLModel.metadata.create_all(engine)

@app.get("/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.utcnow()}

# Include routes
app.include_router(post_routes.router)
app.include_router(user_routes.users_router)
app.include_router(user_routes.auth_router)
app.include_router(admin_routes.admin_router)