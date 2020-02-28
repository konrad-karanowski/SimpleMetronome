import tkinter as tk
from tkinter import ttk
import winsound


class MainFrame(ttk.Frame):

    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs, style='Custom.TFrame')
        self.grid_rowconfigure(0, minsize=100)
        self.grid_columnconfigure(0, minsize=270)

        # variables

        # beats per minute
        self.bpm = tk.IntVar(value=80)
        # counts (num of notes in one beat)
        self.counts = tk.IntVar(value=4)
        # is metronome running
        self.is_running = tk.BooleanVar(value=False)

        # list of ticks
        self.ticks = list()

        # containers

        # container for counts
        self.count_container = ttk.Frame(self, style='Custom.TFrame')
        self.count_container.grid(row=0, column=0, sticky='')
        self.create_ticks(event=None)

        # container for bpm settings
        self.bpm_container = ttk.Frame(self, style='Custom.TFrame')
        self.bpm_container.grid(row=1, column=0, sticky='')
        self.bpm_container.grid_columnconfigure(1, minsize=100)
        self.create_bpm_settings()

        # container for addition tools and buttons
        self.tools_container = ttk.Frame(self)
        self.tools_container.grid(row=2, column=0, sticky='')
        self.create_tools()

    def create_ticks(self, event):
        """
        Create all ticks in app
        :return:
        """
        # removing all previous ticks
        for tick in self.count_container.grid_slaves():
            tick.destroy()

        # creating new list of ticks
        self.ticks = list()

        ticks_left = self.counts.get()
        total = 0
        rows = 1 if ticks_left <= 8 else 2
        for i in range(rows):
            for j in range(8):
                if total != ticks_left:
                    new_tick = tk.Canvas(
                        self.count_container,
                        width=32,
                        height=32,
                        bg="#293846",
                        bd=0,
                        highlightthickness=0,
                        relief='ridge'
                    )
                    new_tick.create_oval(1, 1, 31, 31, outline='', fill='yellow')
                    new_tick.grid(row=i, column=j, sticky='nsew', padx=0, pady=0)
                    self.ticks.append(new_tick)
                    total += 1
                else:
                    break

        # change first tick to orange (accent on first note)
        self.ticks[0].itemconfig(1, fill='orange')

    def create_bpm_settings(self):
        """
        Create all widgets in bpm setting container
        :return:
        """
        separator = ttk.Separator(
            self.bpm_container,
            orient='horizontal'
        )
        separator.grid(row=0, column=0, columnspan=3, sticky='ew', pady=5)

        self.bpm_label = ttk.Label(
            self.bpm_container,
            textvariable=self.bpm,
            anchor='center',
            style='BPM.TLabel'
        )
        self.bpm_label.grid(row=1, column=1, sticky='ew')

        # 11
        self.plus = ttk.Button(
            self.bpm_container,
            command=lambda: self.update_bpm(1),
            text='+1',
            style='Plus.TButton'
        )
        self.plus.grid(row=1, column=2, sticky='e')

        self.minus = ttk.Button(
            self.bpm_container,
            command=lambda: self.update_bpm(-1),
            text='-1',
            style='Plus.TButton'
        )
        self.minus.grid(row=1, column=0, sticky='w')

        self.slider = tk.Scale(
            self.bpm_container,
            from_=1,
            to=300,
            orient='horizontal',
            showvalue=False,
            variable=self.bpm,
            background="#293846"
        )
        self.slider.grid(row=2, column=0, columnspan=3, sticky='ew')

    def create_tools(self):
        """
        Create all other tools for metronome
        :return:
        """
        self.start_button = ttk.Button(
            self.tools_container,
            text='Start',
            command=self.start,
            style='Plus.TButton'
        )
        self.start_button.grid(row=0, column=1, sticky='ew')

        self.stop_button = ttk.Button(
            self.tools_container,
            text='Stop',
            command=self.stop,
            style='Plus.TButton'
        )
        self.stop_button.grid(row=0, column=2, sticky='ew')

        self.counts_combobox = ttk.Combobox(
            self.tools_container,
            values=[i + 1 for i in range(16)],
            textvariable=self.counts,
            state='readonly',
            width=8,
            style='Custom.TCombobox'
        )
        self.counts_combobox.grid(row=0, column=0, sticky='w')
        self.counts_combobox.bind('<<ComboboxSelected>>', self.create_ticks)

    def update_bpm(self, change):
        """
        Updates self.bpm variable
        :param change: change in bpm
        :return:
        """
        new_bpm = self.bpm.get() + change
        if 1 <= new_bpm <= 300:
            self.bpm.set(new_bpm)

    def start(self):
        """
        Start or stop working of metronome
        :return:
        """
        self.is_running.set(True)
        self.start_button.configure(state='disabled')
        self.stop_button.configure(state='enabled')
        # disable option to change count numbers while metronome is running
        self.counts_combobox.configure(state='disabled')

        # start counting
        self.play(tick=self.counts.get() -1)

    def stop(self):
        """
        Stops the timer
        :return:
        """
        self.is_running.set(False)
        self.stop_button.configure(state='disabled')
        self.start_button.configure(state='enabled')
        # sets all ticks colours to default
        self.reset_ticks()
        # bind combobox again
        self.counts_combobox.configure(state='enabled')

    def play(self, tick):
        """
        Counting process
        :param tick: index of a previous item
        :return:
        """
        # counting loop
        if self.is_running.get():
            # changing previous tick to default color:
            self.change_tick(tick)

            # calculating time to wait -101 ms for playing sound and process
            time_to_wait = int(60 / self.bpm.get() * 1000) - 101

            # updating tick index to current
            if tick + 1 == self.counts.get():
                tick = 0
            else:
                tick += 1

            self.play_sound(tick)

            # change color temporary to red
            self.ticks[tick].itemconfigure(1, fill='red')

            # after time of beat, go to next tick
            self.after(
                time_to_wait,
                lambda: self.play(tick)
            )

    def change_tick(self, tick):
        """
        Change tick back to original colour
        :param tick: index of tick
        :return:
        """
        if tick == 0:
            self.ticks[tick].itemconfigure(1, fill='orange')
        else:
            self.ticks[tick].itemconfigure(1, fill='yellow')

    def reset_ticks(self):
        """
        Reset all ticks colours to default
        :return:
        """
        self.ticks[0].itemconfigure(1, fill='orange')
        for tick in self.ticks[1:]:
            tick.itemconfigure(1, fill='yellow')

    def play_sound(self, tick):
        """
        Plays metronome sound
        :param tick: index of tick
        :return:
        """
        # first tick is accent
        if tick == 0:
            winsound.Beep(880, 100)
        else:
            winsound.Beep(440, 100)
