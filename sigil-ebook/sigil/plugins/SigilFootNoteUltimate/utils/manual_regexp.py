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

    def replace_note(self,args):
        tpl = self.note_tpl
        for key in self.note_var_list:
            try:
                tpl = tpl.replace('[%s]'%key,args[key])
            except KeyError:
                #略过捕获组无效错误
                pass
        return tpl

class RegExpNotes():
    def __init__(self,bk,**para):
        #计数器
        self.count = para['count']
        self.count_init = self.count
        #注释缓存表
        self.ref_list = []
        self.notes_list = []
        #跨页注释相关
        self.cross_page = "" # 当前页关联的所有跳转注释页
        self.crossPage_notes = {} #跨页注释缓存(注释原位置修改时使用)
        self.tgt_pages = {} # 注释页
        #epub对象
        self.bk = bk
        #参数
        self.pos_type = para['pos_type']
        self.var_mode = para['var_mode']
        self.span_mode = para['span_mode']

        #替换模板
        self.tpl = CustomTemplate(self.pos_type,para['ref_tpl'],para['note_tpl'],para['foot_tpl'])

        #注标匹配表达式
        self.cre_f = re.compile(self.turn_sigil_regexp(para['re_f']))
        #注释匹配表达式
        self.re_s = self.turn_sigil_regexp(para['re_s'])
        self.check_regexp_format()

        #处理记录
        self.logtext = ''

    def turn_sigil_regexp(self,regexp):
        return re.sub(r"\\x\{([0-9a-fA-F]{1,4})\}",lambda m:"0"*(4-len(m.group(1))) + m.group(1),regexp)
        
    def check_regexp_format(self):
        self.catch_groups_to_note_exp = {'groups':{},'index':{}}
        if self.var_mode == False:
            return
        
        for order in range(1,self.cre_f.groups+1):
            self.re_s,n = re.subn(r'\{%d\}'%order,'{_%d}'%order,self.re_s)
            if n > 0:
                self.catch_groups_to_note_exp['groups']['_%d'%order] = ''
        for gname in self.cre_f.groupindex:
            if '{%s}'%gname in self.re_s:
                self.catch_groups_to_note_exp['index']['%s'%gname] = ''

    def notes_process(self):
        for html_id,linear in self.bk.getspine():
            href = self.bk.id_to_href(html_id)
            filename = os.path.basename(href)

            if self.tgt_pages and filename in self.tgt_pages.keys():
                is_tgt_pages = True
                html = self.tgt_pages[filename]
            else:
                is_tgt_pages = False
                html = self.bk.readfile(html_id)
            
            html = self.notes_analysis(html,filename)

            if len(self.ref_list) <= 0:
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

            if is_tgt_pages:
                self.tgt_pages[filename] = html
            else:
                html = re.sub(r'(?:[\r\n] *){6,}',r'\n',html)
                self.bk.writefile(html_id,html)

            #清理临时列表
            self.notes_list.clear()
            self.ref_list.clear()

        if self.count == 0:
            print('......未能匹配到任何注释......')
            self.logtext += '......未能匹配到任何注释......'
        
        elif self.tgt_pages:
            if self.pos_type == POS_ORI:
                for target_basename in self.crossPage_notes.keys():
                    for filename in self.crossPage_notes[target_basename].keys():
                        sign = CP_NOTE_SIGN[0] + filename + CP_NOTE_SIGN[1]
                        temp_list = self.crossPage_notes[target_basename][filename]
                        self.tgt_pages[target_basename] = re.sub(sign,
                                                                 lambda x:temp_list.pop(0),
                                                                 self.tgt_pages[target_basename],
                                                                 len(temp_list) )
            for basename,html in self.tgt_pages.items():
                manifest_id = self.bk.basename_to_id(basename)
                html = re.sub(r'(?:[\r\n] *){6,}',r'\n',html)
                self.bk.writefile(manifest_id,html)
            self.crossPage_notes.clear()

    def take_notes_content(self, text, end_index, noteref_match, target_basename=None, filename=None):
        re_s = self.re_s

        if self.var_mode == True:
            g1 = self.catch_groups_to_note_exp['groups']
            g2 = self.catch_groups_to_note_exp['index']
            for order in g1:
                g1[order] = noteref_match.group(int(order[1]))
            for key in g2:
                g2[key] = noteref_match.group(key)
            re_s = re_s.format(**{**g1,**g2})
        text_0 = text[0:end_index]
        text_1 = text[end_index:]

        find = re.search(re_s,text_1)
        # 找到一个匹配的注释：
        if find:
            note_groups = find.groups()
            
            if target_basename is None:
                # 非跨页注释
                self.notes_list.append(note_groups)
                if self.pos_type == POS_ORI:
                    text_1 = text_1[0:find.start()] + NOTE_SIGN + text_1[find.end():]
                else:
                    text_1 = text_1[0:find.start()] + text_1[find.end():]
                return text_0 + text_1,True
            else:
                # 跨页注释且位置选项为POS_ORI：
                if self.pos_type == POS_ORI:
                    self.crossPage_notes[target_basename][filename].append(note_groups)
                    return text[0:find.start()] + CP_NOTE_SIGN[0] + filename + CP_NOTE_SIGN[1] + text[find.end():],True
                else:
                    # 跨页但位置选项不为POS_ORI
                    self.notes_list.append(note_groups)
                    text_1 = text_1[0:find.start()] + text_1[find.end():]
                    return text_0 + text_1,True
        # 找不到匹配的注释：
        else:
            return text,False

    def noteref_analysis(self,match):
        # match 是注标表达式的一次匹配（非所有匹配）
        if self.span_mode == False:
            return None
        else:
            ref_text = match.group()
            href = re.search(r'href ?= ?([\'\"])(?P<href>.+?)\1',ref_text)
            if href is not None:
                href = href.group("href")
            else:
                href = ""
            if href != "":
                if "#" in href:
                    target_basename = os.path.basename(href).split('#')[0]
                else:
                    target_basename = os.path.basename(href)
            else:
                target_basename = ""

            return target_basename

    def notes_analysis(self,text,filename):
        cre_f = self.cre_f
        find = cre_f.search(text)
        result_text = ""
        end_index = 0
        start_index = 0
        while find != None:
            start_index = end_index + find.start()
            result_text += text[end_index:start_index]
            end_index += find.end()
            ######################################
            #addition
            # 跨页模式：
            self.cross_page = ""
            target_basename = self.noteref_analysis(find) # 解析注标内容
            if self.span_mode == True and target_basename != filename:
                if target_basename != "" and self.bk.basename_to_id(target_basename) is not None:
                    try:
                        html2 = self.tgt_pages[target_basename]
                    except KeyError:
                        tgt_m_id = self.bk.basename_to_id(target_basename)
                        html2 = self.bk.readfile(tgt_m_id)
                        self.tgt_pages[target_basename] = html2
                    if self.pos_type == POS_ORI:
                        self.cross_page = target_basename
                        self.crossPage_notes.setdefault(target_basename,collections.OrderedDict())
                        self.crossPage_notes[target_basename].setdefault(filename,list())
                    else:
                        self.cross_page = ""
                    self.tgt_pages[target_basename], is_matched = self.take_notes_content(html2, 0, find, target_basename, filename)
                else:
                    self.cross_page = ""
                    is_matched = False
            # 非跨页模式：
            else:
                self.cross_page = ""
                text,is_matched = self.take_notes_content(text, end_index, find)
            # 匹配成功：
            if is_matched:  #footnote匹配成功
                self.ref_list.append( find.groups()) #注标捕获组内容入列
                # 正则表达式捕获组填充
                if self.cross_page == "":
                    self.ref_list[-1],self.notes_list[-1] = self.turn_tpl_to_instance(self.ref_list[-1], self.notes_list[-1])
                else:
                    self.ref_list[-1],self.crossPage_notes[target_basename][filename][-1] = self.turn_tpl_to_instance(self.ref_list[-1],self.crossPage_notes[target_basename][filename][-1],filename)
                result_text += REF_SIGN
                if self.pos_type == POS_NEXT:
                    text = text[0:end_index] + re.sub(r'(</(?:p|div|h[1-6])>)',r'\1\n%s'%NOTE_SIGN,text[end_index:],1)
            else: #footnote匹配失败
                result_text += find.group()
                break
            ######################################
            find = cre_f.search(text[end_index:])
        result_text += text[end_index:]
        return result_text

    def turn_tpl_to_instance(self,ref_groups,note_groups,filename = ""):
        self.count += 1
        if self.cross_page != "":
            target_href = self.cross_page
            ref_href = filename
        else:
            target_href,ref_href = "",""
        ref_id = 'noteref_%d'%self.count
        note_id = 'note_%d'%self.count
        ref_href = '%s#note_%d'%(target_href,self.count)
        note_href = '%s#noteref_%d'%(filename,self.count)
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