from authlib.integrations.starlette_client import OAuth

from app.config import settings

oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.google_auth.google_client_id,
    client_secret=settings.google_auth.google_client_secret,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params={"scope": "openid email profile"},
    access_token_url="https://oauth2.googleapis.com/token",
    access_token_params=None,
    client_kwargs={"scope": "openid email profile"},
)
