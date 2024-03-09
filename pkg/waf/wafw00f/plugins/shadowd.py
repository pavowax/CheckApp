
NAME = 'Shadow Daemon (Zecure)'


def is_waf(self):
    if not self.matchContent(r"<h\d{1}>\d{3}.forbidden<.h\d{1}>"):
        return False

    if not self.matchContent(r"request forbidden by administrative rules"):
        return False

    return True
