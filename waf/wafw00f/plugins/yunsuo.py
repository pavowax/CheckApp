
NAME = 'Yunsuo (Yunsuo)'


def is_waf(self):
    if self.matchCookie(r'^yunsuo_session='):
        return True

    if self.matchContent(r'class=\"yunsuologo\"'):
        return True

    return False
