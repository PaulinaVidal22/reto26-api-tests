import os
import sys
from pathlib import Path

import pytest
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from api.clients.nettra_client import NettraClient
from api.clients.ithaka_client import IthakaClient

try:
    from api.clients.ithaka_client import IthakaClient
except ModuleNotFoundError:
    IthakaClient = None

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
    return os.getenv("NETTRA_BASE_URL", "http://localhost:8000")


@pytest.fixture(scope="session")
def ithaka_base_url():
    return _get_env_variable("ITHAKA_BASE_URL")


# =========================
# TOKENS (opcionales)
# =========================

@pytest.fixture(scope="session")
def nettra_token():
    return os.getenv("NETTRA_TOKEN")


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
    if IthakaClient is None:
        pytest.skip("IthakaClient no está disponible en este repositorio")
    client = IthakaClient(
        base_url=ithaka_base_url,
        token=ithaka_token
    )
    yield client
    client.close()
