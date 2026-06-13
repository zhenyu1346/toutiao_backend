from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from schemas.users import UserRequest

router = APIRouter(prefix="/api/user",tags=["user"])

@router.post("/register")
async def register(user_data: UserRequest,db: AsyncSession=Depends(get_db)):
    # 注册逻辑：验证用户是否存在 -> 存在 返回错误信息
    #  -> 不存在 创建用户 -> 生成Token -> 响应结果
    return {
        "code": 200,
        "message": "success",
        "data": {
            "token": "用户访问令牌",
            "userInfo": {
                "id": 1,
                "username": user_data.username,
                "bio": "这个人很懒，什么都没有留下",
                "avatar": "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"
            }
        }
    }