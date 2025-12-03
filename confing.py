import os

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()


## ⚙️ CONFIGURAÇÕES GERAIS DA APLICAÇÃO
# ---
# Usado para identificação geral da API/Empresa.

# Nome da empresa/cliente que está usando a API
APP_NAME = 'G-turismo'

# Descrição da empresa ou da API (aparece na documentação, ex: Swagger)
API_DESCRIPTION = 'API para gestão de...'

# Modo de operação: True para desenvolvimento, False para produção.
# O valor 'False' em string do .env é convertido para booleano.
DEBUG_MODE = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')

# Número de processos de worker para o servidor Gunicorn/Uvicorn.
# Mínimo 2 para desenvolvimento, e N+1 ou 2N+1 para produção (onde N é o número de cores da CPU).
UVICORN_WORKERS = int(os.getenv('WORKERS', 2))


## 🔑 CONFIGURAÇÕES DE AUTENTICAÇÃO JWT (JSON Web Token)
# ---
# Utilizadas para a criação, validação e expiração de tokens de acesso.

# Algoritmo de hash para a criação do JWT (ex: HS256)
JWT_ALGORITHM = os.getenv('ALGORITHM')

# Chave secreta principal para assinar o Access Token
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

# Chave secreta separada para assinar o Refresh Token (melhor segurança)
JWT_REFRESH_SECRET_KEY = os.getenv('JWT_REFRESH_SECRET_KEY')

# Tempo de expiração do Access Token em minutos (28800 minutos = 8 horas)
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 60 * 8)
)

# Tempo de expiração do Refresh Token em minutos (60 * 24 = 1 dia)
REFRESH_TOKEN_EXPIRE_MINUTES = int(
    os.getenv('REFRESH_TOKEN_EXPIRE_MINUTES', 60 * 24 * 1)
)


## 🔒 MECANISMOS DE SEGURANÇA
# ---

# Configuração do esquema OAuth2/FastAPI para o formulário de login
OAUTH2_SCHEME = OAuth2PasswordBearer(
    tokenUrl='auth/login',
    scheme_name='JWT Bearer',
)

# Contexto para hashing e verificação de senhas (recomenda-se 'bcrypt')
try:
    PASSWORD_CONTEXT = CryptContext(
        schemes=[str(os.getenv('schemes_PASSWORD'))],
        deprecated=os.getenv('DEPRECATED_PASSWORD'),
    )
    EMAIL_CONTEXT = CryptContext(
        schemes=[str(os.getenv('schemes_EMAIL'))],
        deprecated=os.getenv('DEPRECATED_EMAIL'),
    )
except Exception as e:
    print(e)


# Comfiguração para envios de email
COMPANY_EMAIL = os.getenv('COMPANY_EMAIL')
GOOGLE_APP_KEY_FOR_SENDING_EMAILS = os.getenv('GOOGLE_KEY_APP')
## 📦 EXPORTAÇÕES (Para ser importado por outros módulos)
# ---
# Define explicitamente quais configurações podem ser importadas usando 'from config import *'

__all__ = [
    'APP_NAME',
    'API_DESCRIPTION',
    'DEBUG_MODE',
    'UVICORN_WORKERS',
    'JWT_ALGORITHM',
    'JWT_SECRET_KEY',
    'JWT_REFRESH_SECRET_KEY',
    'ACCESS_TOKEN_EXPIRE_MINUTES',
    'REFRESH_TOKEN_EXPIRE_MINUTES',
    'OAUTH2_SCHEME',
    'PASSWORD_CONTEXT',
]
