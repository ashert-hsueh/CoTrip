from sqlalchemy.orm import Session
from persistence.ledger_repository import LedgerRepository
from persistence.user_repository import UserRepository
from .models.ledger import (
    LedgerCreateRequest,
    LedgerUpdateRequest,
    LedgerResponse,
    LedgerDetailResponse,
    BillItemCreateRequest,
    BillItemUpdateRequest,
    BillItemResponse,
    UserSimpleResponse
)

class LedgerService:
    def __init__(self, db: Session):
        self.ledger_repository = LedgerRepository(db)
        self.user_repository = UserRepository(db)

    # 账本相关操作
    def create_ledger(self, current_user_id: int, request: LedgerCreateRequest) -> dict:
        # 创建账本
        ledger = self.ledger_repository.create_ledger(
            title=request.title,
            creator_id=current_user_id,
            travel_plan_id=request.travel_plan_id
        )

        return {
            "success": True,
            "message": "账本创建成功",
            "ledger": LedgerResponse.from_entity(ledger)
        }

    def get_my_ledgers(self, current_user_id: int) -> dict:
        # 获取当前用户参与的所有账本
        ledgers = self.ledger_repository.get_ledgers_by_user(current_user_id)
        ledger_responses = [LedgerResponse.from_entity(ledger) for ledger in ledgers]

        return {
            "success": True,
            "data": ledger_responses
        }

    def get_ledger_detail(self, current_user_id: int, ledger_id: int) -> dict:
        # 检查用户是否有权限访问账本
        if not self.ledger_repository.is_user_in_ledger(current_user_id, ledger_id):
            return {"success": False, "message": "无权限访问此账本"}

        ledger = self.ledger_repository.get_ledger_by_id(ledger_id)
        if not ledger:
            return {"success": False, "message": "账本不存在"}

        # 获取成员信息
        members = [UserSimpleResponse.from_entity(user) for user in ledger.members.all()]

        # 获取账单条目信息
        bill_items = []
        for bill_item in ledger.bill_items:
            payer_name = bill_item.payer.username
            participants = [UserSimpleResponse.from_entity(user) for user in bill_item.participants.all()]
            bill_items.append(BillItemResponse.from_entity(bill_item, payer_name, participants))

        ledger_detail = LedgerDetailResponse.from_entity(ledger, members, bill_items)

        return {
            "success": True,
            "data": ledger_detail
        }

    def update_ledger(self, current_user_id: int, ledger_id: int, request: LedgerUpdateRequest) -> dict:
        # 检查用户是否有权限访问账本
        if not self.ledger_repository.is_user_in_ledger(current_user_id, ledger_id):
            return {"success": False, "message": "无权限修改此账本"}

        # 更新账本信息
        ledger = self.ledger_repository.update_ledger_title(ledger_id, request.title) if request.title else None
        if request.travel_plan_id is not None:
            ledger = self.ledger_repository.update_ledger_travel_plan(ledger_id, request.travel_plan_id)

        if not ledger:
            return {"success": False, "message": "账本不存在"}

        return {
            "success": True,
            "message": "账本更新成功",
            "ledger": LedgerResponse.from_entity(ledger)
        }

    def delete_ledger(self, current_user_id: int, ledger_id: int) -> dict:
        # 检查用户是否是账本创建者
        ledger = self.ledger_repository.get_ledger_by_id(ledger_id)
        if not ledger or ledger.creator_id != current_user_id:
            return {"success": False, "message": "无权限删除此账本"}

        if self.ledger_repository.delete_ledger(ledger_id):
            return {"success": True, "message": "账本删除成功"}
        return {"success": False, "message": "账本不存在"}

    def add_member_to_ledger(self, current_user_id: int, ledger_id: int, user_id: int) -> dict:
        # 检查用户是否有权限管理账本
        if not self.ledger_repository.is_user_in_ledger(current_user_id, ledger_id):
            return {"success": False, "message": "无权限管理此账本"}

        # 检查目标用户是否存在
        target_user = self.user_repository.get_user_by_id(user_id)
        if not target_user:
            return {"success": False, "message": "目标用户不存在"}

        # 检查用户是否已经是成员
        if self.ledger_repository.is_user_in_ledger(user_id, ledger_id):
            return {"success": False, "message": "用户已在账本中"}

        if self.ledger_repository.add_member_to_ledger(ledger_id, user_id):
            return {
                "success": True,
                "message": "成员添加成功",
                "member": UserSimpleResponse.from_entity(target_user)
            }
        return {"success": False, "message": "添加成员失败"}

    def remove_member_from_ledger(self, current_user_id: int, ledger_id: int, user_id: int) -> dict:
        # 检查用户是否是账本创建者
        ledger = self.ledger_repository.get_ledger_by_id(ledger_id)
        if not ledger or ledger.creator_id != current_user_id:
            return {"success": False, "message": "无权限管理此账本"}

        # 不能移除自己
        if current_user_id == user_id:
            return {"success": False, "message": "不能移除自己"}

        # 检查用户是否是成员
        if not self.ledger_repository.is_user_in_ledger(user_id, ledger_id):
            return {"success": False, "message": "用户不在账本中"}

        if self.ledger_repository.remove_member_from_ledger(ledger_id, user_id):
            return {"success": True, "message": "成员移除成功"}
        return {"success": False, "message": "移除成员失败"}

    # 账单条目相关操作
    def create_bill_item(self, current_user_id: int, ledger_id: int, request: BillItemCreateRequest) -> dict:
        # 检查用户是否有权限访问账本
        if not self.ledger_repository.is_user_in_ledger(current_user_id, ledger_id):
            return {"success": False, "message": "无权限访问此账本"}

        # 检查付款人是否是账本成员
        if not self.ledger_repository.is_user_in_ledger(request.payer_id, ledger_id):
            return {"success": False, "message": "付款人不是账本成员"}

        # 检查参与者是否都是账本成员
        for participant_id in request.participant_ids:
            if not self.ledger_repository.is_user_in_ledger(participant_id, ledger_id):
                return {"success": False, "message": "参与者包含非账本成员"}

        # 创建账单条目
        bill_item = self.ledger_repository.create_bill_item(
            ledger_id=ledger_id,
            type=request.type,
            amount=request.amount,
            payer_id=request.payer_id,
            participant_ids=request.participant_ids,
            currency=request.currency,
            payment_account=request.payment_account,
            description=request.description,
            occurred_at=request.occurred_at
        )

        # 构造响应
        payer_name = bill_item.payer.username
        participants = [UserSimpleResponse.from_entity(user) for user in bill_item.participants.all()]
        bill_response = BillItemResponse.from_entity(bill_item, payer_name, participants)

        return {
            "success": True,
            "message": "账单创建成功",
            "bill_item": bill_response
        }

    def update_bill_item(self, current_user_id: int, bill_item_id: int, request: BillItemUpdateRequest) -> dict:
        # 获取账单条目
        bill_item = self.ledger_repository.get_bill_item_by_id(bill_item_id)
        if not bill_item:
            return {"success": False, "message": "账单不存在"}

        # 检查用户是否有权限访问账本
        if not self.ledger_repository.is_user_in_ledger(current_user_id, bill_item.ledger_id):
            return {"success": False, "message": "无权限修改此账单"}

        # 如果更新了付款人，检查是否是账本成员
        if request.payer_id is not None and not self.ledger_repository.is_user_in_ledger(request.payer_id, bill_item.ledger_id):
            return {"success": False, "message": "付款人不是账本成员"}

        # 如果更新了参与者，检查是否都是账本成员
        if request.participant_ids is not None:
            for participant_id in request.participant_ids:
                if not self.ledger_repository.is_user_in_ledger(participant_id, bill_item.ledger_id):
                    return {"success": False, "message": "参与者包含非账本成员"}

        # 更新账单条目
        updated_bill_item = self.ledger_repository.update_bill_item(
            bill_item_id=bill_item_id,
            type=request.type,
            amount=request.amount,
            currency=request.currency,
            payment_account=request.payment_account,
            payer_id=request.payer_id,
            participant_ids=request.participant_ids,
            description=request.description,
            occurred_at=request.occurred_at
        )

        if not updated_bill_item:
            return {"success": False, "message": "账单更新失败"}

        # 构造响应
        payer_name = updated_bill_item.payer.username
        participants = [UserSimpleResponse.from_entity(user) for user in updated_bill_item.participants.all()]
        bill_response = BillItemResponse.from_entity(updated_bill_item, payer_name, participants)

        return {
            "success": True,
            "message": "账单更新成功",
            "bill_item": bill_response
        }

    def delete_bill_item(self, current_user_id: int, bill_item_id: int) -> dict:
        # 获取账单条目
        bill_item = self.ledger_repository.get_bill_item_by_id(bill_item_id)
        if not bill_item:
            return {"success": False, "message": "账单不存在"}

        # 检查用户是否有权限访问账本
        if not self.ledger_repository.is_user_in_ledger(current_user_id, bill_item.ledger_id):
            return {"success": False, "message": "无权限删除此账单"}

        if self.ledger_repository.delete_bill_item(bill_item_id):
            return {"success": True, "message": "账单删除成功"}
        return {"success": False, "message": "账单删除失败"}
