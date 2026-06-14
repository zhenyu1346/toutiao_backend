from passlib.context import CryptContext

# bcrypt_sha256: passlib 内置方案，自动对密码做 SHA256 预处理，突破 bcrypt 72 字节限制
pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

# 密码加密
def get_hash_password(password: str):
    return pwd_context.hash(password)


# 密码验证：verify 返回True/False
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)