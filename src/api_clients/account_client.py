from src.api_clients.base_client import BaseClient

class AccountClient(BaseClient):
    """
    Cliente para os endpoints de /Account/v1
    """
    def __init__(self):
        super().__init__()
        self.endpoint = "/Account/v1"

    def create_user(self, username, password):
        """Cria um novo usuário."""
        payload = {"userName": username, "password": password}
        return self.post(f"{self.endpoint}/User", data=payload)

    def generate_token(self, username, password):
        """Gera um token de autenticação."""
        payload = {"userName": username, "password": password}
        return self.post(f"{self.endpoint}/GenerateToken", data=payload)

    def is_authorized(self, username, password):
        """Verifica se as credenciais são válidas."""
        payload = {"userName": username, "password": password}
        return self.post(f"{self.endpoint}/Authorized", data=payload)

    def get_user_details(self, user_id):
        """Busca os detalhes do usuário (requer token na sessão)."""
        # O token deve ser setado na sessão antes de chamar este método
        return self.get(f"{self.endpoint}/User/{user_id}")