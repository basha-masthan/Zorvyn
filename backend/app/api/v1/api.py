from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, records, dashboard

api_router = APIRouter()
api_router.include_router(auth.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(records.router, prefix="/records", tags=["records"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
