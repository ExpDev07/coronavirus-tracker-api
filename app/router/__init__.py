from fastapi import APIRouter

# Create the router.
router = APIRouter()

# The routes.
from .v2 import latest, sources, locations  # isort:skip
