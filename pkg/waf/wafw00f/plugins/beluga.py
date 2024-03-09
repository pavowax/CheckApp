
NAME = 'Beluga CDN (Beluga)'


def is_waf(self):
    if self.matchHeader(('Server', r'Beluga')):
        return True

    if self.matchCookie(r'^beluga_request_trail='):
        return True

    return False
