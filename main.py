from fastapi import FastAPI
from routers import news,users
from fastapi.middleware.cors import CORSMiddleware

from utils.exception_handlers import register_exception_handlers

app = FastAPI()

# 注册全局异常处理器
register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # 允许的域名列表
    allow_credentials=True, # 允许携带cookie
    allow_methods=["*"],   # 允许的HTTP方法列表
    allow_headers=["*"],   # 允许的HTTP请求头列表
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# 挂载路由/注册路由
app.include_router(router=news.router)
app.include_router(router=users.router)
