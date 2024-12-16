from typing import Annotated

from sqlmodel import SQLModel

from common.utils import DictToModelValidator, ModelToDictValidator


class Vices(SQLModel):
    smoking: bool
    drinking: bool
    drugs: bool


class BMI(SQLModel):
    weight_kg: float
    height_cm: float


class UserProfile(SQLModel):
    vices: Vices|None = None
    bmi: BMI|None = None
    hours_of_sleep: float|None = None
    single: bool|None = None


UserProfileDict = Annotated[UserProfile,
                            DictToModelValidator(UserProfile),
                            ModelToDictValidator]
