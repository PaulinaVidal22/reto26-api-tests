# Reto 2026 – QA – API Tests (Ithaka & Nettra)

## 1. Introducción

El presente repositorio contiene la implementación de pruebas automatizadas de API correspondientes a los proyectos **Ithaka** y **Nettra**, desarrollados en el marco del Reto 2026.

La organización del trabajo responde a una separación por tipo de prueba (API, E2E, Performance, IA), concentrándose este repositorio exclusivamente en la validación del comportamiento y contratos de las APIs.

La automatización se diseñó considerando principios de mantenibilidad, escalabilidad y separación de responsabilidades.

---

## 2. Stack Tecnológico

Para el desarrollo de las pruebas se seleccionaron herramientas del ecosistema Python ampliamente adoptadas en la industria:

* **pytest**: framework principal de ejecución.
* **httpx**: cliente HTTP moderno para consumo de APIs.
* **pydantic**: validación estructural y tipado fuerte de modelos.
* **schemathesis**: validación contractual basada en especificaciones OpenAPI.
* **pytest-html**: generación de reportes ejecutivos.
* **pytest-xdist**: ejecución paralela.
* **python-dotenv**: gestión de variables de entorno.

La elección del stack responde a los siguientes criterios:

* Compatibilidad entre herramientas.
* Amplia adopción en entornos profesionales.
* Curva de aprendizaje adecuada al equipo.
* Capacidad de escalar hacia integración continua.

---

## 3. Estructura del Proyecto

```
api/
│
├── clients/              # Clientes HTTP (uno por proyecto)
├── models/               # Modelos Pydantic para validación de respuestas
├── schemas/              # Especificaciones OpenAPI / JSON Schema
├── tests/
│   ├── ithaka/
│   ├── nettra/
│   └── conftest.py
│
├── data/                 # Datos de prueba estructurados
├── reports/              # Reportes generados (no versionados)
│
docs/
scripts/
│
pytest.ini
requirements.txt
.env.example
```

Se adopta el patrón de un cliente HTTP por sistema, permitiendo encapsular particularidades de autenticación y configuración.

---

## 4. Configuración del Entorno

### 4.1 Creación de entorno virtual

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

### 4.2 Instalación de dependencias

```bash
pip install -r requirements.txt
```

---

## 5. Variables de Entorno

El proyecto utiliza un archivo `.env` para gestionar configuraciones sensibles como URLs base y tokens de autenticación.

Crear un archivo `.env` a partir de `.env.example`:

```
NETTRA_BASE_URL=
NETTRA_TOKEN=

ITHAKA_BASE_URL=
ITHAKA_TOKEN=
```

Las credenciales no deben versionarse.

---

## 6. Ejecución de Pruebas

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
```

Ejecución paralela:

```bash
pytest -n auto
```

---

## 7. Generación de Reportes

Para generar un reporte HTML:

```bash
pytest --html=api/reports/report.html --self-contained-html
```

El reporte generado se almacena en `api/reports/`.

---

## 8. Estrategia de Pruebas

La estrategia adoptada contempla distintos niveles de validación:

### 8.1 Validación Funcional

Verificación de:

* Códigos de estado HTTP.
* Contenido de respuestas.
* Comportamiento esperado según especificación.

### 8.2 Validación Estructural

Uso de modelos Pydantic para asegurar:

* Tipado correcto.
* Presencia de campos obligatorios.
* Consistencia estructural de las respuestas.

### 8.3 Validación Contractual

Integración con Schemathesis para:

* Validar cumplimiento de especificaciones OpenAPI.
* Detectar inconsistencias entre implementación y contrato.

### 8.4 Clasificación de Pruebas

Se emplean marcadores para organizar la ejecución:

* `smoke`: pruebas críticas.
* `regression`: suite completa.
* `ithaka` / `nettra`: segmentación por sistema.
* `contract`: validación contractual.

---

## 9. Criterios de Calidad

El desarrollo de las pruebas sigue los siguientes principios:

* Separación de responsabilidades (clientes, modelos, tests).
* Configuración centralizada mediante fixtures.
* Reutilización de código.
* Independencia entre pruebas.
* Fail fast ante configuraciones incorrectas.
* No hardcodeo de configuraciones sensibles.

---

## 10. Recursos

### Ithaka

* Swagger: [http://ithaka-api.reto-ucu.net/docs](http://ithaka-api.reto-ucu.net/docs)
* Frontend: [http://ithaka-frontend-infra.reto-ucu.net/](http://ithaka-frontend-infra.reto-ucu.net/)
* Backend: [https://github.com/ucudal/reto-summer-2026-ithaka-backend.git](https://github.com/ucudal/reto-summer-2026-ithaka-backend.git)
* Frontend Repo: [https://github.com/ucudal/reto-summer-2026-ithaka-frontend](https://github.com/ucudal/reto-summer-2026-ithaka-frontend)

### Nettra

* Colección Postman:
  [https://app.getpostman.com/join-team?invite_code=25e25952e4d6a103ccfbc7fe0c50eb9d26d4d3f80ef31f9c6655d53c481e79d6&target_code=be78cac999c93f8d0d25eab7d8add558](https://app.getpostman.com/join-team?invite_code=25e25952e4d6a103ccfbc7fe0c50eb9d26d4d3f80ef31f9c6655d53c481e79d6&target_code=be78cac999c93f8d0d25eab7d8add558)
