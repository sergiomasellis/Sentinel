"""Logging configuration for Sentinel"""

import structlog
from structlog.processors import JSONRenderer, add_log_level, dict_tracebacks
from structlog.stdlib import add_logger_name


def configure_logging(debug: bool = False) -> None:
    """Configure structured logging with structlog"""
    
    processors = [
        add_log_level,
        add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]
    
    if debug:
        processors.append(structlog.dev.ConsoleRenderer())
    else:
        processors.extend([
            dict_tracebacks,
            JSONRenderer()
        ])
    
    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Get a structured logger instance"""
    return structlog.get_logger(name)