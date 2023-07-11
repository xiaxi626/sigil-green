#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os,math,time,shutil,traceback,zipfile
from utils.compress import SUBPROCESS, ImagesProcess,TEMPDIR
from utils.posprocess import LOG,size_f,PosProcess
import MainUI
from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import Image


MH = 600                    # Main Height
Pr_W = int(MH * 0.95)       # Progress Width
Pr_H = int(Pr_W / 4.2)      # Progress Height
Font = QtGui.QFont('SimSun',12)

#----------------------
#寻找图片路径
#----------------------
def walk_pics(top):    
    pics = []
    for root,dirs,files in os.walk(top,topdown=True): # topdown = True 遍历子目录
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext.lower() in ['.jpg','.jpeg','.png','.bmp','.webp']:
                pic_path = os.path.join(root,file)
                try:
                    with Image.open(pic_path) as img:
                        fmt = img.format
                except:
                    print('！！！文件错误： "%s" 为无效图片，程序将忽略该文件'%pic_path)
                else:
                    pics.append((pic_path,fmt))
    return pics #返回一个图片路径列表

#----------------------
#进度条UI部分
#----------------------

class Progress(QtWidgets.QWidget):
    def __init__(self,parent = None):
        super().__init__()
        self.parent_ = parent
        self.initUI()
        self.center()
    def initUI(self):

        self.setFixedSize(Pr_W,Pr_H)
        self.setWindowTitle('  ')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/plugin.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.setFont(Font)

        tip = QtWidgets.QLabel('图片正在处理中，请等待……')
        tip.setFixedSize(int(Pr_W*1),int(Pr_H*0.2))
        tip.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.pbar = pbar = QtWidgets.QProgressBar()
        pbar.setFixedHeight(int(Pr_H*0.26))
        pbar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        pbar.setValue(0)
        
        cancel = QtWidgets.QPushButton('取消')
        cancel.clicked.connect(QtCore.QCoreApplication.instance().quit)
        cancel.setFixedSize(int(Pr_W*0.18),int(Pr_H*0.23))
        layout = QtWidgets.QVBoxLayout()
        layout_ = QtWidgets.QHBoxLayout()
        layout_.addStretch(1)
        layout_.addWidget(cancel)

        for obj in [tip,1,pbar,1,layout_]:
            if type(obj).__name__ in ('QHBoxLayout','QVBoxLayout','QGridLayout'):
                layout.addLayout(obj)
            elif type(obj).__name__ == 'int':
                layout.addStretch(obj)
            else:
                layout.addWidget(obj)
        self.setLayout(layout)
    def update_value(self,step):
        self.pbar.setValue(step)
    def center(self):
        qr = self.frameGeometry() 
        cp = QtWidgets.QDesktopWidget().availableGeometry().center() #获得屏幕中心点
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def parent(self):
        return self.parent_

#----------------------
#主体UI部分
#----------------------

