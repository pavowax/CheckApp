
NAME = 'Newdefend (NewDefend)'


def is_waf(self):
    # This header can be obtained without attack mode
    # Most reliable fingerprint
    if self.matchHeader(('Server', 'Newdefend')):
        return True

    # Reliable ones within blockpage
    if self.matchContent(r'www\.newdefend\.com/feedback'):
        return True

    if self.matchContent(r'/nd\-block/'):
        return True

    return False
