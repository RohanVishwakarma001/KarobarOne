# Owner: mousamdas156@gmail.com
# ================================================================================
# Module: src/core/logging.py
# Purpose: Centralized Structured Logging (structlog)
# Last updated: 2026-07-11
# ================================================================================
"""
Centralized structured logging with structlog.

All application logs (requests, errors, DB events) are captured in a single,
consistent format:
  - Production: JSON (for log aggregation — ELK, Datadog, CloudWatch)
  - Development: Colorized console output (human-readable)

Request-scoped context (request_id, method, path) is automatically injected
into every log line via contextvars.
"""

import logging
import sys

import structlog

from app.core.config import getSettings


def setupLogging() -> None:
    """
    Configure structlog and standard library logging.

    Purpose:
        Sets up centralized structured logging (Console/JSON) and connects
        the standard library logging to the structlog pipeline.

    Parameters:
        None

    Return value:
        None
    """
    settings = getSettings()

    # Shared processors applied to all log entries
    sharedProcessors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
    ]

    if settings.debug:
        # Development: colorized, human-readable output
        renderer: structlog.types.Processor = structlog.dev.ConsoleRenderer()
    else:
        # Production: JSON for log aggregation tools
        renderer = structlog.processors.JSONRenderer()

    # Configure structlog
    structlog.configure(
        processors=[
            *sharedProcessors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Bridge structlog formatting into standard library logging
    formatter = structlog.stdlib.ProcessorFormatter(
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            renderer,
        ],
        foreign_pre_chain=sharedProcessors,
    )

    # Replace root handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    rootLogger = logging.getLogger()
    rootLogger.handlers.clear()
    rootLogger.addHandler(handler)
    rootLogger.setLevel(settings.logLevel.upper())

    # Capture uvicorn/SQLAlchemy logs through our pipeline
    for loggerName in ("uvicorn.access", "uvicorn.error", "sqlalchemy.engine"):
        libLogger = logging.getLogger(loggerName)
        libLogger.handlers.clear()
        libLogger.propagate = True


def getLogger(name: str | None = None) -> structlog.stdlib.BoundLogger:
    """
    Return a bound structlog logger.

    Purpose:
        Retrieves a namespace logger bound to context variables.

    Parameters:
        name: Name of the logger, typically __name__.

    Return value:
        A structlog bound logger instance.
    """
    return structlog.get_logger(name)