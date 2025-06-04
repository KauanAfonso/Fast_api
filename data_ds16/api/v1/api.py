from fastapi import APIRouter
from api.v1.endpoints import profissao, local

api_router = APIRouter()

api_router.include_router(profissao.router, prefix="/profissao", tags=["Profissão"])
api_router.include_router(local.router, prefix="/local", tags=["Local"])