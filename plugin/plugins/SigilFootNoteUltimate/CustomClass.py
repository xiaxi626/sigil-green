# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import re,os

#基础高亮模板
class Highlighter(QtGui.QSyntaxHighlighter):
    def __init__(self,parent:QtGui.QTextDocument = None):
        super().__init__(parent)
        self.initFormat()
        self.initRegexp()

    def initFormat(self):
        self.Format = {}
        for name in ("keyword","annotation"):
            self.Format[name] = QtGui.QTextCharFormat()
            self.Format[name].setFontWeight(QtGui.QFont.Normal)
        self.Format["keyword"].setForeground(QtCore.Qt.blue)
        self.Format["annotation"].setForeground(QtCore.Qt.darkGreen)

    def initRegexp(self):
        self.Rules = {}
        self.Rules["annotation"] = QtCore.QRegularExpression(r"<!.*?-->")

    def highlightBlock(self, text): #highlightBlock 是必须重定义的自运行函数。
        for name in ["keyword","annotation"]:
            i = self.Rules[name].globalMatch(text)
            while i.hasNext():
                match = i.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), self.Format[name])

#自动匹配模式替换模板
class Highlighter_A(Highlighter):
    def __init__(self,parent:QtGui.QTextDocument = None):
        super().__init__(parent)
        self.Rules["keyword"] = QtCore.QRegularExpression(r"\[(num|note|ref|id|href)\]")
#手动匹配模式替换模板
class Highlighter_B(Highlighter):
    def __init__(self,parent:QtGui.QTextDocument = None):
        super().__init__(parent)
        self.Rules["keyword"] = QtCore.QRegularExpression(r"\[(num|id|href|n[1-9]|r[1-9])\]")
#页尾节点替换模板
class Highlighter_C(Highlighter):
    def __init__(self,parent:QtGui.QTextDocument = None):
        super().__init__(parent)
        self.Rules["keyword"] = QtCore.QRegularExpression(r"\[pos\]")

#无高亮的高亮模板
class HighlighterClose(QtGui.QSyntaxHighlighter):
    def __init__(self,parent:QtGui.QTextDocument = None):
        super().__init__(parent)
    def highlightBlock(self,text):
        pass
    
#基础高亮模板控件
class TemplateEdit(QtWidgets.QTextEdit):
    def __init__(self,parent = None):
        super().__init__(parent = parent)
    def getText(self):
        text = self.toPlainText()
        return re.sub(r'(?s)<!--.*?-->\n?','',text)
#自动匹配模式替换模板控件
class TemplateEdit_A(TemplateEdit):
    def __init__(self,parent = None):
        super().__init__(parent = parent)
        self.highlighter = Highlighter_A(self.document())
#手动匹配模式替换模板控件
class TemplateEdit_B(TemplateEdit):
    def __init__(self,parent = None):
        super().__init__(parent = parent)
        self.highlighter = Highlighter_B(self.document())
#页尾节点替换模板控件
class TemplateEdit_C(TemplateEdit):
    def __init__(self,parent = None):
        super().__init__(parent = parent)
        self.open_highlighter()
    def close_highlighter(self):
        self.highlighter = HighlighterClose(self.document())
    def open_highlighter(self):
        self.highlighter = Highlighter_C(self.document())


#调用保存配置
class SavedConfGroupBox(QtWidgets.QGroupBox):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.rightMenuShow)
        self.setStyleSheet("QMenu::item{padding:6px 15px;font-size:12px;}"+
                           "QMenu::item:selected {background:#90C8F6}")
    def rightMenuShow(self,pos):
        menu = QtWidgets.QMenu(self)
        menu.addAction(QtGui.QIcon(),'导入配置')
        menu.addAction(QtGui.QIcon(),'导出配置')
        menu.triggered.connect(lambda act:self.menuslot(act,None))
        menu.exec_(QtGui.QCursor.pos())
    def menuslot(self,act,cur_item = None):
        child = self.findChild(SavedConfListWidget)
        child.menuslot(act,cur_item)

