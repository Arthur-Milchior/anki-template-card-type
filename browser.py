from aqt import mw
from anki.hooks import addHook
from aqt.qt import QAction, QKeySequence
from aqt.utils import tooltip
from .config import readIfRequired, objects
from .editTemplate import compileAndSaveModel


def runBrowser(browser, action, note):
    if note:
        return runBrowserNote(browser,action)
    else:
        return runBrowserCard(browser,action)
    
def runBrowserNote(browser, action):
    mw.checkpoint("Change template on notes")
    mw.progress.start()
    nids=browser.selectedNotes()
    mids = set()
    readIfRequired()
    for nid in nids:
        note = mw.col.getNote(nid)
        mid = note.mid
        mids.add(mid)
    for mid in mids:
        model = mw.col.models.get(mid)
        compileAndSaveModel(model, action = action, objects = objects)
    mw.progress.finish()
    tooltip(f"Ending {action} on notes")
        
def runBrowserCard(browser, action):
    mw.checkpoint("Change template on cards")
    mw.progress.start()
    readIfRequired()
    cids=browser.selectedCards()
    mids = dict()
    for cid in cids:
        card = mw.col.getCard(cid)
        note = card.note()
        mid = note.mid
        if mid not in mids:
            mids[mid]=set()
        ord = card.ord
        mids[mid].add(ord)
    for mid in mids:
        model = mw.col.models.get(mid)
        compileAndSaveModel(model, action = action, objects = objects, ords=mids[mid])
    mw.progress.finish()
    tooltip(f"Ending {action} on cards")
    
    
def setupMenu(browser):
    a = QAction("ReTemplate Card", browser)
    a.triggered.connect(lambda : runBrowser(browser,"ReTemplate",False))
    browser.form.menuEdit.addAction(a)
    a.setShortcut(QKeySequence("Ctrl+Shift+T"))
    
    a = QAction("Template Note", browser)
    a.setShortcut(QKeySequence("Ctrl+Alt+T"))
    a.triggered.connect(lambda : runBrowser(browser,"Template",True))
    browser.form.menuEdit.addAction(a)
    
    a = QAction("ReTemplate note", browser)
    a.setShortcut(QKeySequence("Ctrl+Alt+Shift+T"))
    a.triggered.connect(lambda : runBrowser(browser,"ReTemplate",True))
    browser.form.menuEdit.addAction(a)

    a = QAction("\"frontSide\" to each back", browser)
    a.triggered.connect(lambda : runBrowser(browser,"FrontSide",True))
    browser.form.menuEdit.addAction(a)

    a = QAction("Clean Template note", browser)
    a.triggered.connect(lambda : runBrowser(browser,"Clean template",True))
    browser.form.menuEdit.addAction(a)
addHook("browser.setupMenus", setupMenu)
