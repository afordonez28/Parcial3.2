from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User

async def create_user(db: AsyncSession, user: User):
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def find_user_doc(db: AsyncSession, documento: str):
    result = await db.execute(select(User).where(User.documento == documento))
    return result.scalar_one_or_none()

async def update_user(db: AsyncSession, id: int, datos_actualizados: dict):
    user = await db.get(User, id)
    if not user:
        return None
    for key, value in datos_actualizados.items():
        if hasattr(user, key) and key != "id":
            setattr(user, key, value)
    await db.commit()
    await db.refresh(user)
    return user

async def delete_user(db: AsyncSession, id: int):
    user = await db.get(User, id)
    if user:
        await db.delete(user)
        await db.commit()
    return user