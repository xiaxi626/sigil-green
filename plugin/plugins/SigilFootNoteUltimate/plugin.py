#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os,re
from PyQt5 import QtCore, QtGui, QtWidgets
from utils.auto_amzn import AutoNotes
from utils.manual_regexp import RegExpNotes
from utils.manual_interlinear_notes import RegExpInterlinearNotes
import configparser
import MainUI

try:
    from os import startfile
except ImportError:
    from platform import system
    from subprocess import Popen

    platform_ = system()

    if platform_ == 'Linux':
        def startfile(path):
            'Open a file or directory (For Linux)'
            Popen(['xdg-open', path])
    elif platform_ == 'Darwin':
        def startfile(path):
            'Open a file or directory (For Mac OS X)'
            Popen(['open', path])
    else:
        raise NotImplementedError('此平台未能实现startfile：%s' % platform_)

#----------------------
#主体UI部分
#----------------------

AUTO_AMZN,MANUAL_REGEXP = 1,2
POS_ORI,POS_TAIL,POS_NEXT = 1,2,3

# TODO:接下来给特殊变量赋予内容

class MainWin(QtWidgets.QMainWindow):
    def __init__(self,dpi = 1.0):
        super().__init__()
        self.dpi = dpi
        self.ui = MainUI.Ui_MainWindow()
        self.ui.setupUi(self)
        self.initUi()
        self.initWidgets()
        self.initFunctions()
        self.initProperties()
        self.initConfigureObj()
        self.load_saved_ini(None)
        self.initSavedConfList()
        self.show()
    def initUi(self):
        width = int(430 * self.dpi)
        height = 550
        self.resize(width, height)
    def initProperties(self):
        self.isRun = False #　执行开关
        self.run_type = 0 # 注释识别类型
        self.pos_type = 0 # 注释插入位置
        self.ref_re = '' # 注标正则
        self.note_re = '' #　注释正则
        self.ref_tpl = '' # 注标模板
        self.note_tpl = '' # 注释模板
        self.foot_tpl = '' # 页尾节点模板
        self.check_loss = True # 自动识别检查遗漏
        self.var_mode = False # 正则表达式变量模式
        self.span_mode = False # 跨页模式
        self.noRef_mode = False # 无注标模式
    def initWidgets(self):
        #------------------------------------------------------------------
        # 这里把“变量传承模式”控件隐藏掉，其功能代码未删改。重启功能删除这句即可。
        #self.ui.var_mode_cbox.hide() 
        #------------------------------------------------------------------
        self.setWindowIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__),'plugin.png')))
        self.ui.tabWidget.setCurrentIndex(0)
        self.tabBarWidget_1 = self.ui.tabWidget.widget(1)
        self.tabBarWidget_2 = self.ui.tabWidget.widget(2)
        self.ui.tabWidget.removeTab(2)

    def initFunctions(self):
        self.ui.comfirm_pbtn.clicked.connect(self.run)
        self.ui.cancel_pbtn.clicked.connect(self.close)
        self.ui.save_pbtn.clicked.connect(lambda x:self.save_ini(1))
        self.ui.readme_pbtn.clicked.connect(self.readme)
        #按钮组1 self.ui.regexp_rbtn 和 self.ui.auto_rbtn
        self.ui.buttonGroup_runtype.buttonClicked[int].connect(lambda x:self.switch(1))
        #按钮组2 self.ui.subpos_default_rbtn、self.ui.subpos_end_rbtn、self.ui.subpos_noteref_rbtn
        self.ui.buttonGroup_subpos.buttonClicked[int].connect(lambda x:self.switch(2))
        self.ui.noRef_mode_cbox.stateChanged.connect(lambda x:self.switch(3))

    def switch(self,sender):

        if sender == 1: 
            if self.ui.amzn_rbtn.isChecked():
                self.ui.check_loss_cbox.setEnabled(True)
            else:
                self.ui.check_loss_cbox.setEnabled(False)
            self.change_tabVisible_by_runType()
        elif sender == 2: 
            self.disable_footTemplate_by_subpos()
        elif sender == 3:
            self.set_noRefCbox_ui()

    def initConfigureObj(self):
        curdir = os.path.dirname(os.path.realpath(__file__))
        self.cfgpath = os.path.join(curdir,'config.ini')
        self.conf = configparser.ConfigParser()
        if os.path.exists(self.cfgpath):
            self.conf.read(self.cfgpath, encoding="utf-8")
        
    def write_ini(self):
        with open(self.cfgpath,'w',encoding='utf-8') as cf:
            self.conf.write(cf)

    def initSettings(self):
        
        if self.run_type == AUTO_AMZN:
            self.ui.amzn_rbtn.setChecked(True)
        elif self.run_type == MANUAL_REGEXP:
            self.ui.regexp_rbtn.setChecked(True)
        if self.pos_type == POS_ORI:
            self.ui.subpos_default_rbtn.setChecked(True)
        elif self.pos_type == POS_TAIL:
            self.ui.subpos_end_rbtn.setChecked(True)
        elif self.pos_type == POS_NEXT:
            self.ui.subpos_noteref_rbtn.setChecked(True)
        
        if self.check_loss == True:
            self.ui.check_loss_cbox.setChecked(True)
        else:
            self.ui.check_loss_cbox.setChecked(False)

        if self.var_mode == True:
            self.ui.var_mode_cbox.setChecked(True)
        else:
            self.ui.var_mode_cbox.setChecked(False)

        if self.span_mode == True:
            self.ui.span_mode_cbox.setChecked(True)
        else:
            self.ui.span_mode_cbox.setChecked(False)

        if self.noRef_mode == True:
            self.ui.noRef_mode_cbox.setChecked(True)
        else:
            self.ui.noRef_mode_cbox.setChecked(False)

        self.change_tabVisible_by_runType()
        self.disable_footTemplate_by_subpos()
        if not self.ui.amzn_rbtn.isChecked():
            self.ui.check_loss_cbox.setEnabled(False)
        else:
            self.ui.check_loss_cbox.setEnabled(True)
        
    def initSavedConfList(self):
        try:
            listitem_spine = self.conf.get('listitem','spine').split(',')
        except:
            return
        if listitem_spine == [""]:
            return
        for item_text in listitem_spine:
            self.ui.saved_conf.addConfItem(item_text)
    
    def refresh_listitem_spine(self):
        self.conf.set("listitem","spine",','.join(self.ui.saved_conf.getAllItemsText()))

    def del_ini_savedsection(self,saved_name):
        conf = self.conf
        for section in conf.sections():
            if section.startswith("saved_") and conf.get(section,"saved_name") == saved_name:
                break
        conf.remove_section(section)
        self.refresh_listitem_spine()
        
    def change_ini_savedname(self,saved_name,changed_name):
        conf = self.conf
        for section in conf.sections():
            if section.startswith("saved_") and conf.get(section,"saved_name") == saved_name:
                break
        conf.set(section,"saved_name",changed_name)
        self.refresh_listitem_spine()


    def load_saved_ini(self,saved_name):
        conf = self.conf
        if not os.path.exists(self.cfgpath):
            self.run_type = AUTO_AMZN
            self.pos_type = POS_TAIL
            self.check_loss = True
            self.var_mode = False
            self.span_mode = False
            self.noRef_mode = False
        else:

            default_value = {
                'run_type':AUTO_AMZN,
                'pos_type':POS_TAIL,
                'check_loss':"1",
                'var_mode':"0",
                'span_mode':"0",
                'noref_mode':"0"
            }
            # 获取section
            if saved_name is None:
                section = "settings"
            else:
                for section in conf.sections():
                    if section.startswith("saved_") and conf[section].get("saved_name") == saved_name:
                        break
            # 开始配置
            try:
                self.run_type = int(conf.get(section,"run_type"))
            except:
                self.run_type = AUTO_AMZN
            try:
                self.pos_type = int(conf.get(section,"pos_type"))
            except:
                self.pos_type = POS_TAIL
            try:
                var_mode = conf.get(section,"var_mode")
                self.var_mode = True if var_mode == "1" else False
            except:
                self.var_mode = False
            try:
                span_mode = conf.get(section,"span_mode")
                self.span_mode = True if span_mode == "1" else False
            except:
                self.span_mode = False
            try:
                noRef_mode = conf.get(section,"noref_mode")
                self.noRef_mode = True if noRef_mode == "1" else False
            except:
                self.noRef_mode = False
            try:
                check_loss = conf.get(section,"check_loss")
                self.check_loss = True if check_loss == "1" else False
            except:
                self.check_loss = True
            try:
                self.ref_re = conf.get(section,"noteref")
                self.note_re = conf.get(section,"footnote")
                self.ui.regexp_noteref_le.setText(self.ref_re)
                self.ui.regexp_footnote_le.setText(self.note_re)
            except:
                self.ref_re = ""
                self.note_re = ""

            try:
                ref_tpl_auto = linebreak_turn(conf.get(section,'ref_template_auto'),'r')
                self.ui.noteref_te_auto.setPlainText(ref_tpl_auto)
                note_tpl_auto = linebreak_turn(conf.get(section,'note_template_auto'),'r')
                self.ui.note_te_auto.setPlainText(note_tpl_auto)
                foot_tpl_auto = linebreak_turn(conf.get(section,'foot_template_auto'),'r')
                self.ui.foot_te_auto.setPlainText(foot_tpl_auto)
                ref_tpl_man = linebreak_turn(conf.get(section,'ref_template_man'),'r')
                self.ui.noteref_te_man.setPlainText(ref_tpl_man)
                note_tpl_man = linebreak_turn(conf.get(section,'note_template_man'),'r')
                self.ui.note_te_man.setPlainText(note_tpl_man)
                foot_tpl_man = linebreak_turn(conf.get(section,'foot_template_man'),'r')
                self.ui.foot_te_man.setPlainText(foot_tpl_man)
            except:
                pass

        self.initSettings()

    def save_ini(self,sendor,saved_name=None):
        # sendor : 1 来自按钮 2 来自右键菜单
        self.get_settings()
        self.ref_re = self.ui.regexp_noteref_le.text()
        self.note_re = self.ui.regexp_footnote_le.text()
        ref_tpl_auto = linebreak_turn(self.ui.noteref_te_auto.toPlainText(),'t')
        note_tpl_auto = linebreak_turn(self.ui.note_te_auto.toPlainText(),'t')
        foot_tpl_auto = linebreak_turn(self.ui.foot_te_auto.toPlainText(),'t')
        ref_tpl_man = linebreak_turn(self.ui.noteref_te_man.toPlainText(),'t')
        note_tpl_man = linebreak_turn(self.ui.note_te_man.toPlainText(),'t')
        foot_tpl_man = linebreak_turn(self.ui.foot_te_man.toPlainText(),'t')

        conf = self.conf
        conf.remove_section("regexp")
        conf.remove_section("template")

        for section in ["settings","listitem"]:
            try:
                conf.add_section(section)
            except:
                pass
        

        conf["settings"] = {
            "run_type": str(self.run_type),
            "pos_type": str(self.pos_type),
            "check_loss": '1' if self.check_loss else '0',
            "var_mode": '1' if self.var_mode else '0',
            "span_mode": '1' if self.span_mode else '0',
            "noref_mode": "1" if self.noRef_mode else "0",
            "noteref": self.ref_re,
            "footnote": self.note_re,
            "ref_template_auto": ref_tpl_auto,
            "note_template_auto": note_tpl_auto,
            "foot_template_auto": foot_tpl_auto,
            "ref_template_man": ref_tpl_man,
            "note_template_man": note_tpl_man,
            "foot_template_man": foot_tpl_man
        }
        if sendor == 2: #来自右键菜单
            if saved_name is None: # 保存为新配置
                isAddItem = True
                i = 1
                while "saved_%d"%i in conf.sections():
                    i += 1
                saved_section = "saved_%d"%i
                saved_name = "新建配置 %d"%i
                conf.add_section(saved_section)
            else: # 覆盖保存
                isAddItem = False
                for sec in conf.sections():
                    if not sec.startswith("saved_"):
                        continue
                    if conf.get(sec,"saved_name") == saved_name:
                        saved_section = sec
                        break
            conf[saved_section]["saved_name"] = saved_name
            for key,value  in conf["settings"].items():
                conf[saved_section][key] = value
            if isAddItem:
                self.ui.saved_conf.addConfItem(saved_name)
                self.refresh_listitem_spine()

    def get_settings(self):
        if self.ui.amzn_rbtn.isChecked():
            self.run_type = AUTO_AMZN
        elif self.ui.regexp_rbtn.isChecked():
            self.run_type = MANUAL_REGEXP
        if self.ui.subpos_default_rbtn.isChecked():
            self.pos_type = POS_ORI
        elif self.ui.subpos_end_rbtn.isChecked():
            self.pos_type = POS_TAIL
        elif self.ui.subpos_noteref_rbtn.isChecked():
            self.pos_type = POS_NEXT
        self.check_loss = self.ui.check_loss_cbox.isChecked()
        self.var_mode = self.ui.var_mode_cbox.isChecked()
        self.span_mode = self.ui.span_mode_cbox.isChecked()
        self.noRef_mode = self.ui.noRef_mode_cbox.isChecked()
    def check_regexp_format(self):
        self.ref_re = self.ui.regexp_noteref_le.text()
        self.note_re = self.ui.regexp_footnote_le.text()
        ref_cre = re.compile(self.ref_re)
        if ref_cre.groups == 0:
            QtWidgets.QMessageBox.information(self,'警告','你已开启注标捕获组传承模式，注标表达式必须设置捕获组！')
            return False
        group = 0
        for order in range(1,ref_cre.groups+1):
            if '{%d}'%order in self.note_re:
                group += 1
        for gname in ref_cre.groupindex:
            if '{%s}'%gname in self.note_re:
                group += 1
        if group == 0:
            QtWidgets.QMessageBox.information(self,'警告','你已开启注标捕获组传承模式，但注释表达式没有设置合适的占位符！')
            return False
        return True

    def set_noRefCbox_ui(self):
        if self.ui.noRef_mode_cbox.isChecked():
            self.ui.var_mode_cbox.setEnabled(False)
            self.ui.span_mode_cbox.setEnabled(False)
            self.ui.regexp_noteref_lbl.setEnabled(False)
            self.ui.regexp_noteref_le.setEnabled(False)
        else:
            self.ui.var_mode_cbox.setEnabled(True)
            self.ui.span_mode_cbox.setEnabled(True)
            self.ui.regexp_noteref_lbl.setEnabled(True)
            self.ui.regexp_noteref_le.setEnabled(True)

    def change_tabVisible_by_runType(self):
        for w in [self.ui.regexp_noteref_lbl,
                self.ui.regexp_footnote_lbl,
                self.ui.regexp_noteref_le,
                self.ui.regexp_footnote_le,
                self.ui.var_mode_cbox,
                self.ui.span_mode_cbox,
                self.ui.noRef_mode_cbox]:
            if self.ui.regexp_rbtn.isChecked():
                w.setEnabled(True)
            else:
                w.setEnabled(False)
        
        if self.ui.regexp_rbtn.isChecked():
            self.set_noRefCbox_ui()

        if self.ui.amzn_rbtn.isChecked():
            self.ui.tabWidget.removeTab(1)
            self.ui.tabWidget.addTab(self.tabBarWidget_1, QtGui.QIcon(), "替换模板【自动识别】")
            #self.ui.tabWidget.setTabVisible(2, False)
            #self.ui.tabWidget.setTabVisible(1, True)
        elif self.ui.regexp_rbtn.isChecked():
            self.ui.tabWidget.removeTab(1)
            self.ui.tabWidget.addTab(self.tabBarWidget_2, QtGui.QIcon(), "替换模板【手动识别】")
            #self.ui.tabWidget.setTabVisible(1, False)
            #self.ui.tabWidget.setTabVisible(2, True)

    def disable_footTemplate_by_subpos(self):
        if self.ui.subpos_end_rbtn.isChecked():
            self.ui.foot_te_auto.setEnabled(True)
            self.ui.foot_te_man.setEnabled(True)
            self.ui.foot_te_auto.open_highlighter()
            self.ui.foot_te_man.open_highlighter()
            self.ui.tailnode1_lbl.setEnabled(True)
            self.ui.tailnode2_lbl.setEnabled(True)
        else:
            self.ui.foot_te_auto.setEnabled(False)
            self.ui.foot_te_man.setEnabled(False)
            self.ui.foot_te_auto.close_highlighter()
            self.ui.foot_te_man.close_highlighter()
            self.ui.tailnode1_lbl.setEnabled(False)
            self.ui.tailnode2_lbl.setEnabled(False)

    def readme(self):
        template_path = os.path.join(os.path.dirname(__file__),'readme.doc')
        startfile(template_path)

    def closeEvent(self, a0):
        self.write_ini()
        super().closeEvent(a0)

    def run(self):
        self.get_settings()
        if self.run_type == MANUAL_REGEXP and self.var_mode == True:
            format_check = self.check_regexp_format()
            if format_check is not True:
                return
        self.ref_re = self.ui.regexp_noteref_le.text()
        self.note_re = self.ui.regexp_footnote_le.text()
        if self.run_type == AUTO_AMZN:
            self.ref_tpl = self.ui.noteref_te_auto.getText()
            self.note_tpl = self.ui.note_te_auto.getText()
            self.foot_tpl = self.ui.foot_te_auto.getText()
            self.check_loss = self.ui.check_loss_cbox.isChecked()
        elif self.run_type == MANUAL_REGEXP:
            self.ref_tpl = self.ui.noteref_te_man.getText()
            self.note_tpl = self.ui.note_te_man.getText()
            self.foot_tpl = self.ui.foot_te_man.getText()
        self.isRun = True
        self.close()

