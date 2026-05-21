FROM python:3.10-slim

WORKDIR /code

# Instalar dependencias del sistema necesarias a nivel de runtime (como libgomp1 para scikit-learn)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copiar requerimientos y preinstalar dependencias en la raíz del contenedor
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copiar absolutamente todo el repositorio al contenedor para mantener la estructura de datos
COPY . .

# Cambiar el directorio de trabajo a la aplicación interactiva de Shiny
# Se usa comillas debido al espacio en el nombre de la carpeta
WORKDIR "/code/04 Aplicacion Shiny"

# Exponer el puerto por defecto de Hugging Face Spaces (7860) e iniciar la app robustamente vía python -m
CMD ["python", "-m", "shiny", "run", "app.py", "--host", "0.0.0.0", "--port", "7860"]
