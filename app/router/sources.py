from . import router
from ..data import data_sources


@router.get("/sources")
async def sources():
    """
    Retrieves a list of data-sources that are availble to use.
    """
    return {"sources": list(data_sources.keys())}
