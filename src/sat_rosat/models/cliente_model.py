from dataclasses import dataclass
from typing import Optional

@dataclass
class Cliente:
    id_cliente: int
    codigo_cliente: str
    nombre_cliente: str
    nombre_cliente_comercial: str
    nif_cliente: str
    domicilio: str
    poblacion_id: int
    telefono_1: Optional[int]
    telefono_2: Optional[int]
    nota_cliente: Optional[str]
    nombre_poblacion: str  # Este campo viene de la unión con tabla_poblacion

    def __post_init__(self):
        self.telefono_1 = int(self.telefono_1) if self.telefono_1 is not None else None
        self.telefono_2 = int(self.telefono_2) if self.telefono_2 is not None else None