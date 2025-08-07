# services/appointment_service.py
from sqlalchemy.orm import Session
from app.models import Appointment
from app.schema.appointment import AppointmentCreate, AppointmentUpdate


def get_all_appointments(db: Session):
    return db.query(Appointment).all()


def get_appointment(db: Session, appointment_id: int):
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()


def create_appointment(db: Session, appointment_data: AppointmentCreate):
    new_appointment = Appointment(**appointment_data.dict())
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment


def update_appointment(db: Session, appointment_id: int, update_data: AppointmentUpdate):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if appointment:
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(appointment, key, value)
        db.commit()
        db.refresh(appointment)
    return appointment


def delete_appointment(db: Session, appointment_id: int):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if appointment:
        db.delete(appointment)
        db.commit()
    return appointment
