
NAME = 'AzionCDN (AzionCDN)'


def is_waf(self):
    if self.matchHeader(('Server', r'Azion([-_]CDN)?')):
        return True

    return False
