from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.pet import Pet
import os
import csv
import aiofiles
import io

CSV_FOLDER = "./csv"
PETS_CSV = os.path.join(CSV_FOLDER, "mascotas.csv")
PETS_HEADERS = ["id", "nombre", "duenio", "tipo_mascota", "raza"]

async def create_pet(db: AsyncSession, pet: Pet):
    db.add(pet)
    await db.commit()
    await db.refresh(pet)
    os.makedirs(CSV_FOLDER, exist_ok=True)
    archivo_existe = os.path.exists(PETS_CSV)
    async with aiofiles.open(PETS_CSV, mode="a", newline="", encoding="utf-8") as archivo:
        buffer = io.StringIO()
        writer = csv.DictWriter(buffer, fieldnames=PETS_HEADERS)
        if not archivo_existe or os.stat(PETS_CSV).st_size == 0:
            writer.writeheader()
        writer.writerow({
            "id": pet.id,
            "nombre": pet.nombre,
            "duenio": pet.duenio,
            "tipo_mascota": pet.tipo_mascota,
            "raza": pet.raza
        })
        await archivo.write(buffer.getvalue())
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