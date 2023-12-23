
NAME = 'NinjaFirewall (NinTechNet)'


def is_waf(self):
    if not self.matchContent(r'<title>NinjaFirewall.{0,10}?\d{3}.forbidden'):
        return False

    if not self.matchContent(r'For security reasons?.{0,10}?it was blocked and logged'):
        return False

    return True
