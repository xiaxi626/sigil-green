#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,os,time
import re
import collections

#特殊符号
REF_SIGN = 'Щㅙ'
NOTE_SIGN = '♮☍'
CP_NOTE_SIGN = 'ы㉣'

POS_ORI,POS_TAIL,POS_NEXT = 1,2,3

class CustomTemplate():
    def __init__(self,pos,noteref_tpl:str='',note_tpl:str='',foot_tpl:str=''):
        self.pos = pos
        self.noteref_tpl = noteref_tpl
        self.note_tpl = note_tpl
        self.foot_tpl = foot_tpl
        self.noteref_var_list = []
        self.note_var_list = []
        self.analysis_template()

    def analysis_template(self):

        available_var = {'href':True,'id':True,'num':True}
        for i in range(1,10):
            available_var['r%d'%i] = True
            available_var['n%d'%i] = True

        temp_key_list = re.findall(r'\[(\w+)\]',self.noteref_tpl)
        for key in temp_key_list:
            if available_var[key]:
                self.noteref_var_list.append(key)

        temp_key_list = re.findall(r'\[(\w+)\]',self.note_tpl)
        for key in temp_key_list:
            if available_var[key]:
                self.note_var_list.append(key)
        
        temp = re.split(r'[\t ]*\[pos\]\n?',self.foot_tpl)

        if len(temp) == 2:
            self.foot_open_code = temp[0]
            self.foot_close_code = temp[1]
            indent = ""
            if self.pos == POS_TAIL:
                indent = re.search(r'([\t ]*)\[pos\]',self.foot_tpl).group(1)
            self.note_tpl = re.sub(r'(\n+)',r'\1%s'%indent,self.note_tpl)
            self.note_tpl = indent + self.note_tpl
        else:
            self.foot_open_code = ''
            self.foot_close_code = ''
        
    def replace_noteref(self,args):
        tpl = self.noteref_tpl
        for key in self.noteref_var_list:
            try:
                tpl = tpl.replace('[%s]'%key,args[key])
            except KeyError:
                #略过捕获组无效错误
                pass
        return tpl

    def replace_note(self,args):
        tpl = self.note_tpl
        for key in self.note_var_list:
            try:
                tpl = tpl.replace('[%s]'%key,args[key])
            except KeyError:
                #略过捕获组无效错误
                pass
        return tpl

class RegExpInterlinearNotes():
    def __init__(self,bk,**para):
        #计数器
        self.count = para['count']
        self.count_init = self.count
        #注释缓存表
        self.ref_list = []
        self.notes_list = []
        #epub对象
        self.bk = bk
        #参数
        self.pos_type = para['pos_type']
        #替换模板
        self.tpl = CustomTemplate(self.pos_type,para['ref_tpl'],para['note_tpl'],para['foot_tpl'])
        
        #注释匹配表达式
        self.c_re = re.compile(self.turn_sigil_regexp(para['re_f']))
        
        #处理记录
        self.logtext = ''

    def turn_sigil_regexp(self,regexp):
        return re.sub(r"\\x\{([0-9a-fA-F]{1,4})\}",lambda m:"0"*(4-len(m.group(1))) + m.group(1),regexp)

    def notes_process(self):
        for html_id,linear in self.bk.getspine():
            href = self.bk.id_to_href(html_id)
            filename = os.path.basename(href)
            html = self.bk.readfile(html_id)

            html = self.notes_analysis(html,filename)

            if self.notes_list == []:
                continue

            print('在文件 '+ filename + ' 发现注释 %d 条。\n' % len(self.ref_list))
            self.logtext += '在文件 '+ filename + ' 发现注释 %d 条。\n' % len(self.ref_list)

            html = re.sub(REF_SIGN,lambda x:self.ref_list.pop(0),html,len(self.ref_list))

            if self.pos_type == POS_TAIL:
                footnotes_text = self.tpl.foot_open_code
                for sub_note in self.notes_list:
                    footnotes_text += sub_note + '\n'
                footnotes_text += self.tpl.foot_close_code
                html = re.sub(r'</body>','\n'+ footnotes_text +'\n</body>',html,1)
            
            elif  self.pos_type == POS_NEXT or self.pos_type == POS_ORI:
                if len(self.notes_list) > 0:
                    html = re.sub(NOTE_SIGN,lambda x:self.notes_list.pop(0),html,len(self.notes_list))


            html = re.sub(r'(?:[\r\n] *){6,}',r'\n',html)
            self.bk.writefile(html_id,html)

            #清理临时列表
            self.notes_list.clear()
            self.ref_list.clear()

        if self.count == 0:
            print('......未能匹配到任何注释......')
            self.logtext += '......未能匹配到任何注释......'
        
    def notes_analysis(self,text,filename):
        c_re = self.c_re
        find = c_re.search(text)
        result_text = ""
        end_index = 0
        start_index = 0
        while find != None:
            start_index = end_index + find.start()
            result_text += text[end_index:start_index]
            end_index += find.end()
            ######################################
            #addition
            self.ref_list.append(None)
            self.notes_list.append(None)
            # 正则表达式捕获组填充
            self.ref_list[-1],self.notes_list[-1] = self.turn_tpl_to_instance([], find.groups())
            result_text += REF_SIGN
            if self.pos_type == POS_ORI:
                result_text += NOTE_SIGN
            elif self.pos_type == POS_NEXT:
                text = text[0:end_index] + re.sub(r'(</(?:p|div|h[1-6])>)',r'\1\n%s'%NOTE_SIGN,text[end_index:],1)
            ######################################
            find = c_re.search(text[end_index:])
        result_text += text[end_index:]
        return result_text

    def turn_tpl_to_instance(self,ref_groups,note_groups):
        self.count += 1

        ref_id = 'noteref_%d'%self.count
        note_id = 'note_%d'%self.count
        ref_href = '#note_%d'%(self.count)
        note_href = '#noteref_%d'%(self.count)
        ref_args = {
            'id': ref_id, 'href': ref_href,'num':str(self.count)
        }
        note_args = {
            'id': note_id, 'href': note_href,'num':str(self.count)
        }
        index = 0
        for g in ref_groups:
            index += 1
            ref_args['r%d'%index] = g if g is not None else ""
            note_args['r%d'%index] = g if g is not None else ""
        index = 0
        for g in note_groups:
            index += 1
            ref_args['n%d'%index] = g if g is not None else ""
            note_args['n%d'%index] = g if g is not None else ""
        return self.tpl.replace_noteref(ref_args), self.tpl.replace_note(note_args)
    
    def run(self):
        start = time.perf_counter()

        print('\n\n'+'#'*75+'\n正在使用手动识别规则处理文本\n' +'#'*75+'\n')
        self.logtext += '\n\n'+'#'*75+'\n正在使用手动识别规则处理文本\n' +'#'*75+'\n'

        self.notes_process()
        end = time.perf_counter()

        print("\n"+"-"*75+"\n处理完毕，共处理了 %d 条注释。"%(self.count-self.count_init))
        self.logtext += "\n"+"-"*75+"\n处理完毕，共处理了 %d 条注释。\n"%(self.count-self.count_init)

        print('共耗费时间 %f' % (end-start))
        return self.logtext,self.count

def main():
    pass
    
if __name__ == "__main__":
    main()