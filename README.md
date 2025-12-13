# 🌍 G-Turismo API

## 📋 Sobre o Projeto

**G-Turismo API** é uma plataforma completa de turismo desenvolvida em Python/FastAPI que conecta empresas de turismo com viajantes. A plataforma permite que empresas anunciem pacotes de viagem enquanto oferece aos usuários ferramentas para pesquisa, comparação e avaliação de serviços turísticos.

### 🎯 Objetivo Principal
Criar um ecossistema onde:
- **Empresas de turismo** possam anunciar seus pacotes profissionalmente
- **Viajantes** possam descobrir, comparar e avaliar experiências
- **Todos os usuários** tenham uma experiência transparente e confiável

---

## 🏗️ Arquitetura do Projeto

```
G_turismo_api/
├── 📁 src/                    # Código fonte principal
│   ├── 📁 auth/              # Autenticação e registro
│   ├── 📁 database/          # Configuração do banco de dados
│   ├── 📁 models/            # Modelos de dados (ORM)
│   ├── 📁 profile/           # Gerenciamento de perfil de usuário
│   ├── 📁 services_g_turismo/ # Serviços de turismo (anúncios)
│   ├── 📁 service/           # Serviços auxiliares
│   │   ├── 📁 jwt/          # JWT authentication
│   │   └── 📁 send_email/   # Sistema de email
│   ├── 📁 global_utils/      # Utilitários globais
│   ├── 📁 global_schemas/    # Schemas compartilhados
│   └── 📁 included/          # Configuração de rotas
├── 📁 logs/                  # Logs do sistema
├── main.py                  # Ponto de entrada da aplicação
├── config.py               # Configurações da aplicação
├── pyproject.toml          # Dependências (Poetry)
└── g_turismo.db           # Banco de dados SQLite
```

---

## ✨ Funcionalidades Principais

### 🔐 **Autenticação & Segurança**
- Registro de usuários (viajantes e empresas)
- Login com JWT tokens
- Refresh tokens automático
- Hash de email para privacidade
- Verificação por email

### 👤 **Gestão de Perfil**
- Perfil completo de usuário
- Foto de perfil automática (gerada)
- Status online/offline
- Histórico de buscas e favoritos

### 🏢 **Para Empresas de Turismo**
- Publicação de pacotes de viagem
- Gestão de múltiplos serviços
- Dashboard de anúncios
- Análise de performance

### 🧳 **Para Viajantes**
- Busca avançada de pacotes
- Sistema de comparação
- Avaliações e reviews
- Lista de favoritos
- Histórico de visualizações

### 📧 **Sistema de Comunicação**
- Verificação de email
- Notificações do sistema
- Códigos de confirmação
- Integração com Gmail

---

## 🚀 Tecnologias Utilizadas

### Backend
- **FastAPI** - Framework web moderno e rápido
- **Python 3.12** - Última versão estável
- **Tortoise ORM** - ORM assíncrono
- **SQLite** - Banco de dados (pode migrar para PostgreSQL)
- **JWT** - Autenticação por tokens
- **Pydantic** - Validação de dados

### Utilitários
- **Poetry** - Gerenciamento de dependências
- **Bcrypt** - Hash de senhas
- **Logging** - Sistema de logs estruturado
- **Email** - Integração com SMTP

---

## 📊 Modelo de Dados

### Usuários
- Viajantes (clientes)
- Empresas (fornecedores)
- Administradores

### Serviços de Turismo
- Pacotes de viagem
- Hospedagem
- Passeios
- Transporte
- Guias turísticos

### Interações
- Avaliações
- Favoritos
- Comparações
- Histórico

---

## 🔧 Configuração e Instalação

### Pré-requisitos
- Python 3.12+
- Poetry
- Git

### Passos para Instalação

1. **Clone o repositório**
```bash
git clone <repositorio>
cd G_turismo_api
```

2. **Instale as dependências com Poetry**
```bash
poetry install
```

3. **Ative o ambiente virtual**
```bash
poetry shell
```

4. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Edite o .env com suas configurações
```

5. **Inicialize o banco de dados**
```bash
python main.py
```

6. **Execute a aplicação**
```bash
uvicorn main:app --reload
```

---

## 🌐 Endpoints da API

### Autenticação (`/auth`)
- `POST /register` - Registro de novo usuário
- `POST /login` - Login e obtenção de tokens
- `POST /refresh` - Renovação de token
- `POST /verify-email` - Verificação de email

### Perfil (`/profile`)
- `GET /me` - Informações do usuário atual
- `PUT /update` - Atualização de perfil
- `GET /favorites` - Lista de favoritos
- `GET /history` - Histórico de atividades

### Serviços (`/service`)
- `GET /` - Lista todos os serviços
- `POST /publish` - Publica novo serviço
- `GET /{id}` - Detalhes do serviço
- `POST /{id}/review` - Adiciona avaliação
- `GET /compare` - Compara múltiplos serviços

---

## 🛡️ Segurança

- **Senhas**: Hash com bcrypt
- **Emails**: Hash SHA-256 para buscas
- **Tokens**: JWT com expiração configurável
- **CORS**: Configurado para origens específicas
- **Rate Limiting**: Proteção contra abuso
- **Logs**: Auditoria completa de ações

---

## 📈 Escalabilidade

A arquitetura foi pensada para crescer:

1. **Banco de Dados**: SQLite → PostgreSQL
2. **Cache**: Adicionar Redis
3. **Fila de Tasks**: Celery para tarefas assíncronas
4. **Microserviços**: Separação por domínio
5. **Contêinerização**: Docker/Kubernetes

---

## 🧪 Testes

```bash
# Executar testes unitários
pytest tests/

# Testes com cobertura
pytest --cov=src tests/

# Testes de integração
pytest tests/integration/
```

---

## 📝 Logs e Monitoramento

- **Arquivo de logs**: `logs/system.log`
- **Níveis**: DEBUG, INFO, WARNING, ERROR
- **Estrutura**: JSON formatado para fácil análise
- **Rotação**: Logs diários com retenção

---

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Add nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---



## 🎯 Roadmap

### Fase 1 (Atual) ✅
- [x] Autenticação básica
- [x] Perfil de usuário
- [x] Publicação de serviços
- [x] Sistema de email

### Fase 2 (Em andamento) 🚧
- [ ] Sistema de pagamentos
- [ ] Chat em tempo real
- [ ] Notificações push
- [ ] Dashboard analítico

### Fase 3 (Planejado) 📅
- [ ] Aplicativo mobile
- [ ] IA para recomendações
- [ ] Integração com redes sociais
- [ ] Sistema de cupons e promoções

---

## 🌟 Diferenciais

1. **Transparência**: Avaliações reais de viajantes
2. **Comparação**: Ferramentas para escolha informada
3. **Segurança**: Dados protegidos e privacidade
4. **Simplicidade**: Interface intuitiva para todos
5. **Performance**: API rápida e responsiva

---

**G-Turismo API** - Conectando viajantes a experiências inesquecíveis ✈️🌴
