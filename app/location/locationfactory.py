import datetime

from app.coordinates import Coordinates
from app.location import TimelinedLocation
from app.location.csbs import CSBSLocation
from app.location.nyt import NYTLocation
from app.models import Timeline


class LocationFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_location(org_name, params):
        if org_name == 'NYT':
            confirmed_history = params["confirmed_history"]
            deaths_history = params["deaths_history"]
            return NYTLocation(
                id=params["index"],
                state=params["county_state"][1],
                county=params["county_state"][0],
                coordinates=Coordinates(None, None),  # NYT does not provide coordinates
                last_updated=datetime.utcnow().isoformat() + "Z",  # since last request
                timelines={
                    "confirmed": Timeline(
                        timeline={
                            datetime.strptime(date, "%Y-%m-%d").isoformat() + "Z": amount
                            for date, amount in confirmed_history.items()
                        }
                    ),
                    "deaths": Timeline(
                        timeline={
                            datetime.strptime(date, "%Y-%m-%d").isoformat() + "Z": amount
                            for date, amount in deaths_history.items()
                        }
                    ),
                    "recovered": Timeline(),
                },
            )
        elif org_name == "JHU":
            timelines = params["timelines"];
            return TimelinedLocation(
                # General info.
                params["index"],
                params["country"],
                params["province"],
                # Coordinates.
                Coordinates(latitude=params["coordinates"]["lat"], longitude=params["coordinates"]["long"]),
                # Last update.
                datetime.utcnow().isoformat() + "Z",
                # Timelines (parse dates as ISO).
                {
                    "confirmed": Timeline(
                        timeline={
                            datetime.strptime(date, "%m/%d/%y").isoformat() + "Z": amount
                            for date, amount in timelines["confirmed"].items()
                        }
                    ),
                    "deaths": Timeline(
                        timeline={
                            datetime.strptime(date, "%m/%d/%y").isoformat() + "Z": amount
                            for date, amount in timelines["deaths"].items()
                        }
                    ),
                    "recovered": Timeline(
                        timeline={
                            datetime.strptime(date, "%m/%d/%y").isoformat() + "Z": amount
                            for date, amount in timelines["recovered"].items()
                        }
                    ),
                },
            )
        elif org_name == "CSBS":
            item = params["item"]
            return CSBSLocation(
                    # General info.
                    params["index"],
                    params["state"],
                    params["county"],
                    # Coordinates.
                    Coordinates(item["Latitude"], item["Longitude"]),
                    # Last update (parse as ISO).
                    datetime.strptime(params["last_update"], "%Y-%m-%d %H:%M").isoformat() + "Z",
                    # Statistics.
                    int(item["Confirmed"] or 0),
                    int(item["Death"] or 0),
                )
