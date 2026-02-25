# Reto 2026 – QA – API Tests (Ithaka & Nettra)

## 1. Introducción

El presente repositorio contiene la implementación de pruebas automatizadas de API correspondientes a los proyectos **Ithaka** y **Nettra**, desarrollados en el marco del Reto 2026.

La organización del trabajo responde a una separación por tipo de prueba (API, E2E, Performance, IA), concentrándose este repositorio exclusivamente en la validación del comportamiento y contratos de las APIs.

Actualmente las pruebas se ejecutan contra entornos levantados de forma local. Se contempla que en etapas posteriores los proyectos migren a los servicios de la UCU, por lo que la configuración fue diseñada para desacoplar entorno, credenciales y ejecución.

La automatización fue estructurada considerando principios de mantenibilidad, escalabilidad, reutilización y separación de responsabilidades.

---

## 2. Stack Tecnológico

Para el desarrollo de las pruebas se seleccionaron herramientas del ecosistema Python ampliamente adoptadas en la industria:

* **pytest**: framework principal de ejecución.
* **httpx**: cliente HTTP moderno para consumo de APIs.
* **pydantic**: validación estructural y tipado fuerte de modelos.
* **schemathesis**: validación contractual basada en especificaciones OpenAPI.
* **pytest-html**: generación de reportes ejecutivos.
* **pytest-xdist**: ejecución paralela.
* **pytest-rerunfailures**: reejecución automática de tests inestables.
* **python-dotenv**: gestión de variables de entorno.

La elección del stack responde a los siguientes criterios:

* Compatibilidad entre herramientas.
* Amplia adopción en entornos profesionales.
* Curva de aprendizaje adecuada al equipo.
* Capacidad de escalar hacia integración continua.
* Separación clara entre validación funcional y validación contractual.

---

## 3. Estructura del Proyecto

```
api/
│
├── clients/                      # Clientes HTTP (uno por sistema)
│   ├── base_client.py            # Cliente base con configuración común
│   ├── ithaka_client.py          # Cliente específico Ithaka
│   └── nettra_client.py          # Cliente específico Nettra
│
├── models/                       # Modelos Pydantic para validación estructural
│
├── builders/                     # Constructores de datos dinámicos para tests
│
├── schemas/                      # Especificaciones OpenAPI / JSON Schema
│                                  # (versionadas localmente si aplica)
│
├── tests/
│   ├── ithaka/
│   │   ├── functional/           # Tests funcionales Ithaka
│   │   └── contract/             # Tests de contrato (Schemathesis)
│   │
│   ├── nettra/
│   │   ├── functional/           # Tests funcionales Nettra
│   │   └── contract/             # Tests de contrato (Schemathesis)
│   │
│   └── conftest.py               # Fixtures globales (tokens, configuración, etc.)
│
├── reports/                      # Reportes generados (no versionados)
│
└── __init__.py
│
docs/                             # Documentación técnica adicional
scripts/                          # Scripts auxiliares de ejecución o soporte
│
pytest.ini                        # Configuración central de pytest
requirements.txt                  # Dependencias del proyecto
.env.example                      # Plantilla de variables de entorno
.gitignore                        # Exclusión de archivos no versionables
README.md                         # Documentación principal del proyecto
```

Notas sobre la estructura:

* Se adopta el patrón de un cliente HTTP por sistema, encapsulando autenticación y configuración base.
* Los modelos permiten validar respuestas de forma tipada y desacoplada del test.
* La carpeta `schemas` puede utilizarse para versionar especificaciones OpenAPI o esquemas JSON cuando se requiera validación contractual offline.
* `builders` centraliza la generación de datos dinámicos para evitar hardcodeo en los tests.
* `reports` no debe versionarse.

---

## 4. Requisitos de Versión

El proyecto requiere:

* Python 3.10 o superior.
* pytest >= 8.0 (definido en `pytest.ini` mediante la directiva `minversion = 8.0`).

En caso de utilizar una versión inferior de pytest, la ejecución se detendrá automáticamente.

Se recomienda utilizar entornos virtuales para aislar dependencias.

---

## 5. Configuración del Entorno

### 5.1 Creación de entorno virtual

```bash
python -m venv .venv
```

Activación:

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 5.2 Instalación de dependencias

```bash
pip install -r requirements.txt
```

---

## 6. Variables de Entorno

El proyecto utiliza un archivo `.env` para gestionar configuraciones sensibles como URLs base y tokens de autenticación.

Crear un archivo `.env` a partir de `.env.example`:

```
NETTRA_BASE_URL=
NETTRA_TOKEN=

ITHAKA_BASE_URL=
ITHAKA_TOKEN=
```

Las credenciales no deben versionarse.

Las URLs permiten cambiar entre entorno local, QA o servicios desplegados sin modificar el código de pruebas.

