"""
Logger Simple pour POC
Juste print(), pas de structlog
"""

from datetime import datetime


class SimpleLogger:
    """Logger simple pour POC"""
    
    def __init__(self, name: str):
        self.name = name
    
    def _log(self, level: str, message: str, **kwargs: str):
        """Log basique"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        extras = " ".join([f"{k}={v}" for k, v in kwargs.items()])
        print(f"[{timestamp}] {level} | {self.name} | {message} {extras}")
    
    def debug(self, message: str, **kwargs: str):
        self._log("DEBUG", message, **kwargs)
    
    def info(self, message: str, **kwargs: str):
        self._log("INFO", message, **kwargs)
    
    def warning(self, message: str, **kwargs: str):
        self._log("WARNING", message, **kwargs)
    
    def error(self, message: str, **kwargs: str):
        self._log("ERROR", message, **kwargs)


def get_logger(name: str) -> SimpleLogger:
    """Récupère un logger"""
    return SimpleLogger(name)
