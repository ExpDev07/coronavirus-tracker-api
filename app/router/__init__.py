from fastapi import APIRouter

from .v1 import all, confirmed, deaths, recovered

# The routes.
from .v2 import latest, sources, locations  # isort:skip
