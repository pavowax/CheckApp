
NAME = 'Imunify360 (CloudLinux)'


def is_waf(self):
    if self.matchHeader(('Server', r'imunify360.{0,10}?')):
        return True

    if self.matchContent(r'protected.by.{0,10}?imunify360'):
        return True

    if self.matchContent(r'powered.by.{0,10}?imunify360'):
        return True

    if self.matchContent(r'imunify360.preloader'):
        return True

    return False
