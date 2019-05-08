#!/usr/bin/python3

"""
Copyright (c): 2019 ijgnd
               2018 Rene Schallner

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.


 * This file incorporates work (i.e. the class WinEventFilter, some parts 
 * of the function main) covered by the following copyright and  
 * permission notice:  
 *  
 *     Copyright (c) 2016-2018 Arun Mahapatra
 *  
 * Permission is hereby granted, free of charge, to any person obtaining
 * a copy of this software and associated documentation files (the
 * "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish,
 * distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so, subject to
 * the following conditions:
 * 
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
 * BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
 * ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.

"""

import sys 
import os
import time
import shutil
import configparser

import PyQt5.QtCore
from PyQt5.QtCore import QAbstractNativeEventFilter, QAbstractEventDispatcher
from PyQt5.QtWidgets import QApplication, QMainWindow
from pyqtkeybind import keybinder
import pyautogui

from fuzzypanel_slzk_mod import FuzzySearchPanel
from confirm import confirm


config = configparser.ConfigParser()
config.read('config.ini')
TAGFILE = config.get('Taglist','TAGFILE')
GLOBAL_SHOW_HOTKEY = config['Taglist']['GLOBAL_SHOW_HOTKEY']
CONFIRM_NEW_TAGS = config['Taglist'].getboolean('ASK_FOR_CONFIRMATION_FOR_NEW_TAGS')
UPPERCASE_FIRST = config['Taglist'].getboolean('SORT_LIST__UPPERCASE_BEFORE_LOWERCASE')
BACKUP_BEFORE = config['Taglist']['BACKUP_TAGLIST_BEFORE_ADDING_NEW_TAG_TO_THIS_FOLDER']
if BACKUP_BEFORE.lower() == ("false" or "none" or "0" or ""):
    BACKUP_BEFORE = False






class WinEventFilter(QAbstractNativeEventFilter):
    def __init__(self, keybinder):
        self.keybinder = keybinder
        super().__init__()

    def nativeEventFilter(self, eventType, message):
        ret = self.keybinder.handler(eventType, message)
        return ret, 0


def taglist_as_dict():
    if not os.path.isfile(TAGFILE):
        print('Error. TAGFILE not exist at given location. Update the script.')
        print('Exiting...')
        sys.exit()
    else:
        with open(TAGFILE,"r") as f:
            lines = [i.rstrip('\n') for i in f.readlines()]
            #the fuzzypanel expects a dictionary
            #   key    is shown in the panel
            #   value  is returned
            #in my case it's the same
            ld = {}
            for l in lines:
                ld[l] = l
            return ld


class FuzzySearchDialog(QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_tag_list()
        max_items = 500
        prefill = ""
        self.mw = FuzzySearchPanel(self, item_dict=self.item_dict, max_items=max_items, prefill=prefill)
        self.setCentralWidget(self.mw)

    def load_tag_list(self):
        self.item_dict = taglist_as_dict()
        
    def save_tag(self, val):
        if not CONFIRM_NEW_TAGS:
            return True
        elif confirm('Do you want to add "%s" to your tag list ?' %val,'Confirm new tag',self):
            return True
        else:
            return False
            
    def maybe_create_backup(self):
        if os.path.isdir(BACKUP_BEFORE):
            timestamp = time.strftime('%Y-%m-%d__%H_%M_%S', time.localtime(time.time()))
            newfile = os.path.join(BACKUP_BEFORE,timestamp + 'txt')
            shutil.copy2(TAGFILE,newfile)
              
    def onEnter(self,key,val):
        new_tag_added = False
        if val not in self.item_dict.keys():
            if self.save_tag(val):
                new_tag_added = True
        self.hide()
        #PROBLEM Some strings (those that start with "f" or "n" are interpreted as "Ctrl+shift+f"
        #this is not a general behavior: strings that start with "c" are inserted properly into 
        #Supermemo even though "Ctrl+Shift+C" is a valid shortcuts in Supermemo.
        #I can insert those strings into other apps without problems.
        #Workaround for tagging: just test with a special character first (which seems to work)
        #pyautogui.keyUp('shift')    # doesn't help
        #pyautogui.keyUp('ctrl')    # doesn't help
        pyautogui.typewrite("$" + val, interval=0.005)
        #pyautogui.typewrite("" + val, interval=0.005)
        
        self.mw.input_line.setText("")
        if new_tag_added:   
            self.maybe_create_backup()
            self.item_dict[key] = val
            with open(TAGFILE,"w") as f:
                l = list(self.item_dict.keys())
                if UPPERCASE_FIRST:
                    for i in sorted(l):
                        f.write("%s\n" % i)
                else:
                    for i in sorted(l, key=lambda s: s.casefold()):
                        f.write("%s\n" % i)

            #update taglist window with new tag
            if UPPERCASE_FIRST:
                self.mw.item_dict = {k: self.item_dict[k] for k in sorted(self.item_dict.keys())}
            else:
                self.mw.item_dict = {k: self.item_dict[k] for k in sorted(self.item_dict.keys(),key=lambda s: s.casefold())}
            self.mw.fuzzy_items = list(self.mw.item_dict.keys())[:self.mw.max_items]
            self.mw.update_listbox()

def onGlobalShowHotkey():
    tagselector.show()
    tagselector.activateWindow()
    tagselector.mw.input_line.setFocus()
        

def main():
    global tagselector
    app = QApplication(sys.argv)
    nonShownMainWindow = QMainWindow()
    print('Tag File is at: "%s"' %TAGFILE) 
    print('global shortcut to raise the tag selector window is: "%s"' % GLOBAL_SHOW_HOTKEY )
    
    tagselector = FuzzySearchDialog()
    tagselector.show()   #initial loading takes quite long so do it now
    tagselector.hide()

    #when I extracted this to a new class and a different file this didn't work in 2019-05.
    keybinder.init()
    filter = WinEventFilter(keybinder)
    keybinder.register_hotkey(nonShownMainWindow.winId(), GLOBAL_SHOW_HOTKEY, onGlobalShowHotkey)
    event_dispatcher = QAbstractEventDispatcher.instance()
    event_dispatcher.installNativeEventFilter(filter)

    app.exec_()
    keybinder.unregister_hotkey(nonShownMainWindow.winId(), GLOBAL_SHOW_HOTKEY)  #necessary?


if __name__ == '__main__':
    main()
    
