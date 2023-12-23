
NAME = 'Distil (Distil Networks)'


def is_waf(self):
    if self.matchContent(r'cdn\.distilnetworks\.com/images/anomaly\.detected\.png'):
        return True

    if self.matchContent(r'distilCaptchaForm'):
        return True

    if self.matchContent(r'distilCallbackGuard'):
        return True

    return False
