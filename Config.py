#!/usr/bin/env python3
from Database import Database
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
        elif args[0] == 'myanimelist':
            config.site_url = 'https://myanimelist.net/'
            config.db_name = 'myanimelist'
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
                if '--start=' not in args[1]:
                    print('Invalid option.')
                    exit(code=1)
        except:
            config.mode = 'new'

    try:
        for opt in arguments:
            if '--start=' in opt:
                if int(opt.split('=')[1]):
                    config.start_entry = int(opt.split('=')[1])
                    print('> Start ID: {}'.format(config.start_entry))
                else:
                    print('Start ID input error, format --start=01')
            else:
                if config.db_name == 'nyaa' or config.db_name == 'sukebei' or config.db_name == 'myanimelist':
                    if config.mode == 'new' and config.start_entry is None:
                        db = Database(config.db_dir, config.db_name)
                        config.start_entry = db.last_entry + 1
                elif config.db_name == 'bakabt':
                    db = Database(config.db_dir, config.db_name)
                    config.start_entry = db.last_page
    except:
        exit('Error: Start ID logic error')

    if config.start_entry is None:
        config.start_entry =  1

    return config
