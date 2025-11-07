"""
Production-ready logging configuration template with per-service log files.
Supports emoji console output, structured JSON, and service-specific handlers.

Usage:
    from logging_config import setup_logging, register_service_logger
    
    # Initialize base logging
    setup_logging(env="development", log_dir="logs")
    
    # Register service-specific loggers
    register_service_logger("scraper", log_file="scraper.log", level="DEBUG")
    register_service_logger("api", log_file="api.log", level="INFO")
    
    # Use anywhere in your code
    import logging
    logger = logging.getLogger("scraper")
    logger.info("Scraping started")
    logger.success("Scraping completed!")
    
    # Control options:
    register_service_logger("scraper") # Default: logs to service file + console + app.log
    register_service_logger("api", log_file="my_api.log") # Custom log file name
    register_service_logger("noisy_service", level="WARNING") # Different log level per service
    register_service_logger("isolated", propagate=False, console_output=False) # Isolated (ONLY to service file, no app.log, no console)
    register_service_logger("standalone", propagate=False, console_output=True)  # To service file + console, but not app.log
"""

import logging
import logging.config
import logging.handlers
import os
from typing import Literal, Optional


class EmojiFormatter(logging.Formatter):
    EMOJIS = {
        'DEBUG': '🟣',
        'INFO': '🔵',
        'WARNING': '🟠',
        'ERROR': '🔴',
        'CRITICAL': '🔴🔴',
        'SUCCESS': '🟢'
    }
    
    def format(self, record):
        emoji = self.EMOJIS.get(record.levelname, '')
        record.emoji = emoji
        return super().format(record)
    
    
class JSONFormatter(logging.Formatter):
    """Structured JSON formatter for production logs"""
    
    def format(self, record):
        import json
        log_data = {
            'timestamp': self.formatTime(record, self.datefmt),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        # Add extra fields
        if hasattr(record, 'user_id'):
            log_data['user_id'] = record.user_id
        if hasattr(record, 'request_id'):
            log_data['request_id'] = record.request_id
            
        return json.dumps(log_data)


# Add custom SUCCESS level
SUCCESS_LEVEL = 25
logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")


def _success(self, message, *args, **kwargs):
    """Add logger.success() method"""
    if self.isEnabledFor(SUCCESS_LEVEL):
        self._log(SUCCESS_LEVEL, message, args, **kwargs)

logging.Logger.success = _success

# Global config store
_LOGGING_CONFIG = {
    "env": "development",
    "log_dir": "logs",
    "json_logs": False,
}

def get_config(
    env: Literal["development", "production", "testing"] = "development",
    log_dir: str = "logs",
    enable_file_logging: bool = False,
    json_logs: bool = False,
) -> dict:
    """
    Generate logging configuration based on environment.
    
    Args:
        env: Environment name (development/production/testing)
        log_dir: Directory for log files
        enable_file_logging: Whether to write logs to files
        json_logs: Use JSON formatting for file logs (recommended for production)
    
    Returns:
        Logging configuration dictionary
    """
    
    # Environment-specific defaults
    if env == "production":
        default_level = "INFO"
        console_level = "INFO"
    elif env == "testing":
        default_level = "WARNING"
        console_level = "ERROR"
    else:  # development
        default_level = "DEBUG"
        console_level = "DEBUG"

    # config
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "emoji": {
                "()": EmojiFormatter,
                "format": "%(emoji)s %(asctime)s - %(name)s - [%(levelname)s] - %(message)s",
                "datefmt": "%H:%M:%S"
            },
            "plain": {  # can be used for files
                "format": "%(asctime)s - %(name)s - [%(levelname)s] - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "json": {
                "()": JSONFormatter,
                "datefmt": "%Y-%m-%dT%H:%M:%S"
            }
        },

        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": console_level,
                "formatter": "emoji",
                "stream": "ext://sys.stdout"
            }
        },

        # Global defaults
        "root": {
            "level": default_level,
            "handlers": ["console"],
        },

        # Per-logger overrides 
        "loggers": {
            # Quiet down noisy third-party libraries
            "urllib3": {"level": "WARNING"},
            "requests": {"level": "WARNING"},
            "boto3": {"level": "WARNING"},
            "botocore": {"level": "WARNING"},
            "sqlalchemy.engine": {"level": "WARNING"},
        }
    }
    
    if enable_file_logging:
        file_formatter = "json" if json_logs else "emoji"
        
        config["handlers"].update({
            "file_all": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": file_formatter,
                "filename": os.path.join(log_dir, "app.log"),
                "maxBytes": 10_000_000,  # 10MB
                "backupCount": 5,
                "encoding": "utf8"
            },
        })
        
        config["root"]["handlers"].extend(["file_all"])
    
    return config


