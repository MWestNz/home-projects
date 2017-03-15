#!/usr/bin/env python
# encoding: utf-8
"""
tkentrycomplete.py

A Tkinter widget that features autocompletion.

Created by Mitja Martini on 2008-11-29.
Updated by Russell Adams, 2011/01/24 to support Python 3 and Combobox.
   Licensed same as original (not specified?), or public domain, whichever is less restrictive.
"""
import sys
import os
import Tkinter
import ttk

__version__ = "1.1"

# I may have broken the unicode...
Tkinter_umlauts=['odiaeresis', 'adiaeresis', 'udiaeresis', 'Odiaeresis', 'Adiaeresis', 'Udiaeresis', 'ssharp']

class AutoCompleteEntry(Tkinter.Entry):
        """
        Subclass of Tkinter.Entry that features autocompletion.

        To enable autocompletion use set_completion_list(list) to define
        a list of possible strings to hit.
        To cycle through hits use down and up arrow keys.
        """

        def __init__(self, lista, frame, index, *args, **kwargs):     
            Tkinter.Entry.__init__(self, master=frame, *args, **kwargs)
            self.set_completion_list(lista)
            self.auto_index = index

        def set_completion_list(self, completion_list):
                self._completion_list = sorted(completion_list, key=str.lower) # Work with a sorted list
                self._hits = []
                self._hit_index = 0
                self.position = 0
                self.bind('<KeyRelease>', self.handle_keyrelease)

        def autocomplete(self, delta=0):
                """autocomplete the Entry, delta may be 0/1/-1 to cycle through possible hits"""
                if delta: # need to delete selection otherwise we would fix the current position
                        self.delete(self.position, Tkinter.END)
                else: # set position to end so selection starts where textentry ended
                        self.position = len(self.get())
                # collect hits
                _hits = []
                for element in self._completion_list:
                        if element.lower().startswith(self.get().lower()):  # Match case-insensitively
                                _hits.append(element)
                # if we have a new hit list, keep this in mind
                if _hits != self._hits:
                        self._hit_index = 0
                        self._hits=_hits
                # only allow cycling if we are in a known hit list
                if _hits == self._hits and self._hits:
                        self._hit_index = (self._hit_index + delta) % len(self._hits)
                # now finally perform the auto completion
                if self._hits:
                        self.delete(0,Tkinter.END)
                        self.insert(0,self._hits[self._hit_index])
                        self.select_range(self.position,Tkinter.END)

        def handle_keyrelease(self, event):
                """event handler for the keyrelease event on this widget"""
                if event.keysym == "BackSpace":
                        if self.position > 0:
                                self.delete(self.index(Tkinter.INSERT), Tkinter.END)
                                self.position = self.index(Tkinter.END)
                if event.keysym == "Left":
                        if self.position < self.index(Tkinter.END): # delete the selection
                                self.delete(self.position, Tkinter.END)
                        else:
                                self.position = self.position-1 # delete one character
                                self.delete(self.position, Tkinter.END)
                if event.keysym == "Right":
                        self.position = self.index(Tkinter.END) # go to end (no selection)
                if event.keysym == "Down":
                        self.autocomplete(1) # cycle to next hit
                if event.keysym == "Up":
                        self.autocomplete(-1) # cycle to previous hit
                if len(event.keysym) == 1 or event.keysym in Tkinter_umlauts:
                        self.autocomplete()

class AutoCompleteCombobox(ttk.Combobox):

        def __init__(self, lista, frame, index, *args, **kwargs):     
            ttk.Combobox.__init__(self, master=frame, *args, **kwargs)
            self.main_list = lista
            self.set_completion_list(lista)
            self.combo_index = index

        def set_main_list(self,lista):
            self.main_list = lista

        def set_completion_list(self, completion_list):
                """Use our completion list as our drop down selection menu, arrows move through menu."""
                self._completion_list = sorted(completion_list, key=str.lower) # Work with a sorted list
                self._hits = []
                self._hit_index = 0
                self.position = 0
                self.bind('<KeyRelease>', self.handle_keyrelease)
                self['values'] = self._completion_list  # Setup our popup menu

        def autocomplete(self, delta=0):
                """autocomplete the Combobox, delta may be 0/1/-1 to cycle through possible hits"""
                if delta: # need to delete selection otherwise we would fix the current position
                        self.delete(self.position, Tkinter.END)
                else: # set position to end so selection starts where textentry ended
                        self.position = len(self.get())
                # collect hits
                _hits = []
                for element in self.main_list:
                        elements = element.split()
                        for a in elements:
                            if a.lower().startswith(self.get().lower()) and not element in _hits: # Match case insensitively
                                    _hits.append(element)
                # if we have a new hit list, keep this in mind
                if _hits != self._hits:
                        self._hit_index = 0
                        self._hits=_hits
                # only allow cycling if we are in a known hit list
                if _hits == self._hits and self._hits:
                        self._hit_index = (self._hit_index + delta) % len(self._hits)
                # now finally perform the auto completion
                if self._hits:
                        # self.delete(0,Tkinter.END)
                        # self.insert(0,self._hits[self._hit_index])
                        # self.select_range(self.position,Tkinter.END)
                        self.set_completion_list(self._hits)

        def handle_keyrelease(self, event):
                """event handler for the keyrelease event on this widget"""
                if event.keysym == "BackSpace":
                        self.delete(self.index(Tkinter.INSERT), Tkinter.END)
                        self.position = self.index(Tkinter.END)
                        self.autocomplete(delta=0)
                if event.keysym == "Left":
                        if self.position < self.index(Tkinter.END): # delete the selection
                                self.delete(self.position, Tkinter.END)
                                self.autocomplete(delta=0)
                        else:
                                self.position = self.position-1 # delete one character
                                self.delete(self.position, Tkinter.END)
                                self.autocomplete(delta=0)
                if event.keysym == "Right":
                        self.position = self.index(Tkinter.END) # go to end (no selection)
                        self.autocomplete(delta=0)
                if event.keysym == "Tab":
                    if self.master.clean_player_list in dir(self.master):
                        self.master.clean_player_list(self.master.parent)
                if len(event.keysym) == 1:
                    self.autocomplete(delta=0)
                # No need for up/down, we'll jump to the popup
                # list at the position of the autocompletion

def test(test_list):
        """Run a mini application to test the AutocompleteEntry Widget."""
        root = Tkinter.Tk(className=' AutocompleteEntry demo')
        entry = AutoCompleteEntry(test_list,root,0)
        # entry.set_completion_list(test_list)
        entry.pack()
        entry.focus_set()
        combo = AutoCompleteCombobox(test_list,root,0)
        # combo.set_completion_list(test_list)
        combo.pack()
        combo.focus_set()
        # I used a tiling WM with no controls, added a shortcut to quit
        root.bind('<Control-Q>', lambda event=None: root.destroy())
        root.bind('<Control-q>', lambda event=None: root.destroy())
        root.mainloop()

if __name__ == '__main__':
        test_list = ('ap ple', 'bana na', 'Cran Berry', 'dog wood', 'alpha', 'Acorn', 'Anise' )
        test(test_list)