#!/usr/bin/env python3
from Database import Database
from Config import load_settings

config = load_settings()
db = Database(config.db_dir, config.db_name)
if config.db_name == "nyaa" or config.db_name == "sukebei":
    if config.mode == 'new' and config.start_entry is None:
        config.start_entry = db.last_entry + 1
    elif config.mode == 'missed' and config.start_entry is None or config.mode == 'update' and config.start_entry is None:
        config.start_entry = 1
elif config.db_name == "bakabt":
    config.start_entry = 1

print("Initializing...")

if "bakabt" in config.site_url:
    
    from Bakabt import Baka, BakaEntry
    for i in range(config.start_entry, Baka.last_entry(config.site_url) + 1):
        baka_list = Baka(config.site_url, i).baka_list()
        for k, entry in baka_list.items():
            if isinstance(entry, dict):
                be=BakaEntry(entry['baka_url'], entry['title_orig'])
                status = be.status()
                torrent = be.torrent()
                if config.mode == 'missed':
                    if db.entry_exists(entry['baka_url_id']):
                        continue
                if entry['category'] in db.categories:
                    if not torrent:
                        print("Torrent failed","Name:", entry['title'])
                        continue
                    if config.mode == 'new' and not db.entry_exists(entry['baka_url_id']):
                        print("Insert:",entry['baka_url_id'],"Title:",entry['title'])
                        db.baka_write_torrent((entry['baka_url_id'], entry['baka_url'], entry['title'], entry['resolution'], entry['tags'], entry['sb'], entry['cb'], entry['added'], entry['size'], entry['sld'], torrent, db.categories[entry['category']], db.sub_categories["Default"], db.status[status]))
                    else:
                        print("Update:",entry['baka_url_id'],"Title:",entry['title'])
                        db.baka_update_torrent((entry['baka_url_id'], entry['baka_url'], entry['title'], entry['resolution'], entry['tags'], entry['sb'], entry['cb'], entry['added'], entry['size'], entry['sld'], torrent, db.categories[entry['category']], db.sub_categories["Default"], db.status[status]))
                else:
                    if not entry['category'] in db.categories:
                        print(entry['category'],"not in",db.categories)
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
        entryexists =  entry.exists
        if entryexists is True:
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
                    print('Insert: {}, Title: {}'.format(i, entryname))
                    db.nyaa_write_torrent((i, entryname, entrytag, entrysld, entry.magnet, db.categories[entry.category], db.sub_categories[entry.sub_category], db.status[entry.status]))
                else:
                    print('Update: {}, Title: {}'.format(i, entryname))
                    db.nyaa_update_torrent((i, entryname, entrytag, entrysld,  entry.magnet, db.categories[entry.category], db.sub_categories[entry.sub_category], db.status[entry.status]))
            else:
                if not entry.category in db.categories:
                    print(entry.category,"not in",db.categories)
                if not entry.sub_category in db.sub_categories:
                    print(entry.sub_category,"not in", db.sub_categories)

print("Complete!")
db.c.close()
