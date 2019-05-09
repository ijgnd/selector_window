#### quick select dialog
- Windows, Linux only.
- PyQt5 Dialog that can be called with a global hotkey (with pyqtkeybind). 
This dialog allows to filter the lines that are read from a file. What 
the user selects is  inserted at the cursor with pyautogui
- run python3 src/tag_fuzzy_select_and_insert.py
- there are some user settings, see config.ini. You must adjust
the path of the TAGFILE and the BACKUP.
- syntax for the default seach method: strings (separated by space) can
be in any order, `!` to exclude a string, `"` to search for space (e.g.
`the wind`), `_` to indicate that the line must start with this string(
e.g. `_wind` wont match `some wind`.
- Alpha Quality. Released in the hope of gettig useful feedback.
Use this at your own risk. If you find bugs or have improvements
please let me know.


##### Requirements
This script requires 
- Python3 (only tested with 3.7)
- PyQt5, https://pypi.org/project/PyQt5/ (only tested with 5.12)
- PyAutoGUI, https://pypi.org/project/PyAutoGUI/
- pyqtkeybind, https://pypi.org/project/pyqtkeybind/
- fuzzyfinder, https://pypi.org/project/fuzzyfinder/ (optional)


##### License
AGPLv3


##### Authors, Copyright
Copyright (c): 

- 2019 ijgnd
- 2018 Rene Schallner
- 2016-2018 Arun Mahapatra (for details see top of tag_fuzzy_select_and_insert.py)
               
This script mostly combines python scripts and functions from
different authors. 

The main part of this sofware (filter dialog, search filter) is 
taken from the markdown notetaking software "sublimeless_zk" by
Rene Schallner, https://github.com/renerocksai/sublimeless_zk
which puts special emphasis on quickly linking notes to each other.
Screenshot of the panel at 
https://github.com/renerocksai/sublimeless_zk/blob/master/imgs/insert-link.png


##### Known Issues / Help needed
- Strings that start with some letters (like f,n) are in some apps
treated as hotkeys as "Ctrl+Shift+f" followed by `string[1:]`.
see comments in the file tag_fuzzy_select_and_insert.py
- when raising the window it might be shown in the wrong 
position, see https://stackoverflow.com/questions/40074637/pyqt5-port-how-do-i-hide-a-window-and-let-it-appear-at-the-same-position


##### Extend / To Do
- Taskbar Symbol, Tray Icon
- MacOS? pyqtkeybind which I need for the global hotkey does not work 
on MacOS. PyAutoGUI plans to introduce 
[Ability to set global hotkey on all platforms](https://pyautogui.readthedocs.io/en/latest/roadmap.html)
in the future.


##### Compatibility
Tested on Linux (L) and on Windows 10 Pro 1809 (W).

Working with the following applications:

- Chrome 74, Firefox 66 with Office365 (W)
- Evernote for Desktop (W) 
- Anki 2.0/2.1 (W,L)
- Supermemo 17 (W)
- Word 2019 (W)
- LibreOffice 6.1 (W,L)
- VSCode (W,L)
- Cmd, Powershell (W)
- Nautilus/Files (L)
- Terminal (L)
- emacs (L)

Not working:

- File Explorer (W)


##### user config
adjust the file `config.ini` as needed.

- `TAGFILE`: if you use Windows make sure to use use `\\` where you 
have `\` in your path names (like `C:\\Myfiles\\tags.txt`).
- `GLOBAL_SHOW_HOTKEY`(default `Shift+Ctrl+A`):
- `ASK_FOR_CONFIRMATION_FOR_NEW_TAGS`(default `True`):
- `BACKUP_TAGLIST_BEFORE_ADDING_NEW_TAG_TO_THIS_FOLDER`: set to `False`
to disable save on backup
- `FILTER_WITH_FUZZYFINDER` (default `slzk_mod`): possible values `slzk_mod`,
`slzk`, `fuzzyfinder`. I prefer the sublimeless_zk algorithm 
over https://pypi.org/project/fuzzyfinder/ because the latter is case 
insensitive only, space is not used to separate different search words, 
i.e. every typed letter has to occur in the typed order, i.e. "his eng" 
doesn't find "EnglandHistory", etc. The `slzk` filter doesn't 
allow to seach for "startswith". That's why I changed it to `slzk_mod`
which offers this option. But this was a quick addition and might be
buggy.


##### Discarded Filter/Search Options
- https://github.com/seatgeek/fuzzywuzzy doesn't produce useable results when
search terms are inverted


##### Alternatives that I still need to check
- https://github.com/qutebrowser/qutebrowser/tree/master/qutebrowser/completion
- QCompleter, e.g. https://stackoverflow.com/questions/4827207/how-do-i-filter-the-pyqt-qcombobox-items-based-on-the-text-input
    - complicated - what benefits? RS must have had his reasons not to use it.
    - by default every typed letter has to occur in the typed order
- non-python like fzf, ivy/helm
