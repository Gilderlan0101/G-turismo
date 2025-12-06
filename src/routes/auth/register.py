from fastapi import APIRouter, Depends, HTTPException, status, Body

from src.schemas.auth.schemas_login import LoginResponse
from src.schemas.auth.schemas_register import CrateUser
from src.service.auth_user.auth_register import create_account
from src.service.send_email.send_verification_code import send_code_email, activating_the_account_with_a_code
from src.service.jwt.depends import get_current_user
from src.schemas.auth.schemas_auth import SystemUser
from typing import Dict, Any

router = APIRouter(tags=['Authentication'])


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(target: CrateUser):
    """Responsavel por cadastra uma conta de um usuario"""
    print(target)
    data = {
        'username': target.username,
        'email': target.email,
        'password': target.password,
        'status': target.status,
    }
    create = await create_account(target=data)
    if create:
        return {'message': 'account created successfully'}

    else:
        return create


@router.post(
    '/send_code_for_email',
    response_model=Dict[str, str],
    status_code=status.HTTP_200_OK,
    summary="Envia código de verificação por email",
    description="""
    Envia um código de verificação para o email do usuário autenticado.

    O código será utilizado para verificar a conta do usuário.
    """
)
async def send_code_for_email(
    current_user: SystemUser = Depends(get_current_user),
) -> Dict[str, str]:
    """
    Envia código de verificação para o email do usuário.

    Args:
        current_user: Usuário autenticado obtido através do token JWT.

    Returns:
        Dict com mensagem de sucesso ou erro.

    Raises:
        HTTPException: Se ocorrer um erro durante o processo.
    """
    try:
        # Envia o código de verificação
        send_success = await send_code_email(target_email=current_user.email)

        if send_success:
            return {
                'message': 'Código de verificação enviado com sucesso. Verifique seu email.',
                'email': current_user.email  # Opcional: retornar email para confirmação
            }
        else:
            # Log do erro para debug (em produção, usar logging apropriado)
            print(f"Falha ao enviar código para {current_user.email}")

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Não foi possível enviar o código de verificação. Tente novamente mais tarde.'
            )

    except ValueError as e:
        # Erro de configuração (variáveis de ambiente)
        print(f"Erro de configuração: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Serviço de email não configurado corretamente.'
        )

    except Exception as e:
        # Erro inesperado
        print(f"Erro inesperado ao enviar código: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ocorreu um erro interno. Tente novamente mais tarde.'
        )


@router.post('/comfim_account')
async def comfim_account_with_code(
    code: str = Body(...),
    current_user: SystemUser = Depends(get_current_user),
):

    activate_account = await activating_the_account_with_a_code(
        target_account=current_user.email, code=code
    )

    if activate_account:
        return {
        "mensagem": "Conta ativada com sucesso"
        }

    else:
        return activate_account
