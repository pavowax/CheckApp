
NAME = 'Huawei Cloud Firewall (Huawei)'


def is_waf(self):
    if self.matchCookie(r'^HWWAFSESID='):
        return True

    if self.matchHeader(('Server', r'HuaweiCloudWAF')):
        return True

    if self.matchContent(r'hwclouds\.com'):
        return True

    if self.matchContent(r'hws_security@'):
        return True

    return False
