"""app.data"""
from ..services.location.csbs import CSBSLocationService
from ..services.location.jhu import JhuLocationService
from ..services.location.nyt import NYTLocationService

class data_provide:
    dataProvide = {}

def default_set (this):
    this.dataProvide['nyt'] = NYTLocationService()
    this.dataProvide['csbs'] = CSBSLocationService()
    this.dataProvide['jhu'] = JhuLocationService()

def get_data_provide(this, provide):
    return this.dataProvide.get(source.lower())

