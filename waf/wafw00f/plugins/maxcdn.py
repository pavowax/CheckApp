
NAME = 'MaxCDN (MaxCDN)'


def is_waf(self):
    if self.matchHeader(('X-CDN', r'maxcdn')):
        return True

    return False
