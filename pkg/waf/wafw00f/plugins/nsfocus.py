
NAME = 'NSFocus (NSFocus Global Inc.)'


def is_waf(self):
    if self.matchHeader(('Server', 'NSFocus')):
        return True

    return False
