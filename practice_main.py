from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db, engine
import database_models
from practice_models import Employee as EmployeeSchema

app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return {"message": "Welcome to FastAPI"}

@app.get("/employees")
def get_all_employees(db: Session = Depends(get_db)):
    return db.query(database_models.Employee).all()

@app.get("/employee/{id}")
def get_employee_by_id(id: int, db: Session = Depends(get_db)):
    employee = db.query(database_models.Employee).filter(
        database_models.Employee.id == id
    ).first()

    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    return employee

@app.post("/employee")
def add_employee(employee: EmployeeSchema, db: Session = Depends(get_db)):
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee

@app.put("/employee")
def update_employee(id: int, employee: EmployeeSchema, db: Session = Depends(get_db)):
    db_employee = db.query(database_models.Employee).filter(database_models.Employee.id == id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    for key, value in employee.dict().items():
        setattr(db_employee, key, value)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@app.delete("/employee")
def delete_employee(id: int, db: Session = Depends(get_db)):
    db_employee = db.query(database_models.Employee).filter(database_models.Employee.id == id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(db_employee)
    db.commit()
    return {"message": "Employee deleted successfully"}

#find high salary employees
@app.get("/employees/high_salary")
def get_employee_by_salary(db: Session = Depends(get_db)):
    result = []
    for employee in employees:
        if employee.salary > 45000:
            result.append(employee)
    if result:
        return result
    return "employee not found"
#find employee by department


# Assuming 'employees' is a list of objects defined elsewhere
@app.get("/employee/department/{department}")
def get_employee_by_department(department: str):
    result = []
    for employee in employees:
        # Using dictionary lookup or object attribute depending on your data structure
        if employee.department == department:
            result.append(employee)
            
    if len(result) > 0:
        return result
        
#     # Properly raise a 404 error instead of returning a string
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND, 
#         detail=f"No employees found in the {department} department"
#     )