# Desafio de Automação de API - DemoQA BookStore

Este repositório contém a solução para um desafio técnico de automação de testes de API, utilizando a API `BookStore` do site [DemoQA](https://demoqa.com/swagger/).


## Fluxo de Teste E2E

O fluxo de automação principal validado neste projeto consiste em:

1.  **Criar um Usuário:** Registra um novo usuário com credenciais dinâmicas.
2.  **Gerar Token:** Autentica o usuário recém-criado e obtém um token de acesso.
3.  **Confirmar Autorização:** Valida se o usuário está devidamente autorizado na plataforma.
4.  **Listar Livros:** Obtém a lista de todos os livros disponíveis no sistema.
5.  **Adicionar Livros:** Seleciona dois livros da lista e os "aluga" (adiciona à coleção) do usuário.
6.  **Validar Detalhes:** Busca os detalhes completos do usuário e confirma que os dois livros selecionados estão corretamente associados à sua conta.

---

## Arquitetura e Padrões de Projeto

A solução foi estruturada para ser **escalável**, **legível** e **de fácil manutenção**.

* **Padrão API Client:** A lógica de interação com a API (construção de requisições, headers, endpoints) é abstraída em classes de cliente (`src/api_clients/`). Isso funciona de forma análoga ao padrão *Page Object* para testes de UI, separando a lógica de teste da lógica de automação.
* **Fixtures do Pytest:** O `conftest.py` é utilizado para injetar dependências, como as instâncias dos clientes de API e uma sessão `requests` compartilhada, garantindo que o token de autorização seja persistido entre as requisições.
* **Testes de Fluxo (E2E) com Dependência:** O `pytest-dependency` é usado para garantir que o fluxo E2E seja executado na ordem correta. Se um passo crítico (como a criação do usuário) falhar, os testes subsequentes que dependem dele são pulados (SKIPPED), economizando tempo de execução e fornecendo um feedback claro.
* **Geração de Dados Dinâmicos:** A biblioteca `faker` é usada (`src/utils/data_generator.py`) para criar um novo usuário a cada execução, garantindo que os testes sejam idempotentes e não falhem por conflitos de dados (ex: "usuário já existe").

---

##  Tecnologias Utilizadas

* **[Python 3.10+](https://www.python.org/)**: Linguagem de programação principal.
* **[Pytest](https://docs.pytest.org/)**: Framework de testes para estruturação, execução e asserções.
* **[Requests](https://requests.readthedocs.io/)**: Biblioteca para realizar as requisições HTTP.
* **[pytest-dependency](https://pypi.org/project/pytest-dependency/)**: Plugin para gerenciar a ordem e dependência entre os testes.
* **[Faker](https://faker.readthedocs.io/)**: Para geração de dados de teste dinâmicos.
* **[pytest-html](https://pypi.org/project/pytest-html/)**: (Opcional) Para geração de relatórios de teste em um arquivo HTML único.
* **[Allure Framework](https://qameta.io/allure-framework/)**: (Opcional) Para geração de dashboards de relatório interativos e avançados.

---

##  Instalação e Configuração

Siga os passos abaixo para configurar o ambiente e executar o projeto.

### 1. Pré-requisitos

* Python 3.10 ou superior
* `pip` (gerenciador de pacotes do Python)
* Git

### 2. Clone o Repositório


* git clone [https://github.com/silvandr0/demoqa-api-automation.git](https://github.com/silvandr0/demoqa-api-automation.git)
* cd demoqa-api-automation

### 3. Crie e Ative um Ambiente Virtual

Windows:
python -m venv venv
.\venv\Scripts\activate

macOS / Linux:
python3 -m venv venv
source venv/bin/activate

### 4. Instale as Dependências

pip install -r requirements.txt

### 5. Como Executar os Testes

pytest --html=report.html --self-contained-html

---

### Autor

Desenvolvido por **Silvandro Pedrozo**  
💼 Engenheiro de Qualidade de Software | Especialista em Automação de Testes  
🔗 [LinkedIn](https://www.linkedin.com/in/silvandro)

