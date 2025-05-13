from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Modelo de dados
class Patient(BaseModel):
    id: int
    name: str
    age: int
    condition: Optional[str] = None

# Simulando banco de dados em memória
patients_db = {}

# GET / 
@app.get("/")
def read_root():
    return {"message": "Welcome to the Medical API"}

# GET /medical/patients
@app.get("/medical/patients", response_model=List[Patient])
def get_patients():
    return list(patients_db.values())

# GET /medical/patients/{id}
@app.get("/medical/patients/{id}", response_model=Patient)
def get_patient(id: int):
    if id not in patients_db:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patients_db[id]

# POST /medical/patients
@app.post("/medical/patients", response_model=Patient)
def create_patient(patient: Patient):
    if patient.id in patients_db:
        raise HTTPException(status_code=400, detail="Patient already exists")
    patients_db[patient.id] = patient
    return patient

# PUT /medical/patients
@app.put("/medical/patients", response_model=Patient)
def update_patient(patient: Patient):
    if patient.id not in patients_db:
        raise HTTPException(status_code=404, detail="Patient not found")
    patients_db[patient.id] = patient
    return patient

# DELETE /medical/patients/{id}
@app.delete("/medical/patients/{id}")
def delete_patient(id: int):
    if id not in patients_db:
        raise HTTPException(status_code=404, detail="Patient not found")
    del patients_db[id]
    return {"message": "Patient deleted"}

# GET /medical/patients/find (simulado)
@app.get("/medical/patients/find", response_model=List[Patient])
def find_patients(name: Optional[str] = None):
    if name:
        return [p for p in patients_db.values() if name.lower() in p.name.lower()]
    return list(patients_db.values())
