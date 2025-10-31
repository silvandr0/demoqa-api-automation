from faker import Faker

fake = Faker()

def get_random_user():
    """
    Gera um nome de usuário e uma senha que atende aos
    requisitos de complexidade da API.
    """
    username = f"testuser_{fake.user_name()}_{fake.random_int(min=1000, max=9999)}"
    
    # Política de senha: Pelo menos 8 caracteres, 1 maiúscula, 1 minúscula, 1 número, 1 especial.
    password = f"P@ssword{fake.random_int(min=100, max=999)}!"
    
    return {"username": username, "password": password}