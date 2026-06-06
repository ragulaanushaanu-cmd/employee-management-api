from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import engine, Base, get_db
import models
import schemas

# CREATE TABLES
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Employee Management API")


# ROOT
@app.get("/")
def root():
    return {"message": "Employee Management API is running"}


# CREATE
@app.post("/employees/", response_model=schemas.EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):

    existing = db.query(models.Employee).filter(models.Employee.email == employee.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_emp = models.Employee(**employee.dict())

    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)

    return new_emp


# READ ALL
@app.get("/employees/", response_model=list[schemas.EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):
    return db.query(models.Employee).all()


# READ BY ID
@app.get("/employees/{emp_id}", response_model=schemas.EmployeeResponse)
def get_employee(emp_id: int, db: Session = Depends(get_db)):

    emp = db.query(models.Employee).filter(models.Employee.id == emp_id).first()

    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    return emp


# UPDATE
@app.put("/employees/{emp_id}", response_model=schemas.EmployeeResponse)
def update_employee(emp_id: int, employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):

    emp = db.query(models.Employee).filter(models.Employee.id == emp_id).first()

    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    emp.name = employee.name
    emp.email = employee.email
    emp.department = employee.department
    emp.salary = employee.salary

    db.commit()
    db.refresh(emp)

    return emp


# DELETE
@app.delete("/employees/{emp_id}")
def delete_employee(emp_id: int, db: Session = Depends(get_db)):

    emp = db.query(models.Employee).filter(models.Employee.id == emp_id).first()

    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(emp)
    db.commit()

    return {"message": f"Employee {emp_id} deleted successfully"}

    