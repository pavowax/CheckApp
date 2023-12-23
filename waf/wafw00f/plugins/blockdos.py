
NAME = 'BlockDoS (BlockDoS)'


def is_waf(self):
    if self.matchHeader(('Server', r'blockdos\.net')):
        return True

    return False
