
NAME = 'HyperGuard (Art of Defense)'


def is_waf(self):
    if self.matchCookie('^WODSESSION='):
        return True

    return False
