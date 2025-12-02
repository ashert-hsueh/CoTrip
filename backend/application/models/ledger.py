from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime

# 账本相关模型
@dataclass
class LedgerCreateRequest:
    title: str
    travel_plan_id: Optional[int] = None

@dataclass
class LedgerUpdateRequest:
    title: Optional[str] = None
    travel_plan_id: Optional[int] = None

@dataclass
class LedgerMemberRequest:
    user_id: int

@dataclass
class LedgerResponse:
    id: int
    title: str
    creator_id: int
    travel_plan_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    member_count: int
    total_amount: int

    @classmethod
    def from_entity(cls, ledger):
        # 计算总金额
        total_amount = sum(item.amount for item in ledger.bill_items) if ledger.bill_items else 0

        return cls(
            id=ledger.id,
            title=ledger.title,
            creator_id=ledger.creator_id,
            travel_plan_id=ledger.travel_plan_id,
            created_at=ledger.created_at,
            updated_at=ledger.updated_at,
            member_count=ledger.members.count(),
            total_amount=total_amount
        )

@dataclass
class LedgerDetailResponse(LedgerResponse):
    members: List['UserSimpleResponse']
    bill_items: List['BillItemResponse']

    @classmethod
    def from_entity(cls, ledger, members, bill_items):
        base = LedgerResponse.from_entity(ledger)
        return cls(
            **base.__dict__,
            members=members,
            bill_items=bill_items
        )

# 账单相关模型
@dataclass
class BillItemCreateRequest:
    type: str  # hotel, meal, transport, ticket, other
    amount: int  # 金额（分）
    payer_id: int
    participant_ids: List[int]
    currency: str = "CNY"  # 货币，默认人民币
    payment_account: str = "cash"  # 支付账户，默认现金
    description: Optional[str] = None
    occurred_at: Optional[datetime] = None

@dataclass
class BillItemUpdateRequest:
    type: Optional[str] = None
    amount: Optional[int] = None
    currency: Optional[str] = None
    payment_account: Optional[str] = None
    payer_id: Optional[int] = None
    participant_ids: Optional[List[int]] = None
    description: Optional[str] = None
    occurred_at: Optional[datetime] = None

@dataclass
class BillItemResponse:
    id: int
    ledger_id: int
    type: str
    amount: int
    currency: str
    payment_account: str
    payer_id: int
    payer_name: str
    participants: List['UserSimpleResponse']
    description: Optional[str]
    occurred_at: datetime

    @classmethod
    def from_entity(cls, bill_item, payer_name, participants):
        return cls(
            id=bill_item.id,
            ledger_id=bill_item.ledger_id,
            type=bill_item.type,
            amount=bill_item.amount,
            currency=bill_item.currency,
            payment_account=bill_item.payment_account,
            payer_id=bill_item.payer_id,
            payer_name=payer_name,
            participants=participants,
            description=bill_item.description,
            occurred_at=bill_item.occurred_at
        )

# 用户简单信息模型
@dataclass
class UserSimpleResponse:
    id: int
    username: str
    email: str

    @classmethod
    def from_entity(cls, user):
        return cls(
            id=user.id,
            username=user.username,
            email=user.email
        )
