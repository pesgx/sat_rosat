import flet as ft

class MainView(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

    def build(self):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Text("SAT Rosat - Página Principal", size=20, weight=ft.FontWeight.BOLD),
                                ft.IconButton(ft.icons.LOGOUT, on_click=self.logout)
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        padding=10,
                        bgcolor=ft.colors.SURFACE_VARIANT,
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("Seleccione una tabla para gestionar:", size=20, weight=ft.FontWeight.BOLD),
                                ft.ElevatedButton(text="Poblaciones", on_click=self.navigate_to_poblaciones),
                                ft.ElevatedButton(text="Avisos", on_click=self.navigate_to_table),
                                ft.ElevatedButton(text="Clientes", on_click=lambda _: self.page.go("/clientes")),
                                ft.ElevatedButton(text="Aparatos", on_click=lambda _: self.page.go("/aparatos")),
                                ft.ElevatedButton(text="Marcas", on_click=lambda _: self.page.go("/marcas")),
                                ft.ElevatedButton(text="Empleados", on_click=self.navigate_to_table),
                                ft.ElevatedButton(text="Compañías", on_click=self.navigate_to_table),
                                ft.ElevatedButton(text="Grupos", on_click=lambda _: self.page.go("/grupos")),
                                ft.ElevatedButton(text="Estados", on_click=self.navigate_to_table),
                                ft.ElevatedButton(text="Artículos", on_click=self.navigate_to_table),
                                ft.ElevatedButton(text="Agenda", on_click=self.navigate_to_table),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20,
                        ),
                        padding=ft.padding.all(20),
                        alignment=ft.alignment.center,
                    ),
                ],
                expand=True,
            ),
            expand=True,
        )

    def navigate_to_table(self, e):
        e.control.page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Navegando a {e.control.text}")))
        
    def navigate_to_poblaciones(self, e):
        self.page.go('/poblacion')

    def logout(self, e):
        self.page.go('/login')