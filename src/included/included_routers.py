# included_routes.py
from src.routes.auth.login import router as login
from src.routes.auth.register import router as register


def register_all_routes(app):
    """
    Registra todos os APIRouters no aplicativo FastAPI principal.
    """

    # AUTH
    app.include_router(login, prefix='/auth')
    app.include_router(register, prefix='/auth')


__all__ = ['register_all_routes']
