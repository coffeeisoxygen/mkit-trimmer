"""pydantic schema for member."""

from pydantic import BaseModel, Field, HttpUrl, IPvAnyAddress


class MemberBaseConfig(BaseModel):
    """base config for member schema."""

    model_config = {
        "populate_by_name": True,
        "from_attributes": True,
    }


class MemberCreate(MemberBaseConfig):
    """schema for creating a member."""

    name: str = Field(description="member name", max_length=100)
    ip_address: IPvAnyAddress = Field(description="member IP address")
    report_url: HttpUrl = Field(description="member report URL", max_length=200)
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "name": "member1",
                    "ip_address": "192.168.1.1",
                    "report_url": "http://example.com/report",
                },
            ]
        },
    }


class MemberInDB(MemberCreate):
    """schema for member in database."""

    id: int = Field(description="memberid dari database", ge=1)
    is_active: bool = Field(description="is member active?")
    rate_limit: int = Field(description="rate limit in seconds")
    rl_interval: str = Field(description="satuan rate limit")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "name": "member1",
                    "ip_address": "192.168.1.1",
                    "report_url": "http://example.com/report",
                    "is_active": True,
                    "rate_limit": 1,
                    "rl_interval": "second",
                },
            ]
        },
    }


class MemberUpdate(MemberBaseConfig):
    """schema for updating a member."""

    name: str | None = Field(description="member name", max_length=100)
    ip_address: IPvAnyAddress | None = Field(description="member IP address")
    report_url: HttpUrl | None = Field(description="member report URL", max_length=200)


class MemberAdminUpdate(MemberBaseConfig):
    """schema for admin to update a member."""

    name: str | None = Field(description="member name", max_length=100)
    ip_address: IPvAnyAddress | None = Field(description="member IP address")
    report_url: HttpUrl | None = Field(description="member report URL", max_length=200)
    is_active: bool | None = Field(description="is member active?")
    rate_limit: int | None = Field(description="rate limit in seconds")
    rl_interval: str | None = Field(description="satuan rate limit")
