"""empty message

Revision ID: 3811953957ed
Revises: 
Create Date: 2023-02-22 21:55:43.070908

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3811953957ed'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=250), nullable=True),
    sa.Column('password', sa.String(length=250), nullable=True),
    sa.Column('name', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('schoollevels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('levelname', sa.Text(), nullable=False),
    sa.Column('schoolname', sa.Text(), nullable=False),
    sa.Column('isApply', sa.Boolean(), nullable=True),
    sa.Column('isAddOn', sa.Boolean(), nullable=True),
    sa.Column('schoolscore', sa.Text(), nullable=True),
    sa.Column('addscore', sa.Text(), nullable=True),
    sa.Column('date', sa.String(length=250), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('schoolmajors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('majorName', sa.String(length=250), nullable=False),
    sa.Column('school', sa.String(length=250), nullable=False),
    sa.Column('applyReq', sa.String(length=250), nullable=False),
    sa.Column('langReq', sa.Text(), nullable=False),
    sa.Column('Fee', sa.Text(), nullable=True),
    sa.Column('course', sa.Text(), nullable=False),
    sa.Column('cluster', sa.String(length=250), nullable=True),
    sa.Column('label', sa.String(length=250), nullable=True),
    sa.Column('date', sa.String(length=250), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('majorName')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('schoolmajors')
    op.drop_table('schoollevels')
    op.drop_table('users')
    # ### end Alembic commands ###
