from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.pet import Pet

async def create_pet(db: AsyncSession, pet: Pet):
    db.add(pet)
    await db.commit()
    await db.refresh(pet)
    return pet

async def find_pet_id(db: AsyncSession, id: int):
    result = await db.execute(select(Pet).where(Pet.id == id))
    return result.scalar_one_or_none()

async def update_pet(db: AsyncSession, id: int, datos_actualizados: dict):
    pet = await find_pet_id(db, id)
    if not pet:
        return None
    for key, value in datos_actualizados.items():
        if hasattr(pet, key) and key != "id":
            setattr(pet, key, value)
    await db.commit()
    await db.refresh(pet)
    return pet

async def delete_pet(db: AsyncSession, id: int):
    pet = await find_pet_id(db, id)
    if not pet:
        return None
    await db.delete(pet)
    await db.commit()
    return pet