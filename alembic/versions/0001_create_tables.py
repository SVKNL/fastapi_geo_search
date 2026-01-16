"""create tables

Revision ID: 0001_create_tables
Revises: 
Create Date: 2026-01-16 12:45:00.000000
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "0001_create_tables"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "buildings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("address", sa.String(length=255), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_buildings_address", "buildings", ["address"], unique=False
    )

    op.create_table(
        "activities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.Column("depth", sa.Integer(), nullable=False),
        sa.CheckConstraint(
            "depth >= 1 AND depth <= 3", name="ck_activity_depth_range"
        ),
        sa.ForeignKeyConstraint(
            ["parent_id"], ["activities.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "parent_id", "name", name="uq_activities_parent_name"
        ),
    )
    op.create_index(
        "ix_activities_name", "activities", ["name"], unique=False
    )

    op.create_table(
        "organizations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("building_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["building_id"], ["buildings.id"], ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_organizations_building_id",
        "organizations",
        ["building_id"],
        unique=False,
    )
    op.create_index(
        "ix_organizations_name", "organizations", ["name"], unique=False
    )

    op.create_table(
        "organization_phones",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("phone", sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(
            ["organization_id"], ["organizations.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_organization_phones_organization_id",
        "organization_phones",
        ["organization_id"],
        unique=False,
    )

    op.create_table(
        "organization_activities",
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("activity_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["activity_id"], ["activities.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["organization_id"], ["organizations.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("organization_id", "activity_id"),
    )


def downgrade() -> None:
    op.drop_table("organization_activities")
    op.drop_index(
        "ix_organization_phones_organization_id",
        table_name="organization_phones",
    )
    op.drop_table("organization_phones")
    op.drop_index("ix_organizations_name", table_name="organizations")
    op.drop_index(
        "ix_organizations_building_id", table_name="organizations"
    )
    op.drop_table("organizations")
    op.drop_index("ix_activities_name", table_name="activities")
    op.drop_table("activities")
    op.drop_index("ix_buildings_address", table_name="buildings")
    op.drop_table("buildings")
