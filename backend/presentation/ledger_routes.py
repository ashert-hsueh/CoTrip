from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from application.ledger_service import LedgerService
from database import get_db
from sqlalchemy.orm import Session
from presentation.dependencies.auth import get_current_user_id

router = APIRouter(prefix="/api/ledgers", tags=["ledgers"])

# 请求模型
class LedgerCreateRequest(BaseModel):
    title: str
    travel_plan_id: Optional[int] = None

class LedgerUpdateRequest(BaseModel):
    title: Optional[str] = None
    travel_plan_id: Optional[int] = None

class LedgerMemberRequest(BaseModel):
    user_id: int

class BillItemCreateRequest(BaseModel):
    type: str  # hotel, meal, transport, ticket, other
    amount: int  # 金额（分）
    payer_id: int
    participant_ids: List[int]
    currency: str = "CNY"  # 货币，默认人民币
    payment_account: str = "cash"  # 支付账户，默认现金
    description: Optional[str] = None
    occurred_at: Optional[datetime] = None

class BillItemUpdateRequest(BaseModel):
    type: Optional[str] = None
    amount: Optional[int] = None
    currency: Optional[str] = None
    payment_account: Optional[str] = None
    payer_id: Optional[int] = None
    participant_ids: Optional[List[int]] = None
    description: Optional[str] = None
    occurred_at: Optional[datetime] = None

# 查询参数模型（暂时保留，可能后续需要）
class CurrentUserId(BaseModel):
    user_id: int

# 创建账本
@router.post("/")
async def create_ledger(
    request: LedgerCreateRequest,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    ledger_service = LedgerService(db)
    result = ledger_service.create_ledger(current_user_id, request)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

# 获取当前用户的所有账本
@router.get("/my-ledgers")
async def get_my_ledgers(
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    ledger_service = LedgerService(db)
    result = ledger_service.get_my_ledgers(current_user_id)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

# 获取账本详情
@router.get("/{ledger_id}")
async def get_ledger_detail(
    ledger_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    ledger_service = LedgerService(db)
    result = ledger_service.get_ledger_detail(current_user_id, ledger_id)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

# 更新账本
@router.put("/{ledger_id}")
async def update_ledger(
    ledger_id: int,
    request: LedgerUpdateRequest,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    ledger_service = LedgerService(db)
    result = ledger_service.update_ledger(current_user_id, ledger_id, request)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

# 删除账本
@router.delete("/{ledger_id}")
async def delete_ledger(
    ledger_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    ledger_service = LedgerService(db)
    result = ledger_service.delete_ledger(current_user_id, ledger_id)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

# 添加成员到账本
@router.post("/{ledger_id}/members")
async def add_member_to_ledger(
    ledger_id: int,
    request: LedgerMemberRequest,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    ledger_service = LedgerService(db)
    result = ledger_service.add_member_to_ledger(current_user_id, ledger_id, request.user_id)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

# 从账本移除成员
@router.delete("/{ledger_id}/members/{user_id}")
async def remove_member_from_ledger(
    ledger_id: int,
    user_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    ledger_service = LedgerService(db)
    result = ledger_service.remove_member_from_ledger(current_user_id, ledger_id, user_id)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

# 创建账单条目
@router.post("/{ledger_id}/bill-items")
async def create_bill_item(
    ledger_id: int,
    request: BillItemCreateRequest,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    ledger_service = LedgerService(db)
    result = ledger_service.create_bill_item(current_user_id, ledger_id, request)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

# 更新账单条目
@router.put("/bill-items/{bill_item_id}")
async def update_bill_item(
    bill_item_id: int,
    request: BillItemUpdateRequest,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    ledger_service = LedgerService(db)
    result = ledger_service.update_bill_item(current_user_id, bill_item_id, request)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

# 删除账单条目
@router.delete("/bill-items/{bill_item_id}")
async def delete_bill_item(
    bill_item_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    ledger_service = LedgerService(db)
    result = ledger_service.delete_bill_item(current_user_id, bill_item_id)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result
