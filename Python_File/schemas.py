from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class UserBase(BaseModel):
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserRead(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime

    class Config:
        orm_mode = True


class PatientBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: str
    gender: Optional[str] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None


class PatientCreate(PatientBase):
    pass


class PatientRead(PatientBase):
    id: int
    created_at: datetime
    created_by_id: int

    class Config:
        orm_mode = True


class AppointmentBase(BaseModel):
    patient_id: int
    scheduled_time: datetime
    reason: str


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentRead(AppointmentBase):
    id: int
    status: str
    created_at: datetime
    created_by_id: int

    class Config:
        orm_mode = True


class MedicalRecordBase(BaseModel):
    patient_id: int
    record_type: str
    description: str


class MedicalRecordCreate(MedicalRecordBase):
    pass


class MedicalRecordRead(MedicalRecordBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class HealthCheckResponse(BaseModel):
    status: str = "ok"
    message: str = "Healthcare backend is running"


class AuthDetails(BaseModel):
    email: EmailStr
    password: str
