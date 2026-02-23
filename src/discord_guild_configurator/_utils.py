from pydantic import BaseModel, ConfigDict  # noqa: TID251 (plain BaseModel)


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
