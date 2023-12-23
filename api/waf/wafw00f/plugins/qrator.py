
NAME = 'Qrator (Qrator)'


def is_waf(self):
    if self.matchHeader(('Server', r'QRATOR')):
        return True

    return False