def read_log(bk):
    try:
        log = bk.readfile('Log_by_SigilFootNoteUltimate')
        log = str(log,encoding='utf-8')
        match_ = re.match(r'数字变量起始值 *(\d+)\n+',log)
        count = int(match_.group(1))
        log = log[match_.end():]
    except:
        log = ''
        count = 0
    return log,count
    
def get_config_path():
    curdir = os.path.dirname(os.path.realpath(__file__))
    cfgpath = os.path.join(curdir,'config.ini')
    return cfgpath

def linebreak_turn(string,mode="t"):
    new_string = ""
    if mode == 't':
        new_string = re.sub(r'\n',r'\\n',string)
    elif mode == 'r':
        new_string = re.sub(r'\\n',r'\n',string)
    else:
        new_string = string
    return new_string

def run(bk):
    #scaleRate = QtWidgets.QApplication(sys.argv).screens()[0].logicalDotsPerInch()/96


    app = QtWidgets.QApplication(sys.argv)
    dpi = app.screens()[0].logicalDotsPerInch()/96
    win = MainWin(dpi)
    app.exec_()

    log,count = read_log(bk)
    log_ = ''

    if win.isRun == True:
        if win.run_type == AUTO_AMZN:
            log_,count = AutoNotes(
                bk,
                pos_type = win.pos_type,
                check_loss = win.check_loss,
                ref_tpl = win.ref_tpl,
                note_tpl = win.note_tpl,
                foot_tpl = win.foot_tpl,
                count = count
            ).run()
        elif win.run_type == MANUAL_REGEXP:
            if win.noRef_mode == False:
                log_,count = RegExpNotes(
                    bk,
                    pos_type = win.pos_type,
                    var_mode = win.var_mode,
                    span_mode = win.span_mode,
                    re_f = win.ref_re,
                    re_s = win.note_re,
                    ref_tpl = win.ref_tpl,
                    note_tpl = win.note_tpl,
                    foot_tpl = win.foot_tpl,
                    count = count
                ).run()
            elif win.noRef_mode == True:
                log_,count = RegExpInterlinearNotes(
                    bk,
                    pos_type = win.pos_type,
                    re_f = win.note_re,
                    ref_tpl = win.ref_tpl,
                    note_tpl = win.note_tpl,
                    foot_tpl = win.foot_tpl,
                    count = count
                    ).run()

    log = log + log_
    log = '数字变量起始值 %d\n\n'%count + log
    if count > 0:
        try:
            bk.addfile('Log_by_SigilFootNoteUltimate', 'Log_by_SigilFootNoteUltimate.txt', log, 'text/plain')
        except:
            bk.writefile('Log_by_SigilFootNoteUltimate', log)

    return 0

if __name__ == "__main__":
    from utils.epubtools import EpubWrapper
    bk = EpubWrapper.EpubBook('test.epub')
    run(bk)
    bk.save_as('test_.epub')