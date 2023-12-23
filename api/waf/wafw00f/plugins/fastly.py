
NAME = 'Fastly (Fastly CDN)'


def is_waf(self):
    if self.matchHeader(('X-Fastly-Request-ID', r'\w+')):
        return True

    return False
