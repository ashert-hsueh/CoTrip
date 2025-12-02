from sqlalchemy.orm import Session
from database.entities.ledger_entity import LedgerEntity, BillItemEntity, user_ledger_association, user_billitem_association
from database.entities.user_entity import UserEntity

class LedgerRepository:
    def __init__(self, db: Session):
        self.db = db

    # 账本相关操作
    def create_ledger(self, title: str, creator_id: int, travel_plan_id: int = None) -> LedgerEntity:
        ledger = LedgerEntity(
            title=title,
            creator_id=creator_id,
            travel_plan_id=travel_plan_id
        )
        self.db.add(ledger)
        self.db.commit()
        self.db.refresh(ledger)

        # 添加创建者为成员
        creator = self.db.query(UserEntity).get(creator_id)
        if creator:
            ledger.members.append(creator)
            self.db.commit()
            self.db.refresh(ledger)

        return ledger

    def get_ledger_by_id(self, ledger_id: int) -> LedgerEntity:
        return self.db.query(LedgerEntity).filter(LedgerEntity.id == ledger_id).first()

    def get_ledgers_by_user(self, user_id: int):
        return self.db.query(LedgerEntity).join(
            user_ledger_association,
            LedgerEntity.id == user_ledger_association.c.ledger_id
        ).filter(user_ledger_association.c.user_id == user_id).all()

    def update_ledger_title(self, ledger_id: int, new_title: str) -> LedgerEntity:
        ledger = self.get_ledger_by_id(ledger_id)
        if ledger:
            ledger.title = new_title
            self.db.commit()
            self.db.refresh(ledger)
        return ledger

    def update_ledger_travel_plan(self, ledger_id: int, travel_plan_id: int = None) -> LedgerEntity:
        ledger = self.get_ledger_by_id(ledger_id)
        if ledger:
            ledger.travel_plan_id = travel_plan_id
            self.db.commit()
            self.db.refresh(ledger)
        return ledger

    def delete_ledger(self, ledger_id: int) -> bool:
        ledger = self.get_ledger_by_id(ledger_id)
        if ledger:
            self.db.delete(ledger)
            self.db.commit()
            return True
        return False

    def add_member_to_ledger(self, ledger_id: int, user_id: int) -> bool:
        ledger = self.get_ledger_by_id(ledger_id)
        user = self.db.query(UserEntity).get(user_id)

        if ledger and user and user not in ledger.members:
            ledger.members.append(user)
            self.db.commit()
            self.db.refresh(ledger)
            return True
        return False

    def remove_member_from_ledger(self, ledger_id: int, user_id: int) -> bool:
        ledger = self.get_ledger_by_id(ledger_id)
        user = self.db.query(UserEntity).get(user_id)

        if ledger and user and user in ledger.members:
            ledger.members.remove(user)
            self.db.commit()
            self.db.refresh(ledger)
            return True
        return False

    def is_user_in_ledger(self, user_id: int, ledger_id: int) -> bool:
        ledger = self.get_ledger_by_id(ledger_id)
        if not ledger:
            return False
        return any(member.id == user_id for member in ledger.members)

    # 账单条目相关操作
    def create_bill_item(self, ledger_id: int, type: str, amount: int, payer_id: int,
                        participant_ids: list, currency: str = "CNY",
                        payment_account: str = "cash", description: str = None,
                        occurred_at: str = None) -> BillItemEntity:
        bill_item = BillItemEntity(
            ledger_id=ledger_id,
            type=type,
            amount=amount,
            currency=currency,
            payment_account=payment_account,
            payer_id=payer_id,
            description=description,
            occurred_at=occurred_at
        )

        self.db.add(bill_item)
        self.db.commit()
        self.db.refresh(bill_item)

        # 添加参与者
        for user_id in participant_ids:
            user = self.db.query(UserEntity).get(user_id)
            if user:
                bill_item.participants.append(user)

        self.db.commit()
        self.db.refresh(bill_item)
        return bill_item

    def get_bill_item_by_id(self, bill_item_id: int) -> BillItemEntity:
        return self.db.query(BillItemEntity).filter(BillItemEntity.id == bill_item_id).first()

    def get_bill_items_by_ledger(self, ledger_id: int):
        return self.db.query(BillItemEntity).filter(BillItemEntity.ledger_id == ledger_id).order_by(BillItemEntity.occurred_at.desc()).all()

    def update_bill_item(self, bill_item_id: int, type: str = None, amount: int = None,
                        currency: str = None, payment_account: str = None, payer_id: int = None,
                        participant_ids: list = None, description: str = None,
                        occurred_at: str = None) -> BillItemEntity:
        bill_item = self.get_bill_item_by_id(bill_item_id)
        if not bill_item:
            return None

        if type is not None:
            bill_item.type = type
        if amount is not None:
            bill_item.amount = amount
        if currency is not None:
            bill_item.currency = currency
        if payment_account is not None:
            bill_item.payment_account = payment_account
        if payer_id is not None:
            bill_item.payer_id = payer_id
        if description is not None:
            bill_item.description = description
        if occurred_at is not None:
            bill_item.occurred_at = occurred_at

        # 更新参与者
        if participant_ids is not None:
            bill_item.participants.clear()
            for user_id in participant_ids:
                user = self.db.query(UserEntity).get(user_id)
                if user:
                    bill_item.participants.append(user)

        self.db.commit()
        self.db.refresh(bill_item)
        return bill_item

    def delete_bill_item(self, bill_item_id: int) -> bool:
        bill_item = self.get_bill_item_by_id(bill_item_id)
        if bill_item:
            self.db.delete(bill_item)
            self.db.commit()
            return True
        return False
