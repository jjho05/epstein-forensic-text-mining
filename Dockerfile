FROM python:3.9-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

WORKDIR "/code/04 Aplicacion Shiny"

# Puerto 7860 mandatorio en Hugging Face Spaces
CMD ["shiny", "run", "app.py", "--host", "0.0.0.0", "--port", "7860"]
