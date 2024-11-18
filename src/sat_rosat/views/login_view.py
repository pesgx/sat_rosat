import flet as ft
from sat_rosat.controllers.auth_controller import AuthController

class LoginView(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.auth_controller = AuthController()

    def build(self):
        self.username = ft.TextField(label="Usuario", autofocus=True)
        self.password = ft.TextField(label="Contraseña", password=True)
        self.login_button = ft.ElevatedButton(text="Iniciar sesión", on_click=self.login)
        self.message = ft.Text()

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("SAT Rosat - Inicio de sesión", size=24, weight=ft.FontWeight.BOLD),
                    self.username,
                    self.password,
                    self.login_button,
                    self.message
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            width=400,
            padding=20,
        )

    def login(self, e):
        if self.auth_controller.authenticate(self.username.value, self.password.value):
            self.page.go('/')  # Redirige a la página principal
        else:
            self.message.value = "Usuario o contraseña incorrectos"
            self.message.color = ft.colors.RED
            self.update()