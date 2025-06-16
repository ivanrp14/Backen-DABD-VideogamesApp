from dotenv import load_dotenv
import os

# Cargar .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
ALGORITHM = os.getenv("ALGORITHM", "HS256")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL no està definida a .env")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY no està definida a .env")
