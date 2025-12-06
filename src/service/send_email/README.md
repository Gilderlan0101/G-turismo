# Documentação do Módulo de Serviço de Email

## Visão Geral

Este módulo fornece funcionalidades completas para envio de emails e verificação de contas através de códigos de autenticação. Foi projetado seguindo princípios de separação de responsabilidades (SOLID) e oferece alta testabilidade e manutenibilidade.

## Estrutura do Módulo

### 1. Classes Principais

#### EmailConfig
Responsável pelo carregamento e validação das configurações de email a partir de variáveis de ambiente.

**Atributos:**
- `google_app_key`: Chave de aplicação do Google para envio de emails
- `company_email`: Email da empresa remetente
- `app_title`: Título da aplicação

**Métodos:**
- `_validate_config()`: Valida se todas as configurações necessárias estão presentes

#### EmailSender
Gerencia a conexão e envio de emails através de servidores SMTP.

**Configurações SMTP:**
- Gmail: `smtp.gmail.com:465`
- Outlook: `smtp.office365.com:465`

**Métodos Principais:**
- `send()`: Envia email para um destinatário
- `_send_with_server()`: Tenta envio usando um servidor específico
- `_create_message()`: Cria objeto MIMEText para envio

#### UserCodeManager
Gerencia códigos de verificação de usuários e regras de negócio relacionadas.

**Métodos Estáticos:**
- `update_verification_code()`: Atualiza código temporário do usuário
- `can_send_new_code()`: Verifica condições para envio de novo código

#### VerificationEmailService
Serviço de alto nível para orquestração do processo de envio de emails de verificação.

**Métodos:**
- `send_verification_code()`: Processo completo de envio de código
- `_generate_email_body()`: Gera conteúdo do email
- `_generate_email_subject()`: Gera assunto do email

### 2. Funções Públicas (Legacy Support)

#### send_code_email(target_email: str) -> bool
Função principal para envio de códigos de verificação. Mantida para compatibilidade.

#### verify_status_account(code_authentication: str, target_email: str) -> bool
Verifica e atualiza status da conta com código de autenticação.

#### send_email_message(receiver_email: str, subject: str, body: str) -> bool
Função genérica para envio de mensagens de email.

#### activating_the_account_with_a_code(target_account: str, code: str) -> bool
Ativa a conta do usuário após verificação do código.

## Requisitos de Configuração

### Variáveis de Ambiente Necessárias

```bash
GOOGLE_KEY_APP=          # Chave de aplicação do Google para SMTP
COMPANY_EMAIL=           # Email remetente da empresa
APP_TITLE=               # Título da aplicação para o assunto do email
```

### Dependências

- Python 3.7+
- `smtplib` (biblioteca padrão)
- `ssl` (biblioteca padrão)
- `email.mime.text` (biblioteca padrão)
- `python-dotenv`
- `fastapi` (apenas para HTTPException)
- Tortoise ORM (para modelo `User`)

## Fluxo de Uso

### 1. Envio de Código de Verificação

```python
# Método recomendado (nova implementação)
config = EmailConfig()
email_sender = EmailSender(config)
service = VerificationEmailService(email_sender, config)
await service.send_verification_code("usuario@exemplo.com")

# Método legacy (compatibilidade)
await send_code_email("usuario@exemplo.com")
```

### 2. Verificação de Código

```python
# Atualizar código no banco
await verify_status_account("1234", "usuario@exemplo.com")

# Ativar conta com código
await activating_the_account_with_a_code("usuario@exemplo.com", "1234")
```

### 3. Envio Genérico de Email

```python
send_email_message(
    receiver_email="destinatario@exemplo.com",
    subject="Assunto do Email",
    body="Corpo da mensagem"
)
```

## Regras de Negócio

### Envio de Códigos
1. Um novo código pode ser enviado se:
   - O usuário não possui código temporário, OU
   - A conta não está verificada e já existe um código

2. Após verificação bem-sucedida:
   - `verified_account` = True
   - `status` = True
   - Código temporário é limpo

### Validação de Códigos
1. Códigos devem ter no máximo 4 caracteres
2. O código fornecido pelo usuário deve corresponder exatamente ao código armazenado
3. Códigos são comparados como strings

## Tratamento de Erros

### Exceções Personalizadas
- `ValueError`: Configurações de ambiente ausentes
- `HTTPException`: Erros específicos com códigos de status HTTP apropriados

### Códigos de Status HTTP
- 401: Código inválido
- 510: Código muito longo (>4 caracteres)
- 500: Erro interno do servidor

## Logging e Debug

O módulo utiliza prints para logging básico. Para produção, recomenda-se substituir por um sistema de logging apropriado.

```python
# Exemplo de substituição para produção
import logging
logger = logging.getLogger(__name__)

# Substituir print(f"Erro: {e}") por:
logger.error(f"Erro: {e}")
```

## Considerações de Segurança

1. **Códigos temporários**: São armazenados como strings no banco de dados
2. **Comparação segura**: Uso de `str()` para garantir comparação consistente
3. **Validação de entrada**: Verificação de comprimento e tipo de dados
4. **Conexão segura**: Uso de SMTP_SSL para comunicação criptografada

## Melhorias Futuras

1. Implementar sistema de logging estruturado
2. Adicionar suporte a templates de email (HTML)
3. Implementar fila de emails para processamento assíncrono
4. Adicionar métricas e monitoramento
5. Suporte a múltiplos provedores de email

## Exemplo Completo de Uso

```python
# Configuração e uso do serviço
config = EmailConfig()
email_sender = EmailSender(config)
service = VerificationEmailService(email_sender, config)

# Enviar código de verificação
success = await service.send_verification_code("usuario@exemplo.com")

if success:
    # Verificar código do usuário
    activation = await activating_the_account_with_a_code(
        "usuario@exemplo.com",
        "1234"
    )

    if activation:
        print("Conta ativada com sucesso")
    else:
        print("Falha na ativação da conta")
```

## Notas de Migração

Para projetos existentes, as funções públicas (`send_code_email`, `verify_status_account`, `send_email_message`) mantêm compatibilidade com código legado. Para novas implementações, recomenda-se usar as classes diretamente para melhor controle e testabilidade.
