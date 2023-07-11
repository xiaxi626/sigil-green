import os,sys,re,shutil
from urllib.parse import unquote
try:
    from .compress import TEMPDIR
except:
    from compress import TEMPDIR

LOG = []

def isConverted(log):
    if log['OUT_FMT'] and log['SRC_FMT'] != log['OUT_FMT']:
        return True
    else:
        return False

#计算bookpath
def get_bookpath(relative_path,refer_bkpath):
    # relative_path 相对路径，一般是href
    # refer_bkpath 参考的绝对路径

    relative_ = re.split(r'[\\/]',relative_path)
    refer_ = re.split(r'[\\/]',refer_bkpath)
    
    back_step = 0
    while relative_[0] == '..':
        back_step += 1
        relative_.pop(0) 

    if len(refer_) <= 1:
        return '/'.join(relative_)
    else:
        refer_.pop(-1)

    if back_step < 1:
        return '/'.join(refer_+relative_)
    elif back_step > len(refer_):
        return '/'.join(relative_)

    #len(refer_) > 1 and back_setp <= len(refer_):
    while back_step > 0 and len(refer_) > 0:
        refer_.pop(-1)
        back_step -= 1
    
    return '/'.join(refer_ + relative_)

#寻找epub中与目标文件关联的链接并修改
def modRelatedFile(bk,converted_files):
    def sub_link(match):
        img_href = unquote(match.group('href'))
        img_bkpath = get_bookpath(img_href, file_bkpath)
        if img_bkpath in converted_files['BOOKPATH'].keys():
            new_href = bk.get_relativepath(file_bkpath,converted_files['BOOKPATH'][img_bkpath])
            subs = match.group('a') + new_href + match.group('b')
            nonlocal substituted
            substituted = True
        else:
            subs = match.group()
        return subs
    
    if not bk:
        return

    for id,href in list(bk.text_iter())+list(bk.css_iter()):
        #略过Id不存在的错误
        try:
            text = bk.readfile(id)
        except Exception as e:
            if e == 'Id does not exist in manifest':
                continue

        file_bkpath = get_bookpath(href, opf_bkpath)
        
        substituted = False
        if href.lower().endswith('.html') or href.lower().endswith('.xhtml'):
            text = re.sub(r'(?P<a><img[^>]* src[\n\t ]*=[\n\t ]*(?P<quo>[\'\"]))(?P<href>.+?)(?P<b>(?P=quo)[^>]*>)',sub_link,text)
            text = re.sub(r'(?P<a><image[^>]* xlink:href[\n\t ]*=[\n\t ]*(?P<quo>[\'\"]))(?P<href>.+?)(?P<b>(?P=quo)[^>]*>)',sub_link,text)
            text = re.sub(r'(?P<a>:[\n\t ]*url\( *(?P<quo>[\'\"])?)(?P<href>.+?)(?P<b>(?P=quo)? *\))',sub_link,text)
        elif href.lower().endswith('.css'):
            text = re.sub(r'(?P<a>:[\n\t ]*url\( *(?P<quo>[\'\"])?)(?P<href>.+?)(?P<b>(?P=quo)? *\))',sub_link,text)

        if substituted == True:
            bk.writefile(id,text)
    #修改 metadata 关联
    metadata = bk.getmetadataxml()
    t1 = re.search(r'<meta[^>]* name="cover"[^>]*/>',metadata)
    if t1 is not None:
        t2 = re.search(r'content="(.*?)"',t1.group())
        if t2 is not None and t2.group(1) in converted_files['ID'].keys():
            new_metadata = metadata[0:t1.start()] + \
                            '<meta content="%s" name="cover"/>'%converted_files['ID'][t2.group(1)] + \
                            metadata[t1.end():]
            bk.setmetadataxml(new_metadata)


#添加转换格式的图片，思路是先删去旧图片及其在opf中的信息，再添加新图片及其在opf中的信息。
def add_converted_file(old_path,new_path,bk=None):
    if not bk:
        return
    root = bk._w.ebook_root
    old_bookpath = short_path(old_path,root)
    if bk.launcher_version() >= 20190927:
        old_id = bk.bookpath_to_id(old_bookpath)
    else:
        old_href = bk.get_relativepath(opf_bkpath,old_bookpath)
        old_id = bk.href_to_id(old_href)
    if old_id:
        bk.deletefile(old_id)
    filename = os.path.basename(new_path)
    new_id = filename
    new_id = 'x' + new_id if '0' <= new_id[0] <= '9' else new_id
    with open(new_path,'rb') as f:
        File = f.read()
        try:
            bk.addfile(new_id,filename,File)
        except Exception as e:
            print('\n\n  添加文件 \"%s\" 时出错！\n  错误原因： %s'%(filename,e))
            raise
    new_bookpath = bk.id_to_bookpath(new_id)
    return old_id,old_bookpath,new_id,new_bookpath

