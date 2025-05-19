from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    env_name: str = "local"
    db_path: str = "vpn.db"

    wg_endpoint: str = "127.0.0.1:51820"
    host_domain: str = "vpn.local"

    stripe_key: str = ""
    stripe_price_id: str = ""
    stripe_webhook_secret: str = "whsec_59d42e73016df9504c0c4d420a519d6329e4255cf184401f15db4b89a051d5e0"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()