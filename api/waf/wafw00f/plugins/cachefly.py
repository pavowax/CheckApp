
NAME = 'CacheFly CDN (CacheFly)'


def is_waf(self):
    if self.matchHeader(('BestCDN', r'Cachefly')):
        return True

    if self.matchCookie(r'^cfly_req.*='):
        return True

    return False
