"""add title column

Revision ID: 635b52ea9473
Revises: 34c2f1936057
Create Date: 2016-02-18 09:48:38.667760

"""

# revision identifiers, used by Alembic.
revision = '635b52ea9473'
down_revision = '34c2f1936057'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('bookmark', sa.Column('title', sa.String(50)))



def downgrade():
    op.drop_column('bookmark', 'title')
