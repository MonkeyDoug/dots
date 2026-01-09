import os
from libqtile import widget
from libqtile.lazy import lazy
from qtile_extras.popup.toolkit import (
    PopupRelativeLayout,
    PopupWidget,
    PopupGridLayout,
    PopupText,
    PopupImage,
)
from libqtile.log_utils import logger
from color import colors
from settings import settings
from xutils import get_icon
import os


util_popup, groups_popup = None, None


def show_groups(qtile):
    global groups_popup

    if groups_popup:
        groups_popup.kill()
        groups_popup = None
        return

    focused_index = 0
    max_windows = max([len(group.windows) for group in qtile.groups])
    counter = 1

    controls = []
    for i, group in enumerate(qtile.groups):
        if len(group.name) == 0:
            continue
        foreground_color = colors["comment"]

        if len(group.windows) > 0:
            foreground_color = colors["purple"]

        if group.screen:
            focused_index = i
            foreground_color = colors["green"]

        controls.append(
            PopupText(
                text=group.label,
                row=0,
                col=i,
                h_align="center",
                fontsize=settings["font_size"],
                foreground=foreground_color,
                mouse_callbacks={"Button1": lazy.group[group.name].toscreen()},
            )
        )
        for j, window in enumerate(group.windows):
            icon = get_icon(window.name)
            if not icon:
                controls.append(
                    PopupImage(
                        filename=os.path.join("/home", "dc", "unknown.png"),
                        row=j + 1,
                        col=i,
                        fontsize=settings["font_size"],
                    )
                )
                continue
            icon.save(
                os.path.join("/tmp", str(counter) + ".png"),
            )
            controls.append(
                PopupImage(
                    filename=os.path.join("/tmp", str(counter) + ".png"),
                    row=j + 1,
                    col=i,
                    fontsize=settings["font_size"],
                )
            )
            counter += 1

    groups_popup = PopupGridLayout(
        qtile,
        width=1000,
        height=min(128 * (max_windows + 1), 0.75 * qtile.screens[0].height),
        controls=controls,
        background=colors["background"],
        border=colors["orange"],
        border_width=2,
        close_on_click=False,
        rows=max_windows + 1,
        cols=9,
        initial_focus=focused_index,
    )
    groups_popup.show(centered=True)


def show_graphs(qtile):
    global util_popup

    if util_popup:
        util_popup.kill()
        util_popup = None
        return

    controls = [
        PopupWidget(
            widget=widget.NvidiaSensors(
                background=colors["background"], fontsize=settings["font_size"]
            ),
            width=0.075,
            height=0.9,
            pos_x=0.025,
            pos_y=0.05,
        ),
        PopupWidget(
            widget=widget.CPUGraph(
                background=colors["background"], margin_x=0, margin_y=0
            ),
            width=0.3875,
            height=0.9,
            pos_x=0.1,
            pos_y=0.05,
        ),
        PopupWidget(
            widget=widget.MemoryGraph(
                background=colors["background"], margin_x=0, margin_y=0
            ),
            width=0.3875,
            height=0.9,
            pos_x=0.5125,
            pos_y=0.05,
        ),
        PopupWidget(
            widget=widget.Battery(
                format="{char} {percent:2.0%}",
                charge_char="󱟦",
                discharge_char="󱟤",
                unknown_char="󱉝",
                low_percentage=0.2,
                low_foreground=colors["red"],
                background=colors["background"],
                fontsize=settings["font_size"],
            ),
            width=0.1,
            height=0.9,
            pos_x=0.925,
            pos_y=0.05,
        ),
    ]

    util_popup = PopupRelativeLayout(
        qtile,
        width=1000,
        height=100,
        controls=controls,
        background=colors["background"],
        border=colors["orange"],
        border_width=2,
        close_on_click=False,
    )
    util_popup.show(centered=True)
