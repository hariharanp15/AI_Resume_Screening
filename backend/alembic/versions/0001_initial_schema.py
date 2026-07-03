"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-07-01
"""
from alembic import op
import sqlalchemy as sa


revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("role", sa.Enum("HR", "RECRUITER", name="userrole"), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
    )
    op.create_table(
        "candidates",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255)),
        sa.Column("phone", sa.String(64)),
        sa.Column("skills", sa.JSON(), nullable=False),
        sa.Column("work_experience", sa.Text()),
        sa.Column("education", sa.Text()),
        sa.Column("resume_text", sa.Text(), nullable=False),
        sa.Column("resume_file_path", sa.String(512), nullable=False),
        sa.Column("embedding", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("created_by", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
    )
    op.create_table(
        "job_descriptions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("required_skills", sa.JSON(), nullable=False),
        sa.Column("experience_requirement", sa.String(255), nullable=False),
        sa.Column("location", sa.String(255), nullable=False),
        sa.Column("employment_type", sa.String(100), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("embedding", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("created_by", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
    )
    op.create_table(
        "evaluations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("candidate_id", sa.Integer(), sa.ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False),
        sa.Column("job_id", sa.Integer(), sa.ForeignKey("job_descriptions.id", ondelete="SET NULL")),
        sa.Column("match_score", sa.Float()),
        sa.Column("missing_skills", sa.JSON(), nullable=False),
        sa.Column("strengths", sa.JSON(), nullable=False),
        sa.Column("weaknesses", sa.JSON(), nullable=False),
        sa.Column("summary", sa.Text()),
        sa.Column("interview_questions", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("created_by", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
    )


def downgrade():
    op.drop_table("evaluations")
    op.drop_table("job_descriptions")
    op.drop_table("candidates")
    op.drop_table("users")
