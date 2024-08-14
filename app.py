
# from us_visa.pipeline.training_pipeline import TrainingPipeline
from us_visa.pipeline.prediction_pipeline import PredictionPipeline

# training_pipeline = TrainingPipeline()

# training_pipeline.initiate_training()

prediction_pipeline  = PredictionPipeline()
prediction = prediction_pipeline.initiate_prediction(case_id='EZYV53',
                                        continent='Asia',
                                        education_of_employee="Bachelor's",
                                        has_job_experience='N',
                                        requires_job_training='N',
                                        no_of_employees=1647,
                                        yr_of_estab=1998,
                                        region_of_employment='Midwest',
                                        prevailing_wage=115014.05,
                                        unit_of_wage='Year',
                                        full_time_position='Y',)

print(prediction)