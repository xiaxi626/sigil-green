#!/Python3/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division, absolute_import, print_function

#********************************************************************************#
#                                                                                #
# MIT Licence(OSI)                                                               #
# Copyright (c) 2017 Bill Thompson                                               #
#                                                                                #
# Permission is hereby granted, free of charge, to any person obtaining a copy   # 
# of this software and associated documentation files (the "Software"), to deal  # 
# in the Software without restriction, including without limitation the rights   #
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell      #
# copies of the Software, and to permit persons to whom the Software is          #
# furnished to do so, subject to the following conditions:                       # 
#                                                                                #
# The above copyright notice and this permission notice shall be included in all #
# copies or substantial portions of the Software.                                #
#                                                                                # 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR     # 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,       #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE    #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER         # 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  # 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE  # 
# SOFTWARE.                                                                      #
#                                                                                #  
#********************************************************************************#


import os, os.path, sys, codecs, shutil, inspect, time
from tempfile import mkdtemp                  
from updater import updateCheck
import options
import tkinter as tk
import tkinter.messagebox as mbox

try:
    from sigil_bs4 import BeautifulSoup
except:
    from bs4 import BeautifulSoup  

SITE_URL = "https://www.mobileread.com/forums/showpost.php?p=4015437&postcount=1"
PLUGIN_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
options.PLUGIN_PATH = PLUGIN_PATH


def checkInternalLinks(bk, wdir): 
    print('\n\n>>> Running checkInternalLinks...')    

    # put epub ids into a list
    id_refs = getAllIDs(bk, wdir)
    
    # put epub file names into a list
    fnames_str = getFileNames(bk, wdir)
    
    #---------------------------------------------------------------------#
    # checks all xhtml file(incl. nav.xhtml) internal links for valid     # 
    # destination ids, valid file names and also flags any empty links    #
    #---------------------------------------------------------------------#
    
    for (id, href) in bk.text_iter():
        filename = os.path.basename(href)
        data = bk.readfile(id)
        soup = BeautifulSoup(data, 'html.parser')
        file_id = id        
                    
        # put all local file ids into a list    
        local_file_ids = []
        for atag in soup.find_all(id=True):
            local_file_ids.append(atag['id']) 
        
        # check all local link ids in the current file        
        print('\n\n>>> checking for bad local links...')            
        for atag in soup.body.find_all(href=True):
            if '#' in atag['href'] and \
                'http:' not in atag['href'] and \
                'https:' not in atag['href'] and \
                'mailto:' not in atag['href']:
                
                # check dest ids in local links like 'href="#myid"'
                if str(atag['href']).strip().startswith('#'):
                    href_id = str(atag['href']).lstrip('#')
                    for id in local_file_ids:
                        if href_id.strip() == id.strip():
                            break
                    else:                           
                        bk.add_result("error", filename, getLineNumber(data, str(atag)), "ERROR: Link > " + \
                                      "Link href:  " + atag['href'] + " (href destination id doesn't exist in the " \
                                      "current file or href is missing the correct file name)")
       
        # checks dest ids in links like '../Text/section-0005.xhtml#myid', 'Text/section-0005.xhtml#myid' and 'section-0005.xhtml#myid'
        print('\n\n>>> checking for bad link ids...')          
        for tag in soup.body.find_all(href=True):
            if 'http:' not in tag['href'] and \
                'https:' not in tag['href']  and \
                'mailto:' not in tag['href'] and \
                not str(tag['href']).startswith('#'):
                
                if '#' in tag['href'] and tag['href'].split('#')[1]:
                    lid = tag['href'].split('#')[1] 
                    for ref in id_refs:
                        if lid.strip() == ref.strip():
                            break
                    else:
                        bk.add_result("error", filename, getLineNumber(data, str(tag)), "ERROR: Bad Link > " + \
                                      "Link href:  " + tag['href'] + " (href destination id doesn't exist)")             

        # checks that the href filename exists
        print('\n\n>>> check href file names...')                  
        for tag in soup.body.find_all(href=True):    
            if 'http:' not in tag['href'] and \
                'https:' not in tag['href'] and \
                'mailto:' not in tag['href']:\
                
                # checks filenames in hrefs like '../Text/section-0005.xhtml#myid', 'Text/section-0005.xhtml' and 'section-0005.xhtml#myid'
                if '#' in tag['href']:
                    section, id = str(tag['href']).split('#')
                    section = section.replace('../Text/','')
                    section = section.replace('Text/','')                        
                    if section.replace(' ','') != '' and section != None: 
                        if section not in fnames_str:
                             bk.add_result('error', filename, getLineNumber(data, str(tag)), 'ERROR: Bad Filename > ' + \
                                           'Link href:  ' + tag['href'] + ' (href file name does not exist)')                      
                
                # checks filenames in page links like '../Text/section-0005.xhtml', 'Text/section-0005.xhtml' and 'section-0005.xhtml'               
                elif '#' not in tag['href']:
                    section = os.path.basename(tag['href'])
                    section = section.replace('../Text/','')     
                    section = section.replace('Text/','')                         
                    if section.replace(' ','') != '' and section != None: 
                        if section not in fnames_str:
                             bk.add_result('error', filename, getLineNumber(data, str(tag)), 'ERROR: Bad Filename > ' + \
                                           'Link href:  ' + tag['href'] + ' (href file name does not exist)') 

        # find and flag any empty links 
        print('\n\n>>> checking for empty links...')                  
        for tag in soup.body.find_all(href=True):
            if str(tag['href']).replace(' ','') == '':
                bk.add_result('error', filename, getLineNumber(data, tag.get_text()), 'ERROR: Empty Link > ' + \
                              'Link text:  &quot;' + tag.get_text().strip() + '&quot; (href contains nothing)')               
      
    checkNCXTOCLinks(bk, wdir)
    return(0)
    
