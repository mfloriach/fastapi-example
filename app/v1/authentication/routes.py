import base64
import hashlib
import hmac

import boto3
from fastapi import APIRouter, HTTPException

from app.core.config import env_vars

from .validator import SignUp

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"]
)

cognito_client = boto3.client('cognito-idp', region_name = env_vars.AWS_REGION)

@router.post("/signin")
async def signin(data: SignUp):
	try:
		res = cognito_client.initiate_auth(
			ClientId=env_vars.AWS_COGNITO_APP_CLIENT_ID,
			AuthFlow="USER_PASSWORD_AUTH",
			AuthParameters={
				"USERNAME": data.email,
				"PASSWORD": data.password,
				'SECRET_HASH': _get_secret_hash(data.email)
			}
		)

		return {"token": res["AuthenticationResult"]["AccessToken"]}
	except cognito_client.exceptions.UserNotFoundException:
		raise HTTPException(status_code=400, detail='user not found')
	except cognito_client.exceptions.NotAuthorizedException:
		raise HTTPException(status_code=400, detail='password incorrect')
	except cognito_client.exceptions.TooManyRequestsException:
		raise HTTPException(status_code=429, detail='too many intends wait a little bit')
    

@router.post("/signup", status_code=201)
async def signup(data: SignUp):
	try:
		cognito_client.sign_up(
			ClientId=env_vars.AWS_COGNITO_APP_CLIENT_ID,
			SecretHash=_get_secret_hash(data.email),
			Username=data.email,
			Password=data.password
		)
	except cognito_client.exceptions.UsernameExistsException:
		raise HTTPException(status_code=400, detail='email already exist')
	except cognito_client.exceptions.InvalidPasswordException:
		raise HTTPException(status_code=400, detail='password does not fit the requeriments')
	except cognito_client.exceptions.TooManyRequestsException:
		raise HTTPException(status_code=429, detail='too many intends wait a little bit')
    

def _get_secret_hash(username):
	key = bytes(env_vars.AWS_COGNITO_APP_CLIENT_SECRET, 'utf-8')
	message = bytes(f'{username}{env_vars.AWS_COGNITO_APP_CLIENT_ID}', 'utf-8')

	return base64.b64encode(hmac.new(key, message, digestmod=hashlib.sha256).digest()).decode()