class MainWin(QtWidgets.QMainWindow):
    def __init__(self,bk=None):
        super().__init__()
        if bk is not None and type(bk) is not str:
            root = bk._w.ebook_root
        elif type(bk) is str:
            root = bk
        else:
            root = None

        self.ui = MainUI.Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_widget()
        self.initFunc()
        self.prothread = None
        self.qss = '''
            #PicsList {min-height:43em;}
            #PicsList::Item:hover{background:#CCE8FF;}
            #PicsList::Item:selected{background:#81bff1;}'''
        self.qss2 = self.qss + "\n#PicsList { border-image:url(':/background/background.svg'); background-color:white }"
        self.setStyleSheet(self.qss)
        if root is None:
            self.ui.PicsList.setStyleSheet(self.qss2) 
        self.show()
        self.initPictures(root)
    
    def initPictures(self,root=None):
        if root is not None:
            self.ui.PicsList.setStyleSheet(self.qss)
        self.initPicThread = WalkPicsThread(self,root)
        self.initPicThread.start()

    def initFunc(self):
        self.ui.format_conv_cbox.stateChanged.connect(lambda state:self.Switch(1, state)) # 格式转化开关
        self.ui.conv_cbb.currentTextChanged.connect(lambda state:self.Switch(11,state)) # 格式转化选择
        self.ui.qlty_cmp_cbox.stateChanged.connect(lambda state:self.Switch(2, state)) # 质量压缩开关
        self.ui.lossless_cmp_cbox.stateChanged.connect(lambda state:self.Switch(3,state)) # 无损压缩开关
        self.ui.lossless_cmp_lev_slider.valueChanged.connect(lambda state:self.Switch(31,state)) # 无损压缩级别调整
        self.ui.comfirm_btn.clicked.connect(self.handle) # 执行按钮
        self.ui.cancel_btn.clicked.connect(self.close) # 取消按钮

        self.ui.select_reverse_btn.clicked.connect(self.ui.PicsList.selectReverse)
        self.ui.select_all_btn.clicked.connect(self.ui.PicsList.selectAll)

        self.ui.sel_bmp_cbox.stateChanged.connect(lambda state:self.Switch(6,state))
        self.ui.sel_jpeg_cbox.stateChanged.connect(lambda state:self.Switch(6,state))
        self.ui.sel_png_cbox.stateChanged.connect(lambda state:self.Switch(6,state))
        self.ui.sel_webp_cbox.stateChanged.connect(lambda state:self.Switch(6,state))

    def init_widget(self):
        if not self.ui.format_conv_cbox.isChecked():
            for w in ergodic_layout(self.ui.layout_conv_vbox):
                w.setEnabled(False)

        if not self.ui.qlty_cmp_cbox.isChecked():
            for w in ergodic_layout(self.ui.layout_qlty_hbox):
                w.setEnabled(False)

        if not self.ui.lossless_cmp_cbox.isChecked():
            for w in ergodic_layout(self.ui.layout_uloss_hbox):
                w.setEnabled(False)

        if self.ui.conv_cbb.currentText() == 'JPEG':
            self.ui.conv_qlty_rbt.setChecked(True)
            self.ui.conv_lossless_rbt.setEnabled(False)
            self.ui.conv_lossless_lev_cbb.setEnabled(False)
        value = self.ui.lossless_cmp_lev_slider.value() 
        self.ui.lossless_cmp_lev_lbl.setText(str(value)+' 级   ')

        self.ui.tip_uloss_lbl.hide()


    def get_all_selected_fmt(self):
        fmt_list = []
        for item in self.ui.PicsList.selectedItems():
            fmt_list.append(item.fmt)
        return fmt_list

    #强制停止所有子线程和子进程
    def kill_all_threads(self):
        if self.prothread is not None:
            # 强制停止子线程
            for st in self.prothread.subthread:
                if st.isRunning():
                    st.terminate()
            if self.prothread.isRunning():
                self.prothread.terminate()
            # 强制停止子进程
            for p in SUBPROCESS:
                if p.poll() == None: # 进程未结束
                    p.kill()
            time.sleep(0.05)

    def Switch(self,sender,state):
        # self.ui.format_conv_cbox
        if sender == 1:
            if self.ui.format_conv_cbox.isChecked():
                for w in ergodic_layout(self.ui.layout_conv_vbox):
                    w.setEnabled(True)
                sender = 11
                state = self.ui.conv_cbb.currentText()
            else:
                for w in ergodic_layout(self.ui.layout_conv_vbox):
                    w.setEnabled(False)
        # self.ui.conv_cbb
        if sender == 11:
            if state == 'JPEG':
                self.ui.conv_qlty_rbt.setEnabled(True)
                self.ui.conv_qlty_spinbox.setEnabled(True)
                self.ui.conv_qlty_rbt.setChecked(True)
                self.ui.conv_lossless_rbt.setEnabled(False)
                self.ui.conv_lossless_lev_cbb.setEnabled(False)
            elif state == 'PNG':
                self.ui.conv_lossless_rbt.setEnabled(True)
                self.ui.conv_lossless_lev_cbb.setCurrentIndex(0)
                self.ui.conv_lossless_lev_cbb.setEnabled(False)
                self.ui.conv_lossless_rbt.setChecked(True)
                self.ui.conv_qlty_rbt.setEnabled(False)
                self.ui.conv_qlty_spinbox.setEnabled(False)
            else:
                self.ui.conv_lossless_rbt.setEnabled(True)
                self.ui.conv_lossless_lev_cbb.setCurrentIndex(2)
                self.ui.conv_lossless_lev_cbb.setEnabled(True)
                self.ui.conv_qlty_rbt.setEnabled(True)
                self.ui.conv_qlty_spinbox.setEnabled(True)
                self.ui.conv_qlty_rbt.setChecked(True)
        # self.ui.qlty_cmp_cbox
        if sender == 2:
            if self.ui.qlty_cmp_cbox.isChecked():
                for w in ergodic_layout(self.ui.layout_qlty_hbox):
                    w.setEnabled(True)
            else:
                for w in ergodic_layout(self.ui.layout_qlty_hbox):
                    w.setEnabled(False)
        #self.ui.lossless_cmp_cbox
        if sender == 3:
            if self.ui.lossless_cmp_cbox.isChecked():
                for w in ergodic_layout(self.ui.layout_uloss_hbox):
                    w.setEnabled(True)
            else:
                for w in ergodic_layout(self.ui.layout_uloss_hbox):
                    w.setEnabled(False)

        # self.ui.lossless_cmp_lev_slider:
        if sender == 31:
            self.ui.lossless_cmp_lev_lbl.setText(str(state)+' 级   ')
            #检测选中图片是否包含PNG，BMP及压缩级别是否过高
            if self.ui.lossless_cmp_lev_slider.value() > 2:
                fmt_list = self.get_all_selected_fmt()
                if 'PNG' in fmt_list or 'BMP' in fmt_list:
                    self.ui.tip_uloss_lbl.setHidden(False)
            else:
                self.ui.tip_uloss_lbl.hide()
        #self.ui.sel_bmp_cbox、...
        if sender == 6:
            sel_formats = []
            for w in (self.ui.sel_bmp_cbox,
                      self.ui.sel_jpeg_cbox,
                      self.ui.sel_png_cbox,
                      self.ui.sel_webp_cbox,):
                if w.isChecked():
                    sel_formats.append(w.text().upper())
            self.ui.PicsList.selectFormat(sel_formats)
    def handle(self):

        if self.ui.PicsList.selectedItems() == []:
            QtWidgets.QMessageBox.information(self,'警告','未发现选择项，请选择图片再执行处理！')
            return
            
        self.hide() #隐藏主窗口

        conv_format,conv_qlty_rate,conv_uloss_lev,jpeg_qlty_rate,webp_qlty_rate,is_colordepth,is_uloss,uloss_lv,uloss_wp = [None for i in range(9)]
        operate = 0 # 操作数为0表示没有任何操作

        if self.ui.format_conv_cbox.checkState() == QtCore.Qt.Checked:
            operate += 1
            conv_format = self.ui.conv_cbb.currentText()
            if self.ui.conv_lossless_rbt.isChecked():
                conv_uloss_lev = self.ui.conv_lossless_lev_cbb.currentIndex()
            else:
                conv_qlty_rate = self.ui.conv_qlty_spinbox.value()

        if self.ui.qlty_cmp_cbox.checkState() == QtCore.Qt.Checked:
            operate += 1
            jpeg_qlty_rate = self.ui.jpeg_qlty_spinbox.value()
            webp_qlty_rate = self.ui.webp_qlty_spinbox.value()
        
        if self.ui.colordepth_cmp_cbox.checkState() == QtCore.Qt.Checked:
            operate += 1
            is_colordepth = True

        if self.ui.lossless_cmp_cbox.checkState() == QtCore.Qt.Checked:
            operate += 1
            is_uloss = True
            # png lossless level range 0 to 7, value 'None' stands for closing lossless compression.
            # Range 0 to 9 webp lossless level , value 'None' stands for closing lossless compression.
            uloss_lv = self.ui.lossless_cmp_lev_slider.value() 
        
        args = {
            'OPERATE':operate,
            'CONV':conv_format,
            'CONV_RATE':conv_qlty_rate,
            'CONV_LV':conv_uloss_lev,
            'J_RATE':jpeg_qlty_rate,
            'W_RATE':webp_qlty_rate,
            'DEPTH':is_colordepth,
            'ULOSS':is_uloss,
            'ULOSS_LV':uloss_lv
        }

        self.prog = Progress(self)
        self.prog.show()

        #图片处理程序调用另外线程处理，防止阻塞主窗口程序。
        self.prothread = GenThread(self.ui.PicsList.selectedItems(),args,self.prog.update_value)
        self.prothread.start()
        #thread = threading.Thread(target=gen_thread,args=(self.ui.PicsList.selectedItems(),args,self.prog.update_value))
        #thread.start()

