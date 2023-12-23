
NAME = 'WebSEAL (IBM)'


def is_waf(self):
    if self.matchHeader(('Server', 'WebSEAL')):
        return True

    if self.matchContent(r"This is a WebSEAL error message template file"):
        return True

    if self.matchContent(r"WebSEAL server received an invalid HTTP request"):
        return True

    return False
