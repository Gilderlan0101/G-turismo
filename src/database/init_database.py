import os
from typing import Any, Dict

from dotenv import load_dotenv
from tortoise import Tortoise
from tortoise.exceptions import ConfigurationError, DBConnectionError

# Assumindo que 'src.ultils.logs' contém o LOGGER configurado
from src.utils.logs import LOGGER

load_dotenv()

# --- Configuração de Constantes (Melhor Prática) ---
# Caminho padrão para o arquivo SQLite local, se não for definido no .env
DEFAULT_SQLITE_PATH = 'local_db.sqlite'


def sqlite_config() -> Dict[str, Any]:
    """
    sqlite_config: Responsável pela configuração do banco de dados.
    Busca credenciais específicas para "production" (MySQL) ou "development" (SQLite)
    baseadas na variável ENVIRONMENT.
    """

    # Salvando o valor da variavel de ambiente.
    ENVIRONMENT = os.getenv('ENVIRONMENT')

    # Valores de credenciais (inicializados para evitar erros de escopo)
    DB_URL: str = ''
    DB_NAME: str = ''

    # ----------------------------------------------------
    # 1. Configuração para AMBIENTES
    # ----------------------------------------------------
    if ENVIRONMENT == 'PRODUCTION':
        # Mantendo a lógica original para MySQL em produção
        LOGGER.info(' [OK] Usando credenciais de **PRODUÇÃO (MySQL)**.')

        # Caso vire serviço crie a conecção mysql aqui
        # DB_USER = os.getenv('DB_USER_PROD')
        # DB_PASS = os.getenv('DB_PASSWORD_PROD')
        # DB_HOST = os.getenv('DB_HOST_PROD')
        # DB_PORT = os.getenv('DB_PORT_PROD')
        DB_NAME = os.getenv('DB_NAME_PROD')

        # Exemplo de URL de conexão para MySQL:
        # DB_URL = f"mysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

        # Como o bloco de produção original estava vazio:
        # Para que o código funcione, vamos definir DB_URL com um valor (apenas um exemplo)
        DB_URL = os.getenv('DATABASE_URL_PROD')

        DB_USER = os.getenv('DB_USER_PROD', 'root')
        DB_PASS = os.getenv('DB_PASSWORD_PROD', '')
        DB_HOST = os.getenv('DB_HOST_PROD', 'localhost')
        DB_PORT = os.getenv('DB_PORT_PROD', '3306')

        ENGINE = 'tortoise.backends.mysql'

    else:   # ENVIRONMENT == 'DEVELOPMENT'
        # ----------------------------------------------------
        # MUDANÇA PRINCIPAL: Configuração para SQLite Local
        # ----------------------------------------------------

        # O SQLite só precisa do caminho do arquivo.
        DB_NAME = os.getenv('DB_NAME_DEV_LOCAL', DEFAULT_SQLITE_PATH)

        # A URL de conexão para SQLite é: sqlite://caminho/do/arquivo
        # OBS: O Tortoise usa 'sqlite:///caminho' para path relativo e 'sqlite:////caminho' para path absoluto.
        DB_URL = f'sqlite://{DB_NAME}'

        # Não precisamos das variáveis host, port, user, pass para SQLite.
        # DB_USER =  None  apenas se estive em produção
        # DB_PASS =  None  apenas se estive em produção
        # DB_HOST = None  apenas se estive em produção
        # DB_PORT = None  apenas se estive em produção

        ENGINE = 'tortoise.backends.sqlite'

        LOGGER.info(
            f' [OK] Usando **DEVELOPMENT (SQLite)**. Arquivo: {DB_NAME}'
        )

        # ----------------------------------------------------

    # ----------------------------------------------------
    # 2. Verificação de Credenciais
    # ----------------------------------------------------
    # Para SQLite, apenas DB_NAME é crítico.

    variable_in_env = []
    # No modo DEVELOPMENT (SQLite), apenas DB_NAME é verificado
    if not DB_NAME:
        variable_in_env.append('DB_NAME')

    # Se fosse MySQL (PRODUCTION), a verificação seria mais completa:
    # if ENVIRONMENT == 'PRODUCTION':
    #     if not DB_USER: variable_in_env.append('DB_USER_PROD')
    #     if not DB_NAME: variable_in_env.append('DB_NAME_PROD')

    if variable_in_env:
        # Mensagem de erro no formato [FAIL]
        LOGGER.error(
            f'[FAIL]  Variáveis de ambiente críticas faltando: {", ".join(variable_in_env)}'
        )
        # Opcional: Levantar exceção aqui se a falta de credenciais for fatal.

    # ----------------------------------------------------
    # 3. Retorno da Configuração do Tortoise
    # ----------------------------------------------------

    # No caso do SQLite, o Tortoise prefere a chave 'db_url' no credentials ou connection
    # O Tortoise simplifica a conexão SQLite usando 'db_url' ou 'database' como o nome/caminho do arquivo.
    # Vou usar o formato `db_url` que é mais universal e limpa a configuração de credenciais desnecessárias.

    if ENGINE == 'tortoise.backends.sqlite':
        connection_credentials = {'db_url': DB_URL}
    else:   # MySQL, etc.
        connection_credentials = {
            'host': DB_HOST,
            'port': int(DB_PORT) if DB_PORT else 3306,
            'user': DB_USER,
            'password': DB_PASS,
            'database': DB_NAME,
            'charset': 'utf8mb4',
            'autocommit': True,
            'minsize': 1,
            'maxsize': 5,
            'sql_mode': 'STRICT_TRANS_TABLES',
            'connect_timeout': 30,  # Timeout de conexão
        }

    return {
        'connections': {
            'default': {
                'engine': ENGINE,  # Dinâmico: sqlite ou mysql
                'credentials': connection_credentials,
                'credentials': {'file_path': 'g_turismo.db'},
            }
        },
        'apps': {
            'models': {
                'models': [
                    'src.models.user',
                ],
                'default_connection': 'default',
            }
        },
        'use_tz': True,
        'timezone': 'America/Sao_Paulo',
    }


