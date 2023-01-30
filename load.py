import tkinter as tk
from typing import Tuple

def plugin_start3(plugin_dir: str) -> str:
    return "CreditBalance"

def plugin_stop() -> None:
    pass

def plugin_app(parent: tk.Frame) -> Tuple[tk.Label, tk.Label]:
    return (tk.Label(parent, text="hello"), tk.Label(parent, text=":D"))