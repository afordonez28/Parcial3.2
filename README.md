# FastAPI Vuelos con Mascotas

## Características

- Registro de usuarios y mascotas
- Consulta de vuelos disponibles
- Reserva y compra de vuelos con validación de disponibilidad
- CRUD de usuarios y mascotas
- Modelado de entidades y estructura modular
- Plantillas HTML para funcionalidad web
- Configuración para despliegue en Render.com

## Configuración

1. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

2. Configura tu archivo `.env` con las credenciales de PostgreSQL.

3. Ejecuta el servidor:
    ```bash
    uvicorn main:app --reload
    ```

4. Visita `http://localhost:8000` en tu navegador.

## Despliegue en Render.com

- Sube el código a un repositorio Git.
- Conecta el repo en Render.com, selecciona entorno Python y configura las variables de entorno del archivo `.env`.