#遍历布局中的控件并返回目标控件
def ergodic_layout(layout):
    
    if not isinstance(layout, QtWidgets.QLayout):
        return []
    
    ret_widget = [] #返回列表

    #index_stack储存当前item指向child_item的指标和最大指标。
    index_stack = [] #[(current_index,max_index),...]
    item_stack = [None] #item地址堆栈

    index_stack.append((0,layout.count()-1))
    item_stack.append(layout)
    item = layout

    while True:
        if item is None:
            break
        #-----------------------------------------
        # 事件部分
        if isinstance(item, QtWidgets.QWidgetItem):
            ret_widget.append(item.widget())
        #------------------------------------------
        index = index_stack[-1][0]
        max_index = index_stack[-1][1]

        if index <= max_index:
            index_stack[-1] = (index + 1,max_index)
            item = item.itemAt(index)
            if 'count' in dir(item):
                index_stack.append((0,item.count()-1))
                item_stack.append(item)
            else:
                index_stack.append((0,-1))
                item_stack.append(item)
        else:
            index_stack.pop(-1)
            item_stack.pop(-1)
            item = item_stack[-1]
    
    return ret_widget

#---------------------
#多线程部分
#---------------------

PROG_VALUE = 0
MAX_CONNECTIONS = 8 # 最大线程并发数
SEMLOCK = QtCore.QSemaphore(MAX_CONNECTIONS) #创建一个线程信号量
MUTEX = QtCore.QMutex()

