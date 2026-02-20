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
