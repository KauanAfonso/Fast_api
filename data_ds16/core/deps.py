'''

Esse arquivo gerenciará as sessões de 
dependencias com o banco.

Nossa api só irá funcionar se a sessão estiver
aberta.


'''

from typing import Generator
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import Session

async def get_session() -> Generator:
    session: AsyncSession = Session()
    #abre e fecha a sessão
    try:
        yield session
    finally:
        await session.close()