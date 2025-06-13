from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.flight import Flight

async def list_available_flights(db: AsyncSession, origen=None, destino=None, fecha=None):
    query = select(Flight).where(Flight.disponible == True)
    if origen:
        query = query.where(Flight.origen == origen)
    if destino:
        query = query.where(Flight.destino == destino)
    if fecha:
        query = query.where(Flight.fecha == fecha)
    result = await db.execute(query)
    return result.scalars().all()

async def reserve_flight(db: AsyncSession, user_id: int, pet_id: int, flight_id: int):
    flight = await db.get(Flight, flight_id)
    if not flight or not flight.disponible or flight.asientos <= 0:
        return "No disponible"
    flight.asientos -= 1
    if flight.asientos == 0:
        flight.disponible = False
    await db.commit()
    await db.refresh(flight)
    return "Reserva exitosa"

async def buy_flight(db: AsyncSession, reserva_id: int):
    # Aquí deberías buscar la reserva y marcarla como pagada, pero es un ejemplo
    return "Compra realizada"