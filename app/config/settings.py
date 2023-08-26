from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mongo_url: str | None = None
    rabbit_mq_host: str | None = None
    rabbit_mq_port: str | None = None
    rabbit_mq_user: str | None = None
    rabbit_mq_password: str | None = None
    rabbit_mq_virtual_host: str | None = None
    rabbit_mq_queue: str | None = None
    celery_broker_url: str | None = None
    celery_result_backend: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
print(settings.model_dump())
