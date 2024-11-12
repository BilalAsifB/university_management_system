import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = (
        f'oracle+cx_oracle://{os.getenv('ORACLE_USER')}:{os.getenv('ORACLE_PASSWORD')}@'
        f'{os.getenv('ORACLE_HOST')}:{os.getenv('ORACLE_PORT')}/{os.getenv('ORACLE_SID')}'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False