"""
minimal adjustment of 
- https://raw.githubusercontent.com/renerocksai/sublimeless_zk/master/src/fuzzypanel.py
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
"""

import sys
import configparser

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


config = configparser.ConfigParser()
config.read('config.ini')
FILTER_WITH = config.get('Taglist','FILTER_WITH').lower()
if FILTER_WITH not in ["slzk_mod","slzk","fuzzyfinder"]:
    print('illegal value in config for "FILTER_WITH"')
    print('exiting...')
    sys.exit()


from search_alsoAtStart import split_search_terms_withStart, process_search_string_withStart
from search import split_search_terms, process_search_string

if FILTER_WITH == "fuzzyfinder":
    from fuzzyfinder import fuzzyfinder



class PanelInputLine(QLineEdit):
    down_pressed = pyqtSignal()
    up_pressed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet('background-color:#ffffff')

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        key = event.key()
        if key == Qt.Key_Down:
            self.down_pressed.emit()
        elif key == Qt.Key_Up:
            self.up_pressed.emit()


class FuzzySearchPanel(QWidget):
    item_selected = pyqtSignal(str, str)    # key, value
    close_requested = pyqtSignal()

    def __init__(self, parent=None, item_dict=None, max_items=20, prefill=""):
        super().__init__(parent)
        self.parent = parent
        self.max_items = max_items
        self.setObjectName("FuzzySearchPanel")
        self.item_dict = item_dict    #    { show_as: associated_value }
        if self.item_dict is None:
            self.item_dict = {}

        self.fuzzy_items = list(self.item_dict.keys())[:max_items]
        self.initUI()
        if prefill:
            self.input_line.setText(prefill)

    def initUI(self):
        vlay = QVBoxLayout()
        self.input_line = PanelInputLine()
        self.list_box = QListWidget()
        for i in range(self.max_items):
            self.list_box.insertItem(i, '')
        vlay.addWidget(self.input_line)
        vlay.addWidget(self.list_box)
        self.update_listbox()
        self.setLayout(vlay)
        self.setMinimumWidth(1000)
        self.list_box.setAlternatingRowColors(True)

        # style
        '''
        self.setStyleSheet(""" QListWidget:item:selected{
                                    background: lightblue;
                                    border: 1px solid #6a6ea9;
                                }
                                QListWidget{
                                    background: #f0f0f0;
                                    show-decoration-selected: 1;
                                    font-family: "Times New Roman"                                
                                }
                                QListWidget::item:alternate {
                                    background: #E0E0E0;
                                }    
                                QLineEdit {
                                    background-color: #ffffff;
                                }             
                                """
                           )
        '''

        # connections
        self.item_selected.connect(self.parent.onEnter)
        self.input_line.textChanged.connect(self.text_changed)
        self.input_line.returnPressed.connect(self.return_pressed)
        self.input_line.down_pressed.connect(self.down_pressed)
        self.input_line.up_pressed.connect(self.up_pressed)
        self.list_box.itemDoubleClicked.connect(self.item_doubleclicked)
        self.list_box.installEventFilter(self)
        self.input_line.setFocus()

    def update_listbox(self):
        for i in range(self.max_items):
            item = self.list_box.item(i)
            if i < len(self.fuzzy_items):
                item.setHidden(False)
                item.setText(self.fuzzy_items[i])
            else:
                item.setHidden(True)
        self.list_box.setCurrentRow(0)

    def text_changed(self):
        search_string = self.input_line.text()
        if FILTER_WITH == "fuzzyfinder":
            if search_string:
                self.fuzzy_items = list(fuzzyfinder(search_string, self.item_dict.keys()))[:self.max_items]   
            else:
                self.fuzzy_items = list(self.item_dict.keys())[:self.max_items]
        else:
            if not search_string:
                search_string = ""
            if FILTER_WITH == "slzk_mod":
                self.fuzzy_items = process_search_string_withStart(search_string,self.item_dict,self.max_items)
            elif FILTER_WITH == "slzk":
                self.fuzzy_items = process_search_string(search_string,self.item_dict,self.max_items)
        self.update_listbox()
        
    def up_pressed(self):
        row = self.list_box.currentRow()
        if row > 0:
            self.list_box.setCurrentRow(row - 1)

    def down_pressed(self):
        row = self.list_box.currentRow()
        if row < len(self.fuzzy_items):
            self.list_box.setCurrentRow(row + 1)

    def return_pressed(self):
        if len(self.fuzzy_items) > 0:
            row = self.list_box.currentRow()
            key = self.fuzzy_items[row]
            value = self.item_dict[key]
            self.item_selected.emit(key, value)
        else:
            key = ""
            value = self.input_line.text()
            self.item_selected.emit(value, value)

    def item_doubleclicked(self):
        row = self.list_box.currentRow()
        key = self.fuzzy_items[row]
        value = self.item_dict[key]
        self.item_selected.emit(key, value)
    
    def eventFilter(self, watched, event):
        if event.type() == QEvent.KeyPress and event.matches(QKeySequence.InsertParagraphSeparator):
            self.return_pressed()
            return True
        else:
            return QWidget.eventFilter(self, watched, event)
