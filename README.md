# AI头条新闻系统

![Python](attachment/1.svg "Python")

![FastAPI](attachment/2.svg "FastAPI")

![MySQL](attachment/3.svg "MySQL")

![License](attachment/4.svg "License")

![Build](attachment/5.svg "Build")

一个基于 FastAPI 和 SQLAlchemy 构建的现代化、高性能异步新闻系统后端，提供完整的用户管理、新闻浏览、收藏和历史记录功能。

## ✨ 核心特性

* **高性能异步架构**：基于 FastAPI & Python asyncio，提供出色的并发处理能力
* **现代化的技术栈**：使用异步 SQLAlchemy ORM、Redis 缓存、bcrypt 密码加密
* **模块化设计**：清晰的代码结构，遵循单一职责原则，便于扩展和维护
* **完善的功能模块**：涵盖用户、新闻、收藏、历史、缓存等核心业务场景
* **专业的缓存策略**：多级缓存设计，显著提升系统响应速度与吞吐量
* **完整的安全保障**：密码加密存储、JWT 令牌认证、SQL 注入防护

## 🚀 快速开始

### 环境要求

* Python 3.8+
* MySQL 8.0+
* Redis 5.0+

### 安装步骤

1. **克隆项目**

```bash
git clone https://github.com/zhenyu1346/toutiao_backend.git
cd toutiao_backend
```

2. **启动服务**

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

启动后访问 `http://localhost:8000/docs` 查看完整的交互式 API 文档。

## 📚 API 接口示例

### 用户认证

```http
POST /api/user/register
Content-Type: application/json

{
  "username": "testuser",
  "password": "securepassword123",
  "nickname": "测试用户"
}
```

```http
POST /api/user/login
Content-Type: application/json

{
  "username": "testuser",
  "password": "securepassword123"
}
```

### 新闻浏览

```http
GET /api/news?category_id=1&page=1&size=20
Authorization: Bearer {access_token}
```

```http
GET /api/news/{news_id}
Authorization: Bearer {access_token}
```

### 收藏管理

```http
POST /api/favorites
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "news_id": 123
}
```

```http
GET /api/favorites
Authorization: Bearer {access_token}
```

完整的 API 接口文档可通过 Swagger UI (`/docs`) 或 ReDoc (`/redoc`) 查看。

## 🏗️ 项目结构

```
toutiao_backend/
├── crud/                           # 数据访问层 (CRUD 操作)
│   ├── favorite.py                 # 收藏相关数据库操作
│   ├── history.py                  # 历史记录相关数据库操作
│   ├── news.py                     # 新闻相关数据库操作
│   └── users.py                    # 用户相关数据库操作
│
├── models/                         # SQLAlchemy 数据模型定义
│   ├── favorite.py                 # 收藏数据模型
│   ├── history.py                  # 历史记录数据模型
│   ├── news.py                     # 新闻数据模型
│   ├── users.py                    # 用户数据模型
│   └── base.py                     # 基础模型类
│
├── routers/                        # API 路由定义
│   ├── favorite.py                 # 收藏相关路由
│   ├── history.py                  # 历史记录相关路由
│   ├── news.py                     # 新闻相关路由
│   ├── users.py                    # 用户相关路由
│   └── __init__.py
│
├── schemas/                        # Pydantic 数据验证模型
│   ├── favorite.py                 # 收藏数据验证模型
│   ├── history.py                  # 历史记录数据验证模型
│   ├── news.py                     # 新闻数据验证模型
│   ├── users.py                    # 用户数据验证模型
│   └── __init__.py
│
├── utils/                          # 工具函数
│   ├── auth.py                     # 认证工具
│   ├── cache.py                    # 缓存工具
│   └── __init__.py
│
├── config/                         # 配置文件
│   ├── db_conf.py                  # 数据库配置
│   ├── cache_conf.py               # Redis 缓存配置
│   └── __init__.py
│
├── requirements.txt                # 项目依赖
├── main.py                         # 应用入口文件
├── init_db.py                      # 数据库初始化脚本
├── .env.example                    # 环境变量示例
└── README.md                       # 项目说明文档
```

## 🗄️ 数据库设计

### 核心数据表

