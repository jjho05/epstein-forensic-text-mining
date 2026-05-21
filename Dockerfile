FROM python:3.11

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR "/code/04 Aplicacion Shiny"

CMD ["python", "-m", "shiny", "run", "app.py", "--host", "0.0.0.0", "--port", "7860"]
