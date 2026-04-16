from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_pascal


class BaseSchema(BaseModel):
    """Базовая схема с поддержкой PascalCase полей (совместимость с C# клиентом).
    Принимает: {"Login": "...", "Password": "..."}
    Отдаёт:    {"Login": "...", "RoleName": "..."}
    """
    model_config = ConfigDict(
        alias_generator=to_pascal,
        populate_by_name=True,
    )
