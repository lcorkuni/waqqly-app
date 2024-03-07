#!/usr/bin/env python3

from fastapi import Request, FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from http import HTTPStatus
import uvicorn

app = FastAPI(title="AAA", description="aaaaaa", version="1.0")
templates = Jinja2Templates(directory="templates")


@app.get("", include_in_schema=False, status_code=HTTPStatus.TEMPORARY_REDIRECT)
@app.get("/", include_in_schema=False, status_code=HTTPStatus.TEMPORARY_REDIRECT)
async def redirect_login():
    return RedirectResponse("/login")


@app.get("/login", response_class=HTMLResponse,
         status_code=HTTPStatus.OK,
         summary="Login Page")
async def login(request: Request):
    return templates.TemplateResponse(name="login.html", context={"request": request, "message": "Hello from FastAPI with Jinja2"})

# Start the application
uvicorn.run(app, host="0.0.0.0", port=8888)
