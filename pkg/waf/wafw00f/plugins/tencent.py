
NAME = 'Tencent Cloud Firewall (Tencent Technologies)'


def is_waf(self):
    if self.matchContent(r'waf\.tencent\-?cloud\.com/'):
        return True

    return False
