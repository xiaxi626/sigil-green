#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division, absolute_import, print_function

import sys
import os
import re
import inspect
from datetime import datetime, timedelta
try:
    import urllib.request as url_request
except ImportError:
    import urllib2 as url_request


_latest_pattern = re.compile(r'Current Version:\s*&quot;([^&]*)&')
_version_pattern = re.compile(r'<version>([^<]*)</version>')
_last_update_check = re.compile(r'<version>([^<]*)</version>')

def updateCheck(site_url, plugin_path):
    latest_version = None
    installed_version = None
   
    try:
        # get the latest version from the MR website page
        req = url_request.Request(site_url)
        response = url_request.urlopen(req)
        web_page = response.read().decode('utf-8', 'ignore')
        m = _latest_pattern.search(web_page)
        if m:
            latest_version = (m.group(1).strip())

        # get installed version of plugin
        plugin_path = os.path.join(plugin_path, "plugin.xml")
        with open(plugin_path,'rb') as f:
            data = f.read().decode('utf-8')
            m = _version_pattern.search(data)
            if m:
                installed_version = m.group(1).strip()
    except:
        pass

    return(latest_version, installed_version)
