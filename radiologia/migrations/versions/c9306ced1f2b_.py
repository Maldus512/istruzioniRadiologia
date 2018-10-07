"""empty message

Revision ID: c9306ced1f2b
Revises: 
Create Date: 2018-10-04 15:10:05.422405

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9306ced1f2b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('exam',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('pictures', sa.String(length=160), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_exam_name'), 'exam', ['name'], unique=True)
    op.create_table('description',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('exam_id', sa.Integer(), nullable=True),
    sa.Column('language', sa.String(length=8), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('audio', sa.String(length=80), nullable=True),
    sa.ForeignKeyConstraint(['exam_id'], ['exam.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_description_language'), 'description', ['language'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_description_language'), table_name='description')
    op.drop_table('description')
    op.drop_index(op.f('ix_exam_name'), table_name='exam')
    op.drop_table('exam')
    # ### end Alembic commands ###