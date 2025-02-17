"""difficulty_zone: cascade delete

Revision ID: 4530f38b59e2
Revises: bef0ec0b5af6
Create Date: 2024-11-12 12:03:13.781282

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4530f38b59e2'
down_revision: Union[str, None] = 'bef0ec0b5af6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('difficulty_zone_ibfk_2', 'difficulty_zone', type_='foreignkey')
    op.drop_constraint('difficulty_zone_ibfk_1', 'difficulty_zone', type_='foreignkey')
    op.create_foreign_key(None, 'difficulty_zone', 'keyboardzone', ['keyboardzone_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'difficulty_zone', 'difficulty', ['difficulty_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'difficulty_zone', type_='foreignkey')
    op.drop_constraint(None, 'difficulty_zone', type_='foreignkey')
    op.create_foreign_key('difficulty_zone_ibfk_1', 'difficulty_zone', 'difficulty', ['difficulty_id'], ['id'])
    op.create_foreign_key('difficulty_zone_ibfk_2', 'difficulty_zone', 'keyboardzone', ['keyboardzone_id'], ['id'])
    # ### end Alembic commands ###
