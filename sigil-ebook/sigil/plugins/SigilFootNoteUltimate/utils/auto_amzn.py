#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,os,time
import re
import collections

#注释正则书写
# NOTEREF_EXPRESSION 的表达式需要捕获到 id, href 两组数据于前两组捕获组
# FOOTNOTE_EXPRESSION href位置留占位符{}，待程序调用format函数处理

#注标匹配表达式
NOTEREF_EXPRESSION = {
#id href 在同一个节点内
1 : r'(?:<s[^>]*>[\r\n\t ]*)?<a[^>]*?((?:id|href)="[^\"]*")[^>]*((?:id|href)="[^\"]*")[^>]*>[\r\n\t ]*(?:<[^>]+>[\r\n\t ]*)*?([^<>\r\n]+?)[\r\n\t ]*(?:</[^>]+>[\r\n\t ]*)*?</a>(?:[\r\n\t ]*</s[^>]*>)?',
#id href 在相邻节点或父子节点里
2 : r'(?:<[as][^>]*>[\r\n\t ]*)?<[as][^>]*?((?:id|href)="[^\"]*")[^>]*>[\r\n\t ]*(?:<[^>]*>[\r\n\t ]*)?<[as][^>]*?((?:id|href)="[^\"]*")[^>]*>[\r\n\t ]*(?:<[as][^>]*>[\r\n\t ]*)?([^<>\r\n]+?)(?:[\r\n\t ]*</[as][^>]*>)+'
}

#注解匹配表达式
FOOTNOTE_EXPRESSION = {
1 : r'(?s)(?:<aside[^>]*>[\r\n\t ]*)?<(?P<tag>p|div)[^>]*>[\r\n\t ]*(?:</?[as][^>]*>[\r\n\t ]*)*?<a[^>]* href="(?P<href>[^\"]*?(?P<to_id>#{}))"[^>]*>.+?</(?P=tag)>(?:[\r\n\t ]*</aside>)?'
}

#检验遗漏表达式
CHECK_EXPRESSION = {
1: r'<a [^>]*(?:id|href)=([\'\"])[^>]*?\1[^>]*(?:id|href)=([\'\"])[^>]*?\2[^>]*>',
2: r'<[asp][^>]* (?:id|href)=[^>]*>[\r\n\t ]*(</?[asp][^>]*>[\r\n\t ]*)*?<[as][^>]* (?:id|href)=[^>]*>',
}

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

        noteref_var = {'href':True,'id':True,'note':True,'ref':True,'num':True}
        temp_key_list = re.findall(r'\[(\w+)\]',self.noteref_tpl)
        for key in temp_key_list:
            if noteref_var[key]:
                self.noteref_var_list.append(key)

        note_var = {'href':True,'id':True,'note':True,'ref':True,'num':True}
        temp_key_list = re.findall(r'\[(\w+)\]',self.note_tpl)
        for key in temp_key_list:
            if note_var[key]:
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
            tpl = tpl.replace('[%s]'%key,args[key])
        return tpl

    def replace_note(self,args):
        tpl = self.note_tpl
        for key in self.note_var_list:
            tpl = tpl.replace('[%s]'%key,args[key])
        return tpl

