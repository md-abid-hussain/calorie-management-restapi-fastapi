# SUBMISSION

## Setting up project

- Clone this repository
- Install python
- Open terminal
- Install venv for virtual environment using pip `pip install venv`
- Create venv
  - Windows : `py -3 -m venv venv`
  - Mac or Linux : `python3 -m venv venv`
- Activate virtual environment
  - Windows : `venv\Scripts\activate.bat`
  - Mac or Linux : `source venv/bin/activate`
- Install the dependencies using `pip install -r requirements.txt`

## Running tests

Run the test using `pytest -v -s`

## Running the API server

Use the following command in terminal to start the server
`uvicorn app.main:app --reload`

## Creating admin and manager

To create admin and manager run `create_admin_&_manager.py`

## Documentation

After running the sever open `http://127.0.0.1:8000/docs` or `http://127.0.0.1:8000/redoc`
