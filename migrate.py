import json
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from api_app.model import (
    Base,
    Entry,
    Skill,
)

JSON_DATETIME_FORMAT = "%m/%d/%Y %I:%M %p"
target_metadata = Base.metadata

with open("planning.json", "rt", encoding="utf-8") as read_content:
    loaded_data = json.load(read_content)

engine = create_engine("sqlite:///local_database.db", future=True)

added_skills = []

with Session(engine) as session:

    for json_entry in loaded_data:
        entry = Entry(
            id=json_entry["id"],
            original_id=json_entry["originalId"],
            talent_id=json_entry["talentId"],
            talent_name=json_entry["talentName"],
            talent_grade=json_entry["talentGrade"],
            booking_grade=json_entry["bookingGrade"],
            operating_unit=json_entry["operatingUnit"],
            office_city=json_entry["officeCity"],
            office_postal_code=json_entry["officePostalCode"],
            job_manager_name=json_entry["jobManagerName"],
            job_manager_id=json_entry["jobManagerId"],
            total_hours=json_entry["totalHours"],
            start_date=datetime.strptime(json_entry["startDate"], JSON_DATETIME_FORMAT),
            end_date=datetime.strptime(json_entry["endDate"], JSON_DATETIME_FORMAT),
            client_name=json_entry["clientName"],
            client_id=json_entry["clientId"],
            industry=json_entry["industry"],
            is_unassigned=json_entry["isUnassigned"],
        )
        session.add(entry)

        for required_skill in json_entry["requiredSkills"]:
            skill = [
                added_skill
                for added_skill in added_skills
                if added_skill.name == required_skill["name"]
                and added_skill.category == required_skill["category"]
            ]
            if len(skill) > 0:
                skill = skill[0]
            else:
                skill = Skill(
                    name=required_skill["name"], category=required_skill["category"]
                )
                session.add(skill)
                added_skills.append(skill)

            entry.required_skills.append(skill)

        for optional_skill in json_entry["optionalSkills"]:
            skill = [
                added_skill
                for added_skill in added_skills
                if added_skill.name == optional_skill["name"]
                and added_skill.category == optional_skill["category"]
            ]
            if len(skill) > 0:
                skill = skill[0]
            else:
                skill = Skill(
                    name=optional_skill["name"], category=optional_skill["category"]
                )
                session.add(skill)
                added_skills.append(skill)

            entry.optional_skills.append(skill)

    session.commit()
