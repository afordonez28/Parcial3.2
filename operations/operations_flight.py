from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.flight import Flight
from models.reservation import Reservation

async def list_available_flights(db: AsyncSession):
    query = select(Flight).where(Flight.disponible == True)
    result = await db.execute(query)
    return result.scalars().all()

async def reserve_flight(db: AsyncSession, user_id: int, pet_id: int, flight_id: int):
    flight = await db.get(Flight, flight_id)
    if not flight or not flight.disponible or flight.asientos <= 0:
        return "No disponible"
    reserva = Reservation(user_id=user_id, pet_id=pet_id, flight_id=flight_id, pagada=False)
    flight.asientos -= 1
    if flight.asientos == 0:
        flight.disponible = False
    db.add(reserva)
    await db.commit()
    await db.refresh(reserva)
    return reserva

async def buy_flight(db: AsyncSession, reserva_id: int):
    reserva = await db.get(Reservation, reserva_id)
    if not reserva or reserva.pagada:
        return "Reserva no encontrada o ya pagada"
    reserva.pagada = True
    await db.commit()
    await db.refresh(reserva)
    return reserva