from functools import partial
from typing import Annotated

from pydantic import AfterValidator
from sqlmodel import Field
from ulid import ULID


ULIDStr = Annotated[str, AfterValidator(lambda v: str(ULID.from_str(v)))]

ULIDField = partial(
    Field,
    default_factory=lambda: str(ULID()),
    max_length=26,
    min_length=26,
)
