import logging
from logging.handlers import RotatingFileHandler

class PygameLogHandler(logging.Handler):
    def __init__(self, max_lines=3):
        super().__init__()
        self.logs = []
        self.max_lines = max_lines

    def emit(self, record):
        msg = self.format(record)
        self.logs.append(msg)
        if len(self.logs) > self.max_lines:
            self.logs.pop(0)

    def get_logs(self):
        return self.logs


# Konfiguracja loggera
def setup_logger():
    logger = logging.getLogger("game")
    logger.setLevel(logging.DEBUG)

    # Rotujący zapis do pliku
    file_handler = RotatingFileHandler("game.log", maxBytes=100000, backupCount=3)
    file_handler.setLevel(logging.DEBUG)

    # Wyświetlanie na ekranie Pygame
    pygame_handler = PygameLogHandler(max_lines=3)
    pygame_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(levelname)s: %(message)s")
    file_handler.setFormatter(formatter)
    pygame_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(pygame_handler)

    return logger, pygame_handler
