
NAME = 'DynamicWeb Injection Check (DynamicWeb)'


def is_waf(self):
    if self.matchHeader(('X-403-Status-By', r'dw.inj.check'), attack=True):
        return True

    if self.matchContent(r'by dynamic check(.{0,10}?module)?'):
        return True

    return False
