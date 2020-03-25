from fastapi import APIRouter

# Create the router.
router = APIRouter()

# The routes.
from . import latest, sources, locations # isort:skip
