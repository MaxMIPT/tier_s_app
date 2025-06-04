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
                "level": "ERROR",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "ERROR",
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
