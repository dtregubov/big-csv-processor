# big-csv-processor
Read, process, write big .csv files - FastAPI, Celery, Pandas

## How to set up the project
1) Clone the repository from GitHub
2) Open project directory
3) Write next command in Terminal:
   1) ```pipenv --python 3.10```
   2) ```pipenv shell```
   3) ```pip install pipenv```
4) Configure your interpreter in IDE
5) Use command ```pipenv update``` to lock and sync dependencies

## How to run

#### Start the Celery worker:
```bash
celery -A main.celery worker --loglevel=info
```

#### Run the FastAPI server:
```bash
uvicorn main:app --reload
```

## How to try

#### Upload a File Using curl
```bash
curl -X POST "http://127.0.0.1:8000/process-file/" -H "Content-Type: application/json" -d '{"file_path": "/Users/hedin/PycharmProjects/big-csv-processor/uploads/example_input_file.csv"}'
```
For running this command on another machine, you should change path to yours

#### Download the Result
```bash
curl "http://127.0.0.1:8000/download-result/e028042c-9cd5-4b00-abf4-d948b79e7461"
```
For downloading this info properly, you need to get a task_id from the first curl and change the last part of curl to your task_id