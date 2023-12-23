
NAME = 'West263 CDN (West263CDN)'


def is_waf(self):
    if self.matchHeader(('X-Cache', r'WS?T263CDN')):
        return True

    return False
