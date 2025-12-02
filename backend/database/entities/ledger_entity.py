from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .user_entity import Base

# 用户-账本关联表
user_ledger_association = Table(
    "user_ledger",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("ledger_id", Integer, ForeignKey("ledgers.id"), primary_key=True)
)

# 用户-账单关联表
user_billitem_association = Table(
    "user_billitem",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("billitem_id", Integer, ForeignKey("bill_items.id"), primary_key=True)
)

class LedgerEntity(Base):
    __tablename__ = "ledgers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    travel_plan_id = Column(Integer, nullable=True)  # 可选的旅行计划关联
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关系定义
    creator = relationship("UserEntity", backref="created_ledgers")
    members = relationship(
        "UserEntity",
        secondary=user_ledger_association,
        backref="participating_ledgers",
        lazy="dynamic"
    )
    bill_items = relationship("BillItemEntity", backref="ledger", cascade="all, delete-orphan")

class BillItemEntity(Base):
    __tablename__ = "bill_items"

    id = Column(Integer, primary_key=True, index=True)
    ledger_id = Column(Integer, ForeignKey("ledgers.id"), nullable=False)
    type = Column(String, nullable=False)  # hotel, meal, transport, ticket, other
    amount = Column(Integer, nullable=False)  # 金额（分）
    currency = Column(String, nullable=False, default="CNY")  # 货币
    payment_account = Column(String, nullable=False, default="cash")  # 支付账户
    payer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    description = Column(String, nullable=True)
    occurred_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关系定义
    payer = relationship("UserEntity", backref="paid_bills")
    participants = relationship(
        "UserEntity",
        secondary=user_billitem_association,
        backref="participated_bills",
        lazy="dynamic"
    )
