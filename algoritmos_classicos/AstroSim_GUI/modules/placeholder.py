import tkinter as tk
import ttkbootstrap as ttk

class PlaceholderEntry(ttk.Entry):
    def __init__(self, master=None, placeholder="", **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = 'grey'
        self.default_fg_color = self['foreground']
        
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)
        
        self._on_focus_out(None)

    def _on_focus_in(self, event):
        if self.get() == self.placeholder:
            self.delete(0, "end")
            self.configure(foreground=self.default_fg_color)

    def _on_focus_out(self, event):
        if not self.get():
            self.insert(0, self.placeholder)
            self.configure(foreground=self.placeholder_color)