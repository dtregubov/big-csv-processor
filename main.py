from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
from celery import Celery
import os
import uuid
import dask.dataframe as dd
from pydantic import BaseModel


app = FastAPI()

# Configure Celery
celery = Celery(__name__, broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

# Define prefix and directory for result
RESULT_FILE_PREFIX = '_example_output_file.csv'
RESULTS_DIR = os.path.join(os.getcwd(), 'results')

# Create directory if it does not exist
os.makedirs(RESULTS_DIR, exist_ok=True)


# pydantic class for file path, can be extended with file url, for example, to support other formats
class FileSource(BaseModel):
    file_path: str


@app.post("/process-file/")
async def schedule_file_for_processing(file_source: FileSource, background_tasks: BackgroundTasks):
    path_to_file = file_source.file_path

    # Generate a unique task ID
    task_id = str(uuid.uuid4())

    # Schedule the processing task
    background_tasks.add_task(process_file_task, path_to_file, task_id)

    return {'task_id': task_id}


@app.get('/download-result/{task_id}')
async def download_result(task_id: str):
    file_name = f'{task_id}{RESULT_FILE_PREFIX}'
    # Check if the result file exists
    result_path = os.path.join(RESULTS_DIR, file_name)
    if os.path.exists(result_path):
        return FileResponse(result_path, media_type='text/csv', filename=file_name)
    else:
        return {'status': 'Processing'}


@celery.task
def process_file_task(file_url, task_id):
    output_path = os.path.join(RESULTS_DIR, f'{task_id}{RESULT_FILE_PREFIX}')
    process_large_csv(file_url, output_path)


# The process_large_csv function from the first part of the task
def process_large_csv(path_to_file, output_file):
    # Read the CSV file in chunks using Dask
    df = dd.read_csv(path_to_file)

    # Group by "Song" and "Date" and sum the "Number of Plays"
    result = df.groupby(['Song', 'Date']).sum().reset_index()

    # Write the result to output file. In this case it's CSV, but we can use s3 for example
    result.to_csv(output_file, single_file=True, index=False)
