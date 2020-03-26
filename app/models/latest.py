from pydantic import BaseModel


class Latest(BaseModel):
    """
    Latest model.
    """

    confirmed: int
    deaths: int
    recovered: int


class LatestResponse(BaseModel):
    """
    Response for latest.
    """

    latest: Latest
