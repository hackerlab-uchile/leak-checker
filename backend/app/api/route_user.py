from auth.auth_handler import get_current_active_user
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse
from schemas.user import UserInfo

router = APIRouter()


@router.get("/logout/")
async def logout(request: Request, response: Response):
    """Logs out the current user, by removing it's JWT token"""
    cookie = request.cookies.get("token", None)
    if cookie:
        resp = JSONResponse(headers=request.headers, content="successful")
        resp.delete_cookie("token")
        return resp
    return {"status": "not succesful"}


@router.get("/me/", response_model=UserInfo | None)
async def user_info(
    user_info: UserInfo | None = Depends(get_current_active_user),
):
    """If valid token, then returns user information. Else, returns null"""
    return user_info if user_info else None
