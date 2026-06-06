from pydantic import BaseModel

# INPUT MODEL
class EmployeeCreate(BaseModel):
    name: str
    department: str
    salary: float
    experience: int


# OUTPUT MODEL
class EmployeeResponse(BaseModel):
    id: int
    name: str
    department: str
    salary: float
    experience: int

    class Config:
        from_attributes = True

