
NAME = 'ArvanCloud (ArvanCloud)'


def is_waf(self):
    if self.matchHeader(('Server', 'ArvanCloud')):
        return True

    return False
