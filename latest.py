
class Outbreak:
    #Aggregate root
    def change_latest(self, time):
        try:
            if Timeline.latest != time:
                return Latest()
            else:
                raise ValueError
        except ValueError:
            print("latest data is not changed")


##########################################################################################

class Timeline(BaseModel):
    """
    Timeline model.
    """

    timeline: Dict[str, int] = {}

    @validator("timeline")
    @classmethod
    def sort_timeline(cls, value):
        """Sort the timeline history before inserting into the model"""
        return dict(sorted(value.items()))

    @property
    def latest(self):
        """Get latest available history value."""
        return list(self.timeline.values())[-1] if self.timeline else 0

    def serialize(self):
        """
        Serialize the model into dict
        TODO: override dict() instead of using serialize
        """
        return {**self.dict(), "latest": self.latest}


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
