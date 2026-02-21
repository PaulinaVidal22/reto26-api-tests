# Reto 2026 - QA - API Tests (Ithaka & Nettra)

Repo de **pruebas de API** para los dos proyectos del Reto:
- **Ithaka**
- **Nettra**

La idea es mantener **un repo por tipo de prueba** (API / E2E / Performance / IA).  
Dentro de cada repo se separa por proyecto (Ithaka / Nettra).

## Estructura

- `api/clients/` clientes o wrappers para llamar a las APIs (1 por proyecto si aplica)
- `api/schemas/` contratos / esquemas (OpenAPI, JSON Schema, etc.)
- `api/tests/ithaka/` tests de API de Ithaka
- `api/tests/nettra/` tests de API de Nettra
- `api/data/` datos de prueba por proyecto
- `api/reports/` salida de reportes (no subir archivos pesados)
- `docs/` documentación útil (links, swagger, notas de endpoints, etc.)
- `scripts/` helpers (por ejemplo: generar token, reset de data, etc.)

## Links útiles

### Ithaka
- Swagger: http://ithaka-api.reto-ucu.net/docs
- Front: http://ithaka-frontend-infra.reto-ucu.net/
- Repo Back: https://github.com/ucudal/reto-summer-2026-ithaka-backend.git
- Repo Front: https://github.com/ucudal/reto-summer-2026-ithaka-frontend

### Nettra
- Postman: 
    https://app.getpostman.com/join-team?invite_code=25e25952e4d6a103ccfbc7fe0c50eb9d26d4d3f80ef31f9c6655d53c481e79d6&target_code=be78cac999c93f8d0d25eab7d8add558
