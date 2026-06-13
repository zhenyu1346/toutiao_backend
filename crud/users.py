import uuid
from datetime import datetime,timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,update
from models.users import User, UserToken
from schemas.users import UserRequest
from utils import security

# 根据用户名查询数据库
async def get_user_by_username(db: AsyncSession,username: str):
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# 创建用户
async def create_user(db: AsyncSession,user_data: UserRequest):
    # 先密码加密处理 -> add用户数据 -> commit提交
    hashed_password = security.get_hash_password(user_data.password)
    user = User(username=user_data.username,password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)  # 从数据库读取最新数据
    return user


# 生成Token
async def create_token(db: AsyncSession,user_id: int):
    # 生成Token + 设置过期时间 - 查询数据库当前用户是否存在 -> 有：更新 - 无：创建Token
    token = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(days=7)
    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()

    if user_token:
        user_token.token = token
        user_token.expires_at = expires_at
        stmt = update(UserToken).where(UserToken.user_id == user_id).values(token=token,expires_at=expires_at)
        await db.execute(stmt)
    else:
        user_token = UserToken(user_id=user_id,token=token,expires_at=expires_at)
        db.add(user_token)
    await db.commit()
    await db.refresh(user_token)
    return user_token