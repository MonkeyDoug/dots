# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess
from libqtile import bar, layout, extension, hook
from qtile_extras import widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen, KeyChord
from libqtile.lazy import lazy
from color import colors
from popup import show_graphs, show_groups

monitor_file = "/tmp/multi_head"
monitors = 1
if os.path.exists(monitor_file):
    with open(monitor_file, "r") as f:
        monitors = int(f.read().strip())

mod = "mod4"
terminal = "kitty"

keys = [
    Key([mod], "k", lazy.layout.previous(), desc="Move focus to previous window"),
    Key([mod], "j", lazy.layout.next(), desc="Move focus to next window"),
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.reset(), desc="Reset all window sizes"),
    Key([mod], "g", lazy.layout.grow(), desc="Shrink"),
    Key([mod], "s", lazy.layout.shrink(), desc="Grow"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "space", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "c", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key(
        [mod, "shift"],
        "b",
        lazy.spawn("zen-browser --new-window bitwarden.com"),
        desc="Open bitwarden in browser",
    ),
    Key(
        [mod],
        "p",
        lazy.spawn(os.path.expanduser("~/.config/rofi/scripts/launcher_t6")),
        desc="Launches rofi",
    ),
    Key([mod], "z", lazy.screen.toggle_group(), desc="Move to last group"),
    Key([mod, "shift"], "e", lazy.spawn("kitty nvim"), desc="Launch neovim"),
    Key(
        [],
        "XF86MonBrightnessUp",
        lazy.spawn("brightnessctl set 10%+"),
        desc="Increase brightness by 10%",
    ),
    Key(
        [],
        "XF86MonBrightnessDown",
        lazy.spawn("brightnessctl set 10%-"),
        desc="Decrease brightness by 10%",
    ),
    Key([], "F7", lazy.spawn("playerctl previous"), desc="Previous media"),
    Key([], "F8", lazy.spawn("playerctl next"), desc="Next media"),
    Key([], "F9", lazy.spawn("playerctl play-pause"), desc="Pause media"),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="Previous media"),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="Next media"),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play"), desc="Pause media"),
    Key([], "Pause", lazy.spawn("playerctl pause"), desc="Pause media"),
    Key(
        ["mod1"],
        "F7",
        lazy.spawn("pamixer -d 1 --allow-boost"),
        desc="Decrease volume by 10%",
    ),
    Key(
        ["mod1"],
        "F8",
        lazy.spawn("pamixer -i 1 --allow-boost"),
        desc="Increase volume by 10%",
    ),
    Key(
        ["mod1"],
        "F9",
        # lazy.spawn("flameshot gui"),
        lazy.spawn("spectacle"),
    ),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn("pamixer -d 1 --allow-boost"),
        desc="Decrease volume by 10%",
    ),
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("pamixer -i 1 --allow-boost"),
        desc="Increase volume by 10%",
    ),
    Key([mod], "w", lazy.to_screen(1), desc="Switch to first screen"),
    Key([mod], "e", lazy.to_screen(0), desc="Switch to second screen"),
    Key([mod], "r", lazy.to_screen(2), desc="Switch to third screen"),
    Key(
        [mod, "mod1"],
        "l",
        lazy.spawn('i3lock-fancy-dualmonitor "" ""'),
        desc="Lock screen",
    ),
    Key(
        [mod],
        "f",
        lazy.window.toggle_floating(),
        desc="Toggle floating",
    ),
    Key([mod], "b", lazy.function(show_graphs)),
    Key([mod], "l", lazy.function(show_groups)),
    Key([], "Print", lazy.spawn("spectacle")),
]

groups = [Group(i, label="󰔷 ") for i in "123456789"]
groups[4] = Group(
    "5",
    label="󰔷 ",
    layout="max",
    matches=[
        Match(
            wm_class=[
                "spotify",
                "discord",
                "clickup",
                "Spotify",
                "easyeffects",
                "slack",
                "Slack",
            ]
        )
    ],
)

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )

layout_settings = {
    "border_focus": colors["green"],
    "border_normal": colors["purple"],
    "border_width": 2,
    "margin": 12,
}

floating_layout = layout.Floating(
    **layout_settings,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)

layouts = [
    layout.Max(
        border_width=0,
        border_focus=colors["green"],
        border_normal=colors["purple"],
        margin=0,
    ),
    layout.MonadTall(**layout_settings, single_margin=0),
    layout.MonadWide(**layout_settings, single_margin=0),
    layout.MonadThreeCol(**layout_settings, single_margin=0),
    floating_layout,
]

screen1 = Screen(
    wallpaper=os.path.expanduser(
        "~/images/wallpapers/wallhaven-xld8rd.jpg",
    ),
    wallpaper_mode="fill",
)

screen3 = Screen(
    wallpaper=os.path.expanduser(
        "~/images/wallpapers/wallhaven-xld8rd.jpg",
    ),
    wallpaper_mode="fill",
)

screen4 = Screen(
    wallpaper=os.path.expanduser(
        "~/images/wallpapers/wallhaven-xld8rd.jpg",
    ),
    wallpaper_mode="fill",
)

screen5 = Screen(
    wallpaper=os.path.expanduser("~/images/wallpapers/wallhaven-xld8rd.jpg"),
    wallpaper_mode="fill",
)

screen6 = Screen(
    wallpaper=os.path.expanduser("~/images/wallpapers/wallhaven-xld8rd.jpg"),
    wallpaper_mode="fill",
)

screen7 = Screen(
    wallpaper=os.path.expanduser("~/images/wallpapers/wallhaven-xld8rd.jpg"),
    wallpaper_mode="fill",
)


if monitors == 1:
    screens = [screen5]
elif monitors == 2:
    screens = [screen5, screen6]
# elif monitors == 3:
#     screens = [screen6, screen7]
else:
    screens = [screen2, screen3, screen4]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = True

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

wmname = "qtile"


@hook.subscribe.startup_once
def start_once():
    script = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.call(script)
