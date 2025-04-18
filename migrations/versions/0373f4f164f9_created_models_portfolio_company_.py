"""created models: portfolio, company, position, price

Revision ID: 0373f4f164f9
Revises: a0d6c972f4df
Create Date: 2025-04-08 18:50:23.020801

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0373f4f164f9'
down_revision: Union[str, None] = 'a0d6c972f4df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('companies',
    sa.Column('ticker', sa.String(length=10), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('sector', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('ticker')
    )
    op.create_index(op.f('ix_companies_ticker'), 'companies', ['ticker'], unique=False)
    op.create_table('prices',
    sa.Column('ticker', sa.String(length=10), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('open', sa.Float(), nullable=False),
    sa.Column('close', sa.Float(), nullable=False),
    sa.Column('high', sa.Float(), nullable=False),
    sa.Column('low', sa.Float(), nullable=False),
    sa.Column('volume', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('ticker', 'date')
    )
    op.create_index(op.f('ix_prices_date'), 'prices', ['date'], unique=False)
    op.create_index(op.f('ix_prices_ticker'), 'prices', ['ticker'], unique=False)
    op.create_table('positions',
    sa.Column('portfolio_id', sa.Integer(), nullable=False),
    sa.Column('company_ticker', sa.String(length=10), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['company_ticker'], ['companies.ticker'], ),
    sa.ForeignKeyConstraint(['portfolio_id'], ['portfolios.id'], ),
    sa.PrimaryKeyConstraint('portfolio_id', 'company_ticker')
    )
    op.create_index(op.f('ix_positions_company_ticker'), 'positions', ['company_ticker'], unique=False)
    op.create_index(op.f('ix_positions_portfolio_id'), 'positions', ['portfolio_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_positions_portfolio_id'), table_name='positions')
    op.drop_index(op.f('ix_positions_company_ticker'), table_name='positions')
    op.drop_table('positions')
    op.drop_index(op.f('ix_prices_ticker'), table_name='prices')
    op.drop_index(op.f('ix_prices_date'), table_name='prices')
    op.drop_table('prices')
    op.drop_index(op.f('ix_companies_ticker'), table_name='companies')
    op.drop_table('companies')
    # ### end Alembic commands ###
