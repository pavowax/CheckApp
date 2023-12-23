
NAME = 'Oracle Cloud (Oracle)'


def is_waf(self):
    if self.matchContent(r'<title>fw_error_www'):
        return True

    if self.matchContent(r'src=\"/oralogo_small\.gif\"'):
        return True

    if self.matchContent(r'www\.oracleimg\.com/us/assets/metrics/ora_ocom\.js'):
        return True

    return False
