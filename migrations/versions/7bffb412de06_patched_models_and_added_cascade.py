"""patched models and added CASCADE

Revision ID: 7bffb412de06
Revises: 0373f4f164f9
Create Date: 2025-04-11 20:28:23.053224

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7bffb412de06'
down_revision: Union[str, None] = '0373f4f164f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('positions_company_ticker_fkey', 'positions', type_='foreignkey')
    op.drop_constraint('positions_portfolio_id_fkey', 'positions', type_='foreignkey')
    op.create_foreign_key(None, 'positions', 'companies', ['company_ticker'], ['ticker'], onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key(None, 'positions', 'portfolios', ['portfolio_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.add_column('prices', sa.Column('company_ticker', sa.String(length=10), nullable=False))
    op.create_index(op.f('ix_prices_company_ticker'), 'prices', ['company_ticker'], unique=False)
    op.create_foreign_key(None, 'prices', 'companies', ['company_ticker'], ['ticker'], onupdate='CASCADE', ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'prices', type_='foreignkey')
    op.drop_index(op.f('ix_prices_company_ticker'), table_name='prices')
    op.drop_column('prices', 'company_ticker')
    op.drop_constraint(None, 'positions', type_='foreignkey')
    op.drop_constraint(None, 'positions', type_='foreignkey')
    op.create_foreign_key('positions_portfolio_id_fkey', 'positions', 'portfolios', ['portfolio_id'], ['id'])
    op.create_foreign_key('positions_company_ticker_fkey', 'positions', 'companies', ['company_ticker'], ['ticker'])
    # ### end Alembic commands ###
