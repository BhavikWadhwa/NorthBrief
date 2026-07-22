from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl


class HealthResponse(BaseModel):
    status: str
    app: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    display_name: str = Field(min_length=2, max_length=80)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str
    display_name: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str
    display_name: str
    is_admin: bool


class PreferenceUpdate(BaseModel):
    country: str = "Canada"
    province: str | None = None
    city: str | None = None
    category_codes: list[str] = Field(default_factory=list)
    local_global_weight: float = Field(default=0.7, ge=0.0, le=1.0)
    finance_weight: float = Field(default=0.4, ge=0.0, le=1.0)
    skip_personalization: bool = False


class FeedItem(BaseModel):
    id: str
    headline: str
    summary: str
    why_this_matters: str
    key_impact: str | None
    category: str
    region: str | None
    source_name: str
    source_domain: str | None
    published_at: datetime | None
    canonical_url: str
    image_url: str | None
    rank_score: float


class FeedResponse(BaseModel):
    items: list[FeedItem]
    total: int


class BookmarkCreate(BaseModel):
    processed_article_id: str


class SourceResponse(BaseModel):
    id: str
    name: str
    feed_url: str
    site_url: str | None
    source_type: str
    default_region_code: str | None
    default_category_code: str | None
    priority: float
    is_active: bool
    last_fetched_at: datetime | None
    last_status: str | None
    failure_count: int


class SourceCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    source_type: str = Field(default="rss")
    feed_url: HttpUrl
    site_url: HttpUrl | None = None
    default_region_code: str | None = None
    default_category_code: str | None = None
    priority: float = Field(default=0.5, ge=0, le=1)
    is_active: bool = True


class SourceUpdate(BaseModel):
    is_active: bool | None = None
    default_region_code: str | None = None
    default_category_code: str | None = None
    priority: float | None = Field(default=None, ge=0, le=1)


class AdminIngestionResponse(BaseModel):
    run_id: str
    status: str
    fetched_count: int
    inserted_count: int
    deduped_count: int
    error_count: int
