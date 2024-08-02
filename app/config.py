from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    access_token_expire_minutes: int
    database_hostname: str
    database_name: str
    database_password: str
    database_port: int
    database_url: str
    database_username: str
    secret_key: str
    algorithm: str


    class Config:
        env_file = ".env"

settings = Settings()