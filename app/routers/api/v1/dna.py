from fastapi import APIRouter
from app.shemas.dna import Dna
router = APIRouter()


@router.post("/")
def dna(dna: Dna):
    return None
