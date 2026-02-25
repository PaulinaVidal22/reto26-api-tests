import os
import httpx
import pytest
from dotenv import load_dotenv

from api.clients.nettra_client import NettraClient
from api.clients.ithaka_client import IthakaClient
from api.builders.nettra.well_builder import WellBuilder

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
def nettra_token(nettra_base_url: str):
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
def nettra_client(nettra_base_url: str, nettra_token: str | None):
    client = NettraClient(
        base_url=nettra_base_url,
        token=nettra_token
    )
    yield client
    client.close()

@pytest.fixture(scope="session")
def ithaka_client(ithaka_base_url: str, ithaka_token: str | None):
    client = IthakaClient(
        base_url=ithaka_base_url,
        token=ithaka_token
    )
    yield client
    client.close()

# =========================
# 
# =========================

@pytest.fixture(scope="session")
def existing_well_with_anomalies(nettra_client: NettraClient, nettra_token: str | None):

    builder = WellBuilder(nettra_client, nettra_token)

    well_id = builder.with_anomalies()

    if not well_id:
        pytest.skip("No existe ningún well con anomalies en el entorno")

    return well_id

@pytest.fixture(scope="session")
def existing_well_with_parameters(nettra_client: NettraClient, nettra_token: str | None):

    builder = WellBuilder(nettra_client, nettra_token)

    well_id = builder.with_parameters()

    if not well_id:
        pytest.skip("No existe ningún well con parameters en el entorno")

    return well_id