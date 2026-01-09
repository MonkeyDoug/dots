import libqtile
import libqtile.config
from libqtile.lazy import lazy
from libqtile.log_utils import logger

# For type hints
from libqtile.core.manager import Qtile
from libqtile.group import _Group
from libqtile.backend import base
from collections.abc import Callable


class MutableScratch(object):
    """For creating a mutable scratch workspace (similar to i3's scratch functionality)"""

    def __init__(self, group_name: str = ""):
        """

        Parameters
        ----------
        win_attr : str
            Attribute added to the qtile.window object to determine whether the
            window is a part of the MutableScratch system
        group_name : str
            Name of the group that holds the windows added to the scratch space
        """

        self.scratch_group_name: str = group_name

        self.win_stack: list = []  # Equivalent of focus_history
        self.showing = False

    def qtile_startup(self):
        """Initialize MutableScratch group on restarts

        Put
            hook.subscribe.startup_complete(<MutScratch>.qtile_startup)
        in your config.py to initialize the windows in the MutScratch group
        """

        qtile = libqtile.qtile
        group = qtile.groups_map[self.scratch_group_name]

        for win in group.windows:
            win.floating = True

        self.win_stack = group.windows.copy()

    def add_current_window(self) -> Callable:
        """Add current window to the MutableScratch system"""

        @lazy.function
        def _add_current_window(qtile: Qtile):
            win: base.Window = qtile.current_window
            layout: base.Layout = qtile.current_layout
            if not self.showing:
                win.hide()
            win.floating = True

            win.togroup(self.scratch_group_name)
            self.win_stack.append(win)
            layout.remove(win)
            layout.reset()

        return _add_current_window

    def remove_current_window(self) -> Callable:
        """Remove current window from MutableScratch system"""

        @lazy.function
        def _remove(qtile: Qtile):
            win = qtile.current_window

            if win in self.win_stack:
                self.win_stack.remove(win)
                qtile.current_layout.add_client(win)
                win.floating = False
                qtile.current_layout.reset()

        return _remove

    def toggle(self) -> Callable:
        """Toggle between hiding/showing MutableScratch windows

        If current window is in the MutableScratch system, hide the window. If
        it isn't, show the next window in the stack.
        """

        @lazy.function
        def _toggle(qtile: Qtile):
            if not self.showing:
                self._show(qtile)
                self.showing = True
            else:
                self._hide()
                self.showing = False

        return _toggle

    def _show(self, qtile: Qtile) -> None:
        for win in self.win_stack:
            win.togroup(qtile.current_group.name)
            win.keep_above(True)
        return

    def _hide(self) -> None:
        for win in self.win_stack:
            win.togroup(self.scratch_group_name)
            win.keep_above(False)
        return
