import flet as ft
from sat_rosat.controllers.poblacion_controller import PoblacionController

class PoblacionView(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.controller = PoblacionController()
        self.init_components()

    def init_components(self):
        self.nombre_poblacion = ft.TextField(label="Nombre de la Población", autofocus=True, expand=True)
        self.codigo_postal = ft.TextField(label="Código Postal", expand=True)
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombre Población")),
                ft.DataColumn(ft.Text("Código Postal")),
            ],
            rows=[],
        )
        self.registro_seleccionado = None

    def build(self):
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Gestión de Poblaciones", size=20, weight=ft.FontWeight.BOLD),
                    ft.ElevatedButton("Volver", on_click=self.volver_pagina_principal)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([self.nombre_poblacion, self.codigo_postal], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.ElevatedButton("Registrar", on_click=self.registrar, bgcolor=ft.colors.BLUE, color=ft.colors.WHITE),
                    ft.ElevatedButton("Actualizar", on_click=self.actualizar, bgcolor=ft.colors.ORANGE, color=ft.colors.WHITE),
                    ft.ElevatedButton("Eliminar", on_click=self.eliminar, bgcolor=ft.colors.RED, color=ft.colors.WHITE),
                    ft.ElevatedButton("Limpiar", on_click=self.limpiar, bgcolor=ft.colors.GREY, color=ft.colors.WHITE),
                ], alignment=ft.MainAxisAlignment.CENTER),
                self.tabla
            ], spacing=20, expand=True),
            padding=20,
            expand=True
        )

    def did_mount(self):
        self.cargar_datos()

    def registrar(self, e):
        if self.validar_campos():
            id_poblacion = self.controller.crear_poblacion(
                self.nombre_poblacion.value,
                int(self.codigo_postal.value)
            )
            if id_poblacion is not None:
                self.mostrar_mensaje("Población registrada correctamente")
                self.cargar_datos()
                self.limpiar(None)
            else:
                self.mostrar_mensaje("Error al registrar la población", es_error=True)

    def actualizar(self, e):
        if self.validar_campos() and self.registro_seleccionado:
            resultado = self.controller.actualizar_poblacion(
                self.registro_seleccionado[0],
                self.nombre_poblacion.value,
                int(self.codigo_postal.value)
            )
            if resultado:
                self.mostrar_mensaje("Población actualizada correctamente")
                self.cargar_datos()
                self.limpiar(None)
            else:
                self.mostrar_mensaje("Error al actualizar la población", es_error=True)

    def eliminar(self, e):
        if self.registro_seleccionado:
            resultado = self.controller.eliminar_poblacion(self.registro_seleccionado[0])
            if resultado:
                self.mostrar_mensaje("Población eliminada correctamente")
                self.cargar_datos()
                self.limpiar(None)
            else:
                self.mostrar_mensaje("Error al eliminar la población", es_error=True)

    def limpiar(self, e):
        self.nombre_poblacion.value = ""
        self.codigo_postal.value = ""
        self.registro_seleccionado = None
        self.nombre_poblacion.focus()
        self.update()

    def cargar_datos(self):
        self.registros = self.controller.obtener_todas_poblaciones_en_poblaciones()
        self.tabla.rows.clear()
        for registro in self.registros:
            self.tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(registro[0]))),
                        ft.DataCell(ft.Text(str(registro[1]))),
                        ft.DataCell(ft.Text(str(registro[2]))),
                    ],
                    on_select_changed=lambda e, reg=registro: self.seleccionar_registro(e, reg)
                )
            )
        self.update()

    def seleccionar_registro(self, e, registro):
        if e.data == "true":  # Asegurarse de que la fila está seleccionada
            self.registro_seleccionado = registro
            self.nombre_poblacion.value = str(registro[1])
            self.codigo_postal.value = str(registro[2])
            self.update()

    def validar_campos(self) -> bool:
        if not self.nombre_poblacion.value or not self.codigo_postal.value:
            self.mostrar_mensaje("Todos los campos son requeridos", es_error=True)
            return False
        try:
            int(self.codigo_postal.value)
            return True
        except ValueError:
            self.mostrar_mensaje("El código postal debe ser un número", es_error=True)
            return False

    def mostrar_mensaje(self, mensaje, es_error=False):
        color = ft.colors.RED if es_error else ft.colors.GREEN
        self.page.show_snack_bar(ft.SnackBar(content=ft.Text(mensaje, color=color)))

    def volver_pagina_principal(self, e):
        self.page.go('/')