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
from pathlib import Path

from libqtile import bar, hook, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration

import colors


mod = "mod4"
browser = "firefox"
terminal = guess_terminal()
launcher = "rofi -show drun -show-icons"
windowsPane = "rofi -show window"
screenshot = "flameshot launcher"


def longNameParse(text):
    if len(text) > 28 : 
        return text[0:26] + "..."
    else:
        return text


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
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
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    Key([mod], "b", lazy.spawn(browser), desc="My Browser"),
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with multiple stack panes
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key(
        [mod],
        "t",
        lazy.window.toggle_floating(),
        desc="Toggle floating on the focused window",
    ),
    Key([],"Print", lazy.spawn(screenshot), desc="launch the screenshot"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod, "shift"], "Return", lazy.spawn(launcher), desc="Spawn launcher"),
    Key([mod, "shift"], "t", lazy.spawn(windowsPane), desc="Spawn windows"),
    Key([mod, "shift"], "g", lazy.shutdown(),desc="shutdown qtile"),
    Key([],"XF86AudioRaiseVolume",lazy.spawn("pactl -- set-sink-volume 0 +1%"), desc="volume up"),
    Key([],"XF86AudioLowerVolume",lazy.spawn("pactl -- set-sink-volume 0 -1%"), desc="volume up"),
    Key([],"XF86AudioPlay",lazy.spawn("pactl set-sink-volume toggle"), desc="mute"),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = []
group_names = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
]

# group_labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9",]
#group_labels = [
#    "DEV",
#    "WWW",
#    "SYS",
#    "DOC",
#    "VBOX",
#    "CHAT",
#    "MUS",
#    "VID",
#    "GFX",
#]
group_labels = ["", "", "", "", "", "", "", "", "",]

# group_layouts = ["monadtall", "mo", "tile", "tile", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall"]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            label=group_labels[i],
        )
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
            # mod1 + shift + letter of group = move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Move focused window to group {}".format(i.name),
            ),
        ]
    )


file_location = os.path.expanduser("~") + "/.theming/colors.json"
genColors = colors.GenerateColorScheme(file_location)


layout_theme = {
    "border_width": 2,
    "margin": 6,
    "border_focus": genColors[1],
    "border_normal": genColors[7],
}

layouts = [
    # layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Columns(**layout_theme),
    layout.Max(**layout_theme),
    layout.Spiral(**layout_theme)
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(**layout_theme),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="BlexMono Nerd Font Mono:style=Semibold Italic Italic",
    fontsize=17,
    padding=10,
)

extension_defaults = widget_defaults.copy()

forground = {"foreground": "000000"}

powerline = {"decorations": [PowerLineDecoration(path="forward_slash")]}

def widgetsList():
    topBar = [
                    widget.GroupBox(
                        fontsize=18,
                        margin_y=5,
                        margin_x=6,
                        padding_y=0,
                        padding_x=5,
                        active=genColors[0],
                        inactive=genColors[1],
                        rounded=False,
                        highlight_color=genColors[7],
                        highlight_method="line",
                        this_current_screen_border=genColors[0],
                        this_screen_border=genColors[7],
                        other_current_screen_border=genColors[0],
                        other_screen_border=genColors[1],
                        background=genColors[7],
                        **powerline,
                    ),
                    widget.Prompt(**powerline),
                    widget.WindowName(
                        center_aligned=True,
                        padding_x=10,
                        foreground=genColors[0],
                        parse_text=longNameParse,
                        **powerline,
                    ),
                    widget.Chord(
                        chords_genColors={
                            "launch": ("#ff0000", "#ffffff"),
                        },
                        name_transform=lambda name: name.upper(),
                    ),
                    widget.Clock(
                        format="󰥔  :\t%A %d-%B-%Y %H:%M",
                        **forground,
                        background=genColors[1],
                        **powerline,
                    ),
                    widget.Pomodoro(
                        **forground,
                        color_active="000000",
                        color_break="000000",
                        color_inactive="000000",
                        background=genColors[3],
                        **powerline,
                    ),
                    widget.Net(
                        format="   :\t{down:3.2f}{down_suffix:<2}↓↑{up:3.2f}{up_suffix:<2}",
                        interface="wlp5s0",
                        background=genColors[4],
                        **forground,
                        **powerline,
                        update_interval=5,
                    ),
                    widget.PulseVolume(
                        fmt="󰕾 :\t{}",
                        **forground,
                        background=genColors[5],
                        **powerline,
                    ),
                    widget.CPU(
                        format="󰻠 :\t{load_percent}%",
                        **forground,
                        background=genColors[6],
                        **powerline,
                        update_interval=5,
                    ),
                    widget.Memory(
                        format="{MemUsed:.0f}{mm}",
                        fmt="󰗚  :\t{}",
                        background=genColors[2],
                        **forground,
                        **powerline,
                        update_interval=5,
                    ),
                    widget.KeyboardLayout(
                        configured_keyboards=["latam"],
                        fmt="󰧺 :\t{}",
                        background=genColors[5],
                        **forground,
                        **powerline,
                    ),
#                    widget.Battery(
#                        charge_char=" ",
#                        discharge_char=" ",
#                        format="󰂄 {char}{percent:2.0%}",
#                        **forground,
#                        background=genColors[6],
#                        **powerline,
#                    ),
                    widget.Spacer(length=8),
                    widget.Systray(
                        background=genColors[7],
                        **powerline,
                    ),

                    widget.QuickExit(
                        **forground,
                        default_text="⏻   ",
                        countdown_format="⏻  {} ",
                        background=genColors[7]
                    ),
                ]
    return topBar

def primaryScreenBar():
    screenBar = bar.Bar(
        widgets=widgetsList(),
        size=32,
        margin=[8,8,8,8],
        background=genColors[7],
    )
    return screenBar

def secondaryScreenBar():
    secondaryWidgets = widgetsList()
    del secondaryWidgets[-2:]
    screenBar = bar.Bar(
        widgets=secondaryWidgets,
        size=32,
        margin=[8,8,8,8],
        background=genColors[7],
    )
    return screenBar


screens = [Screen(top=primaryScreenBar())]

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
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
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
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True


@hook.subscribe.startup_once
def autostart():
    home = Path("~/.config/qtile/autostart.sh").expanduser()
    subprocess.Popen([home])


# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
