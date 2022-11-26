# Backend Coding Challenge

At aspaara a squad of superheroes works on giving superpowers to planning teams.
Through our product dashboard, we give insights into data – a true super-vision
superpower. Join forces with us and build a dashboard of the future!

![aspaara superhero](aspaara_superhero.png)

## Goal

Create a simple backend application that provides an API for a dashboard which
allows a planner to get insights into client and planning information.

You will find the corresponding data that needs to be imported into the database
in `planning.json`, which contains around 10k records.

## Requirements

1. Create proper database tables that can fit the data model.
2. Create a script that imports the data into the database (sqlite).
3. Create REST APIs to get the planning data from the database.
    1. The APIs don't need to be complete, just create what you can in the
       available time.
    2. Please include at least one example on how to do each of the following:
        1. pagination
        2. sorting
        3. filtering / searching

## Data Model

* ID: integer (unique, required)
* Original ID: string (unique, required)
* Talent ID: string (optional)
* Talent Name: string (optional)
* Talent Grade: string (optional)
* Booking Grade: string (optional)
* Operating Unit: string (required)
* Office City: string (optional)
* Office Postal Code: string (required)
* Job Manager Name: string (optional)
* Job Manager ID: string (optional)
* Total Hours: float (required)
* Start Date: datetime (required)
* End Date: datetime (required)
* Client Name: string (optional)
* Client ID: string (required)
* Industry: string (optional)
* Required Skills: array of key-value pair (optional)
* Optional Skills: array of key-value pair (optional)
* Is Unassigned: boolean

## Preferred Tech Stack

* Python 3.8+
* FastAPI
* SQLAlchemy

## Submission

* Please fork the project, commit and push your implementation and add
  `sundara.amancharla@aspaara.com` as a contributor.
* Please update the README with any additional details or steps that are
  required to run your implementation.
* We understand that there is a limited amount of time, so it does not have to
  be perfect or 100% finished. Plan to spend no more than 2-3 hours on it.

For any additional questions on the task please feel free to email
`sundara.amancharla@aspaara.com`.


## Assignment submission

- There are two endpoints implemented. One is simple - to get data by id. Another complex to get multiple results, which are sorted, filtered etc.
- By the look of the source data provided it seems like other tables may be created for talent, job manager, client etc. I decided to keep the database structure flat - corresponding to data model above as I was not sure whether this should be part of the task.
- I've not worked with FastAPI before - I have experience with Flask, so the implementation is probably more in a "Flask" way than in "FastAPI" way.
- Database is accessed through SQLAlchemy with Alembic versioning
- Source code is formatted by black

## Set up and run
Required python version >3.10 - due to type hints for FastAPI

1) Create virtual environment
   - `python -m virtualenv .venv`
2) install required packages
   - `pip install -Ur requirements.txt`
3) Set up DB
   - `alembic upgrade head`
4) Import data from JSON file
   - `python migrate.py`
5) Run app
   - `uvicorn api_app.main:app --reload`

### Examples
- Get single entry by id
  - `http://127.0.0.1:8000/v1/entries/`

- Get multiple entries, second page, with changed page size to 40 (default is 10)
  - `http://127.0.0.1:8000/v1/entries/?page=2&page_size=40`

- Filter by clients name, only newer than 2023-01-01
  - `http://127.0.0.1:8000/v1/entries/?client_name=ruppert&date_from=2023-01-01`

- Sort by entries starting furthest in the future
  - `http://127.0.0.1:8000/v1/entries/?order_by=start_date&descending=True`

- Return only entries with specific skill
  - `127.0.0.1:8000/v1/entries/?required_skills=javascript`

- Don't query skills (query speed up)
  - `http://127.0.0.1:8000/v1/entries/?omit_skills=True`


### NICE TO HAVE - but not really required
- check JSON input data
- proper project structure
- tests
- .env with configuration for database etc.
- wrap in docker image
- flake8