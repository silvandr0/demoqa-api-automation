import requests

class BaseClient:
    """
    Cliente base para todas as interações de API.
    A sessão (com a base_url) é injetada pelo conftest.py
    """
    def __init__(self):
        # A sessão será injetada pelo pytest (veja o conftest.py)
        self.session = None 

    def post(self, endpoint, data=None, headers=None):
        """Helper para requisições POST."""
        url = endpoint  
        
        # O conftest.py vai adicionar a base_url (ex: https://demoqa.com)
        return self.session.post(url, json=data, headers=headers)

    def get(self, endpoint, headers=None):
        """Helper para requisições GET."""
        url = endpoint 
        
        # O conftest.py vai adicionar a base_url (ex: https://demoqa.com)
        return self.session.get(url, headers=headers)

    def set_auth_token(self, token):
        """Adiciona o token de autorização na sessão."""
        self.session.headers.update({"Authorization": f"Bearer {token}"})