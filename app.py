import tkinter as tk
from tkinter import ttk


from frames import MainFrame
from styles import style_config


# all frames in application
FRAMES = {
    'main': MainFrame
}


class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # basic configs
        self.title('Metronome')
        self.geometry('300x220')
        self.resizable(False, False)
        self.configure(background="#293846")

        # config styles using custom function
        style_config(self)

        # main container for frames
        container = ttk.Frame(self, style='Custom.TFrame')
        container.grid()

        # all frames in app
        self.frames = dict()
        for key, frame in FRAMES.items():
            self.frames[key] = frame(container, self)
            self.frames[key].grid(row=0, column=0, sticky='nsew')

        self.show_frame('main')

    def show_frame(self, key):
        """
        Switch between the frames
        :param key: key in dict
        :return:
        """
        frame = self.frames[key]
        frame.tkraise()
