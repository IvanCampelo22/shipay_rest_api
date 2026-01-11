#!/bin/sh

echo "Esperando o banco de dados iniciar..."
until pg_isready -h db -p 5432; do
    sleep 2
done

echo "Executando os testes..."
pytest tests.py

echo "Iniciando o servidor FastAPI..."
exec uvicorn main:app --reload --host 0.0.0.0 --port 5000