
NAME = 'NevisProxy (AdNovum)'


def is_waf(self):
    if self.matchCookie(r'^Navajo'):
        return True

    if self.matchCookie(r'^NP_ID'):
        return True

    return False
