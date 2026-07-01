from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict

app = FastAPI()

# Modelo de dados
class Patient(BaseModel):
    id: int
    name: str
    age: int
    condition: Optional[str] = None


# Modelo padrão de retorno
class PatientResponse(BaseModel):
    message: str
    data: Optional[Patient] = None


class PatientsListResponse(BaseModel):
    message: str
    data: List[Patient]


# Simulando banco de dados em memória
patients_db: Dict[int, Patient] = {}


# GET /
@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Medical API",
        "status": "running"
    }


# GET /medical/patients
@app.get("/medical/patients", response_model=PatientsListResponse)
def get_patients():
    return {
        "message": "Patients listed successfully",
        "data": list(patients_db.values())
    }


# GET /medical/patients/{id}
@app.get("/medical/patients/{id}", response_model=PatientResponse)
def get_patient(id: int):
    if id not in patients_db:
        raise HTTPException(status_code=404, detail="Patient not found")

    return {
        "message": "Patient found successfully",
        "data": patients_db[id]
    }


# POST /medical/patients
@app.post("/medical/patients", response_model=PatientResponse, status_code=201)
def create_patient(patient: Patient):
    if patient.id in patients_db:
        raise HTTPException(status_code=400, detail="Patient already exists")

    patients_db[patient.id] = patient

    return {
        "message": "Patient created successfully",
        "data": patient
    }


# PUT /medical/patients
@app.put("/medical/patients", response_model=PatientResponse)
def update_patient(patient: Patient):
    if patient.id not in patients_db:
        raise HTTPException(status_code=404, detail="Patient not found")

    patients_db[patient.id] = patient

    return {
        "message": "Patient updated successfully",
        "data": patient
    }


# DELETE /medical/patients/{id}
@app.delete("/medical/patients/{id}")
def delete_patient(id: int):
    if id not in patients_db:
        raise HTTPException(status_code=404, detail="Patient not found")

    deleted_patient = patients_db[id]
    del patients_db[id]

    return {
        "message": "Patient deleted successfully",
        "data": deleted_patient
    }


# GET /medical/patients/find
@app.get("/medical/patients/find", response_model=PatientsListResponse)
def find_patients(name: Optional[str] = None):
    if name:
        result = [
            p for p in patients_db.values()
            if name.lower() in p.name.lower()
        ]

        return {
            "message": "Patients filtered successfully",
            "data": result
        }

    return {
        "message": "Patients listed successfully",
        "data": list(patients_db.values())
    }