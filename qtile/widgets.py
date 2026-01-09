from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration
from color import colors


def separator():
    return widget.Sep(
        # foreground=colors['white'],
        foreground=colors["foreground"],
        padding=4,
        linewidth=3,
    )


def separator_sm():
    return widget.Sep(
        # foreground=colors['white'],
        foreground=colors["background"],
        padding=1,
        linewidth=1,
        size_percent=55,
    )


# widget decorations
# base_decor = {
#     "colour": colors["black"],
#     "filled": True,
#     "padding_y": 4,
#     "line_width": 0,
# }


def _left_decor(colors: str, padding_x=None, padding_y=4, round=False):
    radius = 4 if round else [4, 0, 0, 4]
    return [
        RectDecoration(
            colour=colors,
            radius=radius,
            filled=True,
            padding_x=padding_x,
            padding_y=padding_y,
        )
    ]


def _right_decor(round=False):
    radius = 4 if round else [0, 4, 4, 0]
    return [
        RectDecoration(
            # colour=colors["darkgray"],
            colour=colors["comment"],
            radius=radius,
            filled=True,
            padding_y=4,
            padding_x=0,
        )
    ]


w_battery = (
    widget.Battery(
        format="{char}",
        charge_char="󰂄",
        discharge_char="",
        full_char="󰁹",
        unknown_char="󰂃",
        empty_char="󰁺",
        show_short_text=False,
        # foreground=colors["dark"],
        foreground=colors["background"],
        fontsize=18,
        padding=8,
        decorations=_left_decor(colors["yellow"]),
    ),
    separator_sm(),
    widget.Battery(
        format="{percent:2.0%}",
        show_short_text=False,
        foreground=colors["yellow"],
        padding=8,
        decorations=_right_decor(),
    ),
    separator(),
)
