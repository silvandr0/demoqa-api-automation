import pytest
import requests
from src.api_clients.account_client import AccountClient
from src.api_clients.bookstore_client import BookStoreClient

@pytest.fixture(scope="session")
def shared_session():
    """Cria uma única sessão de requests para todos os testes."""
    session = requests.Session()
    session.base_url = "https://demoqa.com" # Adicionando base_url à sessão
    
    # Sobrescrevendo métodos para incluir a base_url
    original_post = session.post
    original_get = session.get
    
    session.post = lambda url, **kwargs: original_post(session.base_url + url, **kwargs)
    session.get = lambda url, **kwargs: original_get(session.base_url + url, **kwargs)
    
    return session

@pytest.fixture(scope="session")
def account_client(shared_session):
    """Fixture para o AccountClient usando a sessão compartilhada."""
    client = AccountClient()
    client.session = shared_session # Injeta a sessão compartilhada
    return client

@pytest.fixture(scope="session")
def bookstore_client(shared_session):
    """Fixture para o BookStoreClient usando a sessão compartilhada."""
    client = BookStoreClient()
    client.session = shared_session # Injeta a sessão compartilhada
    return client