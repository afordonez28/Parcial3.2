import os
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

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

# Registro de usuario
@app.get("/register_user")
async def register_user_form(request: Request):
    return templates.TemplateResponse("register_user.html", {"request": request})

@app.post("/register_user")
async def register_user_post(
    request: Request,
    documento: str = Form(...),
    nombre: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    user = User(documento=documento, nombre=nombre)
    await create_user(db, user)
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

# Registro de mascota
@app.get("/register_pet")
async def register_pet_form(request: Request):
    return templates.TemplateResponse("register_pet.html", {"request": request})

@app.post("/register_pet")
async def register_pet_post(
    request: Request,
    nombre: str = Form(...),
    duenio: str = Form(...),
    tipo_mascota: str = Form(...),
    raza: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    pet = Pet(nombre=nombre, duenio=duenio, tipo_mascota=tipo_mascota, raza=raza)
    await create_pet(db, pet)
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

# Listar vuelos disponibles
@app.get("/flights")
async def list_flights(request: Request, db: AsyncSession = Depends(get_db)):
    flights = await list_available_flights(db)
    return templates.TemplateResponse("list_flights.html", {"request": request, "flights": flights})

# Reservar vuelo desde la lista
@app.post("/reserve_from_list")
async def reserve_from_list(
    request: Request,
    flight_id: int = Form(...),
    user_id: int = Form(...),
    pet_id: int = Form(...),
    db: AsyncSession = Depends(get_db)
):
    reserva = await reserve_flight(db, user_id, pet_id, flight_id)
    msg = f"Reserva exitosa. ID: {reserva.id}" if isinstance(reserva, Reservation) else reserva
    return templates.TemplateResponse("reserve_result.html", {
        "request": request,
        "result": msg
    })

# Página para comprar una reserva
@app.get("/my_reservations")
async def my_reservations(request: Request, db: AsyncSession = Depends(get_db)):
    reservas = (await db.execute(select(Reservation))).scalars().all()
    return templates.TemplateResponse("my_reservations.html", {"request": request, "reservas": reservas})

@app.post("/buy_reservation")
async def buy_reservation(
    request: Request,
    reserva_id: int = Form(...),
    db: AsyncSession = Depends(get_db)
):
    result = await buy_flight(db, reserva_id)
    mensaje = "Compra realizada" if isinstance(result, Reservation) and result.pagada else result
    return templates.TemplateResponse("buy_result.html", {
        "request": request,
        "result": mensaje
    })

# Gestión usuarios y mascotas igual que antes...
# (Puedes seguir usando tu sección /manage y los endpoints CRUD)