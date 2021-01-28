"""empty message

Revision ID: de8ee1cf1311
Revises: 10c120edddaa
Create Date: 2021-01-23 10:12:08.872316

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'de8ee1cf1311'
down_revision = '10c120edddaa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('userpro',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=35), nullable=False),
    sa.Column('password', sa.String(length=40), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=False),
    sa.Column('url', sa.String(length=50), nullable=True),
    sa.Column('location', sa.String(length=40), nullable=False),
    sa.Column('direction', sa.String(length=40), nullable=False),
    sa.Column('vat_number', sa.String(length=20), nullable=True),
    sa.Column('social_reason', sa.String(length=20), nullable=True),
    sa.Column('avatar', sa.String(length=100), nullable=False),
    sa.Column('photos', sa.String(length=200), nullable=True),
    sa.Column('registr_date', sa.DateTime(), nullable=False),
    sa.Column('rol', sa.String(length=30), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone'),
    sa.UniqueConstraint('user_name')
    )
    op.create_table('offers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_pro', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('text', sa.String(length=200), nullable=False),
    sa.Column('counter', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_pro'], ['userpro.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_index('email', table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('email', mysql.VARCHAR(length=120), nullable=False),
    sa.Column('password', mysql.VARCHAR(length=80), nullable=False),
    sa.Column('is_active', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False),
    sa.CheckConstraint('(`is_active` in (0,1))', name='user_chk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('email', 'user', ['email'], unique=True)
    op.drop_table('offers')
    op.drop_table('userpro')
    # ### end Alembic commands ###
