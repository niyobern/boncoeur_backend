"""empty message

Revision ID: fd138ab25184
Revises: f4c73d1ad99a
Create Date: 2022-05-02 21:39:13.522525

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd138ab25184'
down_revision = 'f4c73d1ad99a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('quizes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('files',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('file_url', sa.String(), nullable=False),
    sa.Column('file_type', sa.String(), nullable=False),
    sa.Column('lesson_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['lesson_id'], ['lessons.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', 'lesson_id')
    )
    op.create_table('questions',
    sa.Column('id', sa.Integer(), nullable=True),
    sa.Column('question', sa.String(), nullable=False),
    sa.Column('options', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('answer', sa.String(), nullable=False),
    sa.Column('quiz', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['quiz'], ['quizes.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('lessons', sa.Column('lesson_banner', sa.String(), server_default='some banner', nullable=False))
    op.add_column('votes', sa.Column('lesson_id', sa.Integer(), nullable=False))
    op.drop_constraint('votes_post_id_fkey', 'votes', type_='foreignkey')
    op.create_foreign_key(None, 'votes', 'lessons', ['lesson_id'], ['id'], ondelete='CASCADE')
    op.drop_column('votes', 'post_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('votes', sa.Column('post_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'votes', type_='foreignkey')
    op.create_foreign_key('votes_post_id_fkey', 'votes', 'lessons', ['post_id'], ['id'], ondelete='CASCADE')
    op.drop_column('votes', 'lesson_id')
    op.drop_column('lessons', 'lesson_banner')
    op.drop_table('questions')
    op.drop_table('files')
    op.drop_table('quizes')
    # ### end Alembic commands ###
