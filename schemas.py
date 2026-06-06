from pydantic import BaseModel, EmailStr

# CREATE REQUEST
class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    department: str
    salary: float


# RESPONSE MODEL
class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    department: str
    salary: float

    class Config:
        from_attributes = True