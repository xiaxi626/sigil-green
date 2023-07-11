#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, re, posixpath
from fontTools import ttLib

#==============================================================
# code from http://ttfquery.sourceforge.net/_modules/ttfquery/describe.html#family
#==============================================================

FONT_SPECIFIER_NAME_ID = 4
FONT_SPECIFIER_FAMILY_ID = 1

def shortName(font):
    """Get the short name from the font's names table"""
    name = ""
    family = ""
    for record in font['name'].names:
        if record.nameID == FONT_SPECIFIER_NAME_ID and not name:
            if b'\000' in record.string:
                name = record.string.decode('utf-16-be')
            else:
                name = record.string.decode('utf-8')
        elif record.nameID == FONT_SPECIFIER_FAMILY_ID and not family:
            if b'\000' in record.string:
                family = record.string.decode('utf-16-be')
            else:
                family = record.string.decode('utf-8')
        if name and family:
            break
    return name, family


def modifiers(font):
    """Get weight and italic modifiers for a font"""
    return (
        # weight as an integer
        font['OS/2'].usWeightClass,
        ( # italic
            font['OS/2'].fsSelection &1 or
            font['head'].macStyle&2
        ),
    )

# main routine
def run(bk):
    ''' main routine '''
    font_css = ''
    ps_fonts = []

    # get relative paths for non-standard epubs
    if  bk.launcher_version() >= 20190927:
        styles = bk.group_to_folders('Styles')[0]
        fonts = bk.group_to_folders('Fonts')[0]
        relativepath = posixpath.relpath(fonts, styles)
    else:
        relativepath = '../Fonts'


    # get all fonts
    font_manifest_items = []
    font_manifest_items = list(bk.font_iter())

    # fonts aren't found by bk.font_iter(), if they have the
    # wrong mime type, e.g. 'application/octet-stream'
    if font_manifest_items == []:
        for manifest_id, href, mime in bk.manifest_iter():
            if href.endswith('tf'):
                font_manifest_items.append((manifest_id, href, mime))

    # process all manifested fonts in the Fonts folder
    ebook_root = bk._w.ebook_root

    for manifest_id, href, mime in font_manifest_items:
        font_file_name = os.path.basename(href)

        # sigil 1.x (and higher) supports custom font folders
        if  bk.launcher_version() >= 20190927:
            font_path = os.path.join(bk._w.ebook_root, bk.id_to_bookpath(manifest_id))
        else:
            font_path = os.path.join(ebook_root, 'OEBPS', href)

        print('\nProcessing font: ', font_file_name +  '...')

        # create font object
        try:
            tt = ttLib.TTFont(font_path)

            # get font data
            font_name, font_family = shortName(tt)
            weight, italic = modifiers(tt)

            # display font information
            if tt.sfntVersion == 'OTTO':
                print('\nPostScript font: True\nFamily: {}\nName: {}\nWeight: {}\nItalic: {}'\
                    .format(font_family, font_name, weight, italic == 1))
                if font_family not in ps_fonts:
                    ps_fonts.append(font_family)
            else:
                print('\nFamily: {}\nName: {}\nWeight: {}\nItalic: {}'\
                    .format(font_family, font_name, weight, italic == 1))

            # write font family
            font_css += '@font-face {\n    font-family: ' + "'" + font_family  + "';\n"

            # write font weight
            if weight == 400:
                font_css += '    font-weight: normal;\n'
            elif weight == 700:
                font_css += '    font-weight: bold;\n'
            else:
                font_css += '    font-weight: {};\n'.format(str(weight))

            # write font style (since there is no 'oblique' propery; we'll have to guess)
            if 'oblique' in font_name.lower():
                font_css += '    font-style: oblique;\n'
            elif italic == 1:
                font_css += '    font-style: italic;\n'
            else:
                font_css += '    font-style: normal;\n'

            # write font url
            font_css += "    src: url(" + relativepath + '/' + font_file_name + ");\n}\n\n"

        except Exception as ex:
            exception_info = "\n*** PYTHON ERROR ***\nAn exception of type\
 {0} occurred.\nArguments: {1!r}".format(type(ex).__name__, ex.args)
            print(exception_info)

    #============================
    # add/ update style sheet
    #============================

    if font_css != '':
        # uncomment the next line for double quotes
        #font_css = font_css.replace("'", '"')

        # check for Type 1 CFF fonts; for more information
        # see https://blog.typekit.com/2005/10/06/phasing_out_typ
        if ps_fonts != []:
            print('\nType 1 fonts found!\n\nThe font folder contains the following Type 1\
 (Postscript) fonts: {}.\n(Amazon KDP advises against using Type 1\
 (Postscript) fonts.)'.format(', '.join(ps_fonts)))

        # find the first stylesheet
        first_id = None
        css_iter_list = list(bk.css_iter())
        if len(css_iter_list) != 0:
            first_id = css_iter_list[0][0]
            basename = os.path.basename(css_iter_list[0][1])

        if not first_id or first_id == 'sgc-nav.css':
            # add font declarations to a new stylesheet
            basename = 'font.css'
            bk.addfile(basename, basename, str(font_css), 'text/css')
            print('\nNew stylesheet font.css added.\n')
        else:
            # add font declarations to the first stylesheet
            data = str(bk.readfile(first_id))
            # remove existing font declarations
            data = re.sub(r'\s*@font-face\s*\{\s*[^\}]+\}\s*', '', data)
            bk.writefile(first_id, font_css + data)
            print('\nStylesheet ' + basename + ' updated.\n')

    else:
        print('No fonts found!')

    print('\nClick OK to close.')

    return 0

def main():
    print('I reached main when I should not have\n')
    return -1

if __name__ == "__main__":
    sys.exit(main())
