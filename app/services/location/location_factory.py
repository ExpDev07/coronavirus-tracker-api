"""app.services.location.location_factory.py"""

class LocationFactory:
    def get_location(source):
        if source == 'csbs':
            return CSBSLocationService()

        elif source == 'nyt'
            return NYTLocationService()

        elif source == 'jhu':
            return JhuLocationService()