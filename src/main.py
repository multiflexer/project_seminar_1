import json

import pika

from config import config
from ml_services.model_service import get_model_service, ModelService
from ml_services.preprocessor_service import get_preprocessor_service, PreprocessorService
from ml_services.vectorizer_service import get_vectorizer_service, VectorizerService
from services.redis_service import get_redis_service, RedisService
from schemas.message import MessageIn

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=config.RABBITMQ_SRC_HOST, port=config.RABBITMQ_SRC_PORT))
channel = connection.channel()

preprocessor_service: PreprocessorService = get_preprocessor_service()
vectorizer_service: VectorizerService = get_vectorizer_service()
model_service: ModelService = get_model_service()
redis_service: RedisService = get_redis_service()


def classify_review(ch, method, properties, body):
    try:
        raw_data = json.loads(body.decode("utf-8"))
        msg = MessageIn(**raw_data)
        preprocessed_text = preprocessor_service.preprocess_text(msg.review_text)
        vectorized_text = vectorizer_service.vectorize(preprocessed_text)
        class_result = model_service.predict(vectorized_text)
        redis_service.set_review(msg.review_uuid, class_result)

    except Exception as e:
        ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
    else:
        ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue=config.RABBITMQ_SRC_QUEUE, on_message_callback=classify_review, auto_ack=False)


if __name__ == '__main__':
    try:
        channel.start_consuming()
    except Exception:
        connection.close()
        raise
