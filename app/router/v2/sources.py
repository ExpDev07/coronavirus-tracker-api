"""app.router.v2.sources.py"""
from ...data import DATA_SOURCES
from . import V2


@V2.get("/sources")
async def sources():
    """
    Retrieves a list of data-sources that are availble to use.
    """
    return {"sources": list(DATA_SOURCES.keys())}
