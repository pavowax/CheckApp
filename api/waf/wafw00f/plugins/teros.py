
NAME = 'Teros (Citrix Systems)'


def is_waf(self):
    if self.matchCookie(r'^st8id='):
        return True

    return False