class AutoNotes():
    def __init__(self,bk,**para):
        #初始化正则表达式
        #注标
        self.noteref_exps = NOTEREF_EXPRESSION
        self.re_f_list = [re.compile(rep) for key,rep in self.noteref_exps.items()]
        #注释
        self.footnote_exps = FOOTNOTE_EXPRESSION
        self.re_s_list = [rep for key,rep in self.footnote_exps.items()]
        #检验
        self.check_re_list = [re.compile(rep) for key,rep in CHECK_EXPRESSION.items()]
        #初始化计数器
        self.count = para['count']
        self.count_init = self.count
        #初始化临时变量
        self.cross_page = ''
        self.ref_list = []
        self.notes_list = []
        self.crossPage_notes = {}
        self.tgt_pages = {}
        #初始化epub对象
        self.bk = bk
        #初始化替换位置参数
        self.pos_type = para['pos_type']
        #初始化替换模板
        self.tpl = CustomTemplate(self.pos_type,para['ref_tpl'],para['note_tpl'],para['foot_tpl'])
        #初始化检查遗漏参数
        self.check_loss = para['check_loss']
        self.loss_like = {} # {filename:loss_note}
        #处理记录
        self.logtext = ''

    def main_process(self):
        for html_id,linear in self.bk.getspine():

            self.ref_list.clear()
            self.notes_list.clear()

            href = self.bk.id_to_href(html_id)
            filename = os.path.basename(href)

            if self.tgt_pages and filename in self.tgt_pages.keys():
                is_tgt_pages = True
                html = self.tgt_pages[filename]
            else:
                is_tgt_pages = False
                html = self.bk.readfile(html_id)

            alive = len(self.re_f_list)
            #开始进行注释分析
            html = self.notes_analysis(html,filename,alive)

            #替换前先检查是否有遗漏
            self.check_loss_note(html, filename)

            #开始替换注释
            if self.ref_list != []:
                ref_count = len(self.ref_list)

                print('在文件 '+ filename + ' 发现注释 %d 条。\n' % ref_count)
                self.logtext += '在文件 '+ filename + ' 发现注释 %d 条。\n' % ref_count

                self.notes_list = list(filter(None,self.notes_list))
                # 替换 noteref
                
                html = re.sub(REF_SIGN,lambda x:self.tpl.replace_noteref(self.ref_list.pop(0)),html,ref_count)

                # 替换 note
                if self.notes_list != []:

                    if self.pos_type == POS_TAIL:
                        footnotes_text = self.tpl.foot_open_code
                        for args in self.notes_list:
                            footnotes_text += self.tpl.replace_note(args) + '\n'
                        footnotes_text += self.tpl.foot_close_code
                        html = re.sub(r'</body>','\n'+ footnotes_text +'\n</body>',html,1)

                    elif self.pos_type == POS_NEXT or POS_ORI:
                        html = re.sub(NOTE_SIGN,lambda x:self.tpl.replace_note(self.notes_list.pop(0)),html,len(self.notes_list))
                
                if is_tgt_pages:
                    self.tgt_pages[filename] = html
                else:
                    html = re.sub(r'(?:[\r\n] *){6,}',r'\n',html)
                    self.bk.writefile(html_id,html)

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
                                                                 lambda x:self.tpl.replace_note(temp_list.pop(0)),
                                                                 self.tgt_pages[target_basename],
                                                                 len(temp_list) )
            for basename,html in self.tgt_pages.items():
                manifest_id = self.bk.basename_to_id(basename)
                html = re.sub(r'(?:[\r\n] *){6,}',r'\n',html)
                self.bk.writefile(manifest_id,html)
            self.crossPage_notes.clear()

    def take_notes_content(self, text, end_index, ref_id, alive = 0, filename = None, target_basename = None):
        def func_(match):
            note = match.group()
            note_href = match.group('href') if self.pos_type == POS_ORI else match.group('to_id')
            note_id = re.search(r'id="([^\"]*)"',note).group(1) if re.search(r'id="([^\"]*)"',note) else ""
            content = re.sub(r'</?[pa][^>]*>','',note)
            content = re.sub(r'^\d+\. *|^\d+ +|^[\[\(（［〔][\d一二三四五六七八九十〇]+[\]\)）］〕] *','',content,1)
            self.count += 1
            args = { 'href':note_href, 'id':note_id, 'note':content, 'num':str(self.count) }
            if not self.cross_page:
                self.notes_list.append(args)
                if self.pos_type == POS_ORI:
                    return NOTE_SIGN
                else:
                    return ''
            else:
                self.crossPage_notes[target_basename][filename].append(args)
                return CP_NOTE_SIGN[0] + filename + CP_NOTE_SIGN[1]

        #如果所有正则表达式尝试失败，则alive为0。
        if alive == 0:
            return text,False
        re_s = self.re_s_list[0].format(ref_id)
        text_0 = text[0:end_index]
        text_1 = text[end_index:]
        L1 = len(text_1)
        text_1 = re.sub(re_s,func_,text_1,1)
        L2 = len(text_1)
        if L1 != L2:
            return text_0 + text_1,True
        else:
            self.re_s_list.append(self.re_s_list.pop(0))
            return self.take_notes_content(text, end_index, ref_id, alive - 1)
    
    def noteref_analysis(self,match):
        ref_id = href = ""
        ref_id,href = (match.group(1)[4:-1],match.group(2)[6:-1]) if match.group(1).startswith('i') else (match.group(2)[4:-1],match.group(1)[6:-1])

        if not ref_id: #如果没有ref_id，则ref_id返回为空，匹配失败
            return match.group(),'','',''

        try:
            target_basename,target_id = os.path.basename(href).split('#')
        except ValueError:
            target_basename,target_id = "","{}"

        ref_text = match.group(3)
        
        args = {
            'href':href,
            'target_id':target_id,
            'target_basename':target_basename,
            'id':ref_id,
            'ref':ref_text
        }

        #计算节点是否闭合，不闭合则修饰至闭合。
        tag_open_count = re.findall(r'<[^/]',match.group()).__len__()
        tag_close_count = re.findall(r'</',match.group()).__len__()
        if tag_open_count > tag_close_count:
            n = tag_open_count - tag_close_count
            open_tag = re.match(r'(?:<[^/>]+>[\r\n\t ]*){' + str(n) +r'}',match.group()).group()
            return open_tag + REF_SIGN, args
        elif tag_open_count < tag_close_count:
            n = tag_close_count - tag_open_count
            close_tag = re.match(r'(?s).*((?:[\r\n\t ]*</[^>]+>){'+str(n)+r'})$',match.group()).group(1)
            return REF_SIGN + close_tag, args

        return REF_SIGN, args

    def notes_analysis(self,text,filename,alive):
        #如果所有正则表达式尝试失败，则alive为0。
        if alive == 0:
            return text
        cre_f = self.re_f_list[0]
        find = cre_f.search(text)
        if not find:
            self.re_f_list.append(self.re_f_list.pop(0))
            return self.notes_analysis(text,filename,alive-1)
        result_text = ""
        end_index = 0
        start_index = 0
        while find != None:
            matched_at_least_once = False
            ref_sign, ref_args = self.noteref_analysis(find)
            start_index = end_index + find.start()
            result_text += text[end_index:start_index]
            end_index += find.end()
            ######################################
            #addition
            #目标链接不在同一页
            self.cross_page = ''
            target_basename = ref_args['target_basename']
            if target_basename and target_basename != filename:
                if self.bk.basename_to_id(target_basename) is not None:
                    try:
                        html2 = self.tgt_pages[target_basename]
                    except KeyError:
                        tgt_m_id = self.bk.basename_to_id(target_basename)
                        html2 = self.bk.readfile(tgt_m_id)
                        self.tgt_pages[target_basename] = html2
                    alive = len(self.re_s_list)
                    if self.pos_type == POS_ORI:
                        self.cross_page = target_basename
                        self.crossPage_notes.setdefault(target_basename,collections.OrderedDict())
                        self.crossPage_notes[target_basename].setdefault(filename,list())
                    else:
                        self.cross_page = ''
                    self.tgt_pages[target_basename],is_matched = self.take_notes_content(html2, 0, ref_args['id'], alive, filename, target_basename)
                else:
                    self.cross_page = ''
                    is_matched = False
            #目标链接在同一页
            else:
                self.cross_page = ''
                text,is_matched = self.take_notes_content(text, end_index, ref_args['id'], len(self.re_s_list))
            ######################################
            if is_matched:  #footnote匹配成功
                matched_at_least_once = True
                result_text += ref_sign
                args = {
                    'href':ref_args['href'] if self.pos_type == POS_ORI else '#' + ref_args['target_id'],
                    'id':ref_args['id'],
                    'ref':ref_args['ref'],
                    'num':str(self.count),
                    'note':self.notes_list[-1]['note'] if not self.cross_page else self.crossPage_notes[target_basename][filename][-1]['note']
                }
                self.ref_list.append(args)

                if not self.cross_page:
                    self.notes_list[-1]['ref'] = ref_args['ref']
                else:
                    self.crossPage_notes[target_basename][filename][-1]['ref'] = ref_args['ref']
                if self.pos_type == POS_NEXT:
                    text = text[0:end_index] + re.sub(r'(</(?:p|h[1-6])>)',r'\1\n%s'%NOTE_SIGN,text[end_index:],1)
            else: #footnote匹配失败
                result_text += find.group()
            find = cre_f.search(text[end_index:])
            #---while循环结束---
        
        if not matched_at_least_once:
            self.re_f_list.append(self.re_f_list.pop(0))
            return self.notes_analysis(text,filename,alive-1)

        result_text += text[end_index:]
        return result_text

    def check_loss_note(self,html,filename):
        if self.check_loss == False:
            return
        self.loss_like[filename] = []
        def func_(match):
            self.loss_like[filename].append(match.group())
            return ''
        for re_compiled in self.check_re_list:
            html = re_compiled.sub(func_,html)
    
    def check_loss_log(self):
        if not self.check_loss:
            return ""
        log_text = ""
        loss_count = 0
        for filename,loss_list in self.loss_like.items():
            if len(loss_list) > 0:
                loss_count += len(loss_list)
                log_text += "\n在文件 %s 发现疑似未匹配注释代码 %d 串：\n"%(filename,len(loss_list))
                for loss_note in loss_list:
                    log_text += "特征字符串：" + loss_note + '\n'
        if log_text == "":
            return ""
        print(log_text)
        return log_text

    def run(self):
        start = time.perf_counter()

        print('\n\n'+'#'*75+'\n正在使用自动识别规则处理文本\n' +'#'*75+'\n')
        self.logtext += '\n\n'+'#'*75+'\n正在使用自动识别规则处理文本\n' +'#'*75+'\n'

        self.main_process()
        end = time.perf_counter()
        self.logtext += self.check_loss_log()
        print("\n"+"-"*75+"\n处理完毕，共处理了 %d 条注释。"%(self.count-self.count_init))
        self.logtext += "\n"+"-"*75+"\n处理完毕，共处理了 %d 对注释。\n"%(self.count-self.count_init)

        print('共耗费时间 %.4f s' % (end-start))
        return self.logtext,self.count


def main():
    print ("This module should not be run as a stand-alone module")
    return -1
    
if __name__ == "__main__":
    sys.exit(main)