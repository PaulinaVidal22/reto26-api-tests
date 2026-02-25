import os
import httpx
import pytest
from dotenv import load_dotenv

from api.clients.nettra_client import NettraClient
from api.clients.ithaka_client import IthakaClient
from api.models.nettra.anomaly_models import AnomaliesResponse

load_dotenv()


def _get_env_variable(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Variable de entorno requerida no definida: {name}")
    return value


# =========================
# BASE URLS
# =========================

@pytest.fixture(scope="session")
def nettra_base_url():
    return _get_env_variable("NETTRA_BASE_URL")


@pytest.fixture(scope="session")
def ithaka_base_url():
    return _get_env_variable("ITHAKA_BASE_URL")


# =========================
# TOKENS 
# =========================

@pytest.fixture(scope="session")
def nettra_token(nettra_base_url):
    """
    Obtiene un JWT válido desde el backend de Nettra.
    Falla inmediatamente si las credenciales son inválidas.
    """

    username = _get_env_variable("NETTRA_USERNAME")
    password = _get_env_variable("NETTRA_PASSWORD")

    try:
        response = httpx.post(
            f"{nettra_base_url}/auth/login",
            json={
                "username": username,
                "password": password
            },
            timeout=10.0
        )
    except httpx.RequestError as exc:
        raise RuntimeError(f"No se pudo conectar a Nettra: {exc}") from exc

    if response.status_code != 200:
        raise RuntimeError(
            f"Error autenticando contra Nettra "
            f"[{response.status_code}]: {response.text}"
        )

    data = response.json()

    if "access_token" not in data:
        raise RuntimeError(
            f"Respuesta inesperada del login: {data}"
        )

    return data["access_token"]


@pytest.fixture(scope="session")
def ithaka_token():
    return os.getenv("ITHAKA_TOKEN")


# =========================
# CLIENTES
# =========================

@pytest.fixture(scope="session")
def nettra_client(nettra_base_url, nettra_token):
    client = NettraClient(
        base_url=nettra_base_url,
        token=nettra_token
    )
    yield client
    client.close()


@pytest.fixture(scope="session")
def ithaka_client(ithaka_base_url, ithaka_token):
    client = IthakaClient(
        base_url=ithaka_base_url,
        token=ithaka_token
    )
    yield client
    client.close()

@pytest.fixture(scope="session")
def existing_well_with_anomalies(nettra_client):
    response = nettra_client.get("/wells/")

    assert response.status_code == 200, "No se pudieron obtener wells"

    wells = response.json().get("items", [])
    assert wells, "No existen wells en el entorno"

    for well in wells:
        well_id = well["id"]

        anomalies_response = nettra_client.get_well_anomalies(well_id)

        if anomalies_response.status_code == 200:
            validated = AnomaliesResponse(**anomalies_response.json())
            if validated.data:
                return well_id

    pytest.skip("No existe ningún well con anomalies en el entorno")