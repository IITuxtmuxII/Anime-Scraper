#!/usr/bin/env python3
import getopt
import sys
import os

def load_settings():
    class Configuration(object):
        def __init__(self):
            self.db_dir = os.path.dirname(os.path.realpath(__file__))
            self.db_name = None
            self.mode = None
            self.site_url = None
            self.start_entry = None

    config = Configuration()

    arguments = sys.argv[1:]
    optlist, args = getopt.getopt(arguments, '', ['start='])

    try:
        for opt in arguments:
            if "--start=" in opt:
                if int(opt.split("=")[1]):
                    config.start_entry = int(opt.split("=")[1])
                    print('> Start ID: {}'.format(config.start_entry))
                else:
                    print('Start ID input error, format as "--start=01"')
    except:
        print('Error: Start ID logic error')

    if len(args) == 0:
        print('Please supply arguments.')
        exit(code=1)
    else:
        if args[0] == 'nyaa':
            config.site_url = 'http://www.nyaa.se/'
            config.db_name = 'nyaa'
        elif args[0] == 'sukebei':
            config.site_url = 'http://sukebei.nyaa.se/'
            config.db_name = 'sukebei'
        elif args[0] == 'bakabt':
            config.site_url = 'https://bakabt.me/'
            config.db_name = 'bakabt'
        else:
            print('Invalid url.')
            exit(code=1)

        try:
            config.mode = 'new'
            if args[1] == 'new':
                config.mode = 'new'
            elif args[1] == 'missed':
                config.mode = 'missed'
            elif args[1] == 'update':
                config.mode = 'update'
            else:
                if "--start=" not in args[1]:
                    print('Invalid option.')
                    exit(code=1)
        except:
            config.mode = 'new'
        print(">",config.mode.title(),"mode")
    return config
