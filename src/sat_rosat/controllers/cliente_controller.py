
from sat_rosat.models.cliente_model import ClienteModel

class ClienteController:
    def __init__(self):
        self.model = ClienteModel()

    def obtener_clientes(self):
        return self.model.obtener_todos()

    def obtener_poblaciones(self):
        return self.model.obtener_poblaciones()

    def registrar_cliente(self, codigo, nombre, nif, poblacion_id, telefono, nota):
        self.model.insertar_cliente(codigo, nombre, nif, poblacion_id, telefono, nota)
