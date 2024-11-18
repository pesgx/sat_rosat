class AuthController:
    def authenticate(self, username: str, password: str) -> bool:
        # Aquí deberías implementar la lógica real de autenticación
        # Por ahora, solo permitiremos un usuario de prueba
        return username == "a" and password == "a"