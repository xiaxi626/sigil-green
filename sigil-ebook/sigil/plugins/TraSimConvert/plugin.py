#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from util.langconv import Converter 
import tkinter as tk
import tkinter.font as tf
from tkinter import * 
from GenUtils import centerWindow

def Convert(match,LANG):
    text = match.group()
    conv_text = Converter(LANG).convert(text) # LANG = zh-hans | zh-hant
    conv_text.encode('utf-8')
    return conv_text



def run(bk):
    root = tk.Tk()
    root.title('繁简转化')
    root.geometry('229x110')
    root.resizable(0,0) #禁止修改窗口大小
    CheckVar = tk.IntVar()

    def hit_convert(LANG,):
        if CheckVar.get() == 1:
            for id_type,Id in bk.selected_iter():
                if re.search(r'\.opf$',Id):
                    metadata = bk.getmetadataxml()
                    metadata = re.sub(r'<metadata.*?>.*?</metadata>',lambda x:Convert(x,LANG),metadata,0,re.S)
                    bk.setmetadataxml(metadata)
                    continue
                book = bk.readfile(Id)
                book = re.sub(r'<body.*?>.*</body>|<title.*?>.*?</title>|<text>.*?</text>',lambda x:Convert(x,LANG),book,0,re.S)
                bk.writefile(Id,book)                 
        else:
            for Id,href in bk.text_iter():
                book = bk.readfile(Id)
                book = re.sub(r'<body.*?>.*</body>|<title.*?>.*?</title>',lambda x:Convert(x,LANG),book,0,re.S)
                bk.writefile(Id,book)
            for Id, href, mime in bk.manifest_iter():
                if Id == "ncx":
                    book = bk.readfile('ncx')
                    book = re.sub(r'<text>.*?</text>',lambda x:Convert(x,LANG),book,0,re.S)
                    bk.writefile('ncx',book)
            metadata = bk.getmetadataxml()
            metadata = re.sub(r'<metadata.*?>.*?</metadata>',lambda x:Convert(x,LANG),metadata,0,re.S)
            bk.setmetadataxml(metadata)
        root.quit()
        return 0

    ft = tf.Font(size=20,weight=tf.BOLD)
    b = tk.Button(root, text='简',  width=7, height=2, font=ft, command=lambda:hit_convert('zh-hans'))    
    b.grid(row=0,column=0)
    b2 = tk.Button(root, text='繁', width=7, height=2,font=ft, command=lambda:hit_convert('zh-hant'))   
    b2.grid(row=0,column=1)
    ft2 = tf.Font(size=11,weight=tf.BOLD)
    c = Checkbutton(root, variable = CheckVar, text="仅转换已选择文件", font=ft2, fg="#606060", pady=8, onvalue = 1, offvalue = 0)
    c.grid(row=1,column=0,columnspan=2,sticky=W)
    centerWindow(root) 
    root.mainloop()
    return 0

    
if __name__ == "__main__":
    pass