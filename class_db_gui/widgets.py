'''User defined widgets'''
from tkinter import ttk



class NamedEntry(ttk.Frame):
    '''entry with name(label at front)'''
    def __init__(self, master, label_text, entry_textvariable, *args, **kwargs):
        super().__init__(master)

        self.label = ttk.Label(self, text=label_text)
        self.entry = ttk.Entry(self, textvariable=entry_textvariable, *args, **kwargs) 
        self.label.grid(row=0, column=0, padx=5)
        self.entry.grid(row=0, column=1, padx=5)



class NamedLabel(ttk.Frame):
    '''Label with fixed name(label at front)'''
    def __init__(self, master, label_text, label_textvariable, *args, **kwargs):
        super().__init__(master)

        self.name = ttk.Label(self, text=label_text)
        self.label = ttk.Label(self, textvariable=label_textvariable, *args, **kwargs)
        self.name.grid(row=0, column=0, padx=5)
        self.label.grid(row=0, column=1, padx=5)
