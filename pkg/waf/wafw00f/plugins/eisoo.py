
NAME = 'Eisoo Cloud Firewall (Eisoo)'


def is_waf(self):
    if self.matchHeader(('Server', r'EisooWAF(\-AZURE)?/?')):
        return True

    if self.matchContent(r'<link.{0,10}?href=\"/eisoo\-firewall\-block\.css'):
        return True

    if self.matchContent(r'www\.eisoo\.com'):
        return True

    if self.matchContent(r'&copy; \d{4} Eisoo Inc'):
        return True

    return False
