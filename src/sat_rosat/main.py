import flet as ft
from sat_rosat.views.login_view import LoginView
from sat_rosat.views.main_view import MainView
from sat_rosat.views.poblacion_view import PoblacionView
from sat_rosat.views.aparatos_view import AparatosView
from sat_rosat.views.clientes_view import ClientesView
from sat_rosat.views.marcas_view import MarcasView
from sat_rosat.views.grupos_view import GruposView

def main(page: ft.Page):
    page.title = "SAT ROSAT"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0

    def route_change(route):
        page.views.clear()
        if page.route == "/login":
            page.views.append(LoginView(page))
        elif page.route == "/":
            page.views.append(MainView(page))
        elif page.route == "/poblacion":
            page.views.append(PoblacionView(page))
        elif page.route == "/aparatos":
            page.views.append(AparatosView(page))
        elif page.route == "/clientes":
            page.views.append(ClientesView(page))
        elif page.route == "/marcas":
            page.views.append(MarcasView(page))
        elif page.route == "/grupos":
            page.views.append(GruposView(page))
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/login")

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)