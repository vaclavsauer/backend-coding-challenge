import datetime
from enum import Enum

from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from api_app.model import Entry, Skill


class EntryOrder(str, Enum):
    id = "id"
    original_id = "original_id"
    talent_id = "talent_id"
    talent_name = "talent_name"
    talent_grade = "talent_grade"
    booking_grade = "booking_grade"
    operating_unit = "operating_unit"
    office_city = "office_city"
    office_postal_code = "office_postal_code"
    job_manager_name = "job_manager_name"
    job_manager_id = "job_manager_id"
    total_hours = "total_hours"
    start_date = "start_date"
    end_date = "end_date"
    client_name = "client_name"
    client_id = "client_id"
    industry = "industry"
    is_unassigned = "is_unassigned"


engine = create_engine("sqlite:///local_database.db", future=True)

app = FastAPI()


@app.get("/")
async def root():
    """
    Redirect to documentation
    """
    return RedirectResponse(url="/docs")


@app.get("/v1/entries/{entry_id}")
async def read_entry(entry_id: int):
    """
    Return single entry given by its id.
    """
    with Session(engine) as session:

        data = session.query(Entry).where(Entry.id == entry_id).all()

        if len(data) == 0:
            raise HTTPException(status_code=404, detail="Entry not found")

        return {"data": data[0]}


@app.get("/v1/entries/")
async def read_entries(
    page: int = Query(default=1, gt=0, description="Return Nth page."),
    page_size: int = Query(
        default=10, gt=0, lt=50, description="Number of results per page."
    ),
    order_by: EntryOrder = Query(default=EntryOrder.id, description="Result sort key."),
    descending: bool = Query(
        default=False, description="Return results in descending order."
    ),
    omit_skills: bool = Query(
        default=False, description="Omit skills from result for faster response."
    ),
    talent_name: str
    | None = Query(default=None, description="Search for talent by name."),
    job_manager_name: str
    | None = Query(default=None, description="Search for job manager by name."),
    client_name: str
    | None = Query(default=None, description="Search for client by name."),
    date_from: datetime.date
    | None = Query(
        default=None,
        description="Return results newer than given date. Uses format `%Y-%m-%d`",
    ),
    date_to: datetime.date
    | None = Query(
        default=None,
        description="Return results older than given date. Uses format `%Y-%m-%d`",
    ),
    required_skills: list[str]
    | None = Query(default=None, description="Filter by required skills"),
):
    """
    Return multiple entries.
    """

    with Session(engine) as session:

        order_keys = {enum: Entry.__dict__[enum] for enum in EntryOrder}

        if descending:
            order_key = order_keys[order_by].desc()
        else:
            order_key = order_keys[order_by].asc()

        query = session.query(Entry)

        if required_skills is not None and len(required_skills) > 0:
            query = query.join(Skill, Entry.required_skills)
            for required_skill in required_skills:
                # this does not work for multiple skills
                # use group by instead
                query = query.where(Skill.name.like(f"%{required_skill}%"))

        if talent_name is not None:
            query = query.filter(Entry.talent_name.like(f"%{talent_name}%"))
        if job_manager_name is not None:
            query = query.filter(Entry.job_manager_name.like(f"%{job_manager_name}%"))
        if client_name is not None:
            query = query.filter(Entry.client_name.like(f"%{client_name}%"))
        if date_from is not None:
            query = query.filter(Entry.start_date >= date_from)
        if date_to is not None:
            query = query.filter(Entry.end_date <= date_to)

        count = query.count()

        query_data = (
            query.order_by(order_key)
            .slice((page - 1) * page_size, page * page_size)
            .all()
        )

        # Explicit is better than implicit
        response_data = [
            {
                "id": data.id,
                "original_id": data.original_id,
                "talent_id": data.talent_id,
                "talent_name": data.talent_name,
                "talent_grade": data.talent_grade,
                "booking_grade": data.booking_grade,
                "operating_unit": data.operating_unit,
                "office_city": data.office_city,
                "office_postal_code": data.office_postal_code,
                "job_manager_name": data.job_manager_name,
                "job_manager_id": data.job_manager_id,
                "total_hours": data.total_hours,
                "start_date": data.start_date,
                "end_date": data.end_date,
                "client_name": data.client_name,
                "client_id": data.client_id,
                "industry": data.industry,
                "is_unassigned": data.is_unassigned,
                "required_skills": None
                if omit_skills
                else [
                    {"name": skill.name, "category": skill.category}
                    for skill in data.required_skills
                ],
                "optional_skills": None
                if omit_skills
                else [
                    {"name": skill.name, "category": skill.category}
                    for skill in data.optional_skills
                ],
            }
            for data in query_data
        ]

    return {
        "page": page,
        "count": len(response_data),
        "total_count": count,
        "data": response_data,
    }
