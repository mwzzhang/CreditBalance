import tkinter as tk
from typing import Tuple
import logging
import os

from config import appname

plugin_name = os.path.basename(os.path.dirname(__file__))
logger = logging.getLogger(f"{appname}.{plugin_name}")


def plugin_start3(plugin_dir: str) -> str:
    logger.info("CreditBalance plugin loaded")
    return "CreditBalance"


def plugin_stop() -> None:
    pass


def plugin_app(parent: tk.Frame) -> Tuple[tk.Label, tk.Label]:
    return (tk.Label(parent, text="hello"), tk.Label(parent, text=":D"))
