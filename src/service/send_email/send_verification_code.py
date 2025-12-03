import os
import smtplib
import ssl
from email.mime.text import MIMEText
from dotenv import load_dotenv
from src.utils.generator_code_for_email import secret_verificatio_code_for_emails
from src.models.user import User
# Carrega variáveis de ambiente
load_dotenv()

GOOGLE_APP_KEY_FOR_SENDING_EMAILS = os.getenv('GOOGLE_KEY_APP')
COMPANY_EMAIL=os.getenv('COMPANY_EMAIL')





def send_email_message(receiver_email: str, subject: str, body: str) -> bool:
    """Função para conectar ao servidor SMTP e enviar a mensagem."""

    port = 465  # Porta padrão para SSL
    context = ssl.create_default_context()

    # Cria o objeto da mensagem
    message = MIMEText(body, 'plain', 'utf-8')
    message['Subject'] = subject
    message['From'] = COMPANY_EMAIL
    message['To'] = receiver_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
            server.login(COMPANY_EMAIL, GOOGLE_APP_KEY_FOR_SENDING_EMAILS)
            server.sendmail(COMPANY_EMAIL, receiver_email, message.as_string())

            if not server:
                with smtplib.SMTP_SSL('smtp.office365.com', port, context=context) as server:
                    server.login(COMPANY_EMAIL, GOOGLE_APP_KEY_FOR_SENDING_EMAILS)
                    server.sendmail(COMPANY_EMAIL, receiver_email, message.as_string())

        return True
    except Exception as e:
        # Permite que a função chamadora capture e trate a exceção
        print(str(e))
        return False


async def send_code_email(target_email: str) -> bool:
    """Envia um código de verificação para o email do usuário."""
    if not COMPANY_EMAIL or not GOOGLE_APP_KEY_FOR_SENDING_EMAILS:
        # Lança exceção se as variáveis de ambiente não estiverem configuradas
        raise ValueError(
            'Variáveis de ambiente de email não configuradas (COMPANY_EMAIL/GOOGLE_KEY_APP).'
        )

    # Geração do código
    code_authentication = secret_verificatio_code_for_emails()
    # Salvando o codigo temporariamente no banco de dados para verifição
    # Na rota de verificação o codifgo enviado pelo usuario/cliente deve ser o mesmo
    # Salvo no banco e também o que lhe foi enviado por email
    user = await User.filter(email=target_email).first()
    if user:
        if user.temporary_code is None:
            user.temporary_code=code_authentication
            await user.save()
        return None

    subject = '[{}] Codigo de verificação.'.format(str(os.getenv('APP_TITLE')))

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
