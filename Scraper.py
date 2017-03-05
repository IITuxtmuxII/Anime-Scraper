#!/usr/bin/env python3
from Database import Database
from Config import load_settings
import sys

# TODO try move variables for write_torrent into single variable
# TODO Implement MyAnimeList.net

config = load_settings()
db = Database(config.db_dir, config.db_name)
print('Initializing',config.db_name,'...',config.mode,'mode')

if config.db_name == 'bakabt':

    from Bakabt import Baka, BakaEntry
    for i in range(config.start_entry, Baka.last_entry(config.site_url) + 1):
        baka_list = Baka(config.site_url, i, Baka.last_entry(config.site_url)).baka_list()
        for k, entry in baka_list.items():
            if isinstance(entry, dict):
                if config.mode == 'missed' or config.mode == 'new' and db.entry_exists(entry['baka_url_id']):
                    if db.entry_exists(entry['baka_url_id']):
                        if config.mode == 'new':
                            print('Already in database: {}, Title: {}'.format(entry['baka_url_id'],entry['title']))
                        continue
                be=BakaEntry(entry['baka_url'], entry['title_orig'])
                torrent = be.torrent()
                if entry['category'] in db.categories:
                    if not torrent:
                        print('Torrent failed','Name:', entry['title'])
                        continue
                    status = be.status()
                    if config.mode == 'new' and not db.entry_exists(entry['baka_url_id']):
                        print('Insert: {}, Title: {}'.format(entry['baka_url_id'],entry['title']))
                        db.baka_write_torrent((entry['baka_url_id'], entry['baka_url'], entry['title'], entry['resolution'], entry['tags'], entry['sb'], entry['cb'], entry['added'], entry['size'], entry['sld'], torrent, i, db.categories[entry['category']], db.sub_categories['Default'], db.status[status]))
                    elif config.mode == 'update':
                        print('Update: {}, Title: {}'.format(entry['baka_url_id'],entry['title']))
                        db.baka_update_torrent((entry['baka_url_id'], entry['baka_url'], entry['title'], entry['resolution'], entry['tags'], entry['sb'], entry['cb'], entry['added'], entry['size'], entry['sld'], torrent, i, db.categories[entry['category']], db.sub_categories['Default'], db.status[status]))
                else:
                    if not entry['category'] in db.categories:
                        print(entry['category'],'not in',db.categories)
            else:
                print('Error - {0} : {1}'.format(k, v))

elif config.db_name == 'nyaa' or config.db_name == 'sukebei' or config.db_name == 'myanimelist':

    if config.db_name == 'myanimelist':
        from MyAnimeList import MAL, MALEntry
        nt = MAL(config.site_url)
    elif config.db_name == 'nyaa' or config.db_name == 'sukebei':
        from Nyaa import Nyaa, NyaaEntry
        nt = Nyaa(config.site_url)

    for i in range(config.start_entry, nt.last_entry + 1):
        if config.mode == 'missed':
            if db.entry_exists(i):
                if config.mode == 'new':
                    print('ID exists: {}'.format(i))
                continue

        if config.db_name == 'myanimelist':
            entry = MALEntry(nt, i)
        elif config.db_name == 'nyaa' or config.db_name == 'sukebei':
            entry = NyaaEntry(nt, i)

        if entry.exists is True:
            if entry.category in db.categories and entry.sub_category in db.sub_categories:
                if entry.magnet is None:
                    print('Torrent magnet failed ID:',i)
                    continue
                if config.mode == 'new' and not db.entry_exists(i) or config.mode == 'update':
                    print('Insert: {}, Title: {}'.format(i, entry.name))
                    if config.db_name == 'nyaa' or config.db_name == 'sukebei':
                        db.nyaa_write_torrent((i, entry.name, str(entry.tag), str(entry.sld), entry.magnet, db.categories[entry.category], db.sub_categories[entry.sub_category], db.status[entry.status]))
                    elif config.db_name == 'myanimelist':
                        print('not yet implemented!')
                elif config.mode == 'update':
                    print('Update: {}, Title: {}'.format(i, entry.name))
                    if config.db_name == 'nyaa' or config.db_name == 'sukebei':
                        db.nyaa_update_torrent((i, entry.name, entrytag, entrysld,  entry.magnet, db.categories[entry.category], db.sub_categories[entry.sub_category], db.status[entry.status]))
                    elif config.db_name == 'myanimelist':
                        print('not yet implemented!')
                else:
                    print('Exists: {} [To update set mode to update]'.format(i))
            else:
                if not entry.category in db.categories:
                    print(entry.category,'not in',db.categories)
                if not entry.sub_category in db.sub_categories:
                    print(entry.sub_category,'not in', db.sub_categories)

db.c.close()
print('Complete!')
