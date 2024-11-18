import flet as ft
from sat_rosat.controllers.marca_controller import MarcaController

class MarcasView(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.marca_controller = MarcaController()

    def build(self):
        self.nombre_marca = ft.TextField(label="Nombre de la Marca", expand=True)
        self.grupo_dropdown = ft.Dropdown(label="Grupo", options=[], expand=True)
        
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Grupo")),
            ],
            rows=[]
        )

        self.cargar_grupos()

        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Gestión de Marcas", size=20, weight=ft.FontWeight.BOLD),
                    ft.ElevatedButton(
                        "Volver",
                        on_click=lambda _: self.page.go("/"),
                        bgcolor=ft.colors.BLUE_GREY,
                        color=ft.colors.WHITE
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([self.nombre_marca, self.grupo_dropdown]),
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

    def cargar_grupos(self):
        grupos = self.marca_controller.obtener_todos_grupos()
        self.grupo_dropdown.options = [ft.dropdown.Option(key=str(g[0]), text=g[1]) for g in grupos]
        self.update()

    def registrar(self, e):
        if self.validar_campos():
            nuevo_id = self.marca_controller.crear_marca(self.nombre_marca.value, int(self.grupo_dropdown.value))
            self.actualizar_tabla()
            self.limpiar(None)
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Marca registrada correctamente con ID: {nuevo_id}")))

    def actualizar(self, e):
        if hasattr(self, 'marca_seleccionada') and self.validar_campos():
            self.marca_controller.actualizar_marca(
                self.marca_seleccionada.id_marca,
                self.nombre_marca.value,
                int(self.grupo_dropdown.value)
            )
            self.actualizar_tabla()
            self.limpiar(None)
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text("Marca actualizada correctamente")))

    def eliminar(self, e):
        if hasattr(self, 'marca_seleccionada'):
            self.marca_controller.eliminar_marca(self.marca_seleccionada.id_marca)
            self.actualizar_tabla()
            self.limpiar(None)
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text("Marca eliminada correctamente")))

    def limpiar(self, e):
        self.nombre_marca.value = ""
        self.grupo_dropdown.value = None
        if hasattr(self, 'marca_seleccionada'):
            delattr(self, 'marca_seleccionada')
        self.update()

    def actualizar_tabla(self):
        marcas = self.marca_controller.obtener_todas_marcas()
        self.tabla.rows.clear()
        for marca in marcas:
            self.tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(marca.id_marca)),
                        ft.DataCell(ft.Text(marca.nombre_marca)),
                        ft.DataCell(ft.Text(marca.nombre_grupo)),
                    ],
                    on_select_changed=lambda e, m=marca: self.seleccionar_marca(e, m)
                )
            )
        self.update()

    def seleccionar_marca(self, e, marca):
        self.marca_seleccionada = marca
        self.nombre_marca.value = marca.nombre_marca
        self.grupo_dropdown.value = str(marca.grupo_id)
        self.update()

    def validar_campos(self):
        if not self.nombre_marca.value or not self.grupo_dropdown.value:
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text("Todos los campos son obligatorios")))
            return False
        return True