from pydantic import BaseModel

class Employee(BaseModel):
    id: int
    name: str
    department: str
    salary: int
    experience: int

    class Config:
        from_attributes = True
