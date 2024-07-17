from api import route_breach, route_demo, route_user, route_verify
from fastapi import APIRouter

api_router = APIRouter()


api_router.include_router(route_user.router, prefix="/user", tags=["user"])
api_router.include_router(route_breach.router, prefix="/breach", tags=["breach"])
api_router.include_router(route_verify.router, prefix="/verify", tags=["verify"])
api_router.include_router(route_demo.router, prefix="/demo", tags=["demo"])
