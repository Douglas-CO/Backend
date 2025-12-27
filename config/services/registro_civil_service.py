import requests


class RegistroCivilService:
    BASE_URL = "https://saccs.acess.gob.ec/wsc/registrocivil/infopersona"

    @staticmethod
    def get_persona_by_cedula(cedula: str) -> dict | None:
        try:
            response = requests.get(
                f"{RegistroCivilService.BASE_URL}/{cedula}",
                timeout=5
            )
            data = response.json()
        except Exception:
            return None

        if data.get("status") != 1:
            return None

        persona = data.get("response", {})
        if persona.get("CodigoError") != "000":
            return None

        return persona
