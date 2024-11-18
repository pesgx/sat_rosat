import flet as ft
from sat_rosat.controllers.aparato_controller import AparatoController

class AparatosView(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.controller = AparatoController()
        self.init_components()

    def init_components(self):
        self.nombre_aparato = ft.TextField(label="Nombre del Aparato", autofocus=True, expand=True)
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombre del Aparato")),
            ],
            rows=[],
        )
        self.registro_seleccionado = None

    def build(self):
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Gestión de Aparatos", size=20, weight=ft.FontWeight.BOLD),
                    ft.ElevatedButton("Volver", on_click=self.volver_pagina_principal)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                self.nombre_aparato,
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
            id_aparato = self.controller.crear_aparato(self.nombre_aparato.value)
            if id_aparato is not None:
                self.mostrar_mensaje("Aparato registrado correctamente")
                self.cargar_datos()
                self.limpiar(None)
            else:
                self.mostrar_mensaje("Error al registrar el aparato", es_error=True)

    def actualizar(self, e):
        if self.validar_campos() and self.registro_seleccionado:
            resultado = self.controller.actualizar_aparato(
                self.registro_seleccionado[0],
                self.nombre_aparato.value
            )
            if resultado:
                self.mostrar_mensaje("Aparato actualizado correctamente")
                self.cargar_datos()
                self.limpiar(None)
            else:
                self.mostrar_mensaje("Error al actualizar el aparato", es_error=True)

    def eliminar(self, e):
        if self.registro_seleccionado:
            resultado = self.controller.eliminar_aparato(self.registro_seleccionado[0])
            if resultado:
                self.mostrar_mensaje("Aparato eliminado correctamente")
                self.cargar_datos()
                self.limpiar(None)
            else:
                self.mostrar_mensaje("Error al eliminar el aparato", es_error=True)

    def limpiar(self, e):
        self.nombre_aparato.value = ""
        self.registro_seleccionado = None
        self.nombre_aparato.focus()
        self.update()

    def cargar_datos(self):
        self.registros = self.controller.obtener_todos_aparatos()
        self.tabla.rows.clear()
        for registro in self.registros:
            self.tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(registro[0]))),
                        ft.DataCell(ft.Text(str(registro[1]))),
                    ],
                    on_select_changed=lambda e, reg=registro: self.seleccionar_registro(e, reg)
                )
            )
        self.update()

    def seleccionar_registro(self, e, registro):
        if e.data == "true":
            self.registro_seleccionado = registro
            self.nombre_aparato.value = str(registro[1])
            self.update()

    def validar_campos(self) -> bool:
        if not self.nombre_aparato.value:
            self.mostrar_mensaje("El nombre del aparato es requerido", es_error=True)
            return False
        return True

    def mostrar_mensaje(self, mensaje, es_error=False):
        color = ft.colors.RED if es_error else ft.colors.GREEN
        self.page.show_snack_bar(ft.SnackBar(content=ft.Text(mensaje, color=color)))

    def volver_pagina_principal(self, e):
        self.page.go('/')