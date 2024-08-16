from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from uvicorn import run as app_run
from us_visa.constants import APP_HOST, APP_PORT
from us_visa.pipeline.training_pipeline  import TrainingPipeline
from us_visa.pipeline.prediction_pipeline import PredictionPipeline

app = FastAPI()

app.mount("/static",StaticFiles(directory="static"),name="static")

templates = Jinja2Templates(directory="templates")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DataForm:
    def __init__(self, request:Request):
        self.request = request
        self.case_id =None
        self.continent= None
        self.education_of_employee = None
        self.has_job_experience = None
        self.requires_job_training = None
        self.no_of_employees = None
        self.yr_of_estab = None
        self.region_of_employment = None
        self.prevailing_wage = None
        self.unit_of_wage = None
        self.full_time_position = None 
        
    async def get_usvisa_data(self):
        form = await self.request.form()
        self.case_id = form.get("case_id")
        self.continent = form.get("continent")
        self.education_of_employee = form.get("education_of_employee")
        self.has_job_experience = form.get("has_job_experience")
        self.requires_job_training = form.get("requires_job_training")
        self.no_of_employees = form.get("no_of_employees")
        self.yr_of_estab = form.get("company_establish_year")
        self.region_of_employment = form.get("region_of_employment")
        self.prevailing_wage = form.get("prevailing_wage")
        self.unit_of_wage = form.get("unit_of_wage") 
        self.full_time_position = form.get("full_time_position")
        
@app.get("/",tags=['input'])
async def index(request: Request):
        return templates.TemplateResponse(
            "usvisa.html",{"request": request, "context": "Rendering"})   

          

@app.get("/train")
async def trainRouteClient():
    try:
        train_pipeline = TrainingPipeline()
        
        train_pipeline.initiate_training()
        
        return Response("Training successful !!")
    
    except Exception as e:
        return Response(f"Error Occured {e}")
        

@app.post("/")
async def predictionRouteClinet(request: Request):
    try:
        form = DataForm(request)
        await form.get_usvisa_data()
        
        prediciton_pipeline = PredictionPipeline()
        
        prediction = prediciton_pipeline.initiate_prediction(
                case_id=form.case_id,
                continent=form.continent,
                education_of_employee=form.education_of_employee,
                has_job_experience=form.has_job_experience,
                requires_job_training=form.requires_job_training,
                no_of_employees=form.no_of_employees,
                yr_of_estab=form.yr_of_estab,
                region_of_employment=form.region_of_employment,
                prevailing_wage=form.prevailing_wage,
                unit_of_wage=form.unit_of_wage,
                full_time_position=form.full_time_position
        )
        
        return templates.TemplateResponse(
            "usvisa.html",
            {"request": request, "context": prediction},
        )
        
    except Exception as e:
        return {"status": False, "error": f"{e}"}
                         

if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)          
          