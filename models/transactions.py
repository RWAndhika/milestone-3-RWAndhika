from models.base import Base

from sqlalchemy import Integer, DECIMAL, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import mapped_column

class Transactions(Base):
    __tablename__ = 'transactions'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    from_account_id = mapped_column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=True)
    to_account_id = mapped_column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=True)
    amount = mapped_column(DECIMAL(10, 2), nullable=False)
    type = mapped_column(String(255))
    description = mapped_column(String(255), nullable=True)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
