'''User defined widgets'''

from tkinter import ttk


class LabelEntry(ttk.Frame):
    def __init__(self, master, label_text, entry_textvariable, *args, **kwargs):
        super().__init__(master)

        self.label = ttk.Label(self, text=label_text)
        self.entry = ttk.Entry(self, textvariable=entry_textvariable, *args, **kwargs) 
        self.label.grid(row=0, column=0)
        self.entry.grid(row=0, column=1)