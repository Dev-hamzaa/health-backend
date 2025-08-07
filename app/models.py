from sqlalchemy import Column, Integer, String, Date, DateTime, Text, ForeignKey, Boolean, JSON, DECIMAL
from sqlalchemy.orm import relationship
from config.database import Base
from datetime import datetime

# ========== PATIENT ==========
class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    dob = Column(Date)
    email = Column(String(100), unique=True)
    phone = Column(String(15))
    gender = Column(String(10))
    about = Column(Text, nullable=True)
    emergency_contact = Column(String(15))
    medicalRecordNo = Column(String(50), unique=True)
    address = Column(Text)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))

    doctor = relationship("Doctor", back_populates="patients")

# ========== DOCTOR ==========
class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    specialty = Column(String(100))
    contact = Column(String(15))
    profilePhoto = Column(String, nullable=True)
    about = Column(Text, nullable=True)
    experience = Column(JSON)
    email = Column(String(100), unique=True)
    address = Column(Text)
    available = Column(Boolean, default=True)

    patients = relationship("Patient", back_populates="doctor")
    appointments = relationship("Appointment", back_populates="doctor")
    treatments = relationship("Treatment", secondary="treatment_doctor_association", back_populates="doctors")

# ========== APPOINTMENT ==========
class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    scheduledAt = Column(DateTime)
    status = Column(String(50))
    notes = Column(Text)

    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    patient_id = Column(Integer, ForeignKey("patients.id"))

    doctor = relationship("Doctor", back_populates="appointments")
    patient = relationship("Patient")
    treatments = relationship("Treatment", back_populates="appointment")

# ========== SURGERY PERFORMED ==========
class SurgeryPerformed(Base):
    __tablename__ = "surgeries_performed"

    id = Column(Integer, primary_key=True)
    surgeryType = Column(String(100))
    performedAt = Column(DateTime)
    room = Column(String(50))
    notes = Column(Text, nullable=True)

    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    patient_id = Column(Integer, ForeignKey("patients.id"))

# ========== SURGERY SCHEDULE ==========
class SurgerySchedule(Base):
    __tablename__ = "surgery_schedules"

    id = Column(Integer, primary_key=True)
    surgeryType = Column(String(100))
    scheduledAt = Column(DateTime)
    room = Column(String(50))

    doctor_id = Column(Integer, ForeignKey("doctors.id"))

# ========== TREATMENT ==========
from sqlalchemy import Table

# Association table for many-to-many between Treatment and Doctor
treatment_doctor_association = Table(
    "treatment_doctor_association",
    Base.metadata,
    Column("treatment_id", Integer, ForeignKey("treatments.id")),
    Column("doctor_id", Integer, ForeignKey("doctors.id"))
)

class Treatment(Base):
    __tablename__ = "treatments"

    id = Column(Integer, primary_key=True)
    treatmentType = Column(String(100))
    about = Column(Text)
    category = Column(String(100))
    date = Column(DateTime, default=datetime.utcnow)

    appointment_id = Column(Integer, ForeignKey("appointments.id"))
    patient_id = Column(Integer, ForeignKey("patients.id"))

    appointment = relationship("Appointment", back_populates="treatments")
    patient = relationship("Patient")
    doctors = relationship("Doctor", secondary=treatment_doctor_association, back_populates="treatments")

# ========== REVIEW ==========
class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    rating = Column(Integer)
    comment = Column(Text, nullable=True)

    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    treatment_id = Column(Integer, ForeignKey("treatments.id"))
    patient_id = Column(Integer, ForeignKey("patients.id"))

    createdAt = Column(DateTime, default=datetime.utcnow)

# ========== PAYMENT ==========
class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    amount = Column(DECIMAL(10, 2))
    paidAt = Column(DateTime)
    method = Column(String(50))
    status = Column(String(50))

    patient_id = Column(Integer, ForeignKey("patients.id"))
    treatment_id = Column(Integer, ForeignKey("treatments.id"), nullable=True)

# ========== MESSAGE ==========
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    content = Column(Text)
    sentAt = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50))
    senderType = Column(String(20))
    senderId = Column(Integer)
    receiverType = Column(String(20))
    receiverId = Column(Integer)

# ========== ADMIN USER ==========
class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    role = Column(String(50))
    passwordHash = Column(String(255))

# ========== MEDICATION ==========
class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    dosage = Column(String(50))
    alergy = Column(JSON)
    frequency = Column(String(50))
    prescribedAt = Column(DateTime)

    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))

# ========== HEALTH REPORT ==========
class HealthReport(Base):
    __tablename__ = "health_reports"

    id = Column(Integer, primary_key=True)
    reportType = Column(String(100))
    description = Column(Text, nullable=True)
    filePath = Column(String)
    uploadedAt = Column(DateTime, default=datetime.utcnow)

    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))

# ========== VITAL STATS ==========
class VitalStat(Base):
    __tablename__ = "vital_stats"

    id = Column(Integer, primary_key=True)
    temperature = Column(Integer)
    heart_rate = Column(Integer)
    blood_pressure_systolic = Column(Integer)
    blood_pressure_diastolic = Column(Integer)
    respiratory_rate = Column(Integer)
    recorded_at = Column(DateTime, default=datetime.utcnow)

    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=True)

    patient = relationship("Patient", backref="vital_stats")
