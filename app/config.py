from pydantic import BaseSettings


# This is to handle environment variables
# Validates that they exist and handles type conversion
# Pydantic looks for environment variables (case insensitive) and sets them
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        # set environment variables in a file and this will read them in
        env_file = ".env"


# Sets all the environment variables in variable
# Can then be accessed via ex : "settings.database_password"
settings = Settings()