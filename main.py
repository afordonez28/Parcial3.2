import os
import datetime
from fastapi import FastAPI, Request, Depends, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.future import select
from dotenv import load_dotenv

from models.user import User
from models.pet import Pet
from models.flight import Flight
from models.reservation import Reservation

from operations.operations_user import (
    create_user, find_user_doc, update_user, delete_user
)
from operations.operations_pet import (
    create_pet, find_pet_id, update_pet, delete_pet
)
from operations.operations_flight import (
    list_available_flights, reserve_flight, buy_flight
)

load_dotenv()
DATABASE_URL = (
    f"postgresql+asyncpg://{os.getenv('CLEVER_USER')}:{os.getenv('CLEVER_PASSWORD')}"
    f"@{os.getenv('CLEVER_HOST')}:{os.getenv('CLEVER_PORT')}/{os.getenv('CLEVER_DATABASE')}"
    "?command_timeout=60"
)
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)
templates = Jinja2Templates(directory="templates")

app = FastAPI()

async def get_db():
    async with async_session() as session:
        yield session

# Poblado automático de vuelos en el arranque si la tabla está vacía
@app.on_event("startup")
async def populate_flights():
    async with async_session() as db:
        result = await db.execute(select(Flight))
        flights = result.scalars().all()
        if not flights:
            vuelos = [
                Flight(origen="Bogotá", destino="Medellín", fecha=datetime.date(2025, 7, 10), disponible=True, asientos=12),
                Flight(origen="Medellín", destino="Bogotá", fecha=datetime.date(2025, 7, 13), disponible=True, asientos=9),
                Flight(origen="Cali", destino="Cartagena", fecha=datetime.date(2025, 7, 15), disponible=True, asientos=20),
                Flight(origen="Barranquilla", destino="Leticia", fecha=datetime.date(2025, 7, 16), disponible=True, asientos=3),
                Flight(origen="Bogotá", destino="Cali", fecha=datetime.date(2025, 7, 17), disponible=True, asientos=18),
                Flight(origen="Cali", destino="Bogotá", fecha=datetime.date(2025, 7, 18), disponible=True, asientos=13),
                Flight(origen="Medellín", destino="Cartagena", fecha=datetime.date(2025, 7, 22), disponible=True, asientos=15),
                Flight(origen="Cartagena", destino="Bogotá", fecha=datetime.date(2025, 7, 30), disponible=True, asientos=8),
                Flight(origen="Bogotá", destino="Barranquilla", fecha=datetime.date(2025, 8, 2), disponible=True, asientos=17),
                Flight(origen="Barranquilla", destino="Cali", fecha=datetime.date(2025, 8, 8), disponible=True, asientos=6),
                Flight(origen="Bogotá", destino="Leticia", fecha=datetime.date(2025, 8, 20), disponible=True, asientos=10),
                Flight(origen="Leticia", destino="Bogotá", fecha=datetime.date(2025, 8, 25), disponible=True, asientos=9),
                Flight(origen="Cali", destino="Medellín", fecha=datetime.date(2025, 8, 28), disponible=True, asientos=14),
                Flight(origen="Medellín", destino="Cali", fecha=datetime.date(2025, 9, 1), disponible=True, asientos=11),
                Flight(origen="Cartagena", destino="Barranquilla", fecha=datetime.date(2025, 9, 4), disponible=True, asientos=5),
                Flight(origen="Barranquilla", destino="Medellín", fecha=datetime.date(2025, 9, 10), disponible=True, asientos=7),
                Flight(origen="Leticia", destino="Cartagena", fecha=datetime.date(2025, 9, 15), disponible=True, asientos=4),
                Flight(origen="Cali", destino="Leticia", fecha=datetime.date(2025, 9, 20), disponible=True, asientos=8),
                Flight(origen="Medellín", destino="Barranquilla", fecha=datetime.date(2025, 9, 25), disponible=True, asientos=6),
                Flight(origen="Bogotá", destino="Cartagena", fecha=datetime.date(2025, 10, 1), disponible=True, asientos=12),
            ]
            db.add_all(vuelos)
            await db.commit()

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

