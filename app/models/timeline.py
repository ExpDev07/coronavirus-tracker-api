from typing import Dict

from pydantic import BaseModel


class Timeline(BaseModel):
    """
    Timeline model.
    """

    latest: int
    timeline: Dict[str, int] = {}


class Timelines(BaseModel):
    """
    Timelines model.
    """

    confirmed: Timeline
    deaths: Timeline
    recovered: Timeline
