from typing import List 
from fastapi import APIRouter, status, HTTPException, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.profissao_model import ProfissaoModel
from schemas.profissao_schemas import ProfissaoSchema
from core.deps import get_session

router = APIRouter()# igual app = fastApi()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProfissaoSchema)
async def post_profssao(profissao: ProfissaoSchema, db: AsyncSession = Depends(get_session)):
    nova_profissao = ProfissaoModel(nome=profissao.nome,
                                    area=profissao.area,
                                    formacao=profissao.formacao,
                                    salario=profissao.salario,
                                    foto=profissao.foto
                                    )
    db.add(nova_profissao)
    await db.commit()
    return nova_profissao

@router.get("/", response_model=list[ProfissaoSchema])
async def get_profissoes(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProfissaoModel)
        result = await session.execute(query) #execute a query
        profissoes: list[ProfissaoModel] = result.scalars().all() #Pegar todos os dados

        return profissoes
    
@router.get("/{profissao_id}", response_model=ProfissaoSchema)
async def get_profissao(profissao_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProfissaoModel).filter(ProfissaoModel.id == profissao_id)
        result = await session.execute(query)
        profissao = result.scalar_one_or_none()

        if profissao:
            return profissao
        else:
            raise HTTPException(detail="Profissão não encontrada", status_code=status.HTTP_404_NOT_FOUND)
        
@router.put("/{profissao_id}", response_model=ProfissaoSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_profissao(profissao_id: int, profissao: ProfissaoSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProfissaoModel).filter(ProfissaoModel.id == profissao_id)
        result = await session.execute(query)
        profissao_up = result.scalar_one_or_none()

    if profissao_up:
        profissao_up.nome = profissao.nome
        profissao_up.area = profissao.area
        profissao_up.formacao = profissao.formacao
        profissao_up.salario = profissao.salario
        profissao_up.foto = profissao.foto

        session.add(profissao_up)
        await session.commit()
        return profissao_up
    else:
        raise HTTPException(detail="Profissão não encontrada", status_code=status.HTTP_404_NOT_FOUND)
    
@router.delete("/{profissao_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profissao(profissao_id:int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProfissaoModel).filter(ProfissaoModel.id == profissao_id)
        result = await session.execute(query)
        profissao_delete = result.scalar_one_or_none()

        if profissao_delete:
            await session.delete(profissao_delete)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Profissão não encontrada", status_code=status.HTTP_404_NOT_FOUND)