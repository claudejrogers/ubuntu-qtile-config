from enum import Enum
from pathlib import Path
from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

HOME = str(Path().home())
mod = "mod4"
font = "MesloLGM Nerd Font Mono"
terminal = guess_terminal()
browser = "brave-browser"


class Colors(Enum):
    BACKGROUND = "#282c34"
    FOREGROUND = "#bbc2cf"
    BLACK = "#282c34"
    RED = "#ff6c6b"
    GREEN = "#98be65"
    YELLOW = "#ecbe7b"
    BLUE = "#51afef"
    MAGENTA = "#c678dd"
    CYAN = "#46d9ff"
    WHITE = "#bbc2cf"


class URLApp:
    def __init__(self, url):
        self.url = url
        self.command = f"{browser} --app={url}"

    def lazy_spawn(self):
        return lazy.spawn(self.command)

    def spawn_command(self):
        return qtile.spawn(self.command)


chatgtp = URLApp("https://chat.openai.com")
github = URLApp("https://github.com")
outlook = URLApp("https://outlook.office.com/mail/")
msteams = URLApp("https://teams.microsoft.com/go")

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
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "b", lazy.spawn(browser), desc="Launch browser"),
    Key([mod], "m", outlook.lazy_spawn(), desc="Launch mail"),
    Key([mod], "g", chatgtp.lazy_spawn(), desc="Launch mail"),
    Key([mod, "shift"], "g", github.lazy_spawn(), desc="Launch mail"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key(
        [mod, "shift"],
        "r",
        lazy.spawn("systemctl poweroff"),
        desc="Shutdown computer",
    ),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

groups = [Group(i) for i in "12345678"]

for group in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                group.name,
                lazy.group[group.name].toscreen(),
                desc="Switch to group {}".format(group.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                group.name,
                lazy.window.togroup(group.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(group.name),
            ),
        ]
    )

groups.append(
    Group(name="9", label="󰘐", matches=[Match(wm_class=["Code"])]),
)

keys.extend(
    [
        Key(
            [mod],
            "9",
            lazy.group["9"].toscreen(),
            desc="Switch to group {}".format("9"),
        ),
        Key(
            [mod, "shift"],
            "9",
            lazy.window.togroup("9", switch_group=True),
            desc="Switch to & move focused window to group {}".format("9"),
        ),
    ]
)

layout_theme = {
    "border_focus": Colors.BLUE.value,
    "border_normal": Colors.BACKGROUND.value,
    "border_width": 1,
    "margin": 2,
}


layouts = [
    layout.Columns(**layout_theme),
    layout.Max(**layout_theme),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
    layout.Floating(**layout_theme),
]

widget_defaults = dict(
    font=font,
    fontsize=12,
    padding=3,
    foreground=Colors.FOREGROUND.value,
)
extension_defaults = widget_defaults.copy()

bar_widgets = [
    widget.Spacer(5),
    widget.TextBox(
        "\ue73a",  # nf-dev-ubuntu
        foreground=Colors.RED.value,
        fontsize=24,
        mouse_callbacks={"Button1": lambda: qtile.spawn("rofi -show drun -l 10")},
    ),
    widget.Spacer(5),
    widget.TextBox(
        "\uebeb",  # nf-cod-extensions
        foreground=Colors.BLUE.value,
        fontsize=18,
    ),
    widget.CurrentLayout(foreground=Colors.FOREGROUND.value),
    widget.GroupBox(
        this_screen_border=Colors.BLUE.value,
        this_current_screen_border=Colors.BLUE.value,
        disable_drag=True,
    ),
    widget.TextBox(
        "",
        fontsize=18,
        mouse_callbacks={"Button1": lambda: qtile.spawn("rofi -show window")},
    ),
    widget.TextBox(
        "󰭻",
        fontsize=18,
        mouse_callbacks={"Button1": chatgtp.spawn_command},
    ),
    widget.TextBox(
        "",
        fontsize=18,
        mouse_callbacks={"Button1": github.spawn_command},
    ),
    widget.TextBox(
        "",
        fontsize=18,
        mouse_callbacks={"Button1": outlook.spawn_command},
    ),
    widget.TextBox(
        "󰊻",
        fontsize=18,
        mouse_callbacks={"Button1": msteams.spawn_command},
    ),
    widget.Spacer(5),
    widget.TextBox(
        "\uf120",  # nf-fa-terminal
        foreground=Colors.RED.value,
        fontsize=18,
        prompt=" ",
    ),
    widget.Prompt(foreground=Colors.RED.value),
    widget.Spacer(5),
    widget.WindowName(foreground=Colors.BLUE.value),
    widget.TextBox(
        "󰻠",
        foreground=Colors.BLUE.value,
        fontsize=22,
    ),
    widget.CPU(
        foreground=Colors.BLUE.value,
    ),
    widget.TextBox("|"),
    widget.TextBox(
        "󰍛",
        foreground=Colors.GREEN.value,
        fontsize=22,
    ),
    widget.Memory(
        foreground=Colors.GREEN.value,
        mouse_callbacks={"Button1": lambda: qtile.spawn(f"{terminal} -e htop")},
    ),
    widget.TextBox("|"),
    widget.Volume(
        fmt="Vol: {}",
        foreground=Colors.YELLOW.value,
    ),
    widget.TextBox("|"),
    # widget.Battery(),
    # widget.StatusNotifier(),
    # widget.Systray(),
    widget.CheckUpdates(
        distro="Ubuntu",
        display_format="󰚰 {updates}",
        no_update_string="",
        colour_have_updates=Colors.RED.value,
        colour_have_no_updates=Colors.FOREGROUND.value,
    ),
    widget.TextBox("|"),
    widget.Clock(format="%a %b %d %I:%M %p"),
    widget.TextBox("|"),
    # widget.QuickExit(
    #     default_text=" \uf011 ",  # nf-fa-power_off
    #     countdown_format="[{}]",
    #     foreground=Colors.RED.value,
    #     fontsize=16,
    # ),
    widget.TextBox(
        "\uf011",  # nf-fa-power_off
        foreground=Colors.RED.value,
        fontsize=22,
        mouse_callbacks={
            "Button1": lambda: qtile.spawn(f"sh {HOME}/.local/scripts/powermenu.sh")
        },
    ),
    widget.Spacer(5),
]

screens = [
    Screen(
        wallpaper="/usr/share/backgrounds/Mirror_by_Uday_Nakade.jpg",
        wallpaper_mode="fill",
        top=bar.Bar(
            bar_widgets,
            24,
            background=Colors.BACKGROUND.value,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]
        ),
    ),
]

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
    ],
    border_focus=Colors.BLUE.value,
    border_normal=Colors.BACKGROUND.value,
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

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