class SavedConfListWidget(QtWidgets.QListWidget):
    def __init__(self,parent = None):
        super().__init__(parent = parent)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.rightMenuShow)
        self.setStyleSheet("QListWidget::item:selected{background:#0099FF;color:white;}")
    def addConfItem(self,itemname):
        #self.insertItem(0, itemname)
        self.addItem(itemname)
    def getAllItemsText(self):
        text_list = []
        for index in range(self.count()):
            text_list.append(self.item(index).text())
        return text_list
    def rightMenuShow(self, pos):
        cur_item = self.itemAt(pos)
        menu = QtWidgets.QMenu(self)
        if cur_item is not None and len(self.selectedItems()) <= 1:
            menu.addAction(QtGui.QIcon(),'调用配置')
            menu.addSeparator()
            menu.addAction(QtGui.QIcon(),'覆盖保存')
            menu.addAction(QtGui.QIcon(),'新建配置')
            menu.addSeparator()
            menu.addAction(QtGui.QIcon(),'导入配置')
            menu.addAction(QtGui.QIcon(),'导出配置')
            menu.addSeparator()
            menu.addAction(QtGui.QIcon(),'删除配置')
            menu.triggered.connect(lambda act:self.menuslot(act,cur_item))
            menu.exec_(QtGui.QCursor.pos())
        elif len(self.selectedItems()) > 1:
            menu.addAction(QtGui.QIcon(),'删除配置')
            menu.triggered.connect(lambda act:self.menuslot(act,cur_item,multi_items=True))
            menu.exec_(QtGui.QCursor.pos())
        elif cur_item is None:
            menu.addAction(QtGui.QIcon(),'新建配置')
            menu.addSeparator()
            menu.addAction(QtGui.QIcon(),'导入配置')
            menu.addAction(QtGui.QIcon(),'导出配置')
            menu.triggered.connect(lambda act:self.menuslot(act,cur_item))
            menu.exec_(QtGui.QCursor.pos())
            
    def menuslot(self,act,cur_item,multi_items=False):
        home_dir = os.path.expanduser('~')
        mainwin = self.get_mainwin()
        if act.text() == "调用配置":
            if cur_item is not None:
                saved_name = cur_item.text()
                mainwin.load_saved_ini(saved_name)
        
        elif act.text() == "覆盖保存":
            saved_name = cur_item.text()
            mainwin.save_ini(2,saved_name)

        elif act.text() == "新建配置":
            mainwin.save_ini(2)

        elif act.text() == "删除配置":
            if not multi_items:
                saved_name = cur_item.text()
                self.takeItem(self.row(cur_item))
                mainwin.del_ini_savedsection(saved_name)
            else:
                for item in self.selectedItems():
                    saved_name = item.text()
                    self.takeItem(self.row(item))
                    mainwin.del_ini_savedsection(saved_name)

        elif act.text() == "导入配置":
            fd = QtWidgets.QFileDialog.getOpenFileName(self,'选择ini文件',directory=home_dir,filter="*.ini")
            if not fd[0]:
                return
            self.clear() # 清空列表
            bakpath = fd[0]
            with open(bakpath,'r',encoding='utf-8') as bak:
                data = bak.read()
            with open(mainwin.cfgpath,'w',encoding='utf-8') as cfg:
                cfg.write(data)
            mainwin.initConfigureObj()
            mainwin.initSavedConfList()
        elif act.text() == "导出配置":
            mainwin.write_ini()
            save_file_name = 'SigilFootnoteUltimateConfig_bak.ini'
            fd = QtWidgets.QFileDialog.getSaveFileName(self,'备份ini文件',directory=os.path.join(home_dir,save_file_name),filter="*.ini")
            if not fd[0]:
                return
            with open(mainwin.cfgpath,'r',encoding='utf-8') as cfg:
                data = cfg.read()
            with open(fd[0],'w',encoding='utf-8') as bak:
                bak.write(data)
    def get_mainwin(self):
        mainwin = self.parent()
        while mainwin != None and mainwin.objectName() != "MainWindow":
            mainwin = mainwin.parent()
        return mainwin
    def closeEditor(self, editor, hint):
        mainwin = self.get_mainwin()
        saved_name = self.saved_name
        changed_name = editor.text()
        mainwin.change_ini_savedname(saved_name,changed_name)
        super().closeEditor(editor, hint)
    def mouseDoubleClickEvent(self, e):
        # 双击重命名
        mainwin = self.get_mainwin()
        cur_item = self.itemAt(e.pos())
        cur_item.setFlags(QtCore.Qt.ItemIsEditable|cur_item.flags())
        self.saved_name = cur_item.text()
        self.editItem(cur_item)
    def dropEvent(self, event):
        super().dropEvent(event)
        mainwin = self.get_mainwin()
        mainwin.refresh_listitem_spine()

