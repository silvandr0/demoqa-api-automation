import pytest
from src.utils.data_generator import get_random_user

# Marca a classe inteira como 'e2e' e dependente
@pytest.mark.e2e
@pytest.mark.dependency()
class TestE2EBookFlow:
    
    # Usamos variáveis de classe para compartilhar o estado entre os testes
    # (usuário, ID, token, livros)
    user_data = {}
    user_id = None
    token = None
    books_to_add_isbns = []

    def test_01_create_user(self, account_client):
        """Passo 1: Criar um usuário."""
        TestE2EBookFlow.user_data = get_random_user()
        username = self.user_data['username']
        password = self.user_data['password']
        
        print(f"\n[Passo 1] Criando usuário: {username}")
        response = account_client.create_user(username, password)
        
        assert response.status_code == 201, f"Falha ao criar usuário. Response: {response.text}"
        
        response_data = response.json()
        assert response_data['username'] == username
        assert 'userID' in response_data
        TestE2EBookFlow.user_id = response_data['userID']
        print(f"Usuário criado com ID: {self.user_id}")

    @pytest.mark.dependency(depends=["TestE2EBookFlow::test_01_create_user"])
    def test_02_generate_token(self, account_client, bookstore_client):
        """Passo 2: Gerar token para o usuário."""
        username = self.user_data['username']
        password = self.user_data['password']
        
        print(f"\n[Passo 2] Gerando token para: {username}")
        response = account_client.generate_token(username, password)
        
        assert response.status_code == 200, f"Falha ao gerar token. Response: {response.text}"
        
        response_data = response.json()
        assert response_data['status'] == 'Success'
        assert 'token' in response_data
        TestE2EBookFlow.token = response_data['token']
        print("Token gerado com sucesso.")
        
        # Injeta o token nas sessões de ambos os clientes para requisições futuras
        account_client.set_auth_token(self.token)
        bookstore_client.set_auth_token(self.token)

    @pytest.mark.dependency(depends=["TestE2EBookFlow::test_02_generate_token"])
    def test_03_authorize_user(self, account_client):
        """Passo 3: Confirmar que o usuário está autorizado."""
        username = self.user_data['username']
        password = self.user_data['password']

        print(f"\n[Passo 3] Verificando autorização (endpoint /Authorized)")
        response = account_client.is_authorized(username, password)
        
        assert response.status_code == 200
        # O corpo da resposta deve ser 'true' (booleano)
        assert response.json() is True, "Usuário não foi autorizado com sucesso."
        print("Usuário autorizado com sucesso.")

    @pytest.mark.dependency(depends=["TestE2EBookFlow::test_03_authorize_user"])
    def test_04_list_and_select_books(self, bookstore_client):
        """Passo 4: Listar livros e selecionar dois."""
        print(f"\n[Passo 4] Listando livros disponíveis")
        response = bookstore_client.get_all_books()
        
        assert response.status_code == 200
        response_data = response.json()
        assert 'books' in response_data
        
        # Garante que temos pelo menos 2 livros para escolher
        assert len(response_data['books']) >= 2
        
        # Seleciona os dois primeiros livros da lista
        TestE2EBookFlow.books_to_add_isbns = [
            response_data['books'][0]['isbn'],
            response_data['books'][1]['isbn']
        ]
        print(f"Livros selecionados (ISBN): {self.books_to_add_isbns}")

    @pytest.mark.dependency(depends=["TestE2EBookFlow::test_04_list_and_select_books"])
    def test_05_add_books_to_user(self, bookstore_client):
        """Passo 5: Alugar/Adicionar os livros selecionados ao usuário."""
        user_id = TestE2EBookFlow.user_id
        isbns = TestE2EBookFlow.books_to_add_isbns
        
        print(f"\n[Passo 5] Adicionando livros ao usuário ID: {user_id}")
        response = bookstore_client.add_books_to_user(user_id, isbns)
        
        assert response.status_code == 201, f"Falha ao adicionar livros. Response: {response.text}"
        
        response_data = response.json()
        assert 'books' in response_data
        added_isbns = [book['isbn'] for book in response_data['books']]
        assert sorted(added_isbns) == sorted(isbns), "Os livros na resposta não batem com os enviados."
        print("Livros adicionados com sucesso.")

    @pytest.mark.dependency(depends=["TestE2EBookFlow::test_05_add_books_to_user"])
    def test_06_get_user_details_with_books(self, account_client):
        """Passo 6: Listar detalhes do usuário e verificar os livros alugados."""
        user_id = TestE2EBookFlow.user_id
        
        print(f"\n[Passo 6] Buscando detalhes finais do usuário: {self.user_data['username']}")
        response = account_client.get_user_details(user_id)
        
        assert response.status_code == 200, f"Falha ao buscar detalhes do usuário. Response: {response.text}"
        
        response_data = response.json()
        
        # Validações finais
        assert response_data['userId'] == user_id
        assert response_data['username'] == self.user_data['username']
        assert 'books' in response_data
        
        # Verifica se os livros no perfil do usuário são os que adicionamos
        user_books = response_data['books']
        assert len(user_books) == 2
        
        user_isbns = sorted([book['isbn'] for book in user_books])
        expected_isbns = sorted(TestE2EBookFlow.books_to_add_isbns)
        
        assert user_isbns == expected_isbns, "Os livros no perfil do usuário não correspondem aos alugados."
        
        print("\n--- SUCESSO: Fluxo E2E Concluído ---")
        print(f"Usuário: {response_data['username']} (ID: {response_data['userId']})")
        print("Livros Alugados:")
        for book in user_books:
            print(f"  - Título: {book['title']} (ISBN: {book['isbn']})")