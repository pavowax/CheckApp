
NAME = 'Wallarm (Wallarm Inc.)'


def is_waf(self):
    if self.matchHeader(('Server', r'nginx[\-_]wallarm')):
        return True

    return False
