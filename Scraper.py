#!/usr/bin/env python3
from Database import Database
from load_settings import load_settings

# Nyaa and Sukebei are fully tested
# Bakabt support is 80% implemented
# TODO bakabt torrent logic
# TODO bakabt remove unnessary logic
# TODO bakabt implement database
# TODO move scraper database logic into function
# TODO revise scraper.py into functions

config = load_settings()
db = Database(config.db_dir, config.db_name)
if config.mode == 'new' and config.start_entry is None:
    config.start_entry = db.last_entry + 1
elif config.mode == 'missed' and config.start_entry is None or config.mode == 'update' and config.start_entry is None:
    config.start_entry = 1

print("Initializing...")

if "bakabt" in config.site_url:
    from Bakabt import Baka, BakaEntry
    for i in range(config.start_entry, Baka.last_entry(config.site_url) + 1):
        baka_list = Baka(config.site_url, i).baka_list()
        for k, list_item in baka_list.items():
            if isinstance(list_item, dict):
                '''
                list_item['baka_url']
                list_item['category']
                list_item['title_orig']
                list_item['title']
                list_item['resolution']
                list_item['tags']
                list_item['sb']
                list_item['cb']
                list_item['added']
                list_item['size']
                list_item['downloads']
                list_item['seeders']
                list_item['leechers']
                '''
                #quality = BakaEntry(list_item['baka_url'], list_item['title_orig']).quality()
                torrent = BakaEntry(list_item['baka_url'], list_item['title_orig']).torrent()
                #print(torrent)
                '''
                if config.mode == 'missed':
                    if db.entry_exists(i):
                        continue

                if entry.exists is True:
                    if entry.category in db.categories and entry.sub_category in db.sub_categories:
                        entryname = str(entry.name).rstrip().lstrip()
                        if entry.tag is None:
                            entrytag=""
                        else:
                            entrytag = str(entry.tag).rstrip().lstrip()
                        if entry.magnet is None:
                            print('Torrent magnet failed ID:',i)
                            continue
                        if config.mode == 'new' and not db.entry_exists(i):
                            print('Insert: {}, Name: {}'.format(i, entryname))
                            db.write_torrent((i, entryname, entrytag, entry.magnet, db.categories[entry.category], db.sub_categories[entry.sub_category], db.status[entry.status]))
                        else:
                            print('Update: {}, Name: {}'.format(i, entryname))
                            db.update_torrent((i, entryname, entrytag, entry.magnet, db.categories[entry.category], db.sub_categories[entry.sub_category], db.status[entry.status]))
                    else:
                        if not entry.category in db.categories:
                            print(entry.category,"not in",db.categories)
                        if not entry.sub_category in db.sub_categories:
                            print(entry.sub_category,"not in", db.sub_categories)
                        print('Exists - Entry: {}, Name: {}'.format(i, entry.name))
                '''
            else:
                print("Error - {0} : {1}".format(k, v))

elif "nyaa" in config.site_url or "sukebei" in config.site_url:
    from Nyaa import Nyaa, NyaaEntry
    nt = Nyaa(config.site_url)

    for i in range(config.start_entry, nt.last_entry + 1):
        entry = NyaaEntry(nt, i)
        if config.mode == 'missed':
            if db.entry_exists(i):
                continue

        if entry.exists is True:
            if entry.category in db.categories and entry.sub_category in db.sub_categories:
                entryname = str(entry.name).rstrip().lstrip()
                if entry.magnet is None:
                    print('Torrent magnet failed ID:',i)
                    continue
                if entry.tag == "None":
                    entrytag=""
                else:
                    entrytag = str(entry.tag)
                entrysld = str(entry.sld)
                if config.mode == 'new' and not db.entry_exists(i):
                    print('Insert: {}, Name: {}'.format(i, entryname))
                    db.nyaa_write_torrent((i, entryname, entrytag, entrysld, entry.magnet, db.categories[entry.category], db.sub_categories[entry.sub_category], db.status[entry.status]))
                else:
                    print('Update: {}, Name: {}'.format(i, entryname))
                    db.nyaa_update_torrent((i, entryname, entrytag, entrysld,  entry.magnet, db.categories[entry.category], db.sub_categories[entry.sub_category], db.status[entry.status]))
            else:
                if not entry.category in db.categories:
                    print(entry.category,"not in",db.categories)
                if not entry.sub_category in db.sub_categories:
                    print(entry.sub_category,"not in", db.sub_categories)
                print('Exists - Entry: {}, Name: {}'.format(i, entry.name))

db.c.close()
