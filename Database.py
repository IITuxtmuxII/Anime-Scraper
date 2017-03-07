import json
import sys
import os
import sqlite3


class Database(object):
    def __init__(self, path, filename):
        self.path = path
        self.filename = filename + '.sqlite'
        if os.path.exists(self.path + '/' + self.filename):
            self.file_exists = True
        else:
            self.file_exists = False
        self.c = sqlite3.connect(self.path + '/' + self.filename)
        if self.filename=='nyaa.sqlite' or self.filename=='sukebei.sqlite':
            if not self.file_exists:
                self.nyaa_create_database()
            self.nyaa_verify_database()
        elif self.filename=='bakabt.sqlite':
            if not self.file_exists:
                self.baka_create_database()
        elif self.filename=='myanimelist.sqlite':
            if not self.file_exists:
                self.myanimelist_create_database()
        self.check_categories()
        self.check_status()
        self.load_values()

    @property
    def last_entry(self):
        cur = self.c.cursor()
        cur.execute('SELECT * FROM torrents ORDER BY torrent_id DESC LIMIT 1;')
        try:
            return cur.fetchone()[0]
        except:
            return 0

    @property
    def last_page(self):
        cur = self.c.cursor()
        cur.execute('SELECT * FROM torrents ORDER BY torrent_page DESC LIMIT 1;')
        try:
            return cur.fetchone()[11]
        except:
            return 0

    def nyaa_create_database(self):
        print('Creating database...')
        self.c.execute('CREATE TABLE categories (category_id INTEGER NOT NULL, category_name TEXT NOT NULL, PRIMARY KEY (category_id))')
        self.c.execute('CREATE TABLE sub_categories (sub_category_id INTEGER NOT NULL, sub_category_name TEXT NOT NULL, PRIMARY KEY (sub_category_id))')
        self.c.execute('CREATE TABLE status (status_id INTEGER NOT NULL, status_name TEXT NOT NULL, PRIMARY KEY (status_id))')
        self.c.execute('CREATE TABLE torrents \
            (torrent_id INTEGER NOT NULL, torrent_name VARCHAR NOT NULL, \
            torrent_info VARCHAR NOT NULL, torrent_sld VARCHAR NOT NULL, \
            torrent_magnet VARCHAR NOT NULL, category_id INTEGER NOT NULL, \
            sub_category_id INTEGER NOT NULL, status_id INTEGER NOT NULL, \
            PRIMARY KEY (torrent_id), \
            FOREIGN KEY (category_id) REFERENCES categories(category_id), \
            FOREIGN KEY (sub_category_id) REFERENCES sub_categories(sub_category_id), \
            FOREIGN KEY (status_id) REFERENCES status(status_id))')
        self.c.execute('CREATE TABLE sub_categories (sub_category_id INTEGER NOT NULL, sub_category_name TEXT NOT NULL, PRIMARY KEY (sub_category_id))')
        self.c.execute('CREATE TABLE status (status_id INTEGER NOT NULL, status_name TEXT NOT NULL, PRIMARY KEY (status_id))')
        self.c.execute('CREATE TABLE torrents \
            (torrent_id INTEGER NOT NULL, torrent_url VARCHAR NOT NULL, \
            torrent_name VARCHAR, torrent_resolution VARCHAR, \
            torrent_tags VARCHAR, torrent_sb VARCHAR, \
            torrent_cb VARCHAR NOT NULL, torrent_added VARCHAR NOT NULL, \
            torrent_size VARCHAR NOT NULL, torrent_sld VARCHAR NOT NULL, \
            torrent_file BLOB NOT NULL, torrent_page INTEGER NOT NULL, \
            category_id INTEGER NOT NULL, \
            sub_category_id INTEGER NOT NULL, status_id INTEGER NOT NULL, \
            PRIMARY KEY (torrent_id), \
            FOREIGN KEY (category_id) REFERENCES categories(category_id), \
            FOREIGN KEY (sub_category_id) REFERENCES sub_categories(sub_category_id), \
            FOREIGN KEY (status_id) REFERENCES status(status_id))')

    def baka_create_database(self):
        print('Creating database...')
        self.c.execute('CREATE TABLE categories (category_id INTEGER NOT NULL, category_name TEXT NOT NULL, PRIMARY KEY (category_id))')
        self.c.execute('CREATE TABLE sub_categories (sub_category_id INTEGER NOT NULL, sub_category_name TEXT NOT NULL, PRIMARY KEY (sub_category_id))')
        self.c.execute('CREATE TABLE status (status_id INTEGER NOT NULL, status_name TEXT NOT NULL, PRIMARY KEY (status_id))')
        self.c.execute('CREATE TABLE torrents \
            (torrent_id INTEGER NOT NULL, torrent_url VARCHAR NOT NULL, \
            torrent_name VARCHAR, torrent_resolution VARCHAR, \
            torrent_tags VARCHAR, torrent_sb VARCHAR, \
            torrent_cb VARCHAR NOT NULL, torrent_added VARCHAR NOT NULL, \
            torrent_size VARCHAR NOT NULL, torrent_sld VARCHAR NOT NULL, \
            torrent_file BLOB NOT NULL, torrent_page INTEGER NOT NULL, \
            category_id INTEGER NOT NULL, \
            sub_category_id INTEGER NOT NULL, status_id INTEGER NOT NULL, \
            PRIMARY KEY (torrent_id), \
            FOREIGN KEY (category_id) REFERENCES categories(category_id), \
            FOREIGN KEY (sub_category_id) REFERENCES sub_categories(sub_category_id), \
            FOREIGN KEY (status_id) REFERENCES status(status_id))')

    def myanimelist_create_database(self):
        print('Creating database...')
        self.c.execute('CREATE TABLE categories (category_id INTEGER NOT NULL, category_name TEXT NOT NULL, PRIMARY KEY (category_id))')
        self.c.execute('CREATE TABLE sub_categories (sub_category_id INTEGER NOT NULL, sub_category_name TEXT NOT NULL, PRIMARY KEY (sub_category_id))')
        self.c.execute('CREATE TABLE status (status_id INTEGER NOT NULL, status_name TEXT NOT NULL, PRIMARY KEY (status_id))')
        self.c.execute('CREATE TABLE torrents \
            (torrent_id INTEGER NOT NULL, name VARCHAR NOT NULL, \
            type VARCHAR NOT NULL, episodes VARCHAR NOT NULL, \
            aired_start VARCHAR, aired_end VARCHAR, premiered VARCHAR, \
            published INTEGER NOT NULL, category_id INTEGER NOT NULL, \
            sub_category_id INTEGER NOT NULL, status_id INTEGER NOT NULL, \
            PRIMARY KEY (torrent_id), \
            FOREIGN KEY (category_id) REFERENCES categories(category_id), \
            FOREIGN KEY (sub_category_id) REFERENCES sub_categories(sub_category_id), \
            FOREIGN KEY (status_id) REFERENCES status(status_id))')

    def check_categories(self):
        with open(self.path + '/categories.json') as f:
            if self.filename == 'sukebei.sqlite':
                category_json = json.load(f)['Sukebei']
            elif self.filename == 'nyaa.sqlite':
                category_json = json.load(f)['Nyaa']
            elif self.filename == 'bakabt.sqlite':
                category_json = json.load(f)['Bakabt']
            elif self.filename == 'myanimelist.sqlite':
                category_json = json.load(f)['MyAnimeList']
        cur = self.c.cursor()
        cur.execute('SELECT * FROM categories')
        categories = cur.fetchall()
        if len(categories) == 0:
            for i, cat in enumerate(category_json, start=1):
                self.write_category((i, cat))
        elif len(categories) > 0:
            t1, t2 = zip(*categories)
            next_id = len(categories) + 1
            for cat in category_json:
                if cat not in t2:
                    self.write_category((next_id, cat))
                    next_id += 1
        cur.execute('SELECT * FROM sub_categories')
        sub_categories = cur.fetchall()
        try:
            t1, t2 = zip(*sub_categories)
        except:
            t2 = ()
        next_id = len(sub_categories) + 1
        for cat in category_json:
            for sub_cat in category_json[cat]:
                if sub_cat not in t2:
                    self.write_subcategory((next_id, sub_cat))
                    cur.execute('SELECT * FROM sub_categories')
                    t1, t2 = zip(*cur.fetchall())
                    next_id += 1

    def check_status(self):
        cur = self.c.cursor()
        cur.execute('SELECT * FROM status')
        if self.filename == 'nyaa.sqlite' or self.filename == 'sukebei.sqlite':
            status = ['normal', 'remake', 'trusted', 'a+']
        elif self.filename == 'bakabt.sqlite':
            status = ['normal', 'A', 'B', 'C', 'D']
        elif self.filename == 'myanimelist.sqlite':
            status = ['Finished Airing', 'Currently Airing', 'Not yet aired', 'Unknown']
        db_status = cur.fetchall()
        if len(db_status) == 0:
            for i, stat in enumerate(status, start=1):
                self.write_status((i, stat))
        elif len(db_status) > 0:
            t1, t2 = zip(*db_status)
            next_id = len(db_status) + 1
            for stat in status:
                if stat not in t2:
                    self.write_status((next_id, stat))

    def entry_exists(self, id):
        cur = self.c.cursor()
        t = (id,)
        cur.execute('SELECT * FROM torrents WHERE torrent_id = ?', t)
        if cur.fetchall() == []:
            return False
        else:
            return True

    def load_values(self):
        cur = self.c.cursor()
        self.categories = {}
        self.sub_categories = {}
        self.status = {}
        cur.execute('SELECT * FROM categories')
        for t1, t2 in cur.fetchall():
            self.categories[t2] = t1
        cur.execute('SELECT * FROM sub_categories')
        for t1, t2 in cur.fetchall():
            self.sub_categories[t2] = t1
        cur.execute('SELECT * FROM status')
        for t1, t2 in cur.fetchall():
            self.status[t2] = t1

    def nyaa_verify_database(self):
        print('Verifying database...')
        cur = self.c.cursor()

        comparison = [
            (0, 'category_id', 'INTEGER', 1, None, 1),
            (1, 'category_name', 'TEXT', 1, None, 0)
        ]
        cur.execute('PRAGMA table_info(categories);')
        if cur.fetchall() == comparison:
            print('Table categories verified.')
        else:
            exit('Table categories broken.')

        comparison = [
            (0, 'sub_category_id', 'INTEGER', 1, None, 1),
            (1, 'sub_category_name', 'TEXT', 1, None, 0)
        ]
        cur.execute('PRAGMA table_info(sub_categories);')
        if cur.fetchall() == comparison:
            print('Table sub_categories verified.')
        else:
            exit('Table sub_categories broken.')

        comparison = [
            (0, 'status_id', 'INTEGER', 1, None, 1),
            (1, 'status_name', 'TEXT', 1, None, 0)
        ]
        cur.execute('PRAGMA table_info(status);')
        if cur.fetchall() == comparison:
            print('Table status verified.')
        else:
            exit('Table status broken.')

        comparison = [
            (0, 'torrent_id', 'INTEGER', 1, None, 1),
            (1, 'torrent_name', 'VARCHAR', 1, None, 0),
            (2, 'torrent_info', 'VARCHAR', 1, None, 0),
            (3, 'torrent_sld', 'VARCHAR', 1, None, 0),
            (4, 'torrent_magnet', 'VARCHAR', 1, None, 0),
            (5, 'category_id', 'INTEGER', 1, None, 0),
            (6, 'sub_category_id', 'INTEGER', 1, None, 0),
            (7, 'status_id', 'INTEGER', 1, None, 0)
        ]
        cur.execute('PRAGMA table_info(torrents);')
        if cur.fetchall() == comparison:
            print('Table torrents verified.')
        else:
            exit('Table torrents broken.')

    def write_category(self, data):
        print('Writing category {} into database...'.format(data[1]))
        self.c.execute('INSERT INTO categories VALUES (?, ?)', data)
        self.c.commit()

    def write_subcategory(self, data):
        print('Writing subcategory {} into database...'.format(data[1]))
        self.c.execute('INSERT INTO sub_categories VALUES (?, ?)', data)
        self.c.commit()

    def write_status(self, data):
        print('Writing status {} into database...'.format(data[1]))
        self.c.execute('INSERT INTO status VALUES (?, ?)', data)
        self.c.commit()

    def nyaa_write_torrent(self, data):
        '''torrent_id, torrent_name, torrent_info, torrent_sld, torrent_magnet, category_id, sub_category_id, status_id'''
        self.c.execute('INSERT INTO torrents VALUES (?, ?, ?, ?, ?, ?, ?, ?)', data)
        self.c.commit()

    def nyaa_update_torrent(self, data):
        self.c.execute('UPDATE torrents SET torrent_id=(?),torrent_name=(?),torrent_info=(?),torrent_sld=(?),torrent_magnet=(?),category_id=(?),sub_category_id=(?),status_id=(?) WHERE torrent_id='+str(data[0]), data)
        self.c.commit()

    def baka_write_torrent(self, data):
        '''torrent_id, torrent_url, torrent_name, torrent_resolution, torrent_tags, torrent_sb, torrent_cb, torrent_added, torrent_size, torrent_sld, torrent_file, torrent_page, category_id, sub_category_id, status_id'''
        self.c.execute('INSERT INTO torrents VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
        self.c.commit()

    def baka_update_torrent(self, data):
        self.c.execute('UPDATE torrents SET torrent_id=(?),torrent_url=(?),torrent_name=(?),torrent_resolution=(?),torrent_tags=(?),torrent_sb=(?),torrent_cb=(?),torrent_added=(?),torrent_size=(?),torrent_sld=(?),torrent_file=(?),torrent_page=(?),category_id=(?),sub_category_id=(?),status_id=(?) WHERE torrent_id='+str(data[0]), data)
        self.c.commit()

    def myanimelist_write_torrent(self, data):
        self.c.execute('INSERT INTO torrents VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
        self.c.commit()

    def myanimelist_update_torrent(self, data):
        self.c.execute('UPDATE torrents SET torrent_id=(?),name=(?),type=(?),episodes=(?),aired_start=(?),aired_end=(?),premiered=(?),published=(?),category_id=(?),sub_category_id=(?),status_id=(?) WHERE torrent_id='+str(data[0]), data)
        self.c.commit()
