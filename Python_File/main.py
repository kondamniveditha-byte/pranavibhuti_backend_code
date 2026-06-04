from datetime import datetime
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import auth
import models
import schemas
from database import Base, engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Healthcare Backend API",
    description="A FastAPI backend for a simple healthcare application with auth, patients, appointments, and medical records.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=schemas.HealthCheckResponse)
def health_check():
    return {"status": "ok", "message": "Healthcare backend is running"}


@app.post("/auth/register", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = models.User(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=auth.get_password_hash(user_in.password),
        is_active=True,
        is_admin=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/auth/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/patients/", response_model=schemas.PatientRead)
def create_patient(
    patient_in: schemas.PatientCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    patient = models.Patient(**patient_in.dict(), created_by_id=current_user.id)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


@app.get("/patients/", response_model=List[schemas.PatientRead])
def list_patients(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    return db.query(models.Patient).offset(skip).limit(limit).all()


@app.get("/patients/{patient_id}", response_model=schemas.PatientRead)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    return patient


@app.post("/appointments/", response_model=schemas.AppointmentRead)
def schedule_appointment(
    appointment_in: schemas.AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    patient = db.query(models.Patient).filter(models.Patient.id == appointment_in.patient_id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    if appointment_in.scheduled_time <= datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Appointment must be scheduled in the future")
    appointment = models.Appointment(
        **appointment_in.dict(),
        created_by_id=current_user.id,
        status="scheduled",
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


@app.get("/appointments/", response_model=List[schemas.AppointmentRead])
def list_appointments(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    return db.query(models.Appointment).offset(skip).limit(limit).all()


@app.post("/records/", response_model=schemas.MedicalRecordRead)
def add_medical_record(
    record_in: schemas.MedicalRecordCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    patient = db.query(models.Patient).filter(models.Patient.id == record_in.patient_id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    record = models.MedicalRecord(**record_in.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@app.get("/records/", response_model=List[schemas.MedicalRecordRead])
def list_medical_records(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    return db.query(models.MedicalRecord).offset(skip).limit(limit).all()
