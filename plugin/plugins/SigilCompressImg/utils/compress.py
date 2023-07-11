#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,errno,shutil,uuid
import subprocess
from threading import Thread
from io import BytesIO
from PIL import Image



if __name__ == "__main__":
    from complement import *
else:
    from utils.complement import *

TEMPDIR = make_temp_dir()
ALL_BASENAME = []
SUBPROCESS = []

if 'check_output' not in dir(subprocess):
    def f(*popenargs, **kwargs):
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get('args')
            if cmd is None:
                cmd = popenargs[0]
            raise subprocess.CalledProcessError(retcode, cmd)
        return output
    subprocess.check_output = f


def ImagesProcess(file_path,args):
    # args 键含义：
    # ROTATE    旋转 0 90 180 270
    # CONV      图片格式转JPEG、WEBP开关
    # CONV_RATE 图片转格式质量压缩率
    # CONV_LV  图片转格式无损压缩率 0为无压缩 1-7为有效级别
    # J_RATE    JPEG压缩质量比率
    # W_RATE    WEBP质量压缩比率
    # DEPTH     位深压缩 True or None
    # ULOSS     无损压缩开关
    # ULOSS_LV  无损压缩级别 (png 0-7 webp 0-9)
    # FORMAT    图片格式
    # OPERATE   操作数量，0则表示无任何操作

    #跳过不需要操作的图片

    blank_log = {'SRC':file_path,'OUT':None,'ROTATE':0}
    ignore_this_img = False

    #以下情况操作数减1
    #png,bmp进行质量压缩
    if args['FORMAT'] in ['PNG','BMP'] and (args['J_RATE'] or args['W_RATE']):
        args['OPERATE'] -= 1
    #转化格式不对应
    if args['FORMAT'] ==  args['CONV']:
        args['OPERATE'] -= 1
    #JPEG进行无损压缩
    if args['ULOSS'] and args['FORMAT'] == 'JPEG':
        args['OPERATE'] -= 1
    #非PNG进行位深压缩
    if args['DEPTH'] and args['FORMAT'] != 'PNG':
        args['OPERATE'] -= 1
    
    #操作数为0则不处理图片
    if args['OPERATE'] <= 0:
        ignore_this_img = True
    if ignore_this_img:
        basename = os.path.basename(file_path)
        ALL_BASENAME.append(basename.upper())
        return blank_log
    tempfile = None
    #返回值修饰
    def log(log_dic,src_fmt,out_fmt,rotate):
        log_dic['SRC_FMT'] = src_fmt
        log_dic['OUT_FMT'] = out_fmt
        log_dic['ROTATE'] = rotate if rotate else 0
        return log_dic
    #图片旋转处理
    def rotateImg(img,angle = 0):
        # Image.ROTATE_270 逆时针270度
        # Image.ROTATE_180 逆时针180度
        # Image.ROTATE_90  逆时针90度
        if angle == 90:
            return img.transpose(Image.ROTATE_270) #顺时针90度
        elif angle == 180:
            return img.transpose(Image.ROTATE_180) #顺时针180度
        elif angle == 270:
            return img.transpose(Image.ROTATE_90) #顺时针270度
        else:
            return img
    #创建临时中转文件
    def save_as_tmp(img,fmt): 
        tempfile = os.path.join(TEMPDIR,uuid.uuid4().hex + '.' + fmt.lower())
        img.save(tempfile, fmt,optimize=False)
        return tempfile

    if args['CONV'] == 'JPEG':
        if args['FORMAT'] in ['PNG','BMP','GIF','WEBP']:
            args['J_RATE'] = args['CONV_RATE']
    elif args['CONV'] == 'WEBP':
        if args['FORMAT'] in ['PNG','BMP','GIF','JPEG']:
            args['W_RATE'] = args['CONV_RATE']

    log_dic_seg = {
        'src_fmt':args['FORMAT'],
        'out_fmt':args['CONV'],
        'rotate':args['ROTATE'],
    }

    img = Image.open(file_path)

    #处理WEBP
    if ( args['FORMAT'] == 'WEBP' and args['CONV'] is None ) or args['CONV'] == 'WEBP':
        
        uloss_lv = None
        qlty_rate = None
        if args['FORMAT'] != 'WEBP':
            if  args['CONV']:
                # 无损压缩级别控制，转格式图片【格式转换】的无损设定优先于【无损压缩】设定
                if args['CONV_LV'] is not None:
                    uloss_lv = args['CONV_LV']
                # 质量压缩控制，转格式图片【格式转换】的压缩设定优先于【质量压缩】设定
                else:
                    qlty_rate = args['CONV_RATE']
        else:
            if args['ULOSS']:
                uloss_lv = args['ULOSS_LV']
            if args['W_RATE']:
                qlty_rate = args['W_RATE']

        if args['ROTATE'] in [90,180,270] or args['FORMAT'] == 'BMP':
            if args['ROTATE'] in [90,180,270]:
                img = rotateImg(img,args['ROTATE'])
            tempfile = save_as_tmp(img, 'PNG')
            result_dict = encode_webp(file_path,qlty_rate,uloss_lv,tempfile = tempfile,conv = args['CONV'])
        else:
            result_dict = encode_webp(file_path,qlty_rate,uloss_lv,conv = args['CONV'])
        return log(result_dict, **log_dic_seg)

    #处理PNG
    if (args['FORMAT'] == 'PNG' and args['CONV'] is None) or args['CONV'] == 'PNG':

        uloss_lv = None
        if args['FORMAT'] != 'PNG':
            #这里控制转化图片的无损压缩设定优先于【无损压缩】设置
            if args['CONV']:
                uloss_lv = args['CONV_LV']
                if uloss_lv == 0:
                    args['ULOSS'] = None
        else:
            if args['ULOSS']:
                uloss_lv = args['ULOSS_LV']

        if args['DEPTH'] == True: # 位深压缩最优先，以便传输二进制数据给后续
            if args['FORMAT'] != 'PNG' and args['CONV'] == 'PNG':
                tempfile = tempfile = save_as_tmp(img, 'PNG')
                img = png_quant(tempfile)
            else:
                img = png_quant(file_path)

        if args['ROTATE'] in [90,180,270]:
            img = rotateImg(img,args['ROTATE'])

        if args['ULOSS']: # 无损压缩
            if args['ROTATE'] or args['DEPTH'] or args['CONV']:
                #必须通过创建临时文件中转的情况
                tempfile = save_as_tmp(img, 'PNG')
                return log(optimize_png(file_path,uloss_lv,tempfile=tempfile),**log_dic_seg)
            else:
                return log(optimize_png(file_path,uloss_lv), **log_dic_seg)
        else: #位深压缩或旋转
            basename = os.path.basename(file_path)
            if args['CONV'] is not None:
                basename = os.path.splitext(basename)[0] + '.png'
            basename = auto_rename(basename)
            outfile = os.path.join(TEMPDIR,basename)
            img.save(outfile,'PNG',optimize=True)
            return log( {'SRC':file_path,'OUT':outfile,'ROTATE':0} , **log_dic_seg)

    #处理BMP
    if args['FORMAT'] == 'BMP' and args['ULOSS'] and args['CONV'] is None:
        if args['ROTATE'] in [90,180,270]:
            img = rotateImg(img,args['ROTATE'])
        if args['ROTATE']:
            #必须通过创建临时文件中转的情况
            tempfile = save_as_tmp(img, 'BMP')
            return log(optimize_png(file_path,args['ULOSS_LV'],tempfile=tempfile),**log_dic_seg)
        else:
            return log(optimize_png(file_path,args['ULOSS_LV']), **log_dic_seg)
    #处理JPEG
    if ( args['FORMAT'] == 'JPEG' and args['CONV'] is None ) or args['CONV'] == 'JPEG':

        if args['ROTATE'] in [90,180,270]:
            img = rotateImg(img,args['ROTATE'])

        if args['CONV'] is not None:
            img = img.convert('RGB')

        basename = os.path.basename(file_path)
        if args['CONV'] is not None:
            basename = os.path.splitext(basename)[0] + '.jpg'
        basename = auto_rename(basename)
        outfile = os.path.join(TEMPDIR,basename)
        img.save(outfile,'JPEG',quality=args['J_RATE'] or 100)
        return log( {'SRC':file_path,'OUT':outfile,'ROTATE':0} , **log_dic_seg)

