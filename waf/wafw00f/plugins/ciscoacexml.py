
NAME = 'ACE XML Gateway (Cisco)'


def is_waf(self):
    if self.matchHeader(('Server', 'ACE XML Gateway')):
        return True

    return False
