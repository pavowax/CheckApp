
NAME = 'LimeLight CDN (LimeLight)'


def is_waf(self):
    if self.matchCookie(r'^limelight'):
        return True

    if self.matchCookie(r'^l[mg]_sessid='):
        return True

    return False