def optimize_png(file_path, level=1,tempfile = None , conv = None):
    #level goes from 1 to 7 with 7 being maximum compression
    exe = os.path.join(os.path.dirname(__file__),'optipng.exe')
    cmd = [exe] + '-fix -clobber -strip all -o{} -out'.format(level or 1).split() + [False, True]
    return run_optimizer(file_path,cmd,tempfile,conv)

def encode_webp(file_path, quality = None, uloss_lv = None,  tempfile = None , conv = None):
    # uloss_lv 0级为无压缩
    exe = os.path.join(os.path.dirname(__file__),'cwebp.exe')
    if quality:
        cmd = [exe] + '-q {} -m 4 -quiet -mt'.format(quality).split() + [True,'-o',False]
    else:
        cmd = [exe] + '-z {} -lossless -quiet -mt'.format(uloss_lv or 0).split() + [True,'-o',False]
    return run_optimizer(file_path,cmd,tempfile,conv)


def png_quant(file_path):
    exe = os.path.join(os.path.dirname(__file__),'pngquant.exe')
    cmd = [exe,'--force','256','-','<',file_path]
    compressed_data = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    img = Image.open(BytesIO(compressed_data))
    return img

def run_optimizer(file_path, cmd, tempfile = None , conv = None):
    file_path = os.path.abspath(file_path)
    if tempfile:
        tempfile = os.path.abspath(tempfile)
    cwd = TEMPDIR
    basename = os.path.basename(file_path)
    if conv == 'JPEG':
        basename = os.path.splitext(basename)[0] + '.jpeg'
    elif conv == 'WEBP':
        basename = os.path.splitext(basename)[0] + '.webp'
    basename = auto_rename(basename)
    ext = os.path.splitext(file_path)[1] 
    outfile = os.path.join(TEMPDIR,basename)
    if not os.path.exists(outfile):
        open(outfile,'w+').close()
    fd = os.open(outfile,os.O_RDWR)
    try:
        os.close(fd)
        if tempfile:
            infile, oname = tempfile, os.path.basename(outfile)
        else:
            infile, oname = file_path, os.path.basename(outfile)

        def repl(q, r):
            #将cmd元组中的True值对应位置替换为输入名，False值对应位置替换为输出名。
            cmd[cmd.index(q)] = r
        repl(True, infile), repl(False, oname)

        p = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=None, creationflags=subprocess.DETACHED_PROCESS)
        SUBPROCESS.append(p)
        stderr = p.stdout
        raw = force_unicode(stderr.read())

        if p.wait() != 0:
            print('!!!文件 \"%s\" 处理失败'%file_path)
            processor = os.path.basename(cmd[0])
            print('%s 错误提示：\n%s'%(processor,raw))
            raise
        else:
            shutil.copystat(file_path, outfile)
            return {'SRC':file_path,'OUT':outfile,'ROTATE':0}
    except Exception as e:
        print(e)
        raise
    finally:
        try:
            os.remove(outfile + '.bak')  # optipng creates these files
        except EnvironmentError as err:
            if err.errno != errno.ENOENT:
                raise

def auto_rename(basename):
    if basename.upper() in ALL_BASENAME:
        filename,ext = os.path.splitext(basename)
        Len = len(filename)
        for i in range(Len-1,-1,-1):
            char = filename[i]
            if '0' <= char <= '9':
                continue
            elif char == '_':
                break
            else:
                i = Len
                break
        filename = filename[0:i]
        order = 1
        while (filename + '_' + str(order) + ext).upper() in ALL_BASENAME:
            order += 1
        ALL_BASENAME.append((filename + '_' + str(order) + ext).upper())
        return filename+'_' + str(order)+ext
    else:
        ALL_BASENAME.append(basename.upper())
        return basename

if __name__ == "__main__":
    pass