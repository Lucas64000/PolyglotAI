
from datetime import datetime
from pathlib import Path


class SimpleLogger:
    """Logger simple qui écrit dans des fichiers"""

    def __init__(self, name: str, log_to_console: bool = False):
        self.name = name
        self.log_to_console = log_to_console
        self._ensure_log_directory()
        self.log_file = self._get_log_file_path()

    def _ensure_log_directory(self):
        """Crée le dossier logs s'il n'existe pas"""
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)

    def _get_log_file_path(self) -> Path:
        """Retourne le chemin du fichier de log pour aujourd'hui"""
        today = datetime.now().strftime("%Y-%m-%d")
        return self.log_dir / f"{today}.log"

    def _log(self, level: str, message: str, **kwargs: str):
        """Log dans un fichier"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        extras = " ".join([f"{k}={v}" for k, v in kwargs.items()]) if kwargs else ""
        log_line = f"[{timestamp}] {level} | {self.name} | {message} {extras}\n"

        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_line)
        except Exception as e:
            # Fallback vers print si l'écriture échoue
            print(f"Erreur écriture log: {e}")
            print(log_line.strip())

        # Afficher en console uniquement si demandé
        if self.log_to_console:
            print(log_line.strip())

    def debug(self, message: str, **kwargs: str):
        self._log("DEBUG", message, **kwargs)

    def info(self, message: str, **kwargs: str):
        self._log("INFO", message, **kwargs)

    def warning(self, message: str, **kwargs: str):
        self._log("WARNING", message, **kwargs)

    def error(self, message: str, **kwargs: str):
        self._log("ERROR", message, **kwargs)


def get_logger(name: str, log_to_console: bool = False) -> SimpleLogger:
    """Récupère un logger

    Args:
        name: Nom du logger 
        log_to_console: Si True, affiche aussi en console
    """
    return SimpleLogger(name, log_to_console)
