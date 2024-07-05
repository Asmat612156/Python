from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pickle
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the ML model
try:
    model = pickle.load(open('./Model/ML_Model.pkl', 'rb'))
except Exception as e:
    logger.error(f"Error loading the model: {e}")
    raise

# Database setup
DATABASE_URL = 'postgresql://postgres:abc123@localhost:5432/loan_applications'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class LoanApplication(Base):
    __tablename__ = 'loan_applications'
    id = Column(Integer, primary_key=True, index=True)
    account_no = Column(String, unique=True, index=True)
    full_name = Column(String)
    gender = Column(String)
    marital_status = Column(String)
    dependents = Column(String)
    education = Column(String)
    employment_status = Column(String)
    property_area = Column(String)
    credit_score = Column(String)
    monthly_income = Column(Float)
    co_monthly_income = Column(Float)
    loan_amount = Column(Float)
    loan_duration = Column(Integer)

# Use inspect to check if the table exists
inspector = inspect(engine)
if not inspector.has_table('loan_applications'):
    Base.metadata.create_all(bind=engine)

# Pydantic model for request validation
class LoanApplicationRequest(BaseModel):
    account_no: str
    full_name: str
    gender: int
    marital_status: int
    dependents: int
    education: int
    employment_status: int
    property_area: int
    credit_score: int
    monthly_income: float
    co_monthly_income: float
    loan_amount: float
    loan_duration: int

app = FastAPI()

@app.post("/predict")
def predict_loan(request: LoanApplicationRequest):
    # Mapping form indices to display values
    gen_display = ['Female', 'Male']
    mar_display = ['No', 'Yes']
    dep_display = ['No', 'One', 'Two', 'More than Two']
    edu_display = ['Not Graduate', 'Graduate']
    emp_display = ['Job', 'Business']
    prop_display = ['Rural', 'Semi-Urban', 'Urban']
    cred_display = ['Between 300 to 500', 'Above 500']
    dur_display = [60, 180, 240, 360, 480]

    # Convert duration index to actual duration in months
    duration = dur_display[request.loan_duration]

    # Prepare features for prediction
    features = np.array([[request.gender, request.marital_status, request.dependents, 
                          request.education, request.employment_status, request.monthly_income, 
                          request.co_monthly_income, request.loan_amount, duration, 
                          request.credit_score, request.property_area]])

    # Make prediction
    try:
        prediction = model.predict(features)
    except Exception as e:
        logger.error(f"Error making prediction: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed")

    result = int(prediction[0])

    # Create a new loan application record
    loan_application = LoanApplication(
        account_no=request.account_no,
        full_name=request.full_name,
        gender=gen_display[request.gender],
        marital_status=mar_display[request.marital_status],
        dependents=dep_display[request.dependents],
        education=edu_display[request.education],
        employment_status=emp_display[request.employment_status],
        property_area=prop_display[request.property_area],
        credit_score=cred_display[request.credit_score],
        monthly_income=request.monthly_income,
        co_monthly_income=request.co_monthly_income,
        loan_amount=request.loan_amount,
        loan_duration=duration
    )

    # Save the record to the database
    db = SessionLocal()
    try:
        db.add(loan_application)
        db.commit()
        db.refresh(loan_application)
    except Exception as e:
        logger.error(f"Error saving loan application to the database: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to save loan application")
    finally:
        db.close()

    # Return the prediction result
    if result == 0:
        return {"message": f"Hello: {request.full_name} || Account number: {request.account_no} || According to our calculations, you will not get the loan from the bank."}
    else:
        return {"message": f"Hello: {request.full_name} || Account number: {request.account_no} || Congratulations!! You will get the loan from the bank."}