# ---- CONTROL DE USUARIOS Y MASCOTAS ----
@app.get("/control")
async def control(request: Request, db: AsyncSession = Depends(get_db)):
    users = (await db.execute(select(User))).scalars().all()
    pets = (await db.execute(select(Pet))).scalars().all()
    return templates.TemplateResponse("control.html", {"request": request, "users": users, "pets": pets})

# CRUD USUARIOS
@app.post("/user/create")
async def create_user_post(request: Request, documento: str = Form(...), nombre: str = Form(...), db: AsyncSession = Depends(get_db)):
    user = User(documento=documento, nombre=nombre)
    await create_user(db, user)
    return RedirectResponse(url="/control", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/user/update")
async def update_user_post(request: Request, id: int = Form(...), nombre: str = Form(...), db: AsyncSession = Depends(get_db)):
    await update_user(db, id, {"nombre": nombre})
    return RedirectResponse(url="/control", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/user/delete")
async def delete_user_post(request: Request, id: int = Form(...), db: AsyncSession = Depends(get_db)):
    await delete_user(db, id)
    return RedirectResponse(url="/control", status_code=status.HTTP_303_SEE_OTHER)

# CRUD MASCOTAS
@app.post("/pet/create")
async def create_pet_post(request: Request, nombre: str = Form(...), duenio: str = Form(...), tipo_mascota: str = Form(...), raza: str = Form(...), db: AsyncSession = Depends(get_db)):
    pet = Pet(nombre=nombre, duenio=duenio, tipo_mascota=tipo_mascota, raza=raza)
    await create_pet(db, pet)
    return RedirectResponse(url="/control", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/pet/update")
async def update_pet_post(request: Request, id: int = Form(...), nombre: str = Form(...), duenio: str = Form(...), tipo_mascota: str = Form(...), raza: str = Form(...), db: AsyncSession = Depends(get_db)):
    await update_pet(db, id, {"nombre": nombre, "duenio": duenio, "tipo_mascota": tipo_mascota, "raza": raza})
    return RedirectResponse(url="/control", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/pet/delete")
async def delete_pet_post(request: Request, id: int = Form(...), db: AsyncSession = Depends(get_db)):
    await delete_pet(db, id)
    return RedirectResponse(url="/control", status_code=status.HTTP_303_SEE_OTHER)

# ---- CONSULTA DE VUELOS ----
@app.get("/flights")
async def list_flights(request: Request, db: AsyncSession = Depends(get_db), origen: str = "", destino: str = "", fecha: str = ""):
    flights = await list_available_flights(db, origen or None, destino or None, fecha or None)
    return templates.TemplateResponse("list_flights.html", {"request": request, "flights": flights, "origen": origen, "destino": destino, "fecha": fecha})

# ---- RESERVAR Y COMPRAR ----
@app.get("/reserve_buy")
async def reserve_buy(request: Request, db: AsyncSession = Depends(get_db)):
    reservas = (await db.execute(select(Reservation))).scalars().all()
    return templates.TemplateResponse("reserve_buy.html", {"request": request, "reservas": reservas})

@app.post("/reserve")
async def reserve_post(request: Request, user_id: int = Form(...), pet_id: int = Form(...), flight_id: int = Form(...), db: AsyncSession = Depends(get_db)):
    reserva = await reserve_flight(db, user_id, pet_id, flight_id)
    msg = f"Reserva exitosa. ID: {reserva.id}" if hasattr(reserva, "id") else reserva
    reservas = (await db.execute(select(Reservation))).scalars().all()
    return templates.TemplateResponse("reserve_buy.html", {"request": request, "reservas": reservas, "msg": msg})

@app.post("/buy")
async def buy_post(request: Request, reserva_id: int = Form(...), db: AsyncSession = Depends(get_db)):
    result = await buy_flight(db, reserva_id)
    msg = "Compra realizada" if hasattr(result, "pagada") and result.pagada else result
    reservas = (await db.execute(select(Reservation))).scalars().all()
    return templates.TemplateResponse("reserve_buy.html", {"request": request, "reservas": reservas, "msg": msg})