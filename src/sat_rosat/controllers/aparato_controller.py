from sat_rosat.models.aparato_model import AparatoModel

class AparatoController:
    @staticmethod
    def crear_aparato(nombre_aparato):
        return AparatoModel.crear(nombre_aparato)

    @staticmethod
    def obtener_todos_aparatos():
        return AparatoModel.obtener_todos()

    @staticmethod
    def obtener_aparato(id_aparato):
        return AparatoModel.obtener_por_id(id_aparato)

    @staticmethod
    def actualizar_aparato(id_aparato, nombre_aparato):
        return AparatoModel.actualizar(id_aparato, nombre_aparato)

    @staticmethod
    def eliminar_aparato(id_aparato):
        return AparatoModel.eliminar(id_aparato)