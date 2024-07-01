from models.base import Base

from sqlalchemy import Integer, DECIMAL, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import mapped_column

class Accounts(Base):
    __tablename__ = 'accounts'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    account_type = mapped_column(String(255))
    account_number = mapped_column(String(255), unique=True, nullable=False)
    balance = mapped_column(DECIMAL(10, 2), nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now())