| **表名**          | **说明** | **关键字段**                                                                      |
| --------------- | ------ | ----------------------------------------------------------------------------- |
| `user`          | 用户表    | `id`, `username`, `password_hash`, `nickname`, `avatar`, `created_at`         |
| `user_token`    | 用户令牌表  | `id`, `user_id`, `token`, `expires_at`, `created_at`                          |
| `news_category` | 新闻分类表  | `id`, `name`, `description`, `sort_order`                                     |
| `news`          | 新闻表    | `id`, `title`, `content`, `author`, `category_id`, `view_count`, `created_at` |
| `favorite`      | 收藏表    | `id`, `user_id`, `news_id`, `created_at`                                      |
| `history`       | 浏览历史表  | `id`, `user_id`, `news_id`, `viewed_at`                                       |

## ⚡ 缓存策略

系统采用 Redis 作为缓存层，对高频访问的数据进行缓存，显著提升系统性能和响应速度。

### 缓存类型与策略

| **数据类型** | **缓存键格式**                               | **过期时间** | **作用**         |
| -------- | --------------------------------------- | -------- | -------------- |
| 新闻详情     | `news:detail:{news_id}`                 | 1小时      | 提升新闻详情页访问速度    |
| 新闻列表     | `news:list:{category_id}:{page}:{size}` | 30分钟     | 减少首页和分类页数据查询压力 |
| 分类数据     | `news:categories`                       | 2小时      | 加速导航栏分类数据加载    |
| 用户历史     | `history:list:{user_id}`                | 2小时      | 提高用户历史记录访问性能   |

### 缓存更新机制

* **数据更新时自动清除相关缓存**：当新闻内容更新时，自动清除对应的详情缓存和列表缓存
* **采用缓存失效而非主动更新策略**：保证数据最终一致性
* **支持批量清除特定模式的缓存**：使用 Redis 的 `SCAN` 命令进行模式匹配删除

## 🤝 贡献指南

我们欢迎任何形式的贡献！请遵循以下步骤：

1. **Fork 本仓库**
2. **创建功能分支** (`git checkout -b feature/amazing-feature`)
3. **提交更改** (`git commit -m 'Add some amazing feature'`)
4. **推送到分支** (`git push origin feature/amazing-feature`)
5. **开启 Pull Request**

### 开发规范

* 遵循 [PEP 8](https://peps.python.org/pep-0008/) Python 代码规范
* 使用类型注解（Type Hints）
* 为新增功能编写单元测试
* 更新相关文档

## 📄 许可证

本项目基于 [MIT](LICENSE) 许可证开源。

***

⭐ **如果这个项目对你有帮助，请给我们一个 Star！** ⭐

| **接口**               | **方法** | **说明**   |
| -------------------- | ------ | -------- |
| /api/news/categories | GET    | 获取新闻分类列表 |
| /api/news/list       | GET    | 获取新闻列表   |
| /api/news/detail     | GET    | 获取新闻详情   |

### 收藏相关接口

| **接口**               | **方法** | **说明**   |
| -------------------- | ------ | -------- |
| /api/favorite/check  | GET    | 检查新闻收藏状态 |
| /api/favorite/add    | POST   | 添加收藏     |
| /api/favorite/remove | DELETE | 取消收藏     |
| /api/favorite/list   | GET    | 获取收藏列表   |
| /api/favorite/clear  | DELETE | 情况所有收藏   |

### 浏览历史相关接口

| 接口                                 | 方法     | 说明       |
| ---------------------------------- | ------ | -------- |
| /api/history/add                   | POST   | 添加浏览记录   |
| /api/history/list                  | GET    | 获取浏览历史列表 |
| /api/history/delete/\{history\_id} | DELETE | 删除单条浏览记录 |
| /api/history/clear                 | DELETE | 清空浏览历史   |

## 1-8 认证机制

系统使用基于令牌（Token）的认证机制：

1、用户登录成功后返回访问令牌

2、需要认证的接口的请求头添加Authorization：token值

3、令牌有效期7天

## 1-9 错误处理

系统提供统一的错误处理机制：

* 用户认证失败返回401状态码
* 资源不存在返回404状态码
* 服务器内部错误返回500状态码

## 1-10 开发规范

* 使用异步数据库操作
* 所有密码均加密存储
* 接口返回统一的JSON格式
* 详细的接口文档和示例
* 缓存操作封装成独立函数便于调用

## 1-11 性能优化

* 使用Redis缓存热点数据
* 异步数据库操作提升并发性能
* 合理的数据库索引设计
* 连接池管理减少连接开销
