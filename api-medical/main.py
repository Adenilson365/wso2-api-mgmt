from copy import deepcopy
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel


app = FastAPI(
    title="Medical API",
    version="1.0.0",
    description="API para gerenciamento de pacientes",
)


# ========================================
# Modelos
# ========================================

class Patient(BaseModel):
    id: int
    name: str
    age: int
    condition: Optional[str] = None


class PatientResponse(BaseModel):
    message: str
    data: Optional[Patient] = None


class PatientsListResponse(BaseModel):
    message: str
    data: List[Patient]


# Banco de dados em memória
patients_db: Dict[int, Patient] = {}


# ========================================
# Conversão OpenAPI 3.1 para OpenAPI 3.0
# ========================================

def convert_nullable_schema(value: Any) -> Any:
    """
    Converte estruturas OpenAPI 3.1 como:

        anyOf:
          - type: string
          - type: null

    para o formato OpenAPI 3.0:

        type: string
        nullable: true
    """

    if isinstance(value, list):
        return [convert_nullable_schema(item) for item in value]

    if not isinstance(value, dict):
        return value

    converted = {
        key: convert_nullable_schema(item)
        for key, item in value.items()
    }

    any_of = converted.get("anyOf")

    if isinstance(any_of, list):
        non_null_schemas = [
            schema
            for schema in any_of
            if not (
                isinstance(schema, dict)
                and schema.get("type") == "null"
            )
        ]

        has_null = len(non_null_schemas) != len(any_of)

        if has_null and len(non_null_schemas) == 1:
            base_schema = deepcopy(non_null_schemas[0])

            for key, item in converted.items():
                if key != "anyOf":
                    base_schema[key] = item

            base_schema["nullable"] = True
            return base_schema

    return converted


def create_wso2_openapi() -> Dict[str, Any]:
    schema = get_openapi(
        title="Medical API",
        version="1.0.0",
        description="API para gerenciamento de pacientes",
        routes=app.routes,
    )

    schema = convert_nullable_schema(schema)
    schema["openapi"] = "3.0.3"

    return schema


@app.get(
    "/openapi-wso2.json",
    include_in_schema=False,
)
def openapi_for_wso2():
    return create_wso2_openapi()


# ========================================
# Recursos da API
# ========================================

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Medical API",
        "status": "running",
    }


@app.get(
    "/medical/patients",
    response_model=PatientsListResponse,
)
def get_patients():
    return {
        "message": "Patients listed successfully",
        "data": list(patients_db.values()),
    }


@app.post(
    "/medical/patients",
    response_model=PatientResponse,
    status_code=201,
)
def create_patient(patient: Patient):
    if patient.id in patients_db:
        raise HTTPException(
            status_code=400,
            detail="Patient already exists",
        )

    patients_db[patient.id] = patient

    return {
        "message": "Patient created successfully",
        "data": patient,
    }


@app.put(
    "/medical/patients",
    response_model=PatientResponse,
)
def update_patient(patient: Patient):
    if patient.id not in patients_db:
        raise HTTPException(
            status_code=404,
            detail="Patient not found",
        )

    patients_db[patient.id] = patient

    return {
        "message": "Patient updated successfully",
        "data": patient,
    }


# A rota estática precisa ficar antes da rota /{id}
@app.get(
    "/medical/patients/find",
    response_model=PatientsListResponse,
)
def find_patients(name: Optional[str] = None):
    if name:
        result = [
            patient
            for patient in patients_db.values()
            if name.lower() in patient.name.lower()
        ]

        return {
            "message": "Patients filtered successfully",
            "data": result,
        }

    return {
        "message": "Patients listed successfully",
        "data": list(patients_db.values()),
    }


@app.get(
    "/medical/patients/{id}",
    response_model=PatientResponse,
)
def get_patient(id: int):
    if id not in patients_db:
        raise HTTPException(
            status_code=404,
            detail="Patient not found",
        )

    return {
        "message": "Patient found successfully",
        "data": patients_db[id],
    }


@app.delete(
    "/medical/patients/{id}",
    response_model=PatientResponse,
)
def delete_patient(id: int):
    if id not in patients_db:
        raise HTTPException(
            status_code=404,
            detail="Patient not found",
        )

    deleted_patient = patients_db.pop(id)

    return {
        "message": "Patient deleted successfully",
        "data": deleted_patient,
    }