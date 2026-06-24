from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    ART_INSTITUTE_API_BASE_URL: str = "https://api.artic.edu/api/v1"
    
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()


