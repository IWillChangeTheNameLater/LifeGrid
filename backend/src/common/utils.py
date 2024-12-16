from functools import partial
from typing import Any

from pydantic import AfterValidator, BaseModel, BeforeValidator


def convert_dict_to_model(
    data: dict[str, Any]|BaseModel, *, model: type[BaseModel]
) -> BaseModel:
    if isinstance(data, BaseModel):
        return data
    return model(**data)


def convert_dict_to_model_validator_factory(
    model: type[BaseModel]
) -> BeforeValidator:
    return BeforeValidator(partial(convert_dict_to_model, model=model))


def convert_model_to_dict(model: BaseModel|dict) -> dict[str, Any]:
    if isinstance(model, dict):
        return model
    return model.model_dump(
        mode='json',
        exclude_none=True,
        exclude_unset=True,
        exclude_defaults=True
    )


DictToModelValidator = convert_dict_to_model_validator_factory
ModelToDictValidator = AfterValidator(convert_model_to_dict)
