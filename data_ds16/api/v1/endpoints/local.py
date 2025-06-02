from typing import List
from fastapi import APIRouter, Response, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.future import select
from models.local_model import LocalModel
from schemas.local_shemas import LocalSchema
from core.deps import getSession

router = APIRouter()

@router.post("/", status_code=status.HTTP_200_OK, response_model=LocalSchema)
async def criar_local(local:LocalSchema, db: AsyncConnection = Depends(getSession)):
    pass