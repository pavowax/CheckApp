
NAME = 'Palo Alto Next Gen Firewall (Palo Alto Networks)'


def is_waf(self):
    if self.matchContent(r'Download of virus.spyware blocked'):
        return True

    if self.matchContent(r'Palo Alto Next Generation Security Platform'):
        return True

    return False
