class MetricsProvider():
    """
    Gets latest global metrics from the given source
    """
    async def get_latest_global(self, source):
        locations = await source.get_all()
        return {
            "latest": {
                "confirmed": sum(map(lambda location: location.confirmed, locations)),
                "deaths": sum(map(lambda location: location.deaths, locations)),
                "recovered": sum(map(lambda location: location.recovered, locations)),
            }
        }

    """
    Gets the available locations for a given source, params and with timeline (if requested)
    """
    async def get_available_locations(self, source, params, timelines):
        # Retrieve all the locations.
        locations = await source.get_all()

        # Attempt to filter out locations with properties matching the provided query params.
        for key, value in params.items():
            # Clean keys for security purposes.
            key = key.lower()
            value = value.lower().strip("__")

            # Do filtering.
            try:
                locations = [
                    location
                    for location in locations
                    if str(getattr(location, key)).lower() == str(value)
                ]
            except AttributeError:
                pass
            if not locations:
                raise Exception(
                    detail=f"Source `{source}` does not have the desired location data.",
                )

        # Return final serialized data.
        return {
            "latest": {
                "confirmed": sum(map(lambda location: location.confirmed, locations)),
                "deaths": sum(map(lambda location: location.deaths, locations)),
                "recovered": sum(map(lambda location: location.recovered, locations)),
            },
            "locations": [location.serialize(timelines) for location in locations],
        }

    """
    Gets the location data by id
    """    
    async def get_location_by_id(self, source, id, timelines):
        location = await source.get(id)
        return {"location": location.serialize(timelines)}