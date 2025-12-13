# Módulo de Autenticação (Auth)

## Visão Geral

Este módulo é responsável por gerenciar a autenticação de usuários e o processo de cadastro no sistema. Ele fornece funcionalidades para criação de contas, login, gerenciamento de tokens JWT e tratamento centralizado de erros.

## Estrutura do Diretório

```
src/auth/
├── create_account.py     # Criação de contas de usuário
├── dependencies.py       # Dependências específicas do módulo
├── exceptions.py         # Exceções HTTP personalizadas
├── __init__.py          # Inicialização do pacote
├── README.md            # Documentação do módulo
├── route.py             # Rotas da API
├── schemas.py           # Modelos Pydantic
└── utils.py             # Funções utilitárias
```

## Arquivos e Responsabilidades

### 1. `create_account.py`

Responsável pela criação de novas contas de usuário no sistema.

**Função Principal:**
```python
async def create_account(target) -> Dict[str, Any]:
    """
    Cria uma nova conta de usuário no sistema.

    Args:
        target: Dicionário contendo dados do usuário

    Returns:
        Dict com informações básicas da conta criada

    Raises:
        HTTPException: Em caso de erros de validação ou conflitos
    """
```

**Características:**
- Valida campos obrigatórios antes da criação
- Verifica unicidade de email usando hash de busca
- Criptografa senha antes do armazenamento
- Define conta como não verificada inicialmente
- Retorna apenas informações básicas da conta criada

**Exemplo de uso:**
```python
# Dentro de route.py
@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(target: CreateUser):
    """Endpoint para registro de novos usuários"""

    create = await create_account(target=dict(target))
    if create:
        return {'message': 'Conta criada com sucesso'}
    return create
```

### 2. `exceptions.py`

Centraliza todas as exceções HTTP personalizadas do módulo, melhorando a legibilidade e manutenibilidade do código.

**Vantagens:**
- **Consistência**: Mensagens de erro padronizadas
- **Reutilização**: Mesmos erros em diferentes partes do módulo
- **Manutenção**: Alterações centralizadas em um único local

**Exceções Disponíveis:**
```python
# Erro ao tentar enviar código de verificação por email
ERROR_SEND_EMAIL = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail='Não foi possível enviar o código de verificação. Tente novamente mais tarde.'
)

# Erro de campos obrigatórios não preenchidos
ERROR_MISSING_FIELDS = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Preencha todos os campos obrigatórios.'
)

# Erro de email já cadastrado
EMAIL_ALREADY_EXISTS = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Este endereço de email já está cadastrado no sistema.'
)

# Uso nos outros arquivos:
from src.auth.exceptions import EMAIL_ALREADY_EXISTS, ERROR_MISSING_FIELDS
```

### 3. `schemas.py`

Define todos os modelos Pydantic utilizados exclusivamente pelo módulo de autenticação.

**Modelos Disponíveis:**
```python
class LoginResponse(BaseModel):
    """Resposta após login bem-sucedido"""
    username: str           # Nome de usuário
    access_token: str       # Token JWT para autenticação
    refresh_token: str      # Token para renovação da sessão
    photo_profile: str      # URL da foto de perfil


class CreateUser(BaseModel):
    """Validação de dados para criação de conta"""
    username: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    status: bool = True


class SystemUser(BaseModel):
    """Representação do usuário autenticado no sistema"""
    id: int
    username: str
    email: EmailStr
    photo: Optional[str] = None
    status: bool = True

    model_config = {'from_attributes': True}


class TokenPayload(BaseModel):
    """Payload extraído dos tokens JWT"""
    sub: Optional[str] = None  # Subject (ID do usuário)
    exp: Optional[int] = None  # Timestamp de expiração
```

### 4. `utils.py`

Contém funções utilitárias específicas do módulo, evitando repetição de código.

