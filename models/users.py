from sqlalchemy import Integer, String, Index, DateTime, Enum, ForeignKey
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column,DeclarativeBase


"""-- 用户表
CREATE TABLE IF NOT EXISTS `user` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `username` VARCHAR(50) NOT NULL COMMENT '用户名',
  `password` VARCHAR(255) NOT NULL COMMENT '密码（加密存储）',
  `nickname` VARCHAR(50) NULL DEFAULT NULL COMMENT '昵称',
  `avatar` VARCHAR(255) NULL DEFAULT NULL COMMENT '头像URL',
  `gender` ENUM('male', 'female', 'unknown') NULL DEFAULT 'unknown' COMMENT '性别',
  `bio` VARCHAR(500) NULL DEFAULT NULL COMMENT '个人简介',
  `phone` VARCHAR(20) NULL DEFAULT NULL COMMENT '手机号',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC),
  UNIQUE INDEX `phone_UNIQUE` (`phone` ASC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户信息表';
"""
class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        comment='创建时间'
    )

class User(Base):
    __tablename__ = "user"

    # 创建索引
    __table_args__ = (
        Index('username_UNIQUE', 'username'),
        Index('phone_UNIQUE', 'phone'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment='用户ID')
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment='用户名')
    password: Mapped[str] = mapped_column(String(255), nullable=False, comment='密码（加密存储）')
    nickname: Mapped[Optional[str]] = mapped_column(String(50), comment='昵称')
    avatar: Mapped[Optional[str]] = mapped_column(String(255), comment='头像URL')
    gender: Mapped[str] = mapped_column(Enum('male', 'female', 'unknown'), nullable=False, default='unknown', comment='性别')
    bio: Mapped[Optional[str]] = mapped_column(String(500), comment='个人简介')
    phone: Mapped[Optional[str]] = mapped_column(String(20), unique=True, comment='手机号')
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

"""
CREATE TABLE IF NOT EXISTS `user_token` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '令牌ID',
  `user_id` INT UNSIGNED NOT NULL COMMENT '用户ID',
  `token` VARCHAR(255) NOT NULL COMMENT '令牌值',
  `expires_at` TIMESTAMP NOT NULL COMMENT '过期时间',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `token_UNIQUE` (`token` ASC),
  INDEX `fk_user_token_user_idx` (`user_id` ASC),
  CONSTRAINT `fk_user_token_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `user` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户令牌表';
"""
class UserToken(Base):
    __tablename__ = "user_token"

    # 创建索引
    __table_args__ = (
        Index('token_UNIQUE', 'token'),
        Index('fk_user_token_user_idx', 'user_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment='令牌ID')
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False, comment='用户ID')
    token: Mapped[str] = mapped_column(String(255), nullable=False, comment='令牌值')
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment='过期时间')