from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from authlib.integrations.starlette_client import OAuth
from models import User, Token, RefreshTokenRequest
from utils import create_access_token, create_refresh_token
from auth import authenticate_user, get_current_user_with_scope, get_current_active_user
from fake_db import fake_users_db, fake_refresh_tokens
from datetime import timedelta
from config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from jose import JWTError, jwt
from starlette.middleware.sessions import SessionMiddleware
import logging

app = FastAPI()

# Add SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

oauth = OAuth()
oauth.register(
    name="my_auth",
    client_id="my_client_id",
    client_secret="my_client_secret",
    authorize_url="https://authorization-server.com/authorize",
    access_token_url="https://authorization-server.com/token",
    redirect_uri="https://your-callback-url",
    client_kwargs={"scope": "openid profile email"},
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/authorize")
async def authorize(request: Request):
    redirect_uri = str(request.url_for("auth"))
    logger.info(f"Redirecting to {redirect_uri}")
    return await oauth.my_auth.authorize_redirect(request, redirect_uri)


@app.get("/auth")
async def auth(request: Request):
    token = await oauth.my_auth.authorize_access_token(request)
    user = await oauth.my_auth.parse_id_token(request, token)
    logger.info(f"User {user} authenticated")
    return dict(user)


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires,
    )
    refresh_token = create_refresh_token(data={"sub": user.username})
    fake_refresh_tokens[user.username] = (
        refresh_token  # Store refresh token in the separate dictionary
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@app.post("/refresh", response_model=Token)
async def refresh_access_token(refresh_token_request: RefreshTokenRequest):
    refresh_token = refresh_token_request.refresh_token
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        user = fake_users_db.get(username)

        stored_refresh_token = fake_refresh_tokens.get(username)
        if user is None or stored_refresh_token != refresh_token:
            raise credentials_exception

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user["username"], "role": user["role"]},
            expires_delta=access_token_expires,
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.post("/logout")
async def logout(current_user: User = Depends(get_current_active_user)):
    fake_refresh_tokens.pop(current_user.username, None)  # Remove refresh token
    return {"msg": "Successfully logged out"}


@app.get("/users/me", response_model=User)
async def read_users_me(
    current_user: User = Depends(get_current_user_with_scope("me")),
):
    return current_user


@app.get("/admin", response_model=User)
async def read_admin_data(
    current_user: User = Depends(get_current_user_with_scope("admin")),
):
    return {"admin_data": "This is only for admins"}
