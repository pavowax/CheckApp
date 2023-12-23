
NAME = 'NetContinuum (Barracuda Networks)'


def is_waf(self):
    if self.matchCookie(r'^NCI__SessionId='):
        return True

    return False
