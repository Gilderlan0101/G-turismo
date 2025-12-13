from fastapi import HTTPException, status

# Erro ao tenta envia codigo de verificação para o email do usúario
ERROR_SEND_EMAIL =HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Não foi possível enviar o código de verificação. Tente novamente mais tarde.',
            )

# Erro ao tenta preenche todos os campos ou campos faltantes.
ERROR_MISSING_FIELDS = HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Preencha todos os campos.',
            )

# Erro ao tenta cadastra um email que ja existe ou ja esta verificado
EMAIL_ALREADY_EXISTS = HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Este endereço de e-mail já está cadastrado.',
            )
