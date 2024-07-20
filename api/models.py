from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class RecordMixin:
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Customer(RecordMixin, Base):
    __tablename__ = "customers"

    name = Column(String, nullable=False)

    accounts = relationship("Account", back_populates="customer")


class Account(RecordMixin, Base):
    __tablename__ = "accounts"

    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    balance = Column(Float, nullable=False, default=0.0)

    customer = relationship("Customer", back_populates="accounts")
    transfers_sent = relationship("Transfer", foreign_keys="Transfer.from_account_id", back_populates="from_account")
    transfers_received = relationship("Transfer", foreign_keys="Transfer.to_account_id", back_populates="to_account")


class Transfer(RecordMixin, Base):
    __tablename__ = "transfers"

    from_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    to_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    amount = Column(Float, nullable=False)

    from_account = relationship("Account", foreign_keys=[from_account_id], back_populates="transfers_sent")
    to_account = relationship("Account", foreign_keys=[to_account_id], back_populates="transfers_received")
