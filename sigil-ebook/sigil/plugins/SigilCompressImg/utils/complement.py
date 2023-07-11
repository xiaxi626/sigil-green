import sys,os,tempfile,locale,codecs

filesystem_encoding = sys.getfilesystemencoding()
if filesystem_encoding is None:
    filesystem_encoding = 'utf-8'

try:
    preferred_encoding = locale.getpreferredencoding()
    codecs.lookup(preferred_encoding)
except:
    preferred_encoding = 'utf-8'

class ReadOnlyFileBuffer(object):
    # A zero copy implementation of a file like object. Uses memoryviews for efficiency. 

    def __init__(self, raw):
        self.sz, self.mv = len(raw), (raw if isinstance(raw, memoryview) else memoryview(raw))
        self.pos = 0

    def tell(self):
        return self.pos

    def read(self, n=None):
        if n is None:
            ans = self.mv[self.pos:]
            self.pos = self.sz
            return ans
        ans = self.mv[self.pos:self.pos+n]
        self.pos = min(self.pos + n, self.sz)
        return ans

    def seek(self, pos, whence=os.SEEK_SET):
        if whence == os.SEEK_SET:
            self.pos = pos
        elif whence == os.SEEK_END:
            self.pos = self.sz + pos
        else:
            self.pos += pos
        self.pos = max(0, min(self.pos, self.sz))
        return self.pos

    def getvalue(self):
        return self.mv

    def close(self):
        pass

def get_pre_enc():
    try:
        preferred_encoding = locale.getpreferredencoding()
        codecs.lookup(preferred_encoding)
    except:
        preferred_encoding = 'utf-8'
    return preferred_encoding

def force_unicode(obj, enc=get_pre_enc()):

    def isbytestring(obj):
        return isinstance(obj, bytes)

    if isbytestring(obj):
        try:
            obj = obj.decode(enc)
        except Exception:
            try:
                obj = obj.decode(filesystem_encoding if enc ==
                        preferred_encoding else preferred_encoding)
            except Exception:
                try:
                    obj = obj.decode('utf-8')
                except Exception:
                    obj = repr(obj)
                    if isbytestring(obj):
                        obj = obj.decode('utf-8')
    return obj

def make_temp_dir():
    temp_dir = tempfile.mktemp()
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)
    return temp_dir