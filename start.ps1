# Verificar si Docker Desktop está corriendo
$dockerRunning = Get-Process -Name "Docker Desktop" -ErrorAction SilentlyContinue

if (-not $dockerRunning) {
    Write-Host "Docker no está activo. Iniciando Docker Desktop..."
    Start-Process "Docker Desktop"
    Start-Sleep -Seconds 10
} else {
    Write-Host "Docker ya está activo."
}

# Esperar a que Docker esté listo
while (-not (docker info -ErrorAction SilentlyContinue)) {
    Write-Host "Esperando que Docker esté listo..."
    Start-Sleep -Seconds 2
}

# Levantar servicios con docker-compose
Write-Host "Ejecutando: docker compose up -d"
docker compose up -d

# Levantar la API con Uvicorn
Write-Host "Iniciando la API con Uvicorn..."
uvicorn app.main:app --reload
