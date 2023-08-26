from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mongo_url: str
    rabbit_mq_host: str
    rabbit_mq_port: str
    rabbit_mq_user: str
    rabbit_mq_password: str
    rabbit_mq_virtual_host: str
    rabbit_mq_queue: str
    celery_broker_url: str
    celery_result_backend: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
print(settings.model_dump())
