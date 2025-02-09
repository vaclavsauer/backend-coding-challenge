"""Add Entry, Skill

Revision ID: 64692f285605
Revises: 
Create Date: 2022-11-25 19:02:22.465319

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "64692f285605"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "entry",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("original_id", sa.String(), nullable=False),
        sa.Column("talent_id", sa.String(), nullable=True),
        sa.Column("talent_name", sa.String(), nullable=True),
        sa.Column("talent_grade", sa.String(), nullable=True),
        sa.Column("booking_grade", sa.String(), nullable=True),
        sa.Column("operating_unit", sa.String(), nullable=False),
        sa.Column("office_city", sa.String(), nullable=True),
        sa.Column("office_postal_code", sa.String(), nullable=False),
        sa.Column("job_manager_name", sa.String(), nullable=True),
        sa.Column("job_manager_id", sa.String(), nullable=True),
        sa.Column("total_hours", sa.Float(), nullable=False),
        sa.Column("start_date", sa.DateTime(), nullable=False),
        sa.Column("end_date", sa.DateTime(), nullable=False),
        sa.Column("client_name", sa.String(), nullable=True),
        sa.Column("client_id", sa.String(), nullable=False),
        sa.Column("industry", sa.String(), nullable=True),
        sa.Column("is_unassigned", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "skill",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("category", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "entry_optional_skill_association",
        sa.Column("entry_id", sa.Integer(), nullable=False),
        sa.Column("skill_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["entry_id"],
            ["entry.id"],
        ),
        sa.ForeignKeyConstraint(
            ["skill_id"],
            ["skill.id"],
        ),
        sa.PrimaryKeyConstraint("entry_id", "skill_id"),
    )
    op.create_table(
        "entry_required_skill_association",
        sa.Column("entry_id", sa.Integer(), nullable=False),
        sa.Column("skill_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["entry_id"],
            ["entry.id"],
        ),
        sa.ForeignKeyConstraint(
            ["skill_id"],
            ["skill.id"],
        ),
        sa.PrimaryKeyConstraint("entry_id", "skill_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("entry_required_skill_association")
    op.drop_table("entry_optional_skill_association")
    op.drop_table("skill")
    op.drop_table("entry")
    # ### end Alembic commands ###
