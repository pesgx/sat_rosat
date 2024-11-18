from dataclasses import dataclass

@dataclass
class Marca:
    id_marca: int
    nombre_marca: str
    grupo_id: int
    nombre_grupo: str = ""  # Añadimos este campo para mostrar el nombre del grupo en la tabla
    