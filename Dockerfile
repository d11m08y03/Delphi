FROM python:3.13-slim

WORKDIR /app

COPY requirements/core.txt .

RUN pip install --no-cache-dir -r core.txt

COPY app ./app

COPY main.py .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
