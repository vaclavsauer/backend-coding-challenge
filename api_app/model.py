from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Table,
    DateTime,
    Float,
    Boolean,
)

from sqlalchemy.orm import declarative_base, declared_attr, relationship

Base = declarative_base()


class PublicMixin(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


entry_required_skill_association = Table(
    "entry_required_skill_association",
    Base.metadata,
    Column("entry_id", ForeignKey("entry.id"), primary_key=True),
    Column("skill_id", ForeignKey("skill.id"), primary_key=True),
)

entry_optional_skill_association = Table(
    "entry_optional_skill_association",
    Base.metadata,
    Column("entry_id", ForeignKey("entry.id"), primary_key=True),
    Column("skill_id", ForeignKey("skill.id"), primary_key=True),
)


class Entry(PublicMixin, Base):
    id = Column(Integer, primary_key=True)
    original_id = Column(String, nullable=False)  # "62d396e7"
    talent_id = Column(String)  # "tln_3084"
    talent_name = Column(String)  # "Frau Hermine Caspar MBA."
    talent_grade = Column(String)  # "Intern"
    booking_grade = Column(String)  # ""
    operating_unit = Column(String, nullable=False)  # "Operating Unit 3"
    office_city = Column(String)  # "Hamburg"
    office_postal_code = Column(String, nullable=False)  # "97311"
    job_manager_name = Column(String)  # "Marjan Hande"
    job_manager_id = Column(String)  # "tln_3019"
    total_hours = Column(Float, nullable=False)  # 33.0
    start_date = Column(DateTime, nullable=False)  # "11/01/2022 04:42 PM"
    end_date = Column(DateTime, nullable=False)  # "11/05/2022 07:42 PM"
    client_name = Column(String)  # "Döhn"
    client_id = Column(String, nullable=False)  # "cl_1"
    industry = Column(String)  # "Low technology"
    is_unassigned = Column(Boolean)  # false
    required_skills = relationship("Skill", secondary=entry_required_skill_association)
    optional_skills = relationship("Skill", secondary=entry_optional_skill_association)


class Skill(PublicMixin, Base):
    id = Column(Integer, primary_key=True)
    name = Column(String)  # "German"
    category = Column(String)  # "Language"
