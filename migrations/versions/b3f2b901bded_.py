"""empty message

Revision ID: b3f2b901bded
Revises: 6735852f6de8
Create Date: 2019-10-23 23:52:52.112141

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3f2b901bded'
down_revision = '6735852f6de8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Abilities', sa.Column('test01', sa.Integer(), nullable=True))
    op.add_column('Abilities', sa.Column('test02', sa.Integer(), nullable=True))
    op.add_column('Abilities', sa.Column('test03', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'Abilities', 'stats_templates', ['test02'], ['id'])
    op.create_foreign_key(None, 'Abilities', 'stats_templates', ['test03'], ['id'])
    op.create_foreign_key(None, 'Abilities', 'stats_templates', ['test01'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Abilities', type_='foreignkey')
    op.drop_constraint(None, 'Abilities', type_='foreignkey')
    op.drop_constraint(None, 'Abilities', type_='foreignkey')
    op.drop_column('Abilities', 'test03')
    op.drop_column('Abilities', 'test02')
    op.drop_column('Abilities', 'test01')
    # ### end Alembic commands ###
