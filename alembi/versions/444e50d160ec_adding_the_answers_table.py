"""adding the answers table

Revision ID: 444e50d160ec
Revises: 454413e06769
Create Date: 2022-05-03 14:07:21.250556

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '444e50d160ec'
down_revision = '454413e06769'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('answers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('answer', sa.String(), nullable=True),
    sa.Column('question', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['question'], ['questions.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )



def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('answers')
    # ### end Alembic commands ###
