
NAME = 'DataPower (IBM)'


def is_waf(self):
    if self.matchHeader(('X-Backside-Transport', r'(OK|FAIL)')):
        return True

    return False
