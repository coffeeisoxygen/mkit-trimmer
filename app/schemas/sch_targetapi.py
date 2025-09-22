"""schemas for making api target."""

from pydantic import AnyHttpUrl, BaseModel, Field


class TargetAPIBaseConfig(BaseModel):
    """base config for target api schema."""

    model_config = {
        "populate_by_name": True,
        "from_attributes": True,
    }


class TargetApiCommonFields(TargetAPIBaseConfig):
    """common fields for target api."""

    base_url: AnyHttpUrl = Field(description="base url for target api", max_length=200)
    username: str = Field(description="username api on target", max_length=100)
    password: str = Field(description="password api on target", max_length=100)
    pin: str | None = Field(description="pin api on target", max_length=10)
    email: str | None = Field(description="email api on target", max_length=100)
    msisdn: str | None = Field(description="msisdn api on target", max_length=15)
    time_out: int = Field(description="timeout in seconds", ge=1, le=60)
    retries: int = Field(description="number of retries", ge=0, le=5)


class TargetApiCreate(TargetApiCommonFields):
    """schema for creating a target api."""

    is_active: bool = Field(description="is target api active?", default=True)

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "base_url": "http://example.com/api",
                    "username": "user1",
                    "password": "pass123",
                    "pin": "1234",
                    "email": "user1@example.com",
                    "msisdn": "1234567890",
                    "time_out": 30,
                    "retries": 3,
                    "is_active": True,
                }
            ]
        },
    }


class TargetApiINDB(TargetApiCommonFields):
    """schema for reading a target api."""

    id: int = Field(description="target api id from database", ge=1)
    is_active: bool = Field(description="is target api active?")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "base_url": "http://example.com/api",
                    "username": "user1",
                    "password": "pass123",
                    "pin": "1234",
                    "email": "user1@example.com",
                    "msisdn": "1234567890",
                    "time_out": 30,
                    "retries": 3,
                    "is_active": True,
                }
            ]
        },
    }


class TargetApiUpdate(TargetAPIBaseConfig):
    """schema for updating a target api."""

    base_url: AnyHttpUrl | None = Field(
        description="base url for target api", max_length=200
    )
    username: str | None = Field(description="username api on target", max_length=100)
    password: str | None = Field(description="password api on target", max_length=100)
    pin: str | None = Field(description="pin api on target", max_length=10)
    email: str | None = Field(description="email api on target", max_length=100)
    msisdn: str | None = Field(description="msisdn api on target", max_length=15)
    time_out: int | None = Field(description="timeout in seconds", ge=1, le=60)
    retries: int | None = Field(description="number of retries", ge=0, le=5)

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "base_url": "http://example.com/api",
                    "username": "user1",
                    "password": "pass123",
                    "pin": "1234",
                    "email": "user1@example.com",
                    "msisdn": "1234567890",
                    "time_out": 30,
                    "retries": 3,
                }
            ]
        },
    }
