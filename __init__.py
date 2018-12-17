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
    
    def runBrowser(browser, toClean):
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
            #debug(f"""dealing with model ""\"{model}""\".""")
            readIfRequired()
            compileAndSaveModel(model, toClean = toClean, objects = objects)
        mw.progress.finish()
        tooltip("Ending "+("cleaning " if toClean else "")+"Template")
    
    
    def setupMenu(browser):
        a = QAction("Template", browser)
        a.setShortcut(QKeySequence("Ctrl+Alt+T"))
        a.triggered.connect(lambda : runBrowser(browser,False))
        browser.form.menuEdit.addAction(a)
    
        a = QAction("Clean Template", browser)
        a.setShortcut(QKeySequence("Ctrl+Alt+Shift+T"))
        a.triggered.connect(lambda : runBrowser(browser,True))
        browser.form.menuEdit.addAction(a)
    addHook("browser.setupMenus", setupMenu)
except:
    print("\n".join(reversed(str(traceback.format_exc()).split("\n"))))
    os._exit(1)
