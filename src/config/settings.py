from pathlib import Path

from pydantic import BaseSettings


class Config(BaseSettings):
    ML_BASE_DIR: str = str(Path(__file__).parent.parent)
    PATH_TO_MODEL_PICKLE: str = "objects/model.pickle"
    PATH_TO_VECTORIZER_PICKLE: str = "objects/vectorizer.pickle"

    RABBITMQ_SRC_HOST: str = "localhost"
    RABBITMQ_SRC_PORT: int = 5672
    RABBITMQ_SRC_QUEUE: str = "realtime_reviews"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
