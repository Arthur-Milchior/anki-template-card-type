from aqt import mw
from .editTemplate import applyOnAllTemplate
from anki.hooks import addHook
from aqt.qt import QAction, QKeySequence
from aqt.utils import tooltip

def runBrowser(browser, clean):
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
        applyOnAllTemplate(model,clean)
    mw.progress.finish()
    tooltip("Ending "+("cleaning " if clean else "")+"Template")


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
