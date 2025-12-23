from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.modules.auth.dependencies import get_current_user, require_role, require_permission
from app.modules.auth.models import User
from app.modules.admin.service import get_all_users, update_user_role, ban_user, get_sales_analytics
from pydantic import BaseModel


class UserRoleUpdate(BaseModel):
    role: str


class SalesAnalytics(BaseModel):
    total_orders: int
    total_revenue: float
    top_5_products: List[dict]


router = APIRouter()


@router.get("/users", response_model=List[dict])
def get_users(
    skip: int = 0,
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("manage:users"))
):
    users = get_all_users(db, skip, limit)
    return [{"id": u.id, "email": u.email, "role": u.role, "is_active": u.is_active} for u in users]


@router.patch("/users/{user_id}/role")
def change_user_role(
    user_id: int,
    update: UserRoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("manage:users"))
):
    try:
        user = update_user_role(db, user_id, update.role, current_user)
        return {"message": f"User {user.email} role updated to {user.role}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/users/{user_id}/ban")
def ban_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("manage:users"))
):
    try:
        user = ban_user(db, user_id, current_user)
        return {"message": f"User {user.email} has been banned"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/reports/sales", response_model=SalesAnalytics)
def get_sales_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    return get_sales_analytics(db)