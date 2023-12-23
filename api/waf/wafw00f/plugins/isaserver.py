
NAME = 'ISA Server (Microsoft)'


def is_waf(self):
    if self.matchContent(r'The.{0,10}?(isa.)?server.{0,10}?denied the specified uniform resource locator \(url\)'):
        return True

    return False
