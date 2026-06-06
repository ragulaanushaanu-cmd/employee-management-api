from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, get_db, Base
from database_models import Employee
from models import EmployeeCreate

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def greet():
    return {"message": "Welcome to FastAPI"}


@app.get("/employees")
def get_all_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()


@app.get("/employee/{id}")
def get_employee_by_id(
    id: int,
    db: Session = Depends(get_db)
):
    employee = (
        db.query(Employee)
        .filter(Employee.id == id)
        .first()
    )

    if employee:
        return employee

    return {"message": "Employee Not Found"}


@app.post("/employee")
def add_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
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


@app.put("/employee/{id}")
def update_employee(
    id: int,
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    existing_employee = (
        db.query(Employee)
        .filter(Employee.id == id)
        .first()
    )

    if not existing_employee:
        return {"message": "Employee Not Found"}

    existing_employee.name = employee.name
    existing_employee.department = employee.department
    existing_employee.salary = employee.salary
    existing_employee.experience = employee.experience

    db.commit()
    db.refresh(existing_employee)

    return existing_employee


@app.delete("/employee/{id}")
def delete_employee(
    id: int,
    db: Session = Depends(get_db)
):
    employee = (
        db.query(Employee)
        .filter(Employee.id == id)
        .first()
    )

    if not employee:
        return {"message": "Employee Not Found"}

    db.delete(employee)
    db.commit()

    return {"message": "Employee Deleted Successfully"}

    