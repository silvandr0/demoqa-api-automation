from src.api_clients.base_client import BaseClient

class BookStoreClient(BaseClient):
    """
    Cliente para os endpoints de /BookStore/v1
    """
    def __init__(self):
        super().__init__()
        self.endpoint = "/BookStore/v1"

    def get_all_books(self):
        """Lista todos os livros disponíveis."""
        return self.get(f"{self.endpoint}/Books")

    def add_books_to_user(self, user_id, isbns_list):
        """Adiciona uma coleção de livros ao usuário (requer token)."""
        # Converte a lista de strings ISBN para o formato esperado pela API
        collection = [{"isbn": isbn} for isbn in isbns_list]
        payload = {
            "userId": user_id,
            "collectionOfIsbns": collection
        }
        return self.post(f"{self.endpoint}/Books", data=payload)