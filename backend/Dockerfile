# Usa una imagen base de Python
FROM python:3.11-slim

# Configura el directorio de trabajo
WORKDIR /app


# Instalar dependencias del sistema para psycopg
# 'postgresql-client-sdk' o similar puede variar según la distribución base.
# Si usas una imagen 'slim' que no es Debian/Ubuntu, consulta la documentación.
# Para Debian/Ubuntu:
RUN apt-get update && apt-get install -y \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copia los archivos necesarios al contenedor
COPY ./backend/ /app/

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto de la API
EXPOSE 8000

# Ejecuta el servidor de FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]