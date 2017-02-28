#!/usr/bin/env python3
from Database import Database
from Nyaa import Nyaa, NyaaEntry
import getopt
import os
import sys


def load_settings():
    class Configuration(object):
        def __init__(self):
            self.db_dir = os.path.dirname(os.path.realpath(__file__))
            self.db_name = None
            self.mode = None
            self.nyaa_url = None
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
                    print('Start ID input error, format as "--start=21"')
    except:
        print('Error: Start ID logic error')

    if len(args) == 0:
        print('Please supply arguments.')
        exit(code=1)
    else:
        if args[0] == 'nyaa':
            config.nyaa_url = 'http://www.nyaa.se/'
            config.db_name = 'nyaa'
        elif args[0] == 'sukebei':
            config.nyaa_url = 'http://sukebei.nyaa.se/'
            config.db_name = 'sukebei'
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

config = load_settings()
nt = Nyaa(config.nyaa_url)
db = Database(config.db_dir, config.db_name)

if config.mode == 'new' and config.start_entry is None:
    config.start_entry = db.last_entry + 1
elif config.mode == 'missed' and config.start_entry is None or config.mode == 'update' and config.start_entry is None:
    config.start_entry = 1

print("Initializing...")
for i in range(config.start_entry, nt.last_entry + 1):
    if config.mode == 'missed':
        if db.entry_exists(i):
            continue

    entry = NyaaEntry(nt, i)
    if entry.exists is True:
        if entry.category in db.categories and entry.sub_category in db.sub_categories:
            entryname = str(entry.name).rstrip().lstrip()
            if entry.magnet is None:
                print('Torrent magnet failed ID:',i)
                continue
            if config.mode == 'new' and not db.entry_exists(i):
                print('Insert: {}, Name: {}'.format(i, entryname))
                db.write_torrent((
                    i, entry.name, entry.magnet, db.categories[entry.category],
                    db.sub_categories[entry.sub_category], db.status[entry.status]
                ))
            else: # update
                print('Update: {}, Name: {}'.format(i, entryname))
                db.update_torrent((
                    i, entry.name, entry.magnet, db.categories[entry.category],
                    db.sub_categories[entry.sub_category], db.status[entry.status]
                ))
        else:
            if not entry.category in db.categories:
                print(entry.category,"not in",db.categories)
            if not entry.sub_category in db.sub_categories:
                print(entry.sub_category,"not in", db.sub_categories)
            print('Exists - Entry: {}, Name: {}'.format(i, entry.name))

db.c.close()
