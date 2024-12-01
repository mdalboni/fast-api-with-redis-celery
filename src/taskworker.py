import logging

from celery import Celery
from celery.signals import after_setup_logger

logger = logging.getLogger(__name__)
celery_app = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    include=["src.tasks"]
)

celery_app.conf.update(
    result_expires=3600,
)


@after_setup_logger.connect
def config_loggers(*args, **kwargs):
    formatter = logging.Formatter(
        "{'time':'%(asctime)s', 'process_name': '%(processName)s', 'process_id': '%(process)s', 'thread_name': '%(threadName)s', 'thread_id': '%(thread)s','level': '%(levelname)s', 'logger_name': '%(name)s', 'message': '%(message)s'}"
    )
    # add filehandler
    fh = logging.FileHandler('logs.log')
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)


if __name__ == "__main__":
    celery_app.start()
