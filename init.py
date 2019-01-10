import traceback
import sys
import os

try:
    from aqt import mw
    from anki.hooks import addHook
    from aqt.qt import QAction, QKeySequence
    from aqt.utils import tooltip
    
    from . import templates
    from .config import readIfRequired, objects
    from .debug import debug
    from .imports import *
    from . import tests
    
    from .editTemplate import compileAndSaveModel
    
    def runBrowser(browser, action):
        mw.checkpoint("Change template")
        mw.progress.start()
        
        nids=browser.selectedNotes()
        mids = set()
        for nid in nids:
            note = mw.col.getNote(nid)
            mid = note.mid
            mids.add(mid)
        for mid in mids:
            model = mw.col.models.get(mid)
            #debug("""dealing with model ""\"{model}""\".""")
            readIfRequired()
            compileAndSaveModel(model, action = action, objects = objects)
        mw.progress.finish()
        tooltip(f"Ending {action}")
    
    
    def setupMenu(browser):
        a = QAction("Template", browser)
        a.setShortcut(QKeySequence("Ctrl+Alt+T"))
        a.triggered.connect(lambda : runBrowser(browser,"Template"))
        browser.form.menuEdit.addAction(a)
        
        a = QAction("ReTemplate", browser)
        a.triggered.connect(lambda : runBrowser(browser,"ReTemplate"))
        browser.form.menuEdit.addAction(a)
    
        a = QAction("frontSide to each back", browser)
        a.triggered.connect(lambda : runBrowser(browser,"Back to front"))
        browser.form.menuEdit.addAction(a)
    
        a = QAction("Clean Template", browser)
        a.setShortcut(QKeySequence("Ctrl+Alt+Shift+T"))
        a.triggered.connect(lambda : runBrowser(browser,"Clean"))
        browser.form.menuEdit.addAction(a)
    addHook("browser.setupMenus", setupMenu)
except:
    st = str(traceback.format_exc())
    st = "\n".join(reversed(str(traceback.format_exc()).split("\n")))
    print(st)
    os._exit(1)
