
NAME = 'CdnNS Application Gateway (CdnNs/WdidcNet)'


def is_waf(self):
    if self.matchContent(r'cdnnswaf application gateway'):
        return True

    return False
