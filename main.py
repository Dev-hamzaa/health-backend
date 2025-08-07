from fastapi import FastAPI
from config.database import Base, engine
from app.routes import router as app_router

app = FastAPI(
    title="Hospital Management API",
    version="1.0.0"
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include all app routes
app.include_router(app_router)
