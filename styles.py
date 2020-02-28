from tkinter.ttk import Style
from tkinter import font


"""
All styles for app
"""

BACKGROUND = "#293846"
LIGHT = "#eee"
PRIMARY = "#2e3f4f"


def style_config(root):
    style = Style(root)
    style.theme_use('clam')
    # TODO style all app

    # Frames
    style.configure(
        'Custom.TFrame',
        background=BACKGROUND
    )

    # bpm label
    style.configure(
        'BPM.TLabel',
        padx=10,
        pady=10,
        font=('Segoe UI', 17),
        foreground='white',
        relief='flat',
        background="#293846",
        borderwidth=5,
        bordercolor='white'
    )

    # +/- buttons
    style.configure(
        'Plus.TButton',
        borderwidth=5,
        bordercolor='white',
        background=PRIMARY,
        foregreound='white'
    )

    # combobox
    style.configure(
        'Custom.TCombobox',
        background=PRIMARY,
        troughcolor=PRIMARY
    )