def checkNCXTOCLinks(bk, wdir):
    print('\n\n>>> Running checkTOCNCXLinks()...')
    fname = 'toc.ncx'    
    fnames_str = getFileNames(bk, wdir)
    ids = getAllIDs(bk, wdir)
    
    data = bk.readfile(bk.gettocid())
    xml = BeautifulSoup(data, 'xml')    
    
    #-----------------------------------------------------#
    # checks all ncx src links for valid destination ids, # 
    # valid file names and also flags any empty links     #
    #-----------------------------------------------------#
           
    for tag in xml.find_all('navPoint'):
        for href in tag.find_all('content', limit=1):
            
            # checks destination ids in src links like 'Text/section-0005.xhtml#myid' and 'section-0005.xhtml#myid'
            if '#' in href['src']:
                lid = href['src'].split('#')[1]                
                for ref in ids:
                    if lid.strip() == ref.strip():
                        break
                else:
                    bk.add_result('error', fname, getLineNumber(data, href['src']), 'ERROR: Bad NCX Link > ' + 'Link src:  ' + \
                                  href['src'] + ' (src destination id does not exist)')
                                  
            # checks filenames in src links like 'Text/section-0005.xhtml#myid' and 'section-0005.xhtml#myid'
            if '#' in href['src']:
                section, id = str(href['src']).split('#')
                section = section.replace('Text/','')         
                if section != '' and section != None:                       
                    if section not in fnames_str: 
                         bk.add_result('error', fname, getLineNumber(data, href['src']), 'ERROR: Bad Filename > ' + \
                                       'Link src:  ' + href['src'] + ' (src file name does not exist)')
            
            # checks filenames in page links like 'Text/section-0005.xhtml' or 'section-0005.xhtml'               
            elif '#' not in href['src']:
                section = os.path.basename(href['src'])
                section = section.replace('Text/','').strip()                    
                if section != '' and section != None: 
                    if section not in fnames_str:
                         bk.add_result('error', fname, getLineNumber(data, href['src']), 'ERROR: Bad Filename > ' + \
                                       'Link src:  ' + href['src'] + ' (src file name does not exist)')

            # find any empty src links              
            if str(href['src']).replace(' ','') == '':
                text = tag.find('text').get_text().strip()
                bk.add_result('error', fname, getLineNumber(data, str(href)), 'ERROR: Empty Link > ' + \
                              'Link text:  &quot;' + text + '&quot; (src link contains nothing)')
                                                  
    return(0)     
    
