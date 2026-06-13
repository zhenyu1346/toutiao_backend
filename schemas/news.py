from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict, field_serializer


class NewsBaseInfo(BaseModel):
    """新闻基础信息"""
    id: int
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    author: Optional[str] = None
    views: int
    publish_time: datetime = Field(..., alias="publishTime")
    category_id: int = Field(..., alias="categoryId")

    @field_serializer('publish_time')
    def serialize_publish_time(self, value: datetime) -> str | None:
        return value.strftime("%Y-%m-%d %H:%M:%S") if value else None


class NewsItemResponse(NewsBaseInfo):
    """新闻条目（列表项/相关新闻）"""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class NewsListResponse(BaseModel):
    """新闻列表响应"""
    news_list: List[NewsItemResponse] = Field(..., alias="list")
    total: int
    has_more: bool = Field(..., alias="hasMore")

    model_config = ConfigDict(populate_by_name=True)


class NewsDetailResponse(NewsBaseInfo):
    """新闻详情响应"""
    content: str
    related_news: List[NewsItemResponse] = Field(..., alias="relatedNews")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