class GenThread(QtCore.QThread):
    def __init__(self,selectedItems,args,setValue):
        super().__init__()
        self.selectedItems = selectedItems
        self.args = args
        self.setValue = setValue
        self.subthread = []
        self.task_finished = False
    def run(self):
        task_num = len(self.selectedItems)
        step = int(math.ceil((100/task_num)*100))
        for item in self.selectedItems:
            file_path = item.pic_path
            fmt = item.fmt
            self.args['ROTATE'] = item.widget.angle if item.widget else 0
            if self.args['ROTATE'] != 0:
                self.args['OPERATE'] += 1
            ext = os.path.splitext(item.pic_path)[1][1:]
            self.args['FORMAT'] = fmt
            SEMLOCK.acquire()
            self.subthread.append(ImgThread(file_path,self.args.copy(),step,self.setValue))
            self.subthread[-1].start()
            time.sleep(0.06)

        while SEMLOCK.available() < MAX_CONNECTIONS: #等待直到所有线程结束
            time.sleep(0.1)
        #所有子线程走完，任务结束
        self.task_finished = True

#图片处理线程
class ImgThread(QtCore.QThread):
    sig_i = QtCore.pyqtSignal(int)
    def __init__(self,file_path,args,step,setValue):
        super().__init__()
        self.file_path = file_path
        self.args = args
        self.step = step
        self.sig_i.connect(setValue)
    def run(self):
        #核心功能 图片压缩
        log = ImagesProcess(self.file_path,self.args)
        global LOG,PROG_VALUE
        LOG.append(log)

        #读取进度值全局变量，发送信号到进度条控件。
        MUTEX.lock()
        PROG_VALUE += self.step
        self.sig_i.emit(int(PROG_VALUE/100) if PROG_VALUE < 10000 else 100)
        MUTEX.unlock()
        #进度条走满退出UI主循环。
        SEMLOCK.release()
        if PROG_VALUE >= 10000:
            
            time.sleep(0.3)
            # 进度条计算偏差导致 PROG_VALUE 两次以上大于 100000，
            # 可能导致重复退出 QCoreApplication 的异常，得加上 try 处理异常以防万一。
            try: 
                QtCore.QCoreApplication.instance().quit()
            except AttributeError:
                pass


