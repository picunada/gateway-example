"""RabbitMQ module"""
import os

import aio_pika


async def get_rabbit_mq_client():
    """Init MQ Client"""
    connection = await aio_pika.connect_robust(
        host=os.getenv("RABBIT_MQ_HOST"),
        port=int(os.getenv("RABBIT_MQ_PORT")),
        login=os.getenv("RABBIT_MQ_USER"),
        password=os.getenv("RABBIT_MQ_PASSWORD"),
        virtualhost=os.getenv("RABBIT_MQ_VIRTUAL_HOST"),
    )

    return connection
