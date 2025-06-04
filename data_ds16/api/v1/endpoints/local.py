from typing import List
from fastapi import APIRouter, Response, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.future import select
from models.local_model import LocalModel
from schemas.local_shemas import LocalSchema
from core.deps import get_session

router = APIRouter()

@router.post("/", status_code=status.HTTP_200_OK, response_model=LocalSchema)
async def post_local(local:LocalSchema, db: AsyncConnection = Depends(get_session)):
    novo_local = LocalModel(
        nome=local.nome,
        relacao=local.relacao,
        foto=local.foto
    )

    db.add(novo_local)
    await db.commit()
    return novo_local

@router.post("/", response_model=list[LocalSchema])
async def get_locais(db: AsyncConnection = Depends(get_session)):
    async with db as session:
        query = select(LocalModel)
        result = await session.execute(query)
        locais: list[LocalModel] = result.scalars.all()

        return locais

@router.get("/{local_id}", response_model=LocalSchema)
async def get_local(local_id: int, db: AsyncConnection = Depends(get_session)):
    async with db as session:
        query = select(LocalModel).filter(LocalModel.id == local_id)
        result = await session.execute(query)
        local = result.scalar_one_or_none()

        if local:
            return local
        raise HTTPException(detail="Local não encontrado !", status_code=status.HTTP_404_NOT_FOUND)
    
@router.put("/{local_id}", response_model=LocalSchema)
async def put_local(local_id: int, local: LocalSchema, db: AsyncConnection = Depends(get_session)):
    async with db as session:
        query = select(LocalModel).filter(LocalModel.id == local.id)
        result = await session.execute(query)
        local_up = result.scalar_one_or_none()

        if local_up:
            local_up.nome = local.nome
            local_up.relacao = local.relacao
            local_up.foto = local.foto

            session.add(local_up)
            await session.commit()
            return local_up
        
        else:
            raise HTTPException(detail="Local não encontrada", status_code=status.HTTP_404_NOT_FOUND)

@router.delete("/{local_id}", response_model=LocalSchema, status_code=status.HTTP_404_NOT_FOUND)
async def delete_local(local_id:int, db:AsyncConnection = Depends(get_session)):
    async with db as session:
        query = select(LocalModel).filter(LocalModel.id == local_id)
        result = await session.execute(query)
        local_delete = result.scalar_one_or_none()

        if local_delete:
            await session.delete(local_delete)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Local não encontrado", status_code=status.HTTP_404_NOT_FOUND)