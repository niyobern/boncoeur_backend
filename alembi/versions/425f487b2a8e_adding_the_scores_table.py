"""adding the scores table

Revision ID: 425f487b2a8e
Revises: c16d751fb944
Create Date: 2022-05-03 14:28:46.245386

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '425f487b2a8e'
down_revision = 'c16d751fb944'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('scores',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quiz', sa.Integer(), nullable=True),
    sa.Column('score', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['quiz'], ['quizes.id'], name='quiz_score_fkey', ondelete='cascade'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('scores')
    # ### end Alembic commands ###
