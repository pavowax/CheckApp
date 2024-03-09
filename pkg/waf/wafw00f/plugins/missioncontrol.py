
NAME = 'Mission Control Shield (Mission Control)'


def is_waf(self):
    if self.matchHeader(('Server', 'Mission Control Application Shield')):
        return True

    return False