**Função Principal:**
```python
async def checking_account(target: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Autentica um usuário com email e senha.

    Args:
        target: Dicionário com 'email' e 'password'

    Returns:
        Dict com dados do usuário e tokens JWT ou None
    """
```

**Fluxo da Função:**
1. **Busca do usuário** por email
2. **Validação da senha** criptografada
3. **Geração de tokens** JWT (access e refresh)
4. **Tratamento de erros** específicos para cada cenário

### 5. `route.py`

Define as rotas da API relacionadas à autenticação.

**Endpoints Implementados:**
- `POST /register` - Criação de nova conta
- `POST /login` - Autenticação de usuário
- `POST /refresh` - Renovação de token
- `GET /me` - Informações do usuário atual

**Exemplo de Rota:**
```python
@router.post('/login', response_model=LoginResponse)
async def login(credentials: LoginRequest):
    """Autentica um usuário e retorna tokens JWT"""
    result = await checking_account(dict(credentials))
    if result is None:
        raise INVALID_CREDENTIALS
    return result
```

### 6. `dependencies.py`

Atualmente vazio, destinado a armazenar dependências específicas do módulo como:
- Injeção de dependências personalizadas
- Middlewares específicos
- Configurações de contexto

### 7. `utils.py` (Funções Adicionais)

**Outras funções utilitárias podem incluir:**
- Validação de formato de email
- Normalização de dados de entrada
- Cálculos de segurança (força de senha, etc.)
- Funções auxiliares para tokens

## Padrões de Implementação

### 1. **Tratamento de Erros**
- Use exceções de `exceptions.py` para erros conhecidos
- Mantenha tratamento `try/except` específico em cada função
- Evite expor detalhes internos do sistema em respostas de erro

### 2. **Validação de Dados**
- Utilize schemas do Pydantic para validação de entrada
- Implemente validações de negócio nas funções de serviço
- Sempre sanitize dados antes do processamento

### 3. **Segurança**
- Nunca armazene senhas em texto plano
- Use hash específico para busca de emails
- Valide tokens JWT em todas as rotas protegidas
- Implemente rate limiting para endpoints sensíveis

### 4. **Organização do Código**
- Cada arquivo tem responsabilidade única
- Funções pequenas e focadas
- Comentários em português para contexto local
- Nomeclatura clara e consistente

## Boas Práticas

1. **Imports Relativos**: Use imports relativos dentro do módulo
2. **Documentação**: Mantenha docstrings atualizadas em todas as funções
3. **Testes**: Cada função deve ter testes correspondentes
4. **Logs**: Registre eventos importantes para debug e auditoria
5. **Performance**: Otimize consultas ao banco de dados

## Fluxo de Trabalho Típico

### Criação de Conta:
1. Cliente envia dados para `/register`
2. `route.py` valida com `CreateUser` schema
3. `create_account.py` processa a criação
4. `exceptions.py` trata erros específicos
5. Retorna resposta padronizada

### Autenticação:
1. Cliente envia credenciais para `/login`
2. `utils.py` valida credenciais com `checking_account`
3. Gera tokens JWT com dados do usuário
4. Retorna resposta no formato `LoginResponse`

## Considerações de Segurança

- **Senhas**: Hash bcrypt com salt automático
- **Emails**: Hash SHA-256 para buscas no banco
- **Tokens**: JWT com algoritmo HS256 e expiração configurável
- **Sessões**: Refresh tokens para renovação segura
- **Dados Sensíveis**: Nunca retornados em respostas da API

## Extensibilidade

O módulo foi projetado para facilitar adições futuras:

1. **Novos Schemas**: Adicione em `schemas.py`
2. **Novas Exceções**: Defina em `exceptions.py`
3. **Novas Funções**: Crie em arquivos específicos ou `utils.py`
4. **Novas Rotas**: Adicione endpoints em `route.py`

Esta estrutura permite que o módulo de autenticação cresça de forma organizada enquanto mantém a separação de responsabilidades e facilita a manutenção do código.
