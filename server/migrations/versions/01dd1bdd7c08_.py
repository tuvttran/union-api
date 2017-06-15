"""empty message

Revision ID: 01dd1bdd7c08
Revises: 0b64c7dab5b9
Create Date: 2017-06-14 13:26:28.828834

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01dd1bdd7c08'
down_revision = '0b64c7dab5b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('founder_id', sa.Integer(), nullable=True))
    op.drop_constraint('users_id_fkey', 'users', type_='foreignkey')
    op.create_foreign_key(None, 'users', 'founders', ['founder_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.create_foreign_key('users_id_fkey', 'users', 'founders', ['id'], ['id'])
    op.drop_column('users', 'founder_id')
    # ### end Alembic commands ###