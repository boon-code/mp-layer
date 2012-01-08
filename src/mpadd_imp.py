from mpadd import CustomMpadd
import sys


if sys.version_info[0] == 3:
    import tkinter
    from tkinter.filedialog import *
elif sys.version_info[0] == 2:
    import Tkinter as tkinter
    from tkFileDialog import *


__author__ = 'Manuel Huber'
__copyright__ = "Copyright (c) 2011 Manuel Huber."
__license__ = 'GPLv3'
__docformat__ = "restructuredtext en"


class Mpadd(CustomMpadd):
    
    def __init__(self, controller):
        """Initializes a new instance
        
        :param controller: Controller object.
        """
        self._ctrl = controller
        root = tkinter.Tk()
        self._root = root
        root.bind("<Control_L>v", self._past_event)
        root.bind("<<ListboxSelect>>", self._listbox_event_handler)
        root.bind("<KeyRelease>", self._textbox_event_handler)
        self._sclNames['command'] = self._lstNames.yview
        self._sclExtension['command'] = self._lstExtension.yview
        self._txtName.insert('end', "<Name>")
        self._txtSource.insert('end', "<Source>")
    
    def _past_event(self, event):
        pass
    
    def _textbox_event_handler(self, event):
        pass
    
    def _listbox_event_handler(self, event):
        pass
