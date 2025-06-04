import logging


def setup_logger():
    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(levelname)s - %(name)s - %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": "INFO",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "loggers": {
            "sqlalchemy.engine": {"level": "WARNING"},
            "uvicorn": {"level": "INFO"},
            "uvicorn.error": {"level": "ERROR"},
            "uvicorn.access": {"level": "WARNING"},
            "asyncpg": {"level": "ERROR"},
            "httpx": {"level": "INFO"},
        },
    })
    sa_logger = logging.getLogger("sqlalchemy.engine")
    sa_logger.setLevel(logging.WARNING)
    sa_logger.propagate = False


logger = logging.getLogger("api")
logger.setLevel(logging.INFO)
