from fastapi import APIRouter ,Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from config.database import get_db



# router = APIRouter()
router = APIRouter(prefix="/health-report", tags=["Appointment"])


@router.post('/')
def create_health_report():
    return {"message":"health-report Created"}


@router.get('/')
def get_health_report_list(db: Session = Depends(get_db)):
    return JSONResponse(content={"message":"get health-report lists"})

@router.get("/:id")
def get_health_report_by_id(id: int):
    return {"message": f"health-report with ID {id} retrieved"}
@router.put("/:id")
def update_health_report(id: int):
    return {"message": f"health-report with ID {id} updated"}