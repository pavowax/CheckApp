
NAME = 'KeyCDN (KeyCDN)'


def is_waf(self):
    if self.matchHeader(('Server', 'KeyCDN')):
        return True

    return False
