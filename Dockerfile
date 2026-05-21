# ── Etapa 1: Builder ──────────────────────────────────────────────────────────
# Imagen con compilador para construir paquetes con extensiones en C
FROM python:3.11-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /install

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade --prefix=/install/pkgs -r requirements.txt

# ── Etapa 2: Runtime ──────────────────────────────────────────────────────────
# Imagen slim sin compilador; solo copiamos los paquetes ya compilados
FROM python:3.11-slim

# Dependencia de runtime requerida por scikit-learn (OpenMP)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copiar los paquetes Python compilados desde el builder
COPY --from=builder /install/pkgs /usr/local

WORKDIR /code
COPY . .

WORKDIR "/code/04 Aplicacion Shiny"

CMD ["python", "-m", "shiny", "run", "app.py", "--host", "0.0.0.0", "--port", "7860"]
