import tkinter as tk
from typing import Tuple, Optional
from dataclasses import dataclass
import logging
import os

from config import appname

PLUGIN_NAME = os.path.basename(os.path.dirname(__file__))
logger = logging.getLogger(f"{appname}.{PLUGIN_NAME}")


@dataclass
class CreditRelatedData:
    """
    Dumb container for stuff I want to display

    Doing it this way because I may or may not add rebuy and/or
    Bounty/Combat Bond in the future
    """

    credit: Optional[int]


class CreditBalanceService:
    """
    Implements EDMC plugin interface based on ClickCounter example
    """

    def __init__(self) -> None:
        credit_text: str = "Not available yet :D"
        credit: Optional[int] = None

        plugin_label: Optional[tk.Label] = None
        credit_label: Optional[tk.Label] = None
        logger.info("CreditBalanceService instantiated")

    def on_load(self) -> str:
        """
        on_load is called by plugin_start3 below.

        It is the first point EDMC interacts with our code after loading our module.

        :return: The name of the plugin, which will be used by EDMC for logging and for the settings window
        """
        logger.info("{} loaded" % PLUGIN_NAME)
        return PLUGIN_NAME

    def on_unload(self) -> None:
        """
        on_unload is called by plugin_stop below.

        It is the last thing called before EDMC shuts down. Note that blocking code here will hold the shutdown process.
        """
        # self.on_preferences_closed("", False)  # Save our prefs

    # def setup_preferences(self, parent: nb.Notebook, cmdr: str, is_beta: bool) -> Optional[tk.Frame]:
    #     """
    #     setup_preferences is called by plugin_prefs below.
    #     It is where we can setup our own settings page in EDMC's settings window. Our tab is defined for us.
    #     :param parent: the tkinter parent that our returned Frame will want to inherit from
    #     :param cmdr: The current ED Commander
    #     :param is_beta: Whether or not EDMC is currently marked as in beta mode
    #     :return: The frame to add to the settings window
    #     """
    #     current_row = 0
    #     frame = nb.Frame(parent)

    #     # setup our config in a "Click Count: number"
    #     nb.Label(frame, text='Click Count').grid(row=current_row)
    #     nb.Entry(frame, textvariable=self.click_count).grid(row=current_row, column=1)
    #     current_row += 1  # Always increment our row counter, makes for far easier tkinter design.
    #     return frame

    # def on_preferences_closed(self, cmdr: str, is_beta: bool) -> None:
    #     """
    #     on_preferences_closed is called by prefs_changed below.
    #     It is called when the preferences dialog is dismissed by the user.
    #     :param cmdr: The current ED Commander
    #     :param is_beta: Whether or not EDMC is currently marked as in beta mode
    #     """
    #     # You need to cast to `int` here to store *as* an `int`, so that
    #     # `config.get_int()` will work for re-loading the value.
    #     config.set('click_counter_count', int(self.click_count.get()))  # type: ignore

    # def setup_main_ui(self, parent: tk.Frame) -> tk.Frame:
    #     """
    #     Create our entry on the main EDMC UI.
    #     This is called by plugin_app below.
    #     :param parent: EDMC main window Tk
    #     :return: Our frame
    #     """
    #     current_row = 0
    #     frame = tk.Frame(parent)
    #     button = tk.Button(
    #         frame,
    #         text="Count me",
    #         command=lambda: self.click_count.set(str(int(self.click_count.get()) + 1))  # type: ignore
    #     )
    #     button.grid(row=current_row)
    #     current_row += 1
    #     tk.Label(frame, text="Count:").grid(row=current_row, sticky=tk.W)
    #     tk.Label(frame, textvariable=self.click_count).grid(row=current_row, column=1)
    #     return frame


cbs = CreditBalanceService()


def plugin_start3(plugin_dir: str) -> str:
    """
    Handle start up of the plugin.
    See PLUGINS.md#startup
    """
    return cbs.on_load()


def plugin_stop() -> None:
    """
    Handle shutdown of the plugin.
    See PLUGINS.md#shutdown
    """
    return cbs.on_unload()


# def plugin_prefs(parent: nb.Notebook, cmdr: str, is_beta: bool) -> Optional[tk.Frame]:
#     """
#     Handle preferences tab for the plugin.
#     See PLUGINS.md#configuration
#     """
#     return cc.setup_preferences(parent, cmdr, is_beta)

# def prefs_changed(cmdr: str, is_beta: bool) -> None:
#     """
#     Handle any changed preferences for the plugin.
#     See PLUGINS.md#configuration
#     """
#     return cc.on_preferences_closed(cmdr, is_beta)


# def plugin_app(parent: tk.Frame) -> Optional[tk.Frame]:
#     """
#     Set up the UI of the plugin.
#     See PLUGINS.md#display
#     """
#     return cc.setup_main_ui(parent)
# def plugin_app(parent: tk.Frame) -> Tuple[tk.Label, tk.Label]:
#     global plugin_label, credit_label, credit_text
#     plugin_label = tk.Label(parent, text="Credit:")
#     credit_label = tk.Label(parent, text=credit_text)
#     return (plugin_label, credit_label)


# def journal_
