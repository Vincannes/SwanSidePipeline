"""add acks to comments

Revision ID: 3476e147e632
Revises: 6aa446ee4072
Create Date: 2020-04-10 00:50:31.704488

"""

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
import sqlalchemy_utils
import uuid

# revision identifiers, used by Alembic.
revision = "3476e147e632"
down_revision = "6aa446ee4072"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "comment_acknoledgments",
        sa.Column(
            "comment",
            sqlalchemy_utils.types.uuid.UUIDType(binary=False),
            default=uuid.uuid4,
            nullable=False,
        ),
        sa.Column(
            "person",
            sqlalchemy_utils.types.uuid.UUIDType(binary=False),
            default=uuid.uuid4,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["comment"],
            ["comment.id"],
        ),
        sa.ForeignKeyConstraint(
            ["person"],
            ["person.id"],
        ),
        sa.PrimaryKeyConstraint("comment", "person"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("comment_acknoledgments")
    # ### end Alembic commands ###