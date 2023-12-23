
NAME = 'Barikode (Ethic Ninja)'


def is_waf(self):
    if self.matchContent(r'<strong>barikode<.strong>'):
        return True

    return False
