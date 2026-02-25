def execute_contract_case(case, token):
    """
    Ejecuta un case de Schemathesis con autenticación
    y validación estándar.
    """

    case.headers = {
        "Authorization": f"Bearer {token}"
    }

    response = case.call()

    if 200 <= response.status_code < 500:
        case.validate_response(response)

    return response