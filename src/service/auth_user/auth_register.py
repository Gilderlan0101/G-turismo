from typing import Any, Dict

from fastapi import HTTPException, status

from src.models.user import User
from src.service.jwt.auth import get_hashed_password, verify_password
from src.utils.hashed_email import (create_email_search_hash, get_hashed_email,
                                    verify_email)


async def create_account(target) -> Dict[str, Any]:
    """create_account: Responsavel por cria cota para um usuario"""
    try:

        if not target:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Fill in all the fields.',
            )

        # --- Lógica de Segurança e Otimização de E-mail ---

        # 1. SEGURANÇA (Hash Lento):
        #    Cada conta, ao ser criada, recebe um hash lento e seguro (ex: bcrypt) no campo 'email'.
        #    O hash lento impede ataques de força bruta à senha/e-mail, mas torna a busca ineficiente.

        # 2. PROBLEMA DE PERFORMANCE:
        #    Para verificar se um e-mail já está cadastrado, não podemos buscar diretamente no banco.
        #    A verificação um a um de todos os hashes lentos (descriptografia) é demorada para grandes volumes de dados.

        # 3. SOLUÇÃO DE BUSCA RÁPIDA (Hash Determinístico):
        #    Para otimizar a busca, eu adicionei  uma coluna auxiliar no modelo ('email_search_hash').
        #    Nesta coluna, o e-mail recebe um hash rápido e determinístico (SHA-256).

        # 4. BENEFÍCIOS:
        #    * O formato SHA-256 serve como um índice de busca determinístico para os e-mails.
        #    * Conseguimos fazer uma busca instantânea e direta no banco de dados.
        #    * Isso torna o sistema muito mais rápido, sem comprometer a segurança, pois a verificação lenta
        #      de senha/e-mail continua usando o hash principal (bcrypt).
        user = await User.filter(
            email_search_hash=create_email_search_hash(target.get('email'))
        ).exists()
        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='This email address is already registered.',
            )

        # Caso esse email não esteja no banco de dados vamos cria uma conta para esse usuario
        # Ao cria a conta o usuario tem tera que ativa sua conta com o codigo que foi enviado
        # por email. Para verifica a conta acesser a rota (verified_account)
        if isinstance(target, dict):

            create = await User.create(
                username=get_hashed_email(
                    target.get('username')
                ),  # Podemos reaproveita essa função aqui
                email=get_hashed_email(target.get('email')),
                password=get_hashed_password(target.get('password')),
                status=target.get('status'),
                email_search_hash=create_email_search_hash(
                    target.get('email')
                ),
                verified_account=False,  # Atualize para True quando o usuario verifica a conta
            )

            return {
                'username': target.get('username'),
                'email': target.get('email'),
                'status': True,
            }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error  {}'.format(str(e)),
        )