TORTOISE_ORM = sqlite_config()


async def init_database() -> bool:
    """Inicializa o Tortoise ORM."""

    engine_name = TORTOISE_ORM['connections']['default']['engine'].split('.')[
        -1
    ]

    # Determina o tipo de banco para logs.
    db_type = 'SQLite' if engine_name == 'sqlite' else 'MySQL'

    try:
        LOGGER.info(
            f'🔧 [OK] Configurando banco: **{db_type}** ({engine_name})'
        )
        LOGGER.info(
            f"[OK] Modelos carregados: {len(TORTOISE_ORM['apps']['models']['models'])}"
        )

        await Tortoise.init(config=TORTOISE_ORM)
        LOGGER.info('[OK] Tortoise ORM inicializado!')

        # Testa a conexão. Para SQLite, isso geralmente é implícito no init,
        # mas mantemos o padrão para consistência.
        try:
            # Selecionar 1 é uma query simples para testar a saúde da conexão.
            await Tortoise.get_connection('default').execute_query('SELECT 1')
            LOGGER.info(f'[OK] Conexão com {db_type} verificada!')
        except Exception as e:
            LOGGER.error(f'[FAIL] Falha ao testar conexão {db_type}: {e}')
            return False

        # Cria as tabelas se não existirem
        await Tortoise.generate_schemas()
        LOGGER.info('[OK] Tabelas criadas/verificadas!')

        print_database_info()
        return True

    except DBConnectionError as e:
        # Erro de conexão real (arquivo sqlite inacessível, MySQL offline/credenciais)
        LOGGER.error(
            f'[FAIL] Falha ao conectar ao banco de dados {db_type}: {e}'
        )

        # Log mais detalhado para debugging (adaptado para SQLite ou MySQL)
        creds = TORTOISE_ORM['connections']['default']['credentials']

        if db_type == 'SQLite':
            info = f'Arquivo: {creds.get("db_url", "N/A")}'
        else:
            info = f'Host: {creds.get("host")}:{creds.get("port")}, DB: {creds.get("database")}, User: {creds.get("user")}'

        LOGGER.error(f'🔍 [FAIL] Tentando conectar em: {info}')

        return False
    except ConfigurationError as e:
        LOGGER.error(f'[FAIL] Erro de configuração do Tortoise: {e}')
        return False
    except Exception as e:
        LOGGER.error(f'[FAIL] Erro inesperado ao inicializar banco: {e}')
        return False


async def close_database():
    """Fecha as conexões do banco"""
    try:
        await Tortoise.close_connections()
        LOGGER.info('[OK] Conexões do banco fechadas!')
    except Exception as e:
        # Mantém o emoji no warning, se o seu logger permitir.
        LOGGER.warning(f'[FAIL] ⚠️ Aviso ao fechar conexões: {e}')


def print_database_info():
    """Exibe informações de conexão do DB para o log."""
    conn_config = TORTOISE_ORM['connections']['default']
    creds = conn_config['credentials']
    engine_name = conn_config['engine'].split('.')[-1]
    db_type = 'SQLite' if engine_name == 'sqlite' else 'MySQL'

    LOGGER.info('-----------------------------------------')

    if db_type == 'SQLite':
        db_path = creds.get('db_url', 'N/A').replace('sqlite://', '')
        LOGGER.info(f'📦 [OK] Conectado a **{db_type}**:')
        LOGGER.info(f'   - Caminho do Arquivo: {db_path}')
    else:   # MySQL
        db_name = creds.get('database')
        db_host = creds.get('host')
        db_port = creds.get('port')
        LOGGER.info(f'📦 [OK] Conectado a **{db_type}**:')
        LOGGER.info(f'   - Banco: {db_name}')
        LOGGER.info(f'   - Host: {db_host}:{db_port}')

    LOGGER.info(f'   - Engine: {engine_name}')
    LOGGER.info(f'   - Timezone: {TORTOISE_ORM.get("timezone", "N/A")}')
    LOGGER.info('-----------------------------------------')
