# -*- coding: utf-8 -*-12

from PyQt5 import QtCore, QtGui, QtWidgets
import os,time
import icon_rc
from PIL import Image,ImageQt
from utils.posprocess import size_f

Thum_S = 160 # 缩略图尺寸
Font = QtGui.QFont('SimSun',12)

#----------------------
#缩略图选择列表部分
#----------------------
class ItemDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self,parent = None):
        super().__init__(parent)
    def paint(self, painter, option, index):
        listView = self.parent()
        item = listView.item(index.row())
        if item.widget is None:
            item.widget = widget = ItemWidget(item, listView.rIcon, listView.rIcon2)
            listView.setItemWidget(item,widget)
        super().paint(painter, option, index)
class ItemWidget(QtWidgets.QWidget):
    def __init__(self,item,rIcon,rIcon2):
        super().__init__()
        self.angle = 0
        self.rIcon = rIcon
        self.rIcon2 = rIcon2
        self.initUI()
        self.initMessage(item)
    def initUI(self):
        layout = QtWidgets.QHBoxLayout()
        #创建一个缩略图Label
        self.thumbnail_label = thumbnail_label = QtWidgets.QLabel()
        thumbnail_label.setFixedSize(160,160) #设置缩略图控件尺寸
        thumbnail_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter) 
        layout.addWidget(thumbnail_label)

        #创建一个纵布局容纳信息文本
        self.msg = msg = QtWidgets.QVBoxLayout()
        msg.setSpacing(8)
        msg.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter|QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addLayout(msg)
    
        class R_BUTTON(QtWidgets.QLabel):
            def __init__(self,icon,icon2,func):
                super().__init__()
                self.icon = icon
                self.icon2 = icon2
                self.setPixmap(icon)
                self.setFixedSize(27,27)
                self.setToolTip('旋转图片')
                self.func = func
            def mousePressEvent(self,event):
                if event.button() == QtCore.Qt.LeftButton:
                    self.setPixmap(self.icon2)
            def mouseReleaseEvent(self,event):
                if event.button() == QtCore.Qt.LeftButton:
                    self.setPixmap(self.icon)
                    self.func(90)
        self.rotate_btn = rotate_btn = R_BUTTON(self.rIcon,self.rIcon2,self.rotate)
        rb_lay = QtWidgets.QVBoxLayout()
        rb_lay.setContentsMargins(0,0,16,8)
        rb_lay.addStretch(1)
        rb_lay.addWidget(rotate_btn)
        layout.addLayout(rb_lay)
        layout.setContentsMargins(3,3,3,3) #重设布局边距（默认为10,10,10,10）
        self.setLayout(layout)
    def initMessage(self,item):
        # 初始化缩略图
        
        img = Image.open(item.pic_path).convert('RGBA') # PIL图片
        imgW,imgH = img.size
        #imgW,imgH = 100,100
        img.thumbnail((Thum_S,Thum_S)) # 缩略图
        Qimg = ImageQt.ImageQt(img) # PIL图片 转 QImage图片

        self.thumbnail = thumbnail = QtGui.QPixmap().fromImage(Qimg)
        self.thumbnail_label.setPixmap(thumbnail)

        pic_name = os.path.basename(item.pic_path)
        pic_size = size_f(int(os.path.getsize(item.pic_path)))

        #初始化图片信息
        for text in ['文件： {}'.format(pic_name),
                    '尺寸： {} × {}'.format(imgW,imgH),
                    '大小： {}'.format(pic_size)]:
            lbl = QtWidgets.QLabel(text)
            lbl.setFont(Font)
            lbl.setFixedHeight(28)
            lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
            self.msg.addWidget(lbl)

    def rotate(self,value):
        self.angle = int((self.angle + value) % 360)
        if self.thumbnail.width() > Thum_S or self.thumbnail.height() > Thum_S:
            thumbnail = self.thumbnail.transformed(QtGui.QTransform().rotate(self.angle)).scaled(QtCore.QSize(Thum_S,Thum_S),QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation)
        else:
            thumbnail = self.thumbnail.transformed(QtGui.QTransform().rotate(self.angle))
        self.thumbnail_label.setPixmap(thumbnail)


class PicsListWidget(QtWidgets.QListWidget):
    def __init__(self,parent):
        super().__init__(parent)
        self.initUI()
        self.initRotateIcon()
        self.time_a = time.perf_counter()
        delegate = ItemDelegate(self)
        self.setItemDelegate(delegate)

    def initUI(self):
        self.setAcceptDrops(True) #允许拖曳
        #self.setMinimumHeight(200)
        #self.setFixedWidth(468)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection) #设置按住Ctrl或Shift可选择多项
        QSS = '''QListWidget::Item:hover{background:#CCE8FF;}
            QListWidget::Item:selected{background:#81bff1;}'''
        self.setStyleSheet(QSS)
        self.setSpacing(2)

    def initRotateIcon(self):
        rIcon = QtGui.QPixmap(":/rotate/rotate.png")
        rIcon2 = QtGui.QPixmap(":/rotate/rotate_p.png")
        self.rIcon = rIcon.scaled(QtCore.QSize(27,27),
                        QtCore.Qt.AspectRatioMode.KeepAspectRatio, 
                        QtCore.Qt.TransformationMode.SmoothTransformation)
        self.rIcon2 = rIcon2.scaled(QtCore.QSize(27,27),
                        QtCore.Qt.AspectRatioMode.KeepAspectRatio, 
                        QtCore.Qt.TransformationMode.SmoothTransformation)

    def initPicsList(self,pic): #接收WalkPicsThread传递的参数，初始化图片列表项
        pic_path,fmt = pic
        item = QtWidgets.QListWidgetItem()
        item.setSizeHint(QtCore.QSize(416,168))
        item.pic_path = pic_path # 储存图片路径
        item.fmt = fmt  # 储存图片格式
        #item.widget = widget = ItemWidget(item,self.rIcon,self.rIcon2)
        item.widget = None
        self.addItem(item)
        #self.setItemWidget(item,widget)

    def selectALL(self,completed):
        if completed == True:
            self.selectAll() #列表项全选
        #time_b = time.perf_counter()
        #print('耗时%.2fs'%(time_b-self.time_a))

    def selectReverse(self):
        for row in range(self.count()):
            item = self.item(row)
            if item.isSelected():
                item.setSelected(False)
            else:
                item.setSelected(True)

    def selectFormat(self,formats:list):
        for row in range(self.count()):
            item = self.item(row)
            if item.fmt in formats:
                item.setSelected(True)
            else:
                item.setSelected(False)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1:
            url = event.mimeData().urls()[0].url()
            if url.lower().endswith('.epub'):
                self.url = url
                event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        super().dropEvent(event)
        