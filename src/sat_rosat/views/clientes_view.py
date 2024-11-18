import flet as ft
from sat_rosat.controllers.cliente_controller import ClienteController
from sat_rosat.controllers.poblacion_controller import PoblacionController

class ClientesView(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.cliente_controller = ClienteController()

    def build(self):
        # Campos del formulario
        self.codigo_cliente = ft.TextField(label="Código Cliente", expand=1)
        self.nombre_cliente = ft.TextField(label="Nombre Cliente", expand=2)
        self.nombre_cliente_comercial = ft.TextField(label="Nombre Comercial", expand=2)
        self.nif_cliente = ft.TextField(label="NIF", expand=1)
        self.domicilio = ft.TextField(label="Domicilio", expand=2)
        self.poblacion_combo = ft.Dropdown(label="Población", expand=1)
        self.telefono_1 = ft.TextField(label="Teléfono 1", expand=1)
        self.telefono_2 = ft.TextField(label="Teléfono 2", expand=1)
        self.nota_cliente = ft.TextField(label="Nota", multiline=True, expand=2)

        # Botones
        self.btn_registrar = ft.ElevatedButton("Registrar", on_click=self.registrar, bgcolor=ft.colors.BLUE, color=ft.colors.WHITE)
        self.btn_actualizar = ft.ElevatedButton("Actualizar", on_click=self.actualizar, bgcolor=ft.colors.ORANGE, color=ft.colors.WHITE)
        self.btn_eliminar = ft.ElevatedButton("Eliminar", on_click=self.eliminar, bgcolor=ft.colors.RED, color=ft.colors.WHITE)
        self.btn_limpiar = ft.ElevatedButton("Limpiar", on_click=self.limpiar, bgcolor=ft.colors.GREY, color=ft.colors.WHITE)

        # Tabla
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Código")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("NIF")),
                ft.DataColumn(ft.Text("Población")),
                ft.DataColumn(ft.Text("Teléfono 1")),
            ],
            rows=[],
        )

        # Cargar poblaciones en el combo
        self.cargar_poblaciones()

        return ft.Container(
            content=ft.Column([
                ft.Text("Gestión de Clientes", size=20, weight=ft.FontWeight.BOLD),
                ft.Row([self.codigo_cliente, self.nombre_cliente, self.nombre_cliente_comercial], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([self.nif_cliente, self.domicilio, self.poblacion_combo], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([self.telefono_1, self.telefono_2, self.nota_cliente], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([self.btn_registrar, self.btn_actualizar, self.btn_eliminar, self.btn_limpiar], alignment=ft.MainAxisAlignment.CENTER),
                self.tabla
            ], spacing=20),
            padding=20,
            expand=True
        )


    def cargar_poblaciones(self):
        poblaciones = PoblacionController.obtener_todas_poblaciones()
        self.poblacion_combo.options = [ft.dropdown.Option(key=str(p['id_poblacion']), text=p['nombre_poblacion']) for p in poblaciones]
        self.update()

    def registrar(self, e):
        if self.validar_campos():
            cliente = {
                "codigo_cliente": self.codigo_cliente.value,
                "nombre_cliente": self.nombre_cliente.value,
                "nombre_cliente_comercial": self.nombre_cliente_comercial.value,
                "nif_cliente": self.nif_cliente.value,
                "domicilio": self.domicilio.value,
                "poblacion_id": int(self.poblacion_combo.value),
                "telefono_1": int(self.telefono_1.value) if self.telefono_1.value else None,
                "telefono_2": int(self.telefono_2.value) if self.telefono_2.value else None,
                "nota_cliente": self.nota_cliente.value
            }
            self.cliente_controller.crear_cliente(cliente)
            self.actualizar_tabla()
            self.limpiar(None)
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text("Cliente registrado correctamente")))

    def actualizar(self, e):
        if hasattr(self, 'cliente_seleccionado') and self.validar_campos():
            cliente = {
                "id_cliente": self.cliente_seleccionado['id_cliente'],
                "codigo_cliente": self.codigo_cliente.value,
                "nombre_cliente": self.nombre_cliente.value,
                "nombre_cliente_comercial": self.nombre_cliente_comercial.value,
                "nif_cliente": self.nif_cliente.value,
                "domicilio": self.domicilio.value,
                "poblacion_id": int(self.poblacion_combo.value),
                "telefono_1": int(self.telefono_1.value) if self.telefono_1.value else None,
                "telefono_2": int(self.telefono_2.value) if self.telefono_2.value else None,
                "nota_cliente": self.nota_cliente.value
            }
            self.cliente_controller.actualizar_cliente(cliente)
            self.actualizar_tabla()
            self.limpiar(None)
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text("Cliente actualizado correctamente")))

    def eliminar(self, e):
        if hasattr(self, 'cliente_seleccionado'):
            self.cliente_controller.eliminar_cliente(self.cliente_seleccionado['id_cliente'])
            self.actualizar_tabla()
            self.limpiar(None)
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text("Cliente eliminado correctamente")))

    def limpiar(self, e):
        self.codigo_cliente.value = ""
        self.nombre_cliente.value = ""
        self.nombre_cliente_comercial.value = ""
        self.nif_cliente.value = ""
        self.domicilio.value = ""
        self.poblacion_combo.value = None
        self.telefono_1.value = ""
        self.telefono_2.value = ""
        self.nota_cliente.value = ""
        if hasattr(self, 'cliente_seleccionado'):
            delattr(self, 'cliente_seleccionado')
        self.update()

    def actualizar_tabla(self):
        clientes = self.cliente_controller.obtener_todos_clientes()
        self.tabla.rows.clear()
        for cliente in clientes:
            self.tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(cliente['id_cliente'])),
                        ft.DataCell(ft.Text(cliente['codigo_cliente'])),
                        ft.DataCell(ft.Text(cliente['nombre_cliente'])),
                        ft.DataCell(ft.Text(cliente['nif_cliente'])),
                        ft.DataCell(ft.Text(cliente['nombre_poblacion'])),
                        ft.DataCell(ft.Text(cliente['telefono_1'])),
                    ],
                    on_select_changed=lambda e, c=cliente: self.seleccionar_cliente(e, c)
                )
            )
        self.update()

    def seleccionar_cliente(self, e, cliente):
        self.cliente_seleccionado = cliente
        self.codigo_cliente.value = cliente['codigo_cliente']
        self.nombre_cliente.value = cliente['nombre_cliente']
        self.nombre_cliente_comercial.value = cliente['nombre_cliente_comercial']
        self.nif_cliente.value = cliente['nif_cliente']
        self.domicilio.value = cliente['domicilio']
        self.poblacion_combo.value = str(cliente['poblacion_id'])
        self.telefono_1.value = str(cliente['telefono_1']) if cliente['telefono_1'] else ""
        self.telefono_2.value = str(cliente['telefono_2']) if cliente['telefono_2'] else ""
        self.nota_cliente.value = cliente['nota_cliente']
        self.update()

    def validar_campos(self):
        if not self.codigo_cliente.value or not self.nombre_cliente.value or not self.nif_cliente.value:
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text("Los campos Código, Nombre y NIF son obligatorios")))
            return False
        if len(self.nif_cliente.value) != 9:
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text("El NIF debe tener 9 caracteres")))
            return False
        if self.telefono_1.value and not self.telefono_1.value.isdigit():
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text("El Teléfono 1 debe ser un número")))
            return False
        if self.telefono_2.value and not self.telefono_2.value.isdigit():
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text("El Teléfono 2 debe ser un número")))
            return False
        return True