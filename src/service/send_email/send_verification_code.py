import os
import smtplib
import ssl
from email.mime.text import MIMEText

from dotenv import load_dotenv

from confing import COMPANY_EMAIL, GOOGLE_APP_KEY_FOR_SENDING_EMAILS
from src.utils.generator_code_for_email import \
    secret_verificatio_code_for_emails

# Carrega variáveis de ambiente
load_dotenv()


def send_email_message(receiver_email: str, subject: str, body: str) -> bool:
    """Função para conectar ao servidor SMTP e enviar a mensagem."""

    port = 465  # Porta padrão para SSL
    context = ssl.create_default_context()

    # Cria o objeto da mensagem
    message = MIMEText(body, 'plain', 'utf-8')
    message['Subject'] = subject
    message['From'] = SENDER_EMAIL
    message['To'] = receiver_email

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, port, context=context) as server:
            server.login(SENDER_EMAIL, GOOGLE_APP_KEY)
            server.sendmail(SENDER_EMAIL, receiver_email, message.as_string())
        return True
    except Exception:
        # Permite que a função chamadora capture e trate a exceção
        return False


async def send_code_email(target_email: str) -> bool:
    """Envia um código de verificação para o email do usuário."""
    if not SENDER_EMAIL or not GOOGLE_APP_KEY:
        # Lança exceção se as variáveis de ambiente não estiverem configuradas
        raise ValueError(
            'Variáveis de ambiente de email não configuradas (COMPANY_EMAIL/GOOGLE_KEY_APP).'
        )

    # Geração do código
    code_authentication = secret_verificatio_code_for_emails()

    subject = '[G-turismo] Codigo de verificação.'

    # Corpo da mensagem
    mensagem = f"""
        Olá!

        Ficamos felizes em ter você conosco.

        Para garantir a segurança da sua conta, por favor, utilize o código de verificação abaixo:

        CÓDIGO DE VERIFICAÇÃO: {code_authentication}

        Este código é pessoal e intransferível. Não o compartilhe com ninguém, nem mesmo com funcionários da nossa equipe.

        Se você não solicitou este código, ignore esta mensagem.
    """

    # Chama a função de envio
    return send_email_message(target_email, subject, mensagem)