---

## 7. Configuración de pytest

El archivo `pytest.ini` define:

* Ruta base de tests (`testpaths = api/tests`)
* Convenciones de nombres
* Marcadores personalizados
* Estricta validación de markers (`--strict-markers`)
* Versión mínima requerida de pytest

Marcadores definidos:

* `ithaka`: tests relacionados a Ithaka API.
* `nettra`: tests relacionados a Nettra API.
* `functional`: tests funcionales.
* `contract`: validaciones de contrato OpenAPI (Schemathesis).
* `smoke`: pruebas críticas de alto impacto.
* `security`: autenticación y autorización.
* `regression`: suite completa de regresión.
* `integration`: pruebas contra entorno real.
* `slow`: tests que pueden demorar.

El uso de marcadores permite segmentar ejecuciones según contexto y necesidad.

---

## 8. Ejecución de Pruebas

Ejecutar suite completa:

```bash
pytest
```

Ejecución detallada:

```bash
pytest -v
```

Ejecución por marcador:

```bash
pytest -m smoke
pytest -m nettra
pytest -m contract
```

Ejecución paralela:

```bash
pytest -n auto
```

---

## 9. Reejecución Automática de Tests (Rerun)

Se utiliza la librería `pytest-rerunfailures` para permitir la reejecución automática de tests fallidos en entornos inestables.

Ejemplo de uso:

```bash
pytest --reruns 2
```

Esto volverá a ejecutar cada test fallido hasta dos veces antes de marcarlo como fallo definitivo.

Su uso está orientado a:

* Entornos QA compartidos.
* Servicios con latencia variable.
* Posibles errores intermitentes externos al test.

No se recomienda utilizar esta funcionalidad para ocultar defectos reales del sistema bajo prueba.

---

## 10. Generación de Reportes

Para generar un reporte HTML:

```bash
pytest --html=api/reports/report.html --self-contained-html
```

El reporte generado se almacena en `api/reports/`.

Los reportes no deben versionarse.

---

## 11. Estrategia de Pruebas

La estrategia adoptada contempla distintos niveles de validación:

### 11.1 Validación Funcional

Verificación de:

* Códigos de estado HTTP.
* Contenido de respuestas.
* Comportamiento esperado según especificación funcional.

### 11.2 Validación Estructural

Uso de modelos Pydantic para asegurar:

* Tipado correcto.
* Presencia de campos obligatorios.
* Consistencia estructural de las respuestas.

### 11.3 Validación Contractual

Integración con Schemathesis para:

* Validar cumplimiento de especificaciones OpenAPI.
* Detectar inconsistencias entre implementación y contrato.
* Identificar divergencias entre documentación y backend.

Las validaciones contractuales pueden ejecutarse contra el OpenAPI expuesto por el backend (`/openapi.json`) o contra una versión versionada localmente en la carpeta `schemas`.

### 11.4 Clasificación de Pruebas

Se emplean marcadores para organizar la ejecución según:

* Criticidad (`smoke`).
* Alcance (`regression`).
* Sistema (`ithaka`, `nettra`).
* Tipo (`functional`, `contract`, `integration`, `security`).

---

## 12. Criterios de Calidad

El desarrollo de las pruebas sigue los siguientes principios:

* Separación de responsabilidades (clientes, modelos, tests).
* Configuración centralizada mediante fixtures.
* Reutilización de código.
* Independencia entre pruebas.
* Fail fast ante configuraciones incorrectas.
* No hardcodeo de configuraciones sensibles.
* Uso controlado de reejecución para manejar flakiness.
* Preparación para migración de entorno local a servicios UCU.

---

## 13. Recursos

### Ithaka

Swagger:
[http://ithaka-api.reto-ucu.net/docs](http://ithaka-api.reto-ucu.net/docs)

Frontend:
[http://ithaka-frontend-infra.reto-ucu.net/](http://ithaka-frontend-infra.reto-ucu.net/)

Backend:
[https://github.com/ucudal/reto-summer-2026-ithaka-backend.git](https://github.com/ucudal/reto-summer-2026-ithaka-backend.git)

Frontend Repo:
[https://github.com/ucudal/reto-summer-2026-ithaka-frontend](https://github.com/ucudal/reto-summer-2026-ithaka-frontend)

### Nettra

Colección Postman:
[https://app.getpostman.com/join-team?invite_code=25e25952e4d6a103ccfbc7fe0c50eb9d26d4d3f80ef31f9c6655d53c481e79d6&target_code=be78cac999c93f8d0d25eab7d8add558](https://app.getpostman.com/join-team?invite_code=25e25952e4d6a103ccfbc7fe0c50eb9d26d4d3f80ef31f9c6655d53c481e79d6&target_code=be78cac999c93f8d0d25eab7d8add558)
