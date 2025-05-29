#!/bin/bash

# Verificar si Docker está corriendo
if (! systemctl is-active --quiet docker); then
    echo "Docker no está activo. Iniciando Docker..."
    sudo systemctl start docker
else
    echo "Docker ya está activo."
fi

# Levantar servicios con docker-compose
echo "Ejecutando: docker compose up -d"
docker compose up -d

# Levantar la API con Uvicorn
echo "Iniciando la API con Uvicorn..."
uvicorn app.main:app --reload
