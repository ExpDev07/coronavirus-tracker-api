from fastapi import APIRouter

# The routes.
from .v2 import latest, sources, locations  # isort:skip
from .v1 import confirmed, deaths, recovered, all
