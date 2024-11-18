import flet as ft
from sat_rosat.controllers.grupo_controller import GrupoController

class GruposView(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.grupo_controller = GrupoController()

    def build(self):
        self.nombre_grupo = ft.TextField(label="Nombre del Grupo", expand=True)
        
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombre")),
            ],
            rows=[]
        )

        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Gestión de Grupos", size=20, weight=ft.FontWeight.BOLD),
                    ft.ElevatedButton(
                        "Volver",
                        on_click=lambda _: self.page.go("/"),
                        bgcolor=ft.colors.BLUE_GREY,
                        color=ft.colors.WHITE
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                self.nombre_grupo,
                ft.Row([
                    ft.ElevatedButton("Registrar", on_click=self.registrar, bgcolor=ft.colors.GREEN, color=ft.colors.WHITE),
                    ft.ElevatedButton("Actualizar", on_click=self.actualizar, bgcolor=ft.colors.ORANGE, color=ft.colors.WHITE),
                    ft.ElevatedButton("Eliminar", on_click=self.eliminar, bgcolor=ft.colors.RED, color=ft.colors.WHITE),
                    ft.ElevatedButton("Limpiar", on_click=self.limpiar, bgcolor=ft.colors.BLUE_GREY, color=ft.colors.WHITE),
                ]),
                self.tabla
            ]),
            padding=20,
            expand=True
        )

    def registrar(self, e):
        if self.validar_campos():
            nuevo_id = self.grupo_controller.crear_grupo(self.nombre_grupo.value)
            self.actualizar_tabla()
            self.limpiar(None)
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Grupo registrado correctamente con ID: {nuevo_id}")))

    def actualizar(self, e):
        if hasattr(self, 'grupo_seleccionado') and self.validar_campos():
            self.grupo_controller.actualizar_grupo(
                self.grupo_seleccionado.id_grupo,
                self.nombre_grupo.value
            )
            self.actualizar_tabla()
            self.limpiar(None)
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text("Grupo actualizado correctamente")))

    def eliminar(self, e):
        if hasattr(self, 'grupo_seleccionado'):
            self.grupo_controller.eliminar_grupo(self.grupo_seleccionado.id_grupo)
            self.actualizar_tabla()
            self.limpiar(None)
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text("Grupo eliminado correctamente")))

    def limpiar(self, e):
        self.nombre_grupo.value = ""
        if hasattr(self, 'grupo_seleccionado'):
            delattr(self, 'grupo_seleccionado')
        self.update()

    def actualizar_tabla(self):
        grupos = self.grupo_controller.obtener_todos_grupos()
        self.tabla.rows.clear()
        for grupo in grupos:
            self.tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(grupo.id_grupo)),
                        ft.DataCell(ft.Text(grupo.nombre_grupo)),
                    ],
                    on_select_changed=lambda e, g=grupo: self.seleccionar_grupo(e, g)
                )
            )
        self.update()

    def seleccionar_grupo(self, e, grupo):
        self.grupo_seleccionado = grupo
        self.nombre_grupo.value = grupo.nombre_grupo
        self.update()

    def validar_campos(self):
        if not self.nombre_grupo.value:
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text("El nombre del grupo es obligatorio")))
            return False
        return True