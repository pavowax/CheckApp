
NAME = 'Anquanbao (Anquanbao)'


def is_waf(self):
    if self.matchHeader(('X-Powered-By-Anquanbao', '.+?')):
        return True

    if self.matchContent(r'aqb_cc/error/'):
        return True

    return False
