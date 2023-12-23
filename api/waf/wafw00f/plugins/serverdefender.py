
NAME = 'ServerDefender VP (Port80 Software)'


def is_waf(self):
    if self.matchHeader(('X-Pint', r'p(ort\-)?80')):
        return True

    return False
