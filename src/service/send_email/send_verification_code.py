import os
import smtplib
import ssl
from email.mime.text import MIMEText
from fastapi import HTTPException, status
from typing import Optional
from dotenv import load_dotenv
from src.utils.generator_code_for_email import secret_verificatio_code_for_emails
from src.models.user import User

# Carrega variáveis de ambiente
load_dotenv()


class EmailConfig:
    """Configurações de email carregadas do ambiente."""

    def __init__(self):
        self.google_app_key = str(os.getenv('GOOGLE_KEY_APP'))
        self.company_email = str(os.getenv('COMPANY_EMAIL'))
        self.app_title = str(os.getenv('APP_TITLE'))
        self._validate_config()

    def _validate_config(self) -> None:
        """Valida se as configurações necessárias estão presentes."""
        if not self.company_email or not self.google_app_key:
            raise ValueError(
                'Variáveis de ambiente de email não configuradas. '
                'Verifique COMPANY_EMAIL e GOOGLE_KEY_APP.'
            )


class EmailSender:
    """Classe responsável pelo envio de emails."""

    SMTP_SERVERS = {
        'gmail': {
            'host': 'smtp.gmail.com',
            'port': 465
        },
        'outlook': {
            'host': 'smtp.office365.com',
            'port': 465
        }
    }

    def __init__(self, config: EmailConfig):
        self.config = config
        self.context = ssl.create_default_context()

    def _create_message(self, receiver_email: str, subject: str, body: str) -> MIMEText:
        """Cria o objeto da mensagem de email."""
        message = MIMEText(body, 'plain', 'utf-8')
        message['Subject'] = subject
        message['From'] = self.config.company_email
        message['To'] = receiver_email
        return message

    def _send_with_server(self, server_name: str, message: MIMEText,
                          receiver_email: str) -> bool:
        """Tenta enviar email usando um servidor SMTP específico."""
        server_config = self.SMTP_SERVERS[server_name]

        try:
            with smtplib.SMTP_SSL(
                server_config['host'],
                server_config['port'],
                context=self.context
            ) as server:
                server.login(self.config.company_email, self.config.google_app_key)
                server.sendmail(
                    self.config.company_email,
                    receiver_email,
                    message.as_string()
                )
            return True
        except Exception:
            return False

    def send(self, receiver_email: str, subject: str, body: str) -> bool:
        """
        Envia uma mensagem de email para o destinatário.

        Retorna True se o envio for bem-sucedido, False caso contrário.
        """
        message = self._create_message(receiver_email, subject, body)

        # Tenta primeiro com Gmail, depois com Outlook
        if self._send_with_server('gmail', message, receiver_email):
            return True

        return self._send_with_server('outlook', message, receiver_email)


class UserCodeManager:
    """Gerencia códigos de verificação de usuários."""

    @staticmethod
    async def update_verification_code(user: User, code: str) -> bool:
        """
        Atualiza o código temporário de verificação do usuário.

        Retorna True se o código foi atualizado, False caso contrário.
        """
        try:
            user.temporary_code = str(code)
            await user.save()
            return True
        except Exception as e:
            print(f"Erro ao atualizar código do usuário: {e}")
            return False

    @staticmethod
    async def can_send_new_code(user: User) -> bool:
        """
        Verifica se um novo código pode ser enviado para o usuário.

        Retorna True se:
        1. O usuário não tem código temporário, OU
        2. A conta não está verificada e há um código existente
        """
        if user.temporary_code is None:
            return True

        if not user.verified_account and user.temporary_code is not None:
            return True

        return False


class VerificationEmailService:
    """Serviço para envio de emails de verificação."""

    def __init__(self, email_sender: EmailSender, config: EmailConfig):
        self.email_sender = email_sender
        self.config = config

    def _generate_email_body(self, code: str) -> str:
        """Gera o corpo do email de verificação."""
        return f"""
Olá!

Ficamos felizes em ter você conosco.

Para garantir a segurança da sua conta, por favor, utilize o código de verificação abaixo:

CÓDIGO DE VERIFICAÇÃO: {code}

Este código é pessoal e intransferível. Não o compartilhe com ninguém, nem mesmo com funcionários da nossa equipe.

Se você não solicitou este código, ignore esta mensagem.
        """

    def _generate_email_subject(self) -> str:
        """Gera o assunto do email de verificação."""
        return f'[{self.config.app_title}] Código de verificação.'

    async def send_verification_code(self, target_email: str) -> bool:
        """
        Envia um código de verificação para o email do usuário.

        Retorna True se o email foi enviado com sucesso, False caso contrário.
        """
        try:
            # Busca usuário pelo email
            user = await User.filter(email=target_email).first()
            if not user:
                print(f"Usuário com email {target_email} não encontrado.")
                return False

            # Verifica se pode enviar novo código
            if not await UserCodeManager.can_send_new_code(user):
                print("Não é possível enviar novo código para este usuário.")
                return False

            # Gera e armazena o código
            code = secret_verificatio_code_for_emails()

            if not await UserCodeManager.update_verification_code(user, str(code)):
                print("Falha ao atualizar código do usuário.")
                return False

            # Prepara e envia o email
            subject = self._generate_email_subject()
            body = self._generate_email_body(str(code))

            return self.email_sender.send(target_email, subject, body)

        except Exception as e:
            print(f"Erro no envio de código de verificação: {e}")
            return False


# Funções de interface pública para compatibilidade com código existente
async def send_code_email(target_email: str) -> bool:
    """
    Função pública para envio de código de verificação por email.

    Mantida para compatibilidade com código existente.
    """
    try:
        config = EmailConfig()
        email_sender = EmailSender(config)
        service = VerificationEmailService(email_sender, config)

        return await service.send_verification_code(target_email)
    except ValueError as e:
        print(f"Erro de configuração: {e}")
        return False
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return False


async def verify_status_account(code_authentication: str, target_email: str) -> bool:
    """
    Função pública para verificação de status da conta.

    Mantida para compatibilidade com código existente.
    """
    try:
        user = await User.filter(email=target_email).first()
        if not user:
            return False

        return await UserCodeManager.update_verification_code(user, code_authentication)
    except Exception as e:
        print(f"Erro na verificação de status da conta: {e}")
        return False


def send_email_message(receiver_email: str, subject: str, body: str) -> bool:
    """
    Função pública para envio de mensagens de email.

    Mantida para compatibilidade com código existente.
    """
    try:
        config = EmailConfig()
        email_sender = EmailSender(config)
        return email_sender.send(receiver_email, subject, body)
    except ValueError as e:
        print(f"Erro de configuração: {e}")
        return False
    except Exception as e:
        print(f"Erro no envio de email: {e}")
        return False


async def activating_the_account_with_a_code(target_account:str, code: str) -> bool:
    """Função responsavel por ativa a conta do usuario"""


    if len(code)   > 4:
        raise HTTPException(
            status_code=status.HTTP_510_NOT_EXTENDED,
            detail="Esse valor e muito grande"
        )

    elif not isinstance(code, str):
        len_code = len(code)
        if len_code == 4:
            code = int(code)



    try:
        target = await User.filter(email=target_account).first()

        if target:
            pull_code = target.temporary_code
            # Verificar se o codigo fornecido pelo usuario e igual ao do banco
            if str(pull_code) == code:
                target.verified_account = True
                target.status = True
                await target.save()
                return True

            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Codigo invalido. Tente novamente"
            )

    except Exception as e:
        return False
