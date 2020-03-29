from ...services.location.jhu import get_category
from . import router


@router.get("/deaths")
def deaths():
    deaths = get_category("deaths")
    
    return deaths
