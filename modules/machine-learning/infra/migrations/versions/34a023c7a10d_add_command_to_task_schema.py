"""add command to task schema

Revision ID: 34a023c7a10d
Revises: 94db7e78f4c5
Create Date: 2024-04-26 09:27:57.072259

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '34a023c7a10d'
down_revision: Union[str, None] = '94db7e78f4c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('command', sa.String(length=16), nullable=True))
    op.alter_column('tasks', 'status',
               existing_type=sa.VARCHAR(length=10),
               type_=sa.String(length=16),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tasks', 'status',
               existing_type=sa.String(length=16),
               type_=sa.VARCHAR(length=10),
               existing_nullable=True)
    op.drop_column('tasks', 'command')
    # ### end Alembic commands ###
