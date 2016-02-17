"""add bookmark table

Revision ID: 6a44c45aaf6d
Revises: 419a330b8bf3
Create Date: 2016-02-17 13:54:37.778765

"""

# revision identifiers, used by Alembic.
revision = '6a44c45aaf6d'
down_revision = '419a330b8bf3'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
        op.create_table(
            'bookmark',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('date', sa.DateTime, nullable=False),
            sa.Column('notes', sa.String(200), nullable=False),
            sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id'))
        )


def downgrade():
    op.drop_table('bookmark')
