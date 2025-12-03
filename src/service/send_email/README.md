Documentação do Script de Envio de Código de Verificação por E-mail

Este script Python implementa a lógica necessária para gerar um código de autenticação de 4 dígitos e enviá-lo para um endereço de e-mail especificado, utilizando o servidor SMTP do Gmail com autenticação de chave de aplicativo (App Key).

📄 Funcionalidades Principais

Geração de Código: Gera um código de verificação numérico aleatório de quatro dígitos (1000 a 9999).

Configuração de Ambiente: Carrega credenciais de e-mail e chaves de aplicativo de um arquivo de variáveis de ambiente (.env).

Envio Seguro de E-mail: Conecta-se ao servidor SMTP do Gmail via SSL/TLS (porta 465) para garantir uma comunicação segura.

🛠️ Dependências

O script utiliza as seguintes bibliotecas:

Biblioteca

Propósito

os

Interação com o sistema operacional para carregar variáveis de ambiente.

smtplib

Implementação do protocolo cliente SMTP (Simple Mail Transfer Protocol).

ssl

Fornece wrappers de socket com criptografia de camada de transporte (TLS/SSL).

email.mime.text

Criação do objeto da mensagem de e-mail com corpo de texto.

dotenv

Carregamento de variáveis de ambiente do arquivo .env.

random

Geração de números aleatórios para o código de verificação.

asyncio

(Apenas no bloco de teste) Execução de funções assíncronas.

Você pode instalá-las (exceto as que são nativas do Python) usando pip:

pip install python-dotenv


⚙️ Configuração (Arquivo .env)

Para que o script funcione, você deve criar um arquivo chamado .env no mesmo diretório do script, contendo suas credenciais.

IMPORTANTE: Você deve usar uma Chave de Aplicativo (App Key) do Google e NÃO a senha da sua conta para autenticação, devido às políticas de segurança do Google.

# Exemplo de conteúdo do arquivo .env
COMPANY_EMAIL="seu-email-aqui@gmail.com"
GOOGLE_KEY_APP="sua-chave-de-app-aqui"


O script carregará estas variáveis usando load_dotenv().

🧠 Funções

1. secret_verificatio_code_for_emails() -> str

Gera um código de verificação aleatório.

Retorno

Tipo

Descrição

code

str

Um código numérico de 4 dígitos (ex: "4582").

2. send_email_message(receiver_email: str, subject: str, body: str) -> bool

Estabelece a conexão com o servidor SMTP e envia a mensagem.

Parâmetro

Tipo

Descrição

receiver_email

str

O endereço de e-mail do destinatário.

subject

str

O assunto do e-mail.

body

str

O corpo da mensagem (texto puro).

Lógica de Conexão:

Define a porta 465 (padrão para SSL) e cria um contexto SSL.

Cria o objeto MIMEText (estrutura do e-mail).

Utiliza smtplib.SMTP_SSL para iniciar a conexão segura.

Realiza o server.login() usando SENDER_EMAIL e GOOGLE_APP_KEY.

Envia o e-mail usando server.sendmail().

Retorna True em caso de sucesso ou False em caso de erro.

3. async def send_code_email(target_email: str) -> bool

Orquestra a geração do código e o envio do e-mail formatado.

Parâmetro

Tipo

Descrição

target_email

str

O endereço de e-mail para onde o código será enviado.

Processo:

Verifica se as variáveis de ambiente necessárias estão presentes, levantando um ValueError se não estiverem.

Chama secret_verificatio_code_for_emails() para obter o código.

Monta o subject e a mensagem (corpo do e-mail) com o código de verificação inserido.

Chama send_email_message() para enviar.

🚀 Uso e Teste

O bloco if __name__ == '__main__': demonstra como testar a funcionalidade de envio, executando a função assíncrona send_code_email com um e-mail de teste.

if __name__ == '__main__':
    # ... import asyncio ...
    try:
        test_email = "contatodevorbit@gmail.com" # Substitua pelo seu email de teste
        test_result = asyncio.run(send_code_email(test_email))

        # ... (lógica de impressão do resultado)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")


Para usá-lo em uma aplicação real (ex: um backend web), você importaria e chamaria a função send_code_email(target_email) em seu fluxo de autenticação.