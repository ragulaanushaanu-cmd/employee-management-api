from pydantic import BaseModel

class EmployeeCreate(BaseModel):
    name: str
    department: str
    salary: float
    experience: int

class EmployeeResponse(EmployeeCreate):
    id: int

    class Config:
        from_attributes = True

