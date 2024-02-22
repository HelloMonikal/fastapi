from passlib.context import CryptContext

pwd_contetxt = CryptContext(schemes=['bcrypt'],deprecated="auto")


def hash(password:str):
    return pwd_contetxt.hash(password)

def verify(plain_password,hashed_password):
    return pwd_contetxt.verify(plain_password,hashed_password)