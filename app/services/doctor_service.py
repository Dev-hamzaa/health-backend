
from app.schema import doctor_schema as DoctorSchema
from app.models import Doctor
from sqlalchemy.orm import Session

def create_doctor(db:Session,doctor:DoctorSchema.DoctorCreate):
    new_doctor = Doctor(**doctor.dict())
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    return new_doctor

def get_doctor_list(db:Session):
    return db.query(Doctor).all()

def get_doctor_by_id(doctor_id:int,db:Session ):
    return db.query(Doctor).filter(Doctor.id == doctor_id).first()

def update_doctor(doctor_id:int, updated_doctor:DoctorSchema.DoctorUpdate,db:Session):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        return None
    if doctor:
        update_data = updated_doctor.dict(exclude_unset=True)
        for key, value in update_data.items():
          setattr(doctor, key, value)
        db.commit()
        db.refresh(doctor)
        return doctor
    
def delete_doctor(db:Session,doctor_id:int):
    doctor=db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        return None
    if doctor:
        db.delete(doctor)
        db.commit()
        return True
    