def getAllIDs(bk, wdir):
    print('>>> Running getAllIDs()...')    
    ids = []
    all_ids_list = []
    
    for (id, href) in bk.text_iter():
        filename = os.path.basename(href)
        data = bk.readfile(id)
        soup = BeautifulSoup(data, 'html.parser')

        for tag in soup.body.find_all(id=True):
            ids.append(tag['id'])
            
        all_ids_list.extend(ids)        
     
    return(all_ids_list)  
    
def getFileNames(bk, wdir):
    print('>>> Running getFileNames()...') 
    filenames = []
    
    for (id, href) in bk.text_iter():
        filenames.append(os.path.basename(href.strip()))
    fnames_str = " ".join(filenames)
    
    return(fnames_str)    
            
def getLineNumber(html, text):
    print('>>> Running getLineNumber()...') 
    lines = html.splitlines()
    linum = int()
    
    for index, line in enumerate(lines):
        if text in line:
            linum = index + 1 
           
    return(str(linum))    
     
def show_msgbox(title, msg, msgtype='info'):
    """ For general information, warnings and errors
    """
    localRoot = tk.Tk()
    localRoot.withdraw()
    localRoot.option_add('*font', 'Helvetica -12')
    localRoot.quit()
    if msgtype == 'info':
        return(mbox.showinfo(title, msg))
    elif msgtype == 'warning':
        return(mbox.showwarning(title, msg))
    elif msgtype == 'error':
        return(mbox.showerror(title, msg))
        
def cleanExit(wdir):
    shutil.rmtree(wdir, ignore_errors=True)
    return(0)    
     
def is_connected():
    try:
        sock = socket.create_connection(('8.8.8.8', 53), 1)
        sock.close()
        return True
    except:
        pass

    return(False)        
    
def run(bk):
    print('Python version: ', sys.version, '\n')
    print('Running CheckInternalLinks...\n')
    
    if is_connected: 
        #check for new plugin versions
        latest_version, installed_version = updateCheck(SITE_URL, PLUGIN_PATH)
        if latest_version and latest_version != installed_version:
            options.NEW_PLUGIN_VERSION = True
            options.MSG_NEW_VERSION_AVAILABLE = "A new plugin version is now available from MR - v" + latest_version 

    fnames = []
    for id, href in bk.text_iter():
        fnames.append(os.path.basename(href))
            
    # default epub error    
    if len(fnames) == 1 and fnames[0] == 'Section0001.xhtml':
        msg = 'Default epub contains no data. Please try again.'
        print('\n>>> File Type Error: ' + msg + '\n\nAbort plugin...')
        show_msgbox('Error', msg, msgtype='error')
        cleanExit(WDIR)
        return(0)    
        
    # check the file type -- html or epub
    if len(fnames) == 1:
        msg = 'Epub contains insufficient data or is the wrong file type.\n\nPlease try again.'
        print('\n>>> File Type Error: ' + msg + '\n\nAbort plugin...')
        show_msgbox('File Type Error', msg, msgtype='error')
        cleanExit(WDIR)
        return(0)    
        
    # create a working directory
    WDIR = mkdtemp()

    # process the user selected task
    checkInternalLinks(bk, WDIR)             
    
    if options.SYS_EXIT == True:
       cleanExit(WDIR)
       return(0)        
    
    # inform user if new plugin version is available
    if options.NEW_PLUGIN_VERSION == True:
        msg = options.MSG_NEW_VERSION_AVAILABLE
        show_msgbox('CheckInternalLinks', msg, msgtype='info') 
        
    
    print('\n -- Completed SUCCESSFULLY...')
    cleanExit(WDIR)
    return(0)                
    
def main():
    print('I reached main when I should not have\n')
    return(-1)

if __name__ == "__main__":
    sys.exit(main())                         