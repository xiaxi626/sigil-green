# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(460, 550)
        MainWindow.setWindowTitle("epub注释处理")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_1)
        self.verticalLayout_5.setSpacing(18)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.auto_gbox = QtWidgets.QGroupBox(self.tab_1)
        self.auto_gbox.setMinimumSize(QtCore.QSize(0, 90))
        self.auto_gbox.setMaximumSize(QtCore.QSize(16777215, 90))
        self.auto_gbox.setTitle("自动识别")
        self.auto_gbox.setObjectName("auto_gbox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.auto_gbox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.amzn_rbtn = QtWidgets.QRadioButton(self.auto_gbox)
        self.amzn_rbtn.setText("自动识别带跳转链接的注释")
        self.amzn_rbtn.setObjectName("amzn_rbtn")
        self.buttonGroup_runtype = QtWidgets.QButtonGroup(MainWindow)
        self.buttonGroup_runtype.setObjectName("buttonGroup_runtype")
        self.buttonGroup_runtype.addButton(self.amzn_rbtn)
        self.horizontalLayout_2.addWidget(self.amzn_rbtn)
        self.check_loss_cbox = QtWidgets.QCheckBox(self.auto_gbox)
        self.check_loss_cbox.setChecked(True)
        self.check_loss_cbox.setObjectName("check_loss_cbox")
        self.horizontalLayout_2.addWidget(self.check_loss_cbox)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.verticalLayout_5.addWidget(self.auto_gbox)
        self.manual_gbox = QtWidgets.QGroupBox(self.tab_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.manual_gbox.sizePolicy().hasHeightForWidth())
        self.manual_gbox.setSizePolicy(sizePolicy)
        self.manual_gbox.setTitle("手动识别")
        self.manual_gbox.setObjectName("manual_gbox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.manual_gbox)
        self.verticalLayout_3.setContentsMargins(-1, 12, -1, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(7)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.regexp_rbtn = QtWidgets.QRadioButton(self.manual_gbox)
        self.regexp_rbtn.setText("正则表达式搜索")
        self.regexp_rbtn.setObjectName("regexp_rbtn")
        self.buttonGroup_runtype.addButton(self.regexp_rbtn)
        self.horizontalLayout_5.addWidget(self.regexp_rbtn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.noRef_mode_cbox = QtWidgets.QCheckBox(self.manual_gbox)
        self.noRef_mode_cbox.setObjectName("noRef_mode_cbox")
        self.horizontalLayout_5.addWidget(self.noRef_mode_cbox)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setContentsMargins(-1, 2, -1, 5)
        self.formLayout.setHorizontalSpacing(6)
        self.formLayout.setVerticalSpacing(8)
        self.formLayout.setObjectName("formLayout")
        self.regexp_noteref_lbl = QtWidgets.QLabel(self.manual_gbox)
        self.regexp_noteref_lbl.setText("注标 NoteRef")
        self.regexp_noteref_lbl.setObjectName("regexp_noteref_lbl")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.regexp_noteref_lbl)
        self.regexp_noteref_le = QtWidgets.QLineEdit(self.manual_gbox)
        self.regexp_noteref_le.setText("")
        self.regexp_noteref_le.setObjectName("regexp_noteref_le")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.regexp_noteref_le)
        self.regexp_footnote_lbl = QtWidgets.QLabel(self.manual_gbox)
        self.regexp_footnote_lbl.setText("注释 Footnote")
        self.regexp_footnote_lbl.setObjectName("regexp_footnote_lbl")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.regexp_footnote_lbl)
        self.regexp_footnote_le = QtWidgets.QLineEdit(self.manual_gbox)
        self.regexp_footnote_le.setText("")
        self.regexp_footnote_le.setObjectName("regexp_footnote_le")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.regexp_footnote_le)
        self.verticalLayout_3.addLayout(self.formLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.var_mode_cbox = QtWidgets.QCheckBox(self.manual_gbox)
        self.var_mode_cbox.setEnabled(True)
        self.var_mode_cbox.setObjectName("var_mode_cbox")
        self.horizontalLayout_3.addWidget(self.var_mode_cbox)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.span_mode_cbox = QtWidgets.QCheckBox(self.manual_gbox)
        self.span_mode_cbox.setEnabled(True)
        self.span_mode_cbox.setObjectName("span_mode_cbox")
        self.horizontalLayout_3.addWidget(self.span_mode_cbox)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.verticalLayout_5.addWidget(self.manual_gbox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.subpos_gbox = QtWidgets.QGroupBox(self.tab_1)
        self.subpos_gbox.setTitle("注释替换位置")
        self.subpos_gbox.setObjectName("subpos_gbox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.subpos_gbox)
        self.verticalLayout_2.setSpacing(8)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.subpos_default_rbtn = QtWidgets.QRadioButton(self.subpos_gbox)
        self.subpos_default_rbtn.setText("原文位置")
        self.subpos_default_rbtn.setObjectName("subpos_default_rbtn")
        self.buttonGroup_subpos = QtWidgets.QButtonGroup(MainWindow)
        self.buttonGroup_subpos.setObjectName("buttonGroup_subpos")
        self.buttonGroup_subpos.addButton(self.subpos_default_rbtn)
        self.verticalLayout_2.addWidget(self.subpos_default_rbtn)
        self.subpos_end_rbtn = QtWidgets.QRadioButton(self.subpos_gbox)
        self.subpos_end_rbtn.setText("注释移到页面末尾")
        self.subpos_end_rbtn.setObjectName("subpos_end_rbtn")
        self.buttonGroup_subpos.addButton(self.subpos_end_rbtn)
        self.verticalLayout_2.addWidget(self.subpos_end_rbtn)
        self.subpos_noteref_rbtn = QtWidgets.QRadioButton(self.subpos_gbox)
        self.subpos_noteref_rbtn.setText("注释插入到注标所在下一段")
        self.subpos_noteref_rbtn.setObjectName("subpos_noteref_rbtn")
        self.buttonGroup_subpos.addButton(self.subpos_noteref_rbtn)
        self.verticalLayout_2.addWidget(self.subpos_noteref_rbtn)
        self.horizontalLayout.addWidget(self.subpos_gbox)
        self.groupBox = SavedConfGroupBox(self.tab_1)
        self.groupBox.setTitle("配置模板")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_10.setSpacing(8)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.saved_conf = SavedConfListWidget(self.groupBox)
        self.saved_conf.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.saved_conf.setDragEnabled(True)
        self.saved_conf.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.saved_conf.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.saved_conf.setObjectName("saved_conf")
        self.verticalLayout_10.addWidget(self.saved_conf)
        self.horizontalLayout.addWidget(self.groupBox)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_6.setContentsMargins(15, -1, 15, -1)
        self.verticalLayout_6.setSpacing(6)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_7 = QtWidgets.QLabel(self.tab_2)
        self.label_7.setStyleSheet("")
        self.label_7.setText("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:6px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:120%;\"><span style=\" color:#333341;\">　　注释替换模板本质是一段可加入特殊变量的替换字符串，建议按照HTML语法来写，以免替换后破坏页面的HTML结构。</span></p>\n"
"<p style=\" margin-top:6px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:130%;\"><span style=\" font-weight:600; color:#333341;\">特殊变量<br /></span><span style=\" color:#0000ff;\">[href] </span><span style=\" color:#333341;\">自动分配链接 </span><span style=\" color:#0000ff;\">[ref]  </span><span style=\" color:#333341;\">去标签注标内容 </span><span style=\" color:#0000ff;\">[pos] </span><span style=\" color:#333341;\">页尾节点标记<br /></span><span style=\" color:#0000ff;\">[id]   </span><span style=\" color:#333341;\">自动分配ID   </span><span style=\" color:#0000ff;\">[note]</span><span style=\" color:#333341;\"> 去标签注释内容 </span><span style=\" color:#0000ff;\">[num] </span><span style=\" color:#333341;\">计数器</span></p></body></html>")
        self.label_7.setTextFormat(QtCore.Qt.RichText)
        self.label_7.setWordWrap(True)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_6.addWidget(self.label_7)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setSpacing(6)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_8 = QtWidgets.QLabel(self.tab_2)
        self.label_8.setText("注标模板")
        self.label_8.setObjectName("label_8")
        self.verticalLayout_8.addWidget(self.label_8, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)
        self.noteref_te_auto = TemplateEdit_A(self.tab_2)
        self.noteref_te_auto.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.noteref_te_auto.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&lt;!-- 注标示例模板 --&gt;</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&lt;sup&gt;&lt;a class=&quot;duokan-footnote&quot; href=&quot;[href]&quot; id=&quot;[id]&quot;&gt;&lt;img src=&quot;../Images/note.png&quot;/&gt;&lt;/a&gt;&lt;/sup&gt;</p></body></html>")
        self.noteref_te_auto.setTabStopWidth(18)
        self.noteref_te_auto.setAcceptRichText(False)
        self.noteref_te_auto.setObjectName("noteref_te_auto")
        self.verticalLayout_8.addWidget(self.noteref_te_auto)
        self.label_9 = QtWidgets.QLabel(self.tab_2)
        self.label_9.setText("注释模板")
        self.label_9.setObjectName("label_9")
        self.verticalLayout_8.addWidget(self.label_9, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)
        self.note_te_auto = TemplateEdit_A(self.tab_2)
        self.note_te_auto.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.note_te_auto.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&lt;!-- 注释示例模板 --&gt;</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&lt;li class=&quot;duokan-footnote-item&quot; id=&quot;[id]&quot;&gt;</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    &lt;a href=&quot;[href]&quot;&gt;[note]&lt;/a&gt;</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&lt;/li&gt;</p></body></html>")
        self.note_te_auto.setTabStopWidth(18)
        self.note_te_auto.setAcceptRichText(False)
        self.note_te_auto.setObjectName("note_te_auto")
        self.verticalLayout_8.addWidget(self.note_te_auto)
        self.tailnode1_lbl = QtWidgets.QLabel(self.tab_2)
        self.tailnode1_lbl.setText("页尾节点模板")
        self.tailnode1_lbl.setObjectName("tailnode1_lbl")
        self.verticalLayout_8.addWidget(self.tailnode1_lbl, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)
        self.foot_te_auto = TemplateEdit_C(self.tab_2)
        self.foot_te_auto.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.foot_te_auto.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&lt;!-- 此模板可忽略不填，填写时必须带[pos]变量。 --&gt;</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&lt;hr class=&quot;footnote&quot;/&gt;</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&lt;ol class=&quot;duokan-footnote-content&quot;&gt;</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    [pos]</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&lt;/ol&gt;</p></body></html>")
        self.foot_te_auto.setTabStopWidth(18)
        self.foot_te_auto.setAcceptRichText(False)
        self.foot_te_auto.setObjectName("foot_te_auto")
        self.verticalLayout_8.addWidget(self.foot_te_auto)
        self.verticalLayout_6.addLayout(self.verticalLayout_8)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.tab_3)
        self.verticalLayout_7.setContentsMargins(15, -1, 15, -1)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_11 = QtWidgets.QLabel(self.tab_3)
        self.label_11.setStyleSheet("")
        self.label_11.setText("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:6px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:120%;\"><span style=\" color:#333341;\">　　注释替换模板本质是一段可加入特殊变量的替换字符串，建议按照HTML语法来写，以免替换后破坏页面的HTML结构。</span></p>\n"
"<p style=\" margin-top:6px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:130%;\"><span style=\" font-weight:600; color:#333341;\">特殊变量<br /></span><span style=\" color:#0000ff;\">[href] </span><span style=\" color:#333341;\">自动分配链接  </span><span style=\" color:#0000ff;\">[r1]-[r9] </span><span style=\" color:#333341;\">注标捕获组  </span><span style=\" color:#0000ff;\">[pos]</span><span style=\" color:#333341;\"> 页尾节点标记<br /></span><span style=\" color:#0000ff;\">[id]   </span><span style=\" color:#333341;\">自动分配ID    </span><span style=\" color:#0000ff;\">[n1]-[n9] </span><span style=\" color:#333341;\">注释捕获组  </span><span style=\" color:#0000ff;\">[num] </span><span style=\" color:#333341;\">计数器</span></p></body></html>")
        self.label_11.setTextFormat(QtCore.Qt.RichText)
        self.label_11.setWordWrap(True)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_7.addWidget(self.label_11)
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setSpacing(6)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label_18 = QtWidgets.QLabel(self.tab_3)
        self.label_18.setText("注标模板")
        self.label_18.setObjectName("label_18")
        self.verticalLayout_11.addWidget(self.label_18, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)
        self.noteref_te_man = TemplateEdit_B(self.tab_3)
        self.noteref_te_man.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.noteref_te_man.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&lt;!-- 注标示例模板 --&gt;</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&lt;sup&gt;&lt;a class=&quot;duokan-footnote&quot; href=&quot;[href]&quot; id=&quot;[id]&quot;&gt;&lt;img src=&quot;../Images/note.png&quot;/&gt;&lt;/a&gt;&lt;/sup&gt;</p></body></html>")
        self.noteref_te_man.setTabStopWidth(18)
        self.noteref_te_man.setAcceptRichText(False)
        self.noteref_te_man.setObjectName("noteref_te_man")
        self.verticalLayout_11.addWidget(self.noteref_te_man)
        self.label_19 = QtWidgets.QLabel(self.tab_3)
        self.label_19.setText("注释模板")
        self.label_19.setObjectName("label_19")
        self.verticalLayout_11.addWidget(self.label_19, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)
        self.note_te_man = TemplateEdit_B(self.tab_3)
        self.note_te_man.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.note_te_man.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&lt;!-- 注释示例模板 --&gt;</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&lt;li class=&quot;duokan-footnote-item&quot; id=&quot;[id]&quot;&gt;</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    &lt;a href=&quot;[href]&quot;&gt;[r1]&lt;/a&gt; [n1]</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&lt;/li&gt;</p></body></html>")
        self.note_te_man.setTabStopWidth(18)
        self.note_te_man.setAcceptRichText(False)
        self.note_te_man.setObjectName("note_te_man")
        self.verticalLayout_11.addWidget(self.note_te_man)
        self.tailnode2_lbl = QtWidgets.QLabel(self.tab_3)
        self.tailnode2_lbl.setText("页尾节点模板")
        self.tailnode2_lbl.setObjectName("tailnode2_lbl")
        self.verticalLayout_11.addWidget(self.tailnode2_lbl, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)
        self.foot_te_man = TemplateEdit_C(self.tab_3)
        self.foot_te_man.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.foot_te_man.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&lt;!-- 此模板可忽略不填，填写时必须带[pos]变量。 --&gt;</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&lt;hr class=&quot;footnote&quot;/&gt;</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&lt;ol class=&quot;duokan-footnote-content&quot;&gt;</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    [pos]</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&lt;/ol&gt;</p></body></html>")
        self.foot_te_man.setTabStopWidth(18)
        self.foot_te_man.setAcceptRichText(False)
        self.foot_te_man.setObjectName("foot_te_man")
        self.verticalLayout_11.addWidget(self.foot_te_man)
        self.verticalLayout_7.addLayout(self.verticalLayout_11)
        self.tabWidget.addTab(self.tab_3, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.readme_pbtn = QtWidgets.QPushButton(self.centralwidget)
        self.readme_pbtn.setMinimumSize(QtCore.QSize(55, 30))
        self.readme_pbtn.setMaximumSize(QtCore.QSize(55, 16777215))
        self.readme_pbtn.setText("说明")
        self.readme_pbtn.setObjectName("readme_pbtn")
        self.horizontalLayout_4.addWidget(self.readme_pbtn)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.comfirm_pbtn = QtWidgets.QPushButton(self.centralwidget)
        self.comfirm_pbtn.setMinimumSize(QtCore.QSize(0, 30))
        self.comfirm_pbtn.setText("执行")
        self.comfirm_pbtn.setObjectName("comfirm_pbtn")
        self.horizontalLayout_4.addWidget(self.comfirm_pbtn)
        self.save_pbtn = QtWidgets.QPushButton(self.centralwidget)
        self.save_pbtn.setMinimumSize(QtCore.QSize(0, 30))
        self.save_pbtn.setText("保存")
        self.save_pbtn.setObjectName("save_pbtn")
        self.horizontalLayout_4.addWidget(self.save_pbtn)
        self.cancel_pbtn = QtWidgets.QPushButton(self.centralwidget)
        self.cancel_pbtn.setMinimumSize(QtCore.QSize(0, 30))
        self.cancel_pbtn.setObjectName("cancel_pbtn")
        self.horizontalLayout_4.addWidget(self.cancel_pbtn)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.regexp_noteref_lbl.setBuddy(self.regexp_noteref_le)
        self.regexp_footnote_lbl.setBuddy(self.regexp_footnote_le)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.check_loss_cbox.setText(_translate("MainWindow", "检查遗漏"))
        self.noRef_mode_cbox.setText(_translate("MainWindow", "无注标"))
        self.var_mode_cbox.setText(_translate("MainWindow", "注标捕获组传承给注释表达式"))
        self.span_mode_cbox.setText(_translate("MainWindow", "跨页注释"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("MainWindow", "功能设置"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "替换模板【自动识别】"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "替换模板【手动识别】"))
        self.cancel_pbtn.setText(_translate("MainWindow", "退出"))
from CustomClass import SavedConfGroupBox, SavedConfListWidget, TemplateEdit_A, TemplateEdit_B, TemplateEdit_C
