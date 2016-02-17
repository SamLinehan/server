"""create user table

Revision ID: 419a330b8bf3
Revises:
Create Date: 2016-02-17 11:07:33.469733

"""

# revision identifiers, used by Alembic.
revision = '419a330b8bf3'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('social_id', sa.String(50), nullable=False),
        sa.Column('nickname', sa.String(50), nullable=False),
        sa.Column('email', sa.String(50), nullable=False)
    )


def downgrade():
    op.drop_table('user')
