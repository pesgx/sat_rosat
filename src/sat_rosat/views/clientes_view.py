
import flet as ft
from sat_rosat.controllers.cliente_controller import ClienteController

class ClientesView(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.controller = ClienteController()

    def build(self):
        # Campos del formulario
        self.codigo_cliente = ft.TextField(label="Código Cliente", expand=1)
        self.nombre_cliente = ft.TextField(label="Nombre Cliente", expand=2)
        self.nif_cliente = ft.TextField(label="NIF (9 caracteres)", expand=1)
        self.poblacion_combo = ft.Dropdown(label="Población", expand=2)
        self.telefono = ft.TextField(label="Teléfono", expand=1)
        self.nota = ft.TextField(label="Nota", multiline=True, expand=2)

        # Botones
        self.btn_registrar = ft.ElevatedButton("Registrar", on_click=self.registrar)
        self.btn_actualizar = ft.ElevatedButton("Actualizar", on_click=self.actualizar)
        self.btn_eliminar = ft.ElevatedButton("Eliminar", on_click=self.eliminar)
        self.btn_limpiar = ft.ElevatedButton("Limpiar", on_click=self.limpiar)

        # Tabla de clientes
        self.tabla_clientes = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Código")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("NIF")),
                ft.DataColumn(ft.Text("Población")),
                ft.DataColumn(ft.Text("Teléfono")),
            ],
            rows=[],
        )

        self.cargar_poblaciones()
        self.actualizar_tabla()

        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [self.codigo_cliente, self.nombre_cliente, self.nif_cliente],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Row([self.poblacion_combo, self.telefono, self.nota]),
                    ft.Row(
                        [self.btn_registrar, self.btn_actualizar, self.btn_eliminar, self.btn_limpiar],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    self.tabla_clientes,
                ],
                spacing=20,
            ),
            padding=20,
            expand=True,
        )

    def cargar_poblaciones(self):
        try:
            poblaciones = self.controller.obtener_poblaciones()
            self.poblacion_combo.options = [ft.dropdown.Option(key=str(p['id_poblacion']), text=p['nombre_poblacion']) for p in poblaciones]
            self.update()
        except Exception as e:
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Error al cargar poblaciones: {e}")))

    def actualizar_tabla(self):
        try:
            clientes = self.controller.obtener_clientes()
            self.tabla_clientes.rows.clear()
            for cliente in clientes:
                self.tabla_clientes.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(cliente['id_cliente']))),
                            ft.DataCell(ft.Text(cliente['codigo_cliente'])),
                            ft.DataCell(ft.Text(cliente['nombre_cliente'])),
                            ft.DataCell(ft.Text(cliente['nif_cliente'])),
                            ft.DataCell(ft.Text(cliente['nombre_poblacion'])),
                            ft.DataCell(ft.Text(cliente['telefono'])),
                        ]
                    )
                )
            self.update()
        except Exception as e:
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Error al cargar tabla de clientes: {e}")))

    def registrar(self, e):
        try:
            self.controller.registrar_cliente(
                self.codigo_cliente.value,
                self.nombre_cliente.value,
                self.nif_cliente.value,
                self.poblacion_combo.value,
                self.telefono.value,
                self.nota.value,
            )
            self.actualizar_tabla()
            self.limpiar(None)
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text("Cliente registrado correctamente")))
        except Exception as e:
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Error al registrar cliente: {e}")))

    def actualizar(self, e):
        # Similar lógica para actualizar un cliente
        pass

    def eliminar(self, e):
        # Similar lógica para eliminar un cliente
        pass

    def limpiar(self, e):
        self.codigo_cliente.value = ""
        self.nombre_cliente.value = ""
        self.nif_cliente.value = ""
        self.poblacion_combo.value = None
        self.telefono.value = ""
        self.nota.value = ""
        self.update()
