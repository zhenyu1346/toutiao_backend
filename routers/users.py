from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from config.db_conf import get_db
from models.users import User
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse, UserUpdateRequest, UserChangePasswordRequest
from crud import users
from utils.response import success_response
from utils.auth import get_current_user
router = APIRouter(prefix="/api/user", tags=["user"])


@router.post("/register")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    # 注册逻辑：验证用户是否存在 -> 存在 返回错误信息
    #  -> 不存在 创建用户 -> 生成Token -> 响应结果
    existing_user = await users.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")
    user = await users.create_user(db, user_data)
    token = await users.create_token(db, user.id)
    response_data = UserAuthResponse(token=token, userInfo=UserInfoResponse.model_validate(user))
    return success_response(message='注册成功', data=response_data)


@router.post("/login")
async def login(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    # 登录逻辑：验证用户是否存在 -> 不存在 返回错误信息
    #  -> 存在 验证密码 -> 不正确 返回错误信息
    #  -> 正确 生成Token -> 响应结果
    user = await users.authenticate_token(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    token = await users.create_token(db, user.id)
    response_data = UserAuthResponse(token=token, userInfo=UserInfoResponse.model_validate(user))
    return success_response(message="登录成功", data=response_data)


@router.get("/info")
async def get_user_info(user: User = Depends(get_current_user)):
    # 查询Token、查询用户 -> 封装crud -> 功能整合成一个工具函数 -> 在路由处理函数里面调用
    # Authorization: Bearer <token>
    return success_response(message="获取用户信息成功", data=UserInfoResponse.model_validate(user))


# 修改用户信息：验证Token -> 更新（用户输入数据 put提交 -> 请求体参数 -> 定义pydantic模型类）-> 响应结果
# 参数：用户输入的 + 验证Token的 + db（调用更新的方法）
@router.put("/update")
async def update_user_info(user_data: UserUpdateRequest, user: User = Depends(get_current_user),
                           db: AsyncSession = Depends(get_db)
):
    user = await users.update_user(db,user.username,user_data)
    return success_response(message="更新用户信息成功",data=UserInfoResponse.model_validate(user))


@router.put("/password")
async def update_password(password_data: UserChangePasswordRequest,
                          user: User = Depends(get_current_user),
                          db: AsyncSession = Depends(get_db)
):
    res_change_pwd = await users.change_password(db, user, password_data.old_password, password_data.new_password)

    if not res_change_pwd:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="密码修改失败，请稍后重试")
    return success_response(message="修改密码成功")