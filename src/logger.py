import logging
from logging.handlers import RotatingFileHandler
import os

from utils import get_project_root

class Logger:
    """Global logger class for the application."""
    
    _instance = None
    _logger = None
    
    def __new__(cls):
        """Singleton pattern to ensure only one logger instance."""
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance
    
    def set_log_level(self, level: str):
        """Set the logging level."""
        numeric_level = getattr(logging, level.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError(f'Invalid log level: {level}')
        self._logger.setLevel(numeric_level)
        # Update all handlers to the new level
        for handler in self._logger.handlers:
            handler.setLevel(numeric_level)

    def _initialize_logger(self):
        """Initialize the logger with file and console handlers."""
        project_root = get_project_root()
        if not project_root:
            return None

        logs_dir = os.path.join(project_root, "logs")
        
        # Create logs directory if it doesn't exist
        os.makedirs(logs_dir, exist_ok=True)
        
        # Create logger
        self._logger = logging.getLogger("crypto-agent")
        self._logger.setLevel(logging.DEBUG)
        
        # Prevent duplicate handlers if logger is already configured
        if self._logger.handlers:
            return
        
        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
            datefmt='%H:%M:%S'
        )
        
        # File handler with rotation (10MB max, keep 5 backup files)
        log_file = os.path.join(logs_dir, 'crypto-agent.log')
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)
        
        # Add handlers to logger
        self._logger.addHandler(file_handler)
        # self._logger.addHandler(console_handler)
    
    def get_logger(self):
        """Get the logger instance."""
        return self._logger
    
    def debug(self, message, *args, **kwargs):
        """Log a debug message."""
        if self._logger:
            self._logger.debug(message, *args, stacklevel=2, **kwargs)
    
    def info(self, message, *args, **kwargs):
        """Log an info message."""
        if self._logger:
            self._logger.info(message, *args, stacklevel=2, **kwargs)
    
    def warning(self, message, *args, **kwargs):
        """Log a warning message."""
        if self._logger:
            self._logger.warning(message, *args, stacklevel=2, **kwargs)
    
    def error(self, message, *args, **kwargs):
        """Log an error message."""
        if self._logger:
            self._logger.error(message, *args, stacklevel=2, **kwargs)
    
    def critical(self, message, *args, **kwargs):
        """Log a critical message."""
        if self._logger:
            self._logger.critical(message, *args, stacklevel=2, **kwargs)
    
    def exception(self, message, *args, **kwargs):
        """Log an exception with traceback."""
        if self._logger:
            self._logger.exception(message, *args, stacklevel=2, **kwargs)

# Global logger instance
logger = Logger()