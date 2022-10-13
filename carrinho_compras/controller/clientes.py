from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from carrinho_compras.configuracoes import configuracao
from carrinho_compras.persistence.clientes import AdaptadorCliente

pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
)  # uso do bcrypt porque ele é lento

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(
    plain_password, hashed_password
):  # função que verifica o password  real com o password hasheado
    return pwd_context.verify(
        plain_password, hashed_password
    )  # dai verifica se são iguais e se for ele retorna (verificar se uma senha recebida corresponde ao hash armazenado.)


async def authenticate_user(
    adaptador: AdaptadorCliente, email: EmailStr, password: str
):  # verifica se existe no bando
    usuario = await adaptador.pega(email)
    if not usuario:
        return False
    if not verify_password(
        password, usuario["senha"]
    ):  # ver se a senha que passou é igual a senha que está no usuário
        return False
    return usuario


def create_access_token(
    data: dict, expires_delta: timedelta | None = None
):  # função que cria o token
    to_encode = (
        data.copy()
    )  # é uma copia porem se eu mudar o encode ele não muda o data
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, configuracao.secret_key, algorithm=configuracao.algorithm
    )
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    adaptador: AdaptadorCliente = Depends(),
):  # cria dependência "get_current_user" que  receberá a token como a "str" da subdependência oauth2_scheme
    credentials_exception = HTTPException(  # se tentar dar um get e não tiver autorização ele da uma exception e retorna UNAUTHORIZED
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        },  # quando der UNAUTHORIZED, http 401, retorna WWW-Authenticate
    )
    try:
        payload = jwt.decode(
            token, configuracao.secret_key, algorithms=[configuracao.algorithm]
        )
        email: str = payload.get("sub")
        if email is None:  # se não tem usuario ele da o raise de UNAUTHORIZED
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    usuario = await adaptador.pega(email)
    if usuario is None:
        raise credentials_exception
    return usuario