def size(file_path):
    return int(os.path.getsize(file_path))

def size_f(sz):
    if sz < 1000: # 文件大小在1000字节内
        return str(sz) + ' Bytes'
    elif sz < 10240: #文件大小在10KB内
        return ('%.2f'%(sz/1024)) + ' KB'
    elif sz < 102400: #文件大小在100KB内
        return ('%.1f'%(sz/1024)) + ' KB'
    elif sz < 1024000: # 文件大小在1000KB内
        return ('%d'%(sz/1024)) + ' KB'
    elif sz < 10485760: #文件大小在10MB内
        return ('%.2f'%(sz/1048576)) + ' MB'
    else:
        return ('%.1f'%(sz/1048576)) + ' MB'

def short_path(file_path,root = ''): 
    if root == '':
        return file_path
    else:
        root = re.split(r'[\\/]',root)
        path = re.split(r'[\\/]',file_path)
        while root and root[0] == path[0]:
            root.pop(0),path.pop(0)
        path = '/'.join(path)
        return path
        
def overwrite(src,target):
    target_dir = os.path.dirname(target)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    with open(target,'wb') as t:
        with open(src,'rb') as s:
            data = s.read()
            t.write(data)

def PosProcess(Obj = None,test_mode = False):
    # test_mode 测试模式下不会生成结果图片

    obj_is_a_book = False
    if type(Obj).__name__ == 'BookContainer' or type(Obj).__name__ == 'EpubBook':
        bk = Obj
        root = bk._w.ebook_root
        obj_is_a_book = True
    elif type(Obj) == str:
        bk = None
        root = Obj
        root = os.path.realpath(root)
    else:
        return

    if obj_is_a_book:
        global opf_bkpath
        if bk.launcher_version() >= 20190927:
            opf_bkpath = bk.get_opfbookpath()
        else:
            opf_bkpath = 'OEBPS/content.opf'

    converted_files = {'ID':{},'BOOKPATH':{}} # 记录格式转化的图片组

    COPY,CONV = True,False

    for log in LOG:
        log_text = '  '+short_path(log['SRC'],root)

        if log['OUT'] == None:
            log_text += '\n  该图片无指定任何操作，已忽略。\n\n'
            print(log_text)
            continue

        if isConverted(log):
            COPY,CONV = False,True
            log_text += ' 【{}转{}】'.format(log['SRC_FMT'],log['OUT_FMT'])
            
        if log['ROTATE']:
            log_text += ' 【右旋90度】' if log['ROTATE'] == 90 else ' 【旋转180度】' if log['ROTATE'] == 180 else ' 【左旋90度】'
        log_text += '\n'
        
        sz_1,sz_2 = size(log['SRC']),size(log['OUT'])
        per = round(abs(sz_1-sz_2)/sz_1*100,1)
        op = '减少' if sz_1 >= sz_2 else '增加'
        if log['ROTATE'] or CONV:
            temp_text = '  体积从 {sz_1} {op}到 {sz_2}，{op}了{per}%。'.format(op=op,sz_1=size_f(sz_1),sz_2=size_f(sz_2),per=str(per))
            if op == '增加':
                temp_text += '\n  '
                temp_text += '【图片旋转】' if log['ROTATE'] else ''
                temp_text += '【格式转化】' if CONV else ''
                temp_text += '后体积增大属正常现象，建议配合【质量压缩】或【无损压缩】控制图片体积。'
        elif sz_1 > sz_2:
            temp_text = '  体积从 {sz_1} 减少到 {sz_2}，减少了{per}%。'.format(sz_1=size_f(sz_1),sz_2=size_f(sz_2),per=per)
        else:
            temp_text = '  该图片已优化过，不需要再进行无损压缩。'
            COPY = False
        log_text += temp_text + '\n\n'

        if obj_is_a_book == True and COPY == True:
            overwrite(log['OUT'],log['SRC'])
        elif obj_is_a_book == True and CONV == True:
            old_id,old_bkpath,new_id,new_bkpath = add_converted_file(log['SRC'],log['OUT'],bk)
            converted_files['ID'][old_id] = new_id
            converted_files['BOOKPATH'][old_bkpath] = new_bkpath
        # 非sigil环境
        elif obj_is_a_book == False and test_mode == False:
            root_dir = os.path.join(os.path.dirname(root),'输出')
            basename = os.path.basename(log['OUT'])
            rel_dirname = os.path.dirname(os.path.relpath(log['SRC'],root))
            output_path = os.path.join(root_dir,rel_dirname,basename)
            overwrite(log['OUT'],output_path)

        COPY,CONV = True,False

        print(log_text)
    if obj_is_a_book and converted_files != {'ID':{},'BOOKPATH':{}}:
        modRelatedFile(bk,converted_files)
    return