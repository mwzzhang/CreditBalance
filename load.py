import tkinter as tk
from typing import Any, Dict, Tuple, Optional
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
    rebuy: Optional[int]


class CreditBalanceService:
    """
    Implements EDMC plugin interface based on ClickCounter example
    """

    def __init__(self) -> None:
        # data
        self.data: CreditRelatedData = CreditRelatedData(None, None)

        # display
        self.credit_text: Optional[tk.Label] = None
        self.rebuy_text: Optional[tk.Label] = None
        logger.info("CreditBalanceService instantiated")

    def on_load(self) -> str:
        """
        on_load is called by plugin_start3 below.

        It is the first point EDMC interacts with our code after loading our module.

        :return: The name of the plugin, which will be used by EDMC for logging and for the settings window
        """

        logger.info(f"{PLUGIN_NAME} loaded")
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

    def on_update(self, new_data: CreditRelatedData) -> None:
        logger.debug(f"{PLUGIN_NAME} updating internal state")
        if new_data.credit is not None:
            self.data.credit = new_data.credit
        if new_data.rebuy is not None:
            self.data.rebuy = new_data.rebuy
        
        self.setup_main_ui()
        

    def setup_main_ui(self) -> None:
        """
        Create our entry on the main EDMC UI.
        This is called by plugin_app below.
        :param parent: EDMC main window Tk
        :return: 
        """

        def credit_to_text(credit: Optional[int]) -> str:
            return "Unavailable" if credit is None else str(credit)

        credit_str = credit_to_text(self.data.credit)
        rebuy_str = credit_to_text(self.data.rebuy)

        # ngl I really don't know how tkinter works...
        if self.credit_text is not None and self.rebuy_text is not None:
            self.credit_text.after(0, self.credit_text.config, {"text": credit_str})
            self.rebuy_text.after(0, self.rebuy_text.config, {"text": rebuy_str})

cbs: CreditBalanceService

def plugin_start3(plugin_dir: str) -> str:
    """
    Handle start up of the plugin.
    See PLUGINS.md#startup
    """
    global cbs
    cbs = CreditBalanceService()
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


def plugin_app(parent: tk.Frame) -> tk.Frame:
    """
    Set up the UI of the plugin.
    See PLUGINS.md#display
    """
    # ngl I actually don't know how tkinter works D:
    # I'm sure I can factor common stuff out in the future
    frame: tk.Frame = tk.Frame(parent)
    current_row = 0

    credit_label: tk.Label = tk.Label(frame, text="Credit:")
    credit_label.grid(row=current_row, column=0, sticky=tk.W)
    cbs.credit_text = tk.Label(frame, text="unavailable")
    cbs.credit_text.grid(row=current_row, column=1, sticky=tk.W)

    current_row += 1

    rebuy_label: tk.Label = tk.Label(frame, text="Rebuy:")
    rebuy_label.grid(row=current_row, column=0, sticky=tk.W)
    cbs.rebuy_text = tk.Label(frame, text="unavailable")
    cbs.rebuy_text.grid(row=current_row, column=1, sticky=tk.W)

    cbs.setup_main_ui()
    return frame


def journal_entry(
    cmdr: str,
    is_beta: bool,
    system: str,
    station: str,
    entry: Dict[str, Any],
    state: Dict[str, Any],
) -> Optional[str]:
    """
    Updating state based on journal.
    """
    # # planning on making it lazy
    # match entry["event"]:
    #     case "LoadGame":
    #         pass
    credit: int = state["Credits"]
    rebuy: int = state["Rebuy"]

    #logger.debug(f"{PLUGIN_NAME} got journal entry, credit: {credit}, rebuy: {rebuy}")
    cbs.on_update(CreditRelatedData(credit, rebuy))
