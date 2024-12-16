from pydantic import BaseModel


class Vices(BaseModel):
    smoking: bool
    drinking: bool
    drugs: bool


class BMI(BaseModel):
    weight_kg: float
    height_cm: float


class UserProfile(BaseModel):
    vices: Vices
    bmi: BMI
    hours_of_sleep: float
    single: bool
