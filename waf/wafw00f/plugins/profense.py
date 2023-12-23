
NAME = 'Profense (ArmorLogic)'


def is_waf(self):
    if self.matchHeader(('Server', 'Profense')):
        return True

    if self.matchCookie(r'^PLBSID='):
        return True

    return False
