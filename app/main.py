
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from jose import jwt
from mangum import Mangum

from app.core.database import create_db_and_tables
from app.middlewares.verify_token import get_token, verify_token
from app.v1.authentication.routes import router as AuthRoutes
from app.v1.books.routes import router as BooksRoutes

app = FastAPI(
  title="TestCognito",
  description="cognito example",
  version="1.0.0",
)

@app.middleware("http")
async def validate_access_token(request: Request, call_next):
    try:
        access_token = request.headers.get("Authorization")
        await verify_token(access_token)

        token = get_token(request.headers.get("Authorization"))
        request.state.user_id = jwt.get_unverified_claims(token)["sub"]
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content=e.detail
        )
    
    response = await call_next(request)
    return response

@app.on_event("startup")
async def startup_event():
    await create_db_and_tables()

app.include_router(BooksRoutes)
app.include_router(AuthRoutes)

handler = Mangum(app)