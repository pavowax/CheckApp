
NAME = 'Qiniu (Qiniu CDN)'


def is_waf(self):
    if self.matchHeader(('X-Qiniu-CDN', r'\d+?')):
        return True

    return False
