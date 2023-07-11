#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, posixpath, re, string
from sigil_bs4 import BeautifulSoup

# borrowed from Calibre/Access-Aide plugin
def cleanup_file_name(name):
    ''' generates safe file names and ids '''
    _filename_sanitize = re.compile(r'[\xae\0\\|\?\*<":>\+/]')
    substitute='_'
    one = ''.join(char for char in name if char in string.printable)
    one = _filename_sanitize.sub(substitute, one)
    one = re.sub(r'\s', '_', one).strip()
    one = re.sub(r'^\.+$', '_', one)
    one = one.replace('..', substitute)
    # Windows doesn't like path components that end with a period
    if one.endswith('.'):
        one = one[:-1]+substitute
    # Mac and Unix don't like file names that begin with a full stop
    if len(one) > 0 and one[0:1] == '.':
        one = substitute+one[1:]
    return one

def run(bk):
    ''' main routine '''
    # get relative css folder path
    text = bk.group_to_folders('Text')[0]
    styles = bk.group_to_folders('Styles')[0]
    relativepath = posixpath.relpath(styles, text)
    last_style_contents = None
    last_css_href = None

    # process all html files
    for html_id, href in list(bk.text_iter()):
        html = bk.readfile(html_id)
        html_file_name = os.path.basename(href)
        css_file_name = cleanup_file_name(os.path.splitext(html_file_name)[0] + '.css')

        # parse html with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # find style tag
        style_tag = soup.find('style')

        # only process non-empty style tags
        if style_tag and len(style_tag) == 1:
            style_contents = style_tag.contents[0]
            if style_contents.strip() != '':

                # create new link tag
                if not style_contents == last_style_contents:
                    css_href = relativepath + '/' + css_file_name
                else:
                    css_href = last_css_href
                attributes = {'href' : css_href ,'type' : 'text/css', 'rel' : 'stylesheet'}
                link_tag = soup.new_tag('link', **attributes)

                # replace style tag with link tag
                style_tag.replace_with(link_tag)

                # update html file
                bk.writefile(html_id, str(soup.prettyprint_xhtml(indent_level=0, 
                    eventual_encoding="utf-8", formatter="minimal", indent_chars="  ")))
                print(html_file_name, 'updated')

                # add css file
                if not style_contents == last_style_contents:
                    bk.addfile(css_file_name, css_file_name, style_contents, 'text/css')
                    print(css_file_name, 'added')

                # save last style sheet info
                last_style_contents = style_contents
                last_css_href = css_href

    print('\nPlease click OK to close the Plugin Runner window.')

    return 0

def main():
    print('I reached main when I should not have\n')
    return -1

if __name__ == "__main__":
    sys.exit(main())
