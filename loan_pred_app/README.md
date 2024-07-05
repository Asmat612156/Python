Step 1 :  # Docker Setup
Command "docker version" use to check the installed docker version

Step 2:
Command to run docker container or image (docker run "Image or Container name)

Step 3:
lAUNCH docker container : docker run -it continuumio/anaconda3:latest/bin/bash
 * docke run -it'Image name:latest/bin/bash


 

 Command to run fast API 
    poetry run uvicorn Api.api:app --reload

    poetry run streamlit run ./webapp.py

sampl Payload
    {
  "account_no": "123456",
  "full_name": "Asmat",
  "gender": 1,
  "marital_status": 1,
  "dependents": 2,
  "education": 1,
  "employment_status": 1,
  "property_area": 2,
  "risk_rating_score": 1,
  "monthly_income": 5000.0,
  "co_monthly_income": 2000.0,
  "loan_amount": 100000.0,
  "loan_duration": 3
}
