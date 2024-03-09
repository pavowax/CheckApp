
NAME = 'BitNinja (BitNinja)'


def is_waf(self):
    if self.matchContent(r'Security check by BitNinja'):
        return True

    if self.matchContent(r'Visitor anti-robot validation'):
        return True

    return False
