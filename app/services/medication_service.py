from app.schema import medication_schema as MedicationSchema
from sqlalchemy.orm import Session
from app.models import Medication




def create_medication(medication:MedicationSchema.MedicationCreate,db:Session):
    new_medication = Medication(**medication.dict())
    db.add(new_medication)
    db.commit()
    db.refresh(new_medication)
    return new_medication

def get_medication_list(db:Session):
    return db.query(Medication).all()

def get_medication_by_id(medication_id:int, db:Session):
    return db.query(Medication).filter(Medication.id == medication_id).first()

def update_medication(medication_id:int, updated_medication:MedicationSchema.MedicationUpdate, db:Session):
    medication = db.query(Medication).filter(Medication.id == medication_id).first()
    if not medication:
        return None
    if medication:
        update_data = updated_medication.dict(exclude_unset=True)
        for key, value in update_data.items():
          setattr(medication, key, value)
        db.commit()
        db.refresh(medication)
        return medication

