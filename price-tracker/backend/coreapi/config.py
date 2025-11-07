from decouple import config

class EnvSettings:
    DB_NAME: str = config("DB_NAME", "price_tracker")
    DB_USER: str = config("DB_USER", "postgres")
    DB_PASSWORD: str = config("DB_PASSWORD", "postgres")
    DB_HOST: str = config("DB_HOST", "db")
    DB_PORT: int = config("DB_PORT", cast=int, default=5432)
    
settings = EnvSettings()