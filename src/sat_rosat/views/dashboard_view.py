import flet as ft

class DashboardView(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

    def build(self):
        # Creamos un contenedor para el NavigationRail con altura fija
        self.sidebar = ft.Container(
            content=ft.NavigationRail(
                selected_index=0,
                label_type=ft.NavigationRailLabelType.ALL,
                min_width=100,
                min_extended_width=400,
                group_alignment=-0.9,
                destinations=[
                    ft.NavigationRailDestination(
                        icon=ft.icons.HOME_OUTLINED,
                        selected_icon=ft.icons.HOME,
                        label="Inicio"
                    ),
                    ft.NavigationRailDestination(
                        icon=ft.icons.REPORT_PROBLEM_OUTLINED,
                        selected_icon=ft.icons.REPORT_PROBLEM,
                        label="Avisos"
                    ),
                    ft.NavigationRailDestination(
                        icon=ft.icons.PEOPLE_OUTLINED,
                        selected_icon=ft.icons.PEOPLE,
                        label="Clientes"
                    ),
                    ft.NavigationRailDestination(
                        icon=ft.icons.SETTINGS_OUTLINED,
                        selected_icon=ft.icons.SETTINGS,
                        label="Configuración"
                    ),
                ],
                on_change=self.sidebar_changed
            ),
            expand=True
        )

        # Contenedor principal para el contenido
        self.content_area = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Bienvenido al Dashboard de SAT Rosat", 
                           size=24,
                           text_align=ft.TextAlign.CENTER)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            expand=True,
            padding=20
        )

        # Barra superior
        top_bar = ft.Container(
            content=ft.Row(
                [
                    ft.Text(
                        "SAT Rosat Dashboard",
                        size=20,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.IconButton(
                        icon=ft.icons.LOGOUT,
                        icon_color=ft.colors.BLACK54,
                        tooltip="Cerrar sesión",
                        on_click=self.logout
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            padding=10,
            bgcolor=ft.colors.SURFACE_VARIANT,
        )

        # Estructura principal
        return ft.Container(
            content=ft.Row(
                [
                    # Columna izquierda con el NavigationRail
                    self.sidebar,
                    ft.VerticalDivider(width=1),
                    # Columna derecha con el contenido
                    ft.Column(
                        [
                            top_bar,
                            self.content_area
                        ],
                        expand=True
                    )
                ],
                expand=True,
                spacing=0
            ),
            expand=True
        )

    def sidebar_changed(self, e):
        index = e.control.selected_index
        content = None
        
        if index == 0:
            content = ft.Text("Bienvenido al Dashboard de SAT Rosat", size=24)
        elif index == 1:
            content = ft.Text("Gestión de Avisos", size=24)
        elif index == 2:
            content = ft.Text("Gestión de Clientes", size=24)
        elif index == 3:
            content = ft.Text("Configuración", size=24)
        
        self.content_area.content = ft.Column(
            [content],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        self.content_area.update()

    def logout(self, e):
        self.page.go('/login')