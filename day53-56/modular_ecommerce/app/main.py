from fastapi import FastAPI
from sqlalchemy.orm import Session
import logging
from sqlalchemy import select

from app.database import engine, Base, get_db
from app.modules.auth import router as auth_router
from app.modules.users import router as users_router
from app.modules.products import router as products_router
from app.modules.orders import router as orders_router
from app.modules.admin import router as admin_router
from app.modules.auth.service import hash_password
from app.modules.auth.models import User, Permission, role_permissions

app = FastAPI()

app.include_router(auth_router.router, prefix="/auth", tags=["auth"])
app.include_router(users_router.router, prefix="/users", tags=["users"])
app.include_router(products_router.router, prefix="/products", tags=["products"])
app.include_router(orders_router.router, prefix="/orders", tags=["orders"])
app.include_router(admin_router.router, prefix="/admin", tags=["admin"])

@app.on_event("startup")
def on_startup():
    try:
        Base.metadata.create_all(bind=engine)
        logging.info("Database tables created successfully.")
        
        # Seed admin user if not exists
        db: Session = next(get_db())
        admin_email = "admin@example.com"
        admin_user = db.query(User).filter(User.email == admin_email).first()
        if not admin_user:
            hashed_pw = hash_password("admin123")
            new_admin = User(email=admin_email, hashed_password=hashed_pw, role="admin", full_name="Admin")
            db.add(new_admin)
            db.commit()
            db.refresh(new_admin)
            logging.info("Admin user seeded successfully.")
        
        # Seed permissions
        permissions = ["create:product", "edit:product", "delete:product", "manage:products", "manage:users"]
        for perm_name in permissions:
            perm = db.query(Permission).filter(Permission.name == perm_name).first()
            if not perm:
                new_perm = Permission(name=perm_name)
                db.add(new_perm)
                db.commit()
                db.refresh(new_perm)
        
        # Assign permissions to admin role
        admin_perms = db.query(Permission).all()
        for perm in admin_perms:
            existing = db.execute(select(role_permissions).where(
                role_permissions.c.role == "admin",
                role_permissions.c.permission_id == perm.id
            )).first()
            if not existing:
                db.execute(role_permissions.insert().values(role="admin", permission_id=perm.id))
                db.commit()
        
        logging.info("Permissions seeded successfully.")
        db.close()
    except Exception as e:
        logging.error(f"Startup failed: {e}")
        raise  