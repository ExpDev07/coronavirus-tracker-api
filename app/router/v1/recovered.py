from ...services.location.jhu import get_category
from . import router


@router.get("/recovered")
def recovered():
    recovered = get_category("recovered")
    
    return recovered
