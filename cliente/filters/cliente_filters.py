from datetime import datetime
from cliente.models.cliente_models import Cliente


class Clientefilter:
    @staticmethod
    def filter_id(id: int):
        return Cliente.objects.filter(id=id)

    @staticmethod
    def filter_identificacion(identificacion: str):
        return Cliente.objects.filter(identificacion__icontains=identificacion)
    
    @staticmethod
    def filter_nombre(nombre: str):
        return Cliente.objects.filter(nombre__icontains=nombre)
    
    @staticmethod
    def filter_direccion(direccion: str):
        return Cliente.objects.filter(direccion__icontains=direccion)
    
    @staticmethod
    def filter_fecha_nacimiento(fecha_nacimiento: str):
        try:
            fecha = datetime.strptime(fecha_nacimiento, "%d-%m-%Y").date()
        except ValueError:
            return Cliente.objects.none()

        return Cliente.objects.filter(fecha_nacimiento=fecha)
    
    @staticmethod
    def filter_sexo(sexo: str):
        return Cliente.objects.filter(sexo=sexo)
    
    @staticmethod
    def filter_is_discapacitado(is_discapacitado: bool):
        return Cliente.objects.filter(is_discapacitado=is_discapacitado)

    @staticmethod
    def filter_is_tercera_edad(is_tercera_edad: bool):
        return Cliente.objects.filter(is_tercera_edad=is_tercera_edad)
    
    @staticmethod
    def filter_state(state: bool):
        return Cliente.objects.filter(state=state)
