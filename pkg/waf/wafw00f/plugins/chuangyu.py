
NAME = 'Chuang Yu Shield (Yunaq)'


def is_waf(self):
    if self.matchContent(r'www\.365cyd\.com'):
        return True

    if self.matchContent(r'help\.365cyd\.com/cyd\-error\-help.html\?code=403'):
        return True

    return False
