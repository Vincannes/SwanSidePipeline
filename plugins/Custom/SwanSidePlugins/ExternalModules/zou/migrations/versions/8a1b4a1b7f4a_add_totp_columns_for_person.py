"""Add totp columns for Person

Revision ID: 8a1b4a1b7f4a
Revises: a6c25eed3ea1
Create Date: 2022-11-15 23:15:42.600126

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8a1b4a1b7f4a"
down_revision = "a6c25eed3ea1"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "person", sa.Column("totp_enabled", sa.Boolean(), nullable=True)
    )
    op.add_column(
        "person", sa.Column("totp_secret", sa.String(length=32), nullable=True)
    )
    op.add_column(
        "person",
        sa.Column(
            "otp_recovery_codes",
            sa.ARRAY(sa.LargeBinary(length=60)),
            nullable=True,
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("person", "otp_recovery_codes")
    op.drop_column("person", "totp_secret")
    op.drop_column("person", "totp_enabled")
    # ### end Alembic commands ###