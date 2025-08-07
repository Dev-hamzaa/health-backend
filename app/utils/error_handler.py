from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

app = FastAPI()

async def handle_integrity_error(request: Request, exc: IntegrityError):
    error_msg = str(exc.orig)

    # Duplicate key (unique constraint)
    if "duplicate key value violates unique constraint" in error_msg:
        if 'constraint "' in error_msg:
            constraint_name = error_msg.split('constraint "')[1].split('"')[0]
            if "_" in constraint_name:
                field = constraint_name.split("_")[1]
            else:
                field = "field"
            return JSONResponse(
                status_code=400,
                content={
                    "message": f"A record with this {field} already exists."}
            )

    # NOT NULL constraint failed
    elif "null value in column" in error_msg and "violates not-null constraint" in error_msg:
        column = error_msg.split("null value in column \"")[1].split("\"")[0]
        return JSONResponse(
            status_code=400,
            content={"message": f"Field '{column}' is required."}
        )

    # Foreign key constraint
    elif "violates foreign key constraint" in error_msg:
        constraint = error_msg.split("constraint ")[-1].split("\n")[0]
        return JSONResponse(
            status_code=400,
            content={"message": f"Invalid reference: {constraint}"}
        )

    # Fallback
    return JSONResponse(
        status_code=400,
        content={"message": "Database integrity error"}
    )




# Handle all uncaught exceptions
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "message": str(exc)}
    )