def setup_logging(
    env: Literal["development", "production", "testing"] = "development",
    log_dir: str = "logs",
    enable_file_logging: bool = True,
    json_logs: bool = False,
):
    """
    Configure logging for the application.
    
    Examples:
        # Development (default)
        setup_logging()
        
        # Production
        setup_logging(env="production", log_dir="/var/log/myapp")
        
        # Testing
        setup_logging(env="testing")
    """
    # Store config globally for register_service_logger
    _LOGGING_CONFIG["env"] = env
    _LOGGING_CONFIG["log_dir"] = log_dir
    _LOGGING_CONFIG["json_logs"] = json_logs
    
    # Create log directory if file logging is enabled
    if enable_file_logging:
        os.makedirs(log_dir, exist_ok=True)
    
    # Apply configuration
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
        
    config = get_config(env, log_dir, enable_file_logging, json_logs)
    logging.config.dictConfig(config)
    
    # Log initialization
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized (env={env}, log_dir={log_dir})")
    
    
def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the custom success level.
    
    Args:
        name: Usually __name__ of the calling module
    
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)

def register_service_logger(
    service_name: str,
    log_file: Optional[str] = None,
    level: str = "DEBUG",
    propagate: bool = True,
):
    """
    Register a service-specific logger with its own log file.
    
    Args:
        service_name: Name of the service (e.g., "scraper", "api", "product_grouping")
        log_file: Optional custom log file name (defaults to "{service_name}.log")
        level: Logging level for this service (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        propagate: If True, logs also go to root handlers (console + app.log)
                   If False, logs ONLY go to this service's file (isolated)
    
    Examples:
        # Basic - logs to scraper.log + console + app.log
        register_service_logger("scraper")
        
        # Custom file and level
        register_service_logger("api", log_file="api_service.log", level="INFO")
        
        # Isolated - ONLY to service file, nowhere else
        register_service_logger("noisy_service", propagate=False)
    """
    
    log_dir = _LOGGING_CONFIG["log_dir"]
    json_logs = _LOGGING_CONFIG["json_logs"]
    
    # Default log file name
    if log_file is None:
        log_file = f"{service_name}.log"
    
    # Ensure it's in the log directory
    log_path = os.path.join(log_dir, log_file)
    
    # Get or create the logger
    logger = logging.getLogger(service_name)
    
    # FIX: Check if this service logger is already registered
    # Look for a file handler pointing to our log_path
    for handler in logger.handlers:
        if isinstance(handler, logging.handlers.RotatingFileHandler):
            if os.path.abspath(handler.baseFilename) == os.path.abspath(log_path):
                init_logger = logging.getLogger(__name__)
                init_logger.warning(
                    f"Service logger '{service_name}' already registered with {log_path}. "
                    f"Skipping duplicate registration."
                )
                return
    
    # Configure logger
    logger.setLevel(level)
    logger.propagate = propagate
    
    # Create formatter
    if json_logs:
        formatter = JSONFormatter(datefmt="%Y-%m-%dT%H:%M:%S")
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - [%(levelname)s] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    
    # Add file handler
    file_handler = logging.handlers.RotatingFileHandler(
        log_path,
        maxBytes=10_000_000,
        backupCount=5,
        encoding="utf8"
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Add console handler ONLY if not propagating
    # (If propagating, console output comes from root logger)
    if not propagate:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        
        # Use emoji formatter for console
        emoji_formatter = EmojiFormatter(
            "%(emoji)s %(asctime)s - %(name)s - [%(levelname)s] - %(message)s",
            datefmt="%H:%M:%S"
        )
        console_handler.setFormatter(emoji_formatter)
        logger.addHandler(console_handler)
    
    init_logger = logging.getLogger(__name__)
    init_logger.info(
        f"Registered service logger: {service_name} -> {log_path} "
        f"(level={level}, propagate={propagate})"
    )

if __name__ == "__main__":
    # Demo usage
    print("=== Setting up logging ===")
    setup_logging(env="development", log_dir="logs")
    
    print("\n=== Registering service loggers ===")
    # Register different services
    register_service_logger("scraper", level="DEBUG")
    register_service_logger("api", log_file="api_service.log", level="INFO")
    register_service_logger("product_grouping", level="DEBUG", propagate=False)
    
    print("\n=== Testing loggers ===")
    
    # Use service loggers
    scraper_logger = logging.getLogger("scraper")
    scraper_logger.debug("Scraper debug message")
    scraper_logger.info("Scraper info message")
    scraper_logger.success("Scraper success!")
    
    api_logger = logging.getLogger("api")
    api_logger.info("API request received")
    api_logger.warning("API rate limit approaching")
    
    grouping_logger = logging.getLogger("product_grouping")
    grouping_logger.debug("Grouping products...")
    grouping_logger.success("Products grouped successfully")
    
    print("\n=== Check the logs/ directory for output files ===")