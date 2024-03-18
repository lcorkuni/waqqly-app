#!/usr/bin/env python3
from typing import Optional

import uvicorn
from fastapi import FastAPI, Request, Response, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pathlib import Path

from starlette.datastructures import MutableHeaders

from app_utils import *

app = FastAPI(title="Wagg.ly", description="A dog walkers app", version="1.0")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory=Path(__file__).parent.absolute() / "static"), name="static")


@app.middleware("http")
async def add_auth_header_from_cookie(request: Request, call_next):
    access_token = request.cookies.get("access_token")

    if access_token and "Authorization" not in request.headers.keys():
        new_header = MutableHeaders(request._headers)
        new_header["Authorization"] = f"Bearer {access_token}"
        request._headers = new_header
        request.scope.update(headers=request.headers.raw)

    response = await call_next(request)
    return response


@app.middleware("http")
async def authenticate_docs_access(request: Request, call_next):
    invalid_creds_response = JSONResponse(content={"details": "UNAUTHORIZED: Could not validate credentials"}, status_code=HTTPStatus.UNAUTHORIZED)
    try:
        if "/docs" in request.url.path:
            token = request.cookies.get("access_token")
            if token is None:
                return invalid_creds_response
            current_user = await get_current_user(token)
            if current_user.type != UserType.admin:
                raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="User is not admin")
    except HTTPException:
        return invalid_creds_response

    response = await call_next(request)
    return response


@app.get("", include_in_schema=False, status_code=HTTPStatus.TEMPORARY_REDIRECT)
@app.get("/", include_in_schema=False, status_code=HTTPStatus.TEMPORARY_REDIRECT)
async def redirect_homepage():
    return RedirectResponse("/login")


@app.get("/login", response_class=HTMLResponse,
         status_code=HTTPStatus.OK,
         summary="Returns the Login Page HTML", tags=["Frontend"])
async def login(request: Request):
    return templates.TemplateResponse(name="login.html", context={"request": request})


@app.get("/register", response_class=HTMLResponse,
         status_code=HTTPStatus.OK,
         summary="Returns the Register Page HTML", tags=["Frontend"])
async def register(request: Request):
    return templates.TemplateResponse(name="register.html", context={"request": request})


@app.get("/home", response_class=HTMLResponse,
         status_code=HTTPStatus.OK,
         summary="Returns the Homepage Page HTML", tags=["Frontend"])
async def homepage(request: Request, current_user: Annotated[User, Depends(get_current_user)]):
    return templates.TemplateResponse(name="homepage.html", context={"request": request})


@app.post("/token", tags=["Backend"], response_class=JSONResponse)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> JSONResponse:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    # Create a cookie for the token
    response = JSONResponse(content=access_token)
    response.set_cookie(key="access_token", value=access_token)
    response.set_cookie(key="username", value=user.username)
    return response


@app.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="username")
    return {"message": "Cookies cleared, successfully logged out."}


@app.get("/get_cookies", response_class=JSONResponse)
async def get_cookies(access_token: Optional[str] = Cookie(None), username: Optional[str] = Cookie(None)):
    try:
        cookies = {"access_token": access_token, "username": username}
    except Exception:
        cookies = "No cookies found"
    return cookies


@app.get("/users/me/", response_model=User, tags=["Backend"])
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user


@app.get("/users/me/items/", tags=["Backend"])
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]


@app.get("/password-hash", tags=["Debug"])
async def password_hash(password: str):
    return get_password_hash(password)


@app.get("/user-sign-up",
         status_code=HTTPStatus.OK,
         summary="Register Page")
async def user_sign_up():
    return HTTPStatus.OK


@app.get("/sign-out",
         status_code=HTTPStatus.OK,
         summary="Register Page")
async def sign_out():
    return HTTPStatus.OK


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    uvicorn.run("app:app", port=8000, log_level="info", reload=True)
