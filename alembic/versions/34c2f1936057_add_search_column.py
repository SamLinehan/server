"""add search column

Revision ID: 34c2f1936057
Revises: 6a44c45aaf6d
Create Date: 2016-02-17 18:14:16.605258

"""

# revision identifiers, used by Alembic.
revision = '34c2f1936057'
down_revision = '6a44c45aaf6d'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('bookmark', sa.Column('search', sa.String(50)))



def downgrade():
    op.drop_column('bookmark', 'search')
