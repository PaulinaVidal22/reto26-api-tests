import httpx

def test_login_exitoso():
    r = httpx.post("https://nettra-api.reto-ucu.net/api/v1/auth/login", json={"username":"valido","password":"valida"})
    assert r.status_code == 200
    assert "token" in r.json()

def test_login_no_autorizado():
    r = httpx.post("https://nettra-api.reto-ucu.net/api/v1/auth/login", json={"username":"valido","password":"incorrecta"})
    assert r.status_code == 401

def test_login_peticion_incorrecta():
    r = httpx.post("https://nettra-api.reto-ucu.net/api/v1/auth/login", json={"usuario":"faltante"})
    assert r.status_code == 400