#初始化图片列表线程
class WalkPicsThread(QtCore.QThread):
    pic_signal = QtCore.pyqtSignal(object)
    completed = QtCore.pyqtSignal(bool)
    cursor_state = QtCore.pyqtSignal(object)
    def __init__(self, win, root=None):
        super().__init__()
        self.root = root
        self.pic_signal.connect(win.ui.PicsList.initPicsList)
        self.completed.connect(win.ui.PicsList.selectALL)
        self.cursor_state.connect(win.setCursor)
    def run(self):
        if self.root is not None:
            self.cursor_state.emit(QtCore.Qt.WaitCursor)
            pics = walk_pics(self.root)
            for pic in pics:
                self.pic_signal.emit(pic)
                #time.sleep(0.02)
            self.completed.emit(True)
            self.cursor_state.emit(QtCore.Qt.ArrowCursor)

def epub_sources():
    if len(sys.argv) <= 1:
        return sys.argv
    epub_srcs = []
    exe_path = os.path.dirname(sys.argv[0])
    epub_srcs.append(exe_path)
    for epub_src in sys.argv[1:None]:
        filename = os.path.basename(epub_src)
        basename,ext = os.path.splitext(filename)
        if ext.lower() == '.epub':
            if os.path.exists(epub_src):
                epub_srcs.append(epub_src)
    return epub_srcs

def run(bk=None):
    try:
        app = QtWidgets.QApplication(sys.argv)
        win = MainWin(bk)
        app.exec_()
        if win.prothread is not None:
            while win.prothread.task_finished is not True:
                time.sleep(0.1)
        if LOG != [] and win.prothread.task_finished:
            print('  —————————————开始处理—————————————')
            print('  '+'#'*60)
            PosProcess(bk)
            print('  '+'#'*60)
            print('  —————————————处理完毕—————————————')
            
        if type(bk).__name__ == 'EpubBook':
            print('\n正在打包epub，请勿关闭窗口........')
            bk.save_as()
    except Exception as e:
        print('\n')
        print(traceback.format_exc())
        print("Error: %s\n" % e)
        return -1
    finally:
        win.kill_all_threads()
        if type(bk).__name__ == 'EpubBook':
            bk.__del__()
        shutil.rmtree(TEMPDIR)
    return 0

def test_main(test_mode = True):
    ''' test_mode 测试模式 值为True时仅处理，不输出图片'''
    ebook_root = '测试'
    app = QtWidgets.QApplication(sys.argv)
    win = MainWin(None)
    app.exec_()
    if LOG != [] and win.prothread.task_finished:
        PosProcess(ebook_root,test_mode)
    win.kill_all_threads()
    shutil.rmtree(TEMPDIR)
    if test_mode == True:
        print('测试模式：仅对图片进行处理，处理完不会生成新的图片')
    

if __name__ == "__main__":
    sys.exit(test_main(True))
    try:
        epub_srcs = epub_sources()
        if len(epub_srcs) <= 1:
            print('Error：找不到epub文件，请将有效的epub文件拖曳到pyz文件上！')
        else:
            epub_src = epub_srcs[1]
            bk = EpubWrapper.EpubBook(epub_src,True)
            run(bk)
    except:
        exc_type, exc_value, exc_obj = sys.exc_info()
        traceback.print_tb(exc_obj)
        print('%s: %s'%(exc_type.__name__, exc_value))
    finally:
        pass
        os.system('pause')