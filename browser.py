from anki.hooks import addHook
from aqt import mw
from aqt.qt import QAction, QKeySequence
from aqt.utils import tooltip
from .config import readIfRequired, objects, getObject
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
    shortCut = getObject("Shortcut: ReTemplate Card","Ctrl+Shift+T")
    if shortCut:
        a.setShortcut(QKeySequence(shortCut))

    a = QAction("Template Note", browser)
    shortCut = getObject("Shortcut: Template Note","Ctrl+Alt+T")
    if shortCut:
        a.setShortcut(QKeySequence(shortCut))
    a.triggered.connect(lambda : runBrowser(browser,"Template",True))
    browser.form.menuEdit.addAction(a)

    a = QAction("ReTemplate Note", browser)
    shortCut = getObject("Shortcut: ReTemplate Note","Ctrl+Alt+Shift+T")
    if shortCut:
        a.setShortcut(QKeySequence(shortCut))
    a.triggered.connect(lambda : runBrowser(browser,"ReTemplate",True))
    browser.form.menuEdit.addAction(a)

    a = QAction("\"frontSide\" to each back", browser)
    shortCut = getObject("Shortcut: frontside")
    if shortCut:
        a.setShortcut(QKeySequence(shortCut))
    a.triggered.connect(lambda : runBrowser(browser,"FrontSide",True))
    browser.form.menuEdit.addAction(a)

    a = QAction("Clean Template note", browser)
    shortCut = getObject("Shortcut: Clean Template note")
    if shortCut:
        a.setShortcut(QKeySequence(shortCut))
    a.triggered.connect(lambda : runBrowser(browser,"Clean template",True))
    browser.form.menuEdit.addAction(a)
addHook("browser.setupMenus", setupMenu)
