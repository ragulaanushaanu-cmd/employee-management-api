from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import engine, get_db, Base
from database_models import Employee
from models import EmployeeCreate, EmployeeResponse

app = FastAPI()

# Create tables (OK for learning projects)
Base.metadata.create_all(bind=engine)


@app.get("/")
def greet():
    return {"message": "Welcome to FastAPI Employee Management API"}


# GET ALL EMPLOYEES
@app.get("/employees", response_model=List[EmployeeResponse])
def get_all_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()


# GET EMPLOYEE BY ID
@app.get("/employees/{id}", response_model=EmployeeResponse)
def get_employee_by_id(id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == id).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    return employee


# CREATE EMPLOYEE
@app.post("/employees", response_model=EmployeeResponse, status_code=201)
def add_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    new_employee = Employee(
        name=employee.name,
        department=employee.department,
        salary=employee.salary,
        experience=employee.experience
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee


# UPDATE EMPLOYEE
@app.put("/employees/{id}", response_model=EmployeeResponse)
def update_employee(id: int, employee: EmployeeCreate, db: Session = Depends(get_db)):
    existing_employee = db.query(Employee).filter(Employee.id == id).first()

    if not existing_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    existing_employee.name = employee.name
    existing_employee.department = employee.department
    existing_employee.salary = employee.salary
    existing_employee.experience = employee.experience

    db.commit()
    db.refresh(existing_employee)

    return existing_employee


# DELETE EMPLOYEE
@app.delete("/employees/{id}")
def delete_employee(id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == id).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(employee)
    db.commit()

    return {"message": "Employee deleted successfully"}

    