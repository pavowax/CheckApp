
NAME = 'SquidProxy IDS (SquidProxy)'


def is_waf(self):
    if not self.matchHeader(('Server', r'squid(/[0-9\.]+)?')):
        return False

    if not self.matchContent(r'Access control configuration prevents your request'):
        return False

    return True
