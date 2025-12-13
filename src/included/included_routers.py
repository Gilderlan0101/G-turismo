# included_routes.py
from src.auth.route import router as auth_or_register
from src.profile.user_profile import router as user_profile
from src.services_g_turismo.published_services import router as publish_a_service

def register_all_routes(app):
    """
    Registra todos os APIRouters no aplicativo FastAPI principal.
    """

    # AUTH
    app.include_router(auth_or_register, prefix='/auth')
    # PROFILE
    app.include_router(user_profile, prefix='/profile')
    # PUBLICATION OF SERVICES
    app.include_router(publish_a_service, prefix='/service')


__all__ = ['register_all_routes']
