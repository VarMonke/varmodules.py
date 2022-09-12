from typing import Optional, Literal, Dict, Union
import os
import datetime


class Logger:
    def __init__(self, name: str, console: Optional[bool] = False):
        self.name: str = name
        self.console: bool = console
        os.makedirs("logs", exist_ok=True)

    LEVEL_COLORS: Dict[str, str] = {
        "debug": "\x1b[0;1;34m{}\x1b[0m",
        "info": "\x1b[0;1;32m{}\x1b[0m",
        "warning": "\x1b[0;1;33m{}\x1b[0m",
        "error": "\x1b[0;1;31m{}\x1b[0m",
        "critical": "\x1b[0;1;31;47m{}\x1b[0m",
    }

    def to_file(self, fmt: str) -> None:
        with open(f"logs/{self.name.lower()}.log", "a") as f:
            f.write(fmt)

    def format(
        self,
        message: str,
        *,
        level: Optional[
            Literal["debug", "info", "warning", "error", "critical"]
        ] = "debug",
    ) -> None:
        fmt: str = f"{datetime.datetime.now().strftime('%d/%m %H:%M:%S')}[{self.name.upper()}] {level.upper()}: {message}\n"
        self.to_file(fmt)
        if self.console:
            thing = self.name
            type = self.LEVEL_COLORS.get(level, "[0;1;35m{}[0m").format(level.upper())
            time = datetime.datetime.utcnow().strftime("%d/%m %H:%M:%S")
            print(f"{thing} | {type} {time} {message}")

    def info(
        self,
        message: str,
    ) -> None:
        self.format(message, level="info")

    def warn(
        self,
        message: str,
    ) -> None:
        self.format(message, level="warning")

    def debug(self, message: str) -> None:
        self.format(message, level="debug")

    def error(
        self,
        message: Union[str, Exception],
    ) -> None:
        if isinstance(message, Exception):
            self.format(
                str(message) + message.__traceback__ if message.__traceback__ else "",
                level="error",
            )
            return
        self.format(message, level="error")

    def critical(
        self,
        message: str,
    ) -> None:
        self.format(message, level="critical")