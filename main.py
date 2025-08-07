from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from config.database import Base, engine
from app.routes import router as app_router
from sqlalchemy.exc import IntegrityError
from app.utils.error_handler import handle_integrity_error,generic_exception_handler


app = FastAPI(
    title="Hospital Management API",
    version="1.0.0"
)


# Creation of the Tables in the Database 
Base.metadata.create_all(bind=engine)

# Register Error Handler
app.add_exception_handler(IntegrityError, handle_integrity_error)
app.add_exception_handler(Exception, generic_exception_handler)


# Register Routes
app.include_router(app